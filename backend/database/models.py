"""SQLAlchemy models for storing review history."""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repo = Column(String, nullable=False, index=True)
    pr_number = Column(Integer, nullable=False, index=True)
    status = Column(String, default="completed")
    total_findings = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    findings = relationship("Finding", back_populates="review", cascade="all, delete-orphan")


class Finding(Base):
    __tablename__ = "findings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id = Column(UUID(as_uuid=True), ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    agent = Column(String, nullable=False)  # bug, security, quality
    file = Column(String, nullable=False)
    line = Column(Integer)
    severity = Column(String)  # critical, warning, info
    message = Column(Text)
    suggestion = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    review = relationship("Review", back_populates="findings")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    github_username = Column(String, unique=True, index=True)
    github_avatar_url = Column(String, nullable=True)
    github_name = Column(String, nullable=True)
    github_token = Column(String, nullable=True)  # stores their OAuth token for repo access
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
