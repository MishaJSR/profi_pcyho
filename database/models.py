from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, func, Integer, Boolean


class Base(DeclarativeBase):
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Task(Base):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    answer_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    answers: Mapped[str] = mapped_column(Text, nullable=True)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    addition: Mapped[str] = mapped_column(Text, nullable=True)
    points_for_task: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    is_visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Block(Base):
    __tablename__ = 'block'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block_name: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    has_media: Mapped[bool] = mapped_column(Boolean, nullable=False)
    date_to_post: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    progress_block: Mapped[int] = mapped_column(Integer, default=0)
    callback_button_id: Mapped[str] = mapped_column(Text, nullable=True)
    count_send: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_vebinar: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class MediaBlock(Base):
    __tablename__ = 'media_block'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_id: Mapped[str] = mapped_column(Text, nullable=True)
    video_id: Mapped[str] = mapped_column(Text, nullable=True)


class MediaTask(Base):
    __tablename__ = 'media_task'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_id: Mapped[str] = mapped_column(Text, nullable=False)


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    is_subscribe: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    day_start_subscribe: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    day_end_subscribe: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
