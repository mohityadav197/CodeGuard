from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.jwt_handler import create_access_token, get_current_user
from backend.auth.oauth import oauth
from backend.config import settings
from backend.database.db import get_db
from backend.database.models import User

router = APIRouter(prefix="/auth")


@router.get("/login")
async def login(request: Request):
    redirect_uri = f"{settings.SERVER_URL}/auth/callback"
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def callback(request: Request, db: AsyncSession = Depends(get_db)):
    token = await oauth.github.authorize_access_token(request)
    resp = await oauth.github.get("user", token=token)
    profile = resp.json()

    result = await db.execute(select(User).where(User.github_username == profile["login"]))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            github_username=profile["login"],
            github_avatar_url=profile.get("avatar_url"),
            github_name=profile.get("name"),
            github_token=token.get("access_token"),
            last_login=datetime.now(timezone.utc),
        )
        db.add(user)
    else:
        user.github_avatar_url = profile.get("avatar_url")
        user.github_name = profile.get("name")
        user.github_token = token.get("access_token")
        user.last_login = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(user)

    jwt_token = create_access_token({"user_id": str(user.id), "username": user.github_username})
    return RedirectResponse(f"{settings.FRONTEND_URL}/auth/callback?token={jwt_token}")


@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "github_username": current_user.github_username,
        "github_avatar_url": current_user.github_avatar_url,
        "github_name": current_user.github_name,
        "last_login": current_user.last_login,
    }


@router.post("/logout")
async def logout():
    return {"status": "logged_out"}
