from datetime import datetime

from sqlalchemy import String, Boolean, TIMESTAMP, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    hashed_password: Mapped[str]
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(String(10), default="std")
    is_activ = mapped_column(Boolean, default=True)
    is_admin = mapped_column(Boolean, default=False)
    is_superuser = mapped_column(Boolean, default=False)
    data_joined = mapped_column(TIMESTAMP, default=datetime.utcnow)
    rating: Mapped[float] = mapped_column(Float, default=0)


