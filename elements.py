from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from auth import UserSessionData, get_session_data
from db_manager import getAllChatsOfUser, readAllMessagesInChat, getUserByName, updateMessageReadList, updateUserActiveChat
from pydantic import BaseModel
from datetime import datetime
import uuid


router = APIRouter(tags=["Elements"], prefix="/element")

templates = Jinja2Templates(directory="templates")

class Chat(BaseModel):
    id: uuid.UUID
    name: str
    picture: str
    last_message: str
    msg_time: str
    is_read: bool
    is_active: bool


class Message(BaseModel):
    id: uuid.UUID
    is_mine: bool
    content: str


@router.get("/chatlist", response_class=HTMLResponse)
def chatlist_element(request: Request, user: UserSessionData = Depends(get_session_data)):
    user = getUserByName(user.username)
    chats = getAllChatsOfUser(user.username)
    print(chats)
    if chats == []:
        response = templates.TemplateResponse("empty_chatlist.html", context={'request': request})
    chats_final = []
    for chat in chats:
        is_read = False
        is_active = False
        try:
            last_message = readAllMessagesInChat(chat.id)[::-1][0]
            minute = str(last_message.date_time.minute)
            if len(minute) == 1:
                minute = "0" + minute
            msg_time = str(last_message.date_time.hour) + ":" + minute
            if user.username in last_message.read_list.split():
                is_read = True
            last_message=last_message.content
        except:
            last_message = "Сообщений пока нет"
            msg_time = ""
        if str(chat.id) == user.active_chat:
            is_active = True
        chat = chat.model_dump()
        chat = Chat(**chat, last_message=last_message, msg_time=msg_time, is_read=is_read, is_active=is_active)

        chats_final.append(chat)
    response = templates.TemplateResponse("chat_list.html", context={'request': request, 'chats': chats_final})
    return response


@router.get("/open_chat", response_class=HTMLResponse)
def open_chat(request: Request, chat_id: uuid.UUID = None, user: UserSessionData = Depends(get_session_data), active_chat=False):
    user = getUserByName(user.username)
    if active_chat:
        chat_id = user.active_chat
    updateUserActiveChat(name=user.username, active_chat=str(chat_id))
    chat_list = user.chatlist.split()
    if str(chat_id) in chat_list:
        response = templates.TemplateResponse("chat_element.html", context={'request': request, 'id': chat_id, 'user': user})
        return response


@router.get("/get_messages", response_class=HTMLResponse)
def get_messages(request: Request, chat_id: uuid.UUID, user: UserSessionData = Depends(get_session_data)):
    user = getUserByName(user.username)
    chat_list = user.chatlist.split()
    if str(chat_id) in chat_list:
        messages = readAllMessagesInChat(chat_id)
        message_list= []
        for i in messages:
            read_list = i.read_list + " " + user.username
            updateMessageReadList(i.id, read_list)
            message = Message(id=i.id, is_mine=False, content=i.content)
            if user.username == i.author:
                message = Message(id=i.id, is_mine=True, content=i.content)
            message_list.append(message)
        message_list = message_list[::-1]
        response = templates.TemplateResponse("messages.html", context={'request': request, 'messages': message_list})
        return response