from datetime import datetime
from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, TIMESTAMP, Float, Integer, CheckConstraint, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """User's model"""
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    phone_number = mapped_column(String(30), nullable=True)
    status_id: Mapped[int] = mapped_column(ForeignKey('status.id'),
                                           default=text("(SELECT id FROM status ORDER BY max_size_text_file LIMIT 1)"))
    status: Mapped['status'] = relationship("Status", back_populates="users")
    is_active = mapped_column(Boolean, default=True)
    is_admin = mapped_column(Boolean, default=False)
    is_superuser = mapped_column(Boolean, default=False)
    data_joined = mapped_column(TIMESTAMP, default=datetime.utcnow)
    rating: Mapped[float] = mapped_column(Float, default=0)

    def __repr__(self) -> str:
        return f"id: {self.id} username: {self.username}, status: {self.status}"


class Status(Base):
    """A model of user status and constraints."""
    __tablename__ = 'status'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(String(10), unique=True)
    max_size_text_file: Mapped[int] = mapped_column(Integer(), CheckConstraint('max_size_text_file >= 1024'))
    max_count_text_file: Mapped[int]
    max_size_all_text_files: Mapped[int] = mapped_column(Integer(), CheckConstraint('max_size_all_text_files >= 1024'))
    max_count_text_file_in_collection: Mapped[int]
    max_count_collections_created: Mapped[int]
    max_count_collections_subscriptions: Mapped[int]
    max_count_groups_created: Mapped[int]
    max_count_groups_subscriptions: Mapped[int]
    users: Mapped[List['User']] = relationship(back_populates="status")

    @validates('max_size_text_file', 'max_count_text_file', 'max_count_text_file_in_collection',
               'max_count_collections_created', 'max_count_collections_subscriptions', 'max_count_groups_created',
               'max_count_groups_subscriptions')
    def validate_positive(self, key, value):
        if value is not None and value < -1:
            raise ValueError(f"{key} must be greater than or equal to -1")
        return value

    def __repr__(self):
        return f"Name: {self.name}- id: {self.id}"
