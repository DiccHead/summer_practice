from datetime import datetime
from sqlmodel import Session, select
from database import engine, User, Chat, Message
from pydantic import BaseModel
from error_handling import HandleErrors
import uuid


#Модели для добавления элементов
class AddUser(BaseModel):
    # __table_args__ = (UniqueConstraint("username"),)
    # id: uuid.UUID = Field(primary_key=True, default=None)
    username: str
    password: str
    profile_pic: str = "Guest"
    # registration_date: datetime
    last_online: datetime
    chatlist: str = ""
    active_chat: str = ""


class AddChat(BaseModel):
    # id: uuid.UUID = Field(primary_key=True, default=None)
    name: str = "New Chat"
    picture: str = "Default"
    user_list: str = ""
    # creation_date: datetime
    moderator_list: str = ""


class AddMessage(BaseModel):
    # id: uuid.UUID = Field(primary_key=True, default=None)
    author: str
    chat: uuid.UUID
    # date_time: datetime
    read_list: str = ""
    # is_edited: bool
    content: str = ""
    media: str = ""



#Функции для взаимодействия с базой данных

#USER:
def readAllUsers():
    with Session(engine) as session:
        statement = select(User)
        result = session.exec(statement)
        user_list = []
        for user in result:
            user_list.append(user)
        return user_list
    

def getUserById(id: uuid.UUID):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        result = session.exec(statement)
        try:
            user = result.one()
            return user
        except:
            return "There is no such user"


def getUserByName(name: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        result = session.exec(statement)
        try:
            user = result.one()
            return user
        except:
            return "There is no such user"


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


def editUserByName(name: str, user_input: AddUser):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        result = session.exec(statement)
        try:
            user = result.one()
            user.username = user_input.username
            user.password = user_input.password
            user.profile_pic = user_input.profile_pic
            user.last_online = user_input.last_online
            user.chatlist = user_input.chatlist
            user.active_chat = user_input.active_chat
            session.add(user)
            session.commit()
            return "Edited user successfuly"
        except:
            return "There is no such user"


def deleteUserByName(name: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        result = session.exec(statement)
        try:
            user = result.one()
            session.delete(user)
            session.commit()
            return "Deleted user successfuly"
        except:
            return "There is no such user"


def updateUserChatlist(name: str, new_chatlist: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        result = session.exec(statement)
        try:
            user = result.one()
            user.chatlist = new_chatlist
            session.add(user)
            session.commit()
            return "Updated chatlist successfuly"
        except:
            return "There is no such user"
        

def updateUserActiveChat(name: str, active_chat: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        result = session.exec(statement)
        try:
            user = result.one()
            user.active_chat = active_chat
            session.add(user)
            session.commit()
            return "Updated active chat successfuly"
        except:
            return "There is no such user"
        

def updateUserLastOnline(name: str, last_online: datetime):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        result = session.exec(statement)
        try:
            user = result.one()
            user.last_online = last_online
            session.add(user)
            session.commit()
            return "Updated last online successfuly"
        except:
            return "There is no such user"
        

#CHAT:
def readAllChats():
    with Session(engine) as session:
        statement = select(Chat)
        result = session.exec(statement)
        chat_list = []
        for chat in result:
            chat_list.append(chat)
        return chat_list
    

def getChatById(id: uuid.UUID):
    with Session(engine) as session:
        statement = select(Chat).where(Chat.id == id)
        result = session.exec(statement)
        try:
            chat = result.one()
            return chat
        except:
            return HandleErrors()


def addChat(chat_input: AddChat):
    chat_input = chat_input.model_dump()
    chat = Chat(id=uuid.uuid1(), creation_date=datetime.now(), **chat_input)
    with Session(engine) as session:
        try:
            session.add(chat)
            session.commit()
            return "Chat added successfuly!"
        except:
            return "Something went wrong I guess? If you're reading this, it must be that I forgot to put an error handling function here..."


def editChatById(id: uuid.UUID, chat_input: AddChat):
    with Session(engine) as session:
        statement = select(Chat).where(Chat.id == id)
        result = session.exec(statement)
        try:
            chat = result.one()
            chat.name = chat_input.name
            chat.picture = chat_input.picture
            chat.user_list = chat_input.user_list
            chat.moderator_list = chat_input.moderator_list
            session.add(chat)
            session.commit()
            return "Edited chat successfuly"
        except:
            return HandleErrors()


def deleteChatById(id: uuid.UUID):
    with Session(engine) as session:
        statement = select(Chat).where(Chat.id == id)
        result = session.exec(statement)
        try:
            chat = result.one()
            session.delete(chat)
            session.commit()
            return "Deleted chat successfuly"
        except:
            return HandleErrors()


def updateChatUserList(id: uuid.UUID, input: str):
    with Session(engine) as session:
        statement = select(Chat).where(Chat.id == id)
        result = session.exec(statement)
        try:
            chat = result.one()
            chat.user_list = input
            session.add(chat)
            session.commit()
            return "Updated user list successfuly"
        except:
            return HandleErrors()
        

def getAllChatsOfUser(username: str):
    with Session(engine) as session:
        statement = select(Chat)
        result = session.exec(statement)
        chat_list = []
        for chat in result:
            chat_list.append(chat)
        final_chat_list = []
        for i in chat_list:
            x = i.user_list.split()
            if username in x:
                final_chat_list.append(i)

        return final_chat_list
        

#MESSAGES:
def readAllMessages():
    with Session(engine) as session:
        statement = select(Message)
        result = session.exec(statement)
        message_list = []
        for message in result:
            message_list.append(message)
        return message_list
    

def getMessageById(id: uuid.UUID):
    with Session(engine) as session:
        statement = select(Message).where(Message.id == id)
        result = session.exec(statement)
        try:
            message = result.one()
            return message
        except:
            return HandleErrors()


def addMessage(message_input: AddMessage):
    message_input = message_input.model_dump()
    message = Message(id=uuid.uuid1(), date_time=datetime.now(), is_edited=False, **message_input)
    with Session(engine) as session:
        try:
            session.add(message)
            session.commit()
            return "Message added successfuly!"
        except:
            return "Something went wrong I guess? If you're reading this, it must be that I forgot to put an error handling function here..."


def editMessageById(id: uuid.UUID, message_input: AddMessage):
    with Session(engine) as session:
        statement = select(Message).where(Message.id == id)
        result = session.exec(statement)
        try:
            message = result.one()
            message.author = message_input.author
            message.chat = message_input.chat
            message.read_list = message_input.read_list
            message.content = message_input.content
            message.media = message_input.media
            message.is_edited = True
            session.add(message)
            session.commit()
            return "Edited message successfuly"
        except:
            return HandleErrors()


def deleteMessageById(id: uuid.UUID):
    with Session(engine) as session:
        statement = select(Message).where(Message.id == id)
        result = session.exec(statement)
        try:
            message = result.one()
            session.delete(message)
            session.commit()
            return "Delete message successfuly"
        except:
            return HandleErrors()
        

def readAllMessagesInChat(id: uuid.UUID):
    with Session(engine) as session:
        statement = select(Message).where(Message.chat == id).order_by(Message.date_time)
        result = session.exec(statement)
        message_list = []
        for message in result:
            message_list.append(message)
        return message_list