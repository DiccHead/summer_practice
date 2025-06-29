from datetime import datetime

from sqlmodel import Session, select
from database import engine, User, Chat, Message
from pydantic import BaseModel
import uuid


#Модели для добавления элементов
class AddUser(BaseModel):
    # __table_args__ = (UniqueConstraint("username"),)
    # id: uuid.UUID = Field(primary_key=True, default=None)
    username: str
    password: str
    profile_pic: str
    # registration_date: datetime
    last_online: datetime
    chatlist: str
    active_chat: str



#Функции для взаимодействия с базой данных
def readAllUsers():
    with Session(engine) as session:
        statement = select(User)
        result = session.exec(statement)
        user_list = []
        for user in result:
            user_list.append(user)
        return user_list


def addUser(user_input: AddUser):
    user_input = user_input.model_dump()
    user = User(id=uuid.uuid1(), registration_date=datetime.now(), **user_input)
    with Session(engine) as session:
        try:
            session.add(user)
            session.commit()
            return "User added successfuly!"
        except:
            return "That username is already taken!"