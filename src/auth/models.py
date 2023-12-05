from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, TIMESTAMP, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """User's model"""
    pass
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(String(10), default="STD")
    is_active = mapped_column(Boolean, default=True)
    is_admin = mapped_column(Boolean, default=False)
    is_superuser = mapped_column(Boolean, default=False)
    data_joined = mapped_column(TIMESTAMP, default=datetime.utcnow)
    rating: Mapped[float] = mapped_column(Float, default=0)

    def __repr__(self) -> str:
        return f"id: {self.id} username: {self.username}, status: {self.status},"


