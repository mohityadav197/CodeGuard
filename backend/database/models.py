"""SQLAlchemy models for storing review history."""
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Review(Base):
    __tablename__ = "reviews"
    id = Column(String, primary_key=True)
    repo = Column(String, nullable=False)
    pr_number = Column(Integer, nullable=False)
    status = Column(String, default="completed")
    total_findings = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Finding(Base):
    __tablename__ = "findings"
    id = Column(String, primary_key=True)
    review_id = Column(String, nullable=False)
    agent = Column(String, nullable=False)  # bug, security, quality
    file = Column(String, nullable=False)
    line = Column(Integer)
    severity = Column(String)  # critical, warning, info
    message = Column(Text)
    suggestion = Column(Text)
