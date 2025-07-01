from datetime import datetime
from sqlmodel import SQLModel, create_engine, Field
from sqlalchemy import UniqueConstraint

import uuid


class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("username"),)
    id: uuid.UUID = Field(primary_key=True, default=None)
    username: str
    password: str
    profile_pic: str
    registration_date: datetime
    last_online: datetime
    chatlist: str
    active_chat: str


class Chat(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default=None)
    name: str
    picture: str
    user_list: str
    creation_date: datetime
    moderator_list: str


class Message(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default=None)
    author: str
    chat: uuid.UUID
    date_time: datetime
    read_list: str
    is_edited: bool
    content: str
    media: str



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)
SQLModel.metadata.create_all(engine)