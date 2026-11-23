
from sqlalchemy import (
    Column, Integer, String, Text,
    ForeignKey, DateTime, JSON
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True)
    password = Column(String(255), nullable=False)

    analyses = relationship(
        "EmailAnalysis",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class EmailAnalysis(Base):
    __tablename__ = "email_analyses"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    subject = Column(String(255), default="No subject")
    email_content = Column(Text, nullable=False)

    risk_score = Column(Integer, nullable=False)
    classification = Column(String(50), nullable=False)

    indicators = Column(JSON, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="analyses"
    )
