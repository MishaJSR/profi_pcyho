from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, func, Integer, Boolean


class Base(DeclarativeBase):
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Task(Base):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    exam: Mapped[str] = mapped_column(String(40), nullable=False)
    chapter: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    answer_mode: Mapped[str] = mapped_column(String(10), nullable=False)
    answers: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    addition: Mapped[str] = mapped_column(Text, nullable=True)


class Media(Base):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    format_media: Mapped[str] = mapped_column(String(20), nullable=False)
    path_of_file: Mapped[str] = mapped_column(String(80), nullable=False)


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    is_subscribe: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    day_start_subscribe: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    day_end_subscribe: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
