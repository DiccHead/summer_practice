from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from auth import UserSessionData, get_session_data
from db_manager import getAllChatsOfUser, readAllMessagesInChat
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


@router.get("/chatlist", response_class=HTMLResponse)
def chatlist_element(request: Request, user: UserSessionData = Depends(get_session_data)):
    chats = getAllChatsOfUser(user.username)
    chats_final = []
    for chat in chats:
        last_message = readAllMessagesInChat(chat.id)[::-1][0]
        is_read = False
        is_active = False
        msg_time = str(last_message.date_time.hour) + ":" + str(last_message.date_time.minute)
        if user.username in last_message.read_list.split():
            is_read = True
        if str(chat.id) == user.active_chat:
            is_active = True
        chat = chat.model_dump()
        chat = Chat(**chat, last_message=last_message.content, msg_time=msg_time, is_read=is_read, is_active=is_active)
        if chat.last_message == "":
            chat.last_message = "Сообщений пока нет"
        print(chat)
        chats_final.append(chat)
    response = templates.TemplateResponse("chat_list.html", context={'request': request, 'chats': chats_final})
    return response


@router.get("/open_chat", response_class=HTMLResponse)
def open_chat(request: Request, chat_id: uuid.UUID, user: UserSessionData = Depends(get_session_data)):
    pass