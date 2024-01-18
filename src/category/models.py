from datetime import datetime

from sqlalchemy import String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base
from user.models import User

class Category(Base):
    """A category model for text files."""
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    system_name: Mapped[str] = mapped_column(String(50), unique=True)
    path: Mapped[str] = mapped_column(String(200), unique=True)
    data_joined = mapped_column(TIMESTAMP, default=datetime.utcnow)
    creator: Mapped[int] = mapped_column(ForeignKey(User.id, onupdate='CASCADE'))
    user: Mapped['User'] = relationship('User', back_populates='category')

    def __repr__(self) -> str:
        return f"Category '{self.name}'. Date joined: {self.data_joined}. Creator: {self.creator}"
