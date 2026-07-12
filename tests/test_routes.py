"""Tests for backend/api/routes.py, exercising real DB queries against an
isolated file-backed SQLite database (never the production Postgres/Neon
DB), with authentication mocked via FastAPI dependency overrides.

A temp-file SQLite DB (not `:memory:`) is used with NullPool so that
connections opened from different event loops (the TestClient's internal
portal loop vs. this module's one-off setup loop) never share a single
loop-bound aiosqlite connection object -- the classic pitfall with async
in-memory SQLite in tests.
"""

from __future__ import annotations

import asyncio
import os
import tempfile
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from backend.auth.jwt_handler import get_current_user
from backend.database.db import get_db
from backend.database.models import Base, User
from backend.main import app

_db_fd, _db_path = tempfile.mkstemp(suffix=".db")
os.close(_db_fd)

_test_engine = create_async_engine(f"sqlite+aiosqlite:///{_db_path}", poolclass=NullPool)
_TestSessionLocal = async_sessionmaker(_test_engine, expire_on_commit=False)

_fake_user = User(
    id=uuid.uuid4(),
    github_username="test-user",
    github_avatar_url=None,
    github_name="Test User",
)


async def _override_get_db():
    async with _TestSessionLocal() as session:
        yield session


def _override_get_current_user():
    return _fake_user


@pytest.fixture(scope="module", autouse=True)
def _setup_test_db():
    async def _create():
        async with _test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(_create())
    yield
    os.remove(_db_path)


@pytest.fixture
def client_without_auth():
    # Deliberately NOT entered as a context manager: `with TestClient(app):`
    # fires FastAPI's real startup lifespan event, which calls init_db()
    # against the actual production Neon database -- unrelated to and
    # bypassing the get_db override below (that only affects route-level
    # Depends(get_db), not the app's lifespan hook). Plain construction
    # skips lifespan entirely, which is fine here since our SQLite double's
    # tables are already created directly by the _setup_test_db fixture.
    app.dependency_overrides[get_db] = _override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_auth():
    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_current_user] = _override_get_current_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_health_returns_200_without_auth(client_without_auth):
    response = client_without_auth.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "CodeGuard is running", "version": "1.0.0"}


def test_reviews_requires_auth_returns_401_without_token(client_without_auth):
    response = client_without_auth.get("/api/reviews")
    assert response.status_code == 401


def test_stats_with_mock_user_returns_proper_structure(client_with_auth):
    response = client_with_auth.get("/api/stats")

    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {
        "total_reviews",
        "total_findings",
        "findings_by_agent",
        "findings_by_severity",
        "top_repos",
        "recent_activity",
    }
    assert body["total_reviews"] == 0
    assert body["total_findings"] == 0
    assert body["findings_by_severity"] == {"critical": 0, "warning": 0, "info": 0}
