from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from auth import UserSessionData, get_session_data
from db_manager import getAllChatsOfUser, readAllMessagesInChat, getUserByName, updateMessageReadList, updateUserActiveChat, getMessageById, getChatById
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
    is_read: bool
    author: str
    is_edited: bool


@router.get("/chatlist", response_class=HTMLResponse)
def chatlist_element(request: Request, user: UserSessionData = Depends(get_session_data)):
    user = getUserByName(user.username)
    chats = getAllChatsOfUser(user.username)
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
        chat_id = uuid.UUID(user.active_chat)
    updateUserActiveChat(name=user.username, active_chat=str(chat_id))
    chat_list = user.chatlist.split()
    if str(chat_id) in chat_list:
        chat = getChatById(chat_id)
        response = templates.TemplateResponse("chat_element.html", context={'request': request, 'id': chat_id, 'user': user, 'chat': chat})
        return response


@router.get("/get_messages", response_class=HTMLResponse)
def get_messages(request: Request, chat_id: uuid.UUID, user: UserSessionData = Depends(get_session_data)):
    user = getUserByName(user.username)
    chat_list = user.chatlist.split()
    if str(chat_id) in chat_list:
        messages = readAllMessagesInChat(chat_id)
        message_list= []
        for i in messages:
            if user.username not in i.read_list.split():
                read_list = i.read_list + " " + user.username
            else:
                read_list = i.read_list
            x = [x for x in read_list.split() if x != user.username]
            is_read = False
            if len(x) > 0:
                is_read = True
            updateMessageReadList(i.id, read_list)
            message = Message(id=i.id, is_mine=False, content=i.content, author=i.author, is_read=is_read, is_edited=i.is_edited)
            if user.username == i.author:
                message = Message(id=i.id, is_mine=True, content=i.content, author=i.author, is_read=is_read, is_edited=i.is_edited)
            message_list.append(message)
        message_list = message_list[::-1]
        response = templates.TemplateResponse("messages.html", context={'request': request, 'messages': message_list})
        return response
    

@router.get("/edit_message_form", response_class=HTMLResponse)
def edit_message_form(request: Request, message_id: uuid.UUID, user: UserSessionData = Depends(get_session_data)):
    message = getMessageById(message_id)
    user = getUserByName(user.username)
    if message.author == user.username:
        response = templates.TemplateResponse("message_edit_form.html", context={'request': request, 'message_id': message_id, 'content': message.content, 'username': user.username})
        return response
    

@router.get("/new_chat_form", response_class=HTMLResponse)
def new_chat_form(request: Request, user: UserSessionData = Depends(get_session_data)):
    user = getUserByName(user.username)
    response = templates.TemplateResponse("create_chat_form.html", context={'request': request, 'username': user.username})
    return response


@router.get("/edit_chat_form")
def edit_chat_form(request: Request, chat_id: uuid.UUID, user: UserSessionData = Depends(get_session_data)):
    user = getUserByName(user.username)
    if str(chat_id) in user.chatlist.split():
        is_moderator = False
        chat = getChatById(chat_id)
        user_list = chat.user_list.split()
        moderator_list = chat.moderator_list.split()
        for i in moderator_list:
            if i in user_list:
                user_list.remove(i)
        chat_name = chat.name
        if user.username in moderator_list:
            is_moderator = True
        user_list = " ".join(user_list)
        moderator_list = " ".join(moderator_list)
        response = templates.TemplateResponse("edit_chat_form.html", context={'request': request, 'id': chat_id, 'name': chat_name, 'user_list': user_list, 'moderator_list': moderator_list, 'is_admin': is_moderator, 'username': user.username})
        return response
    

@router.get("/get_search", response_class=HTMLResponse)
def get_search(request: Request):
    response = templates.TemplateResponse("search_element.html", context={'request': request})
    return response


@router.get("/back_to_chatlist", response_class=HTMLResponse)
def back_to_chatlist(request: Request):
    response = templates.TemplateResponse("chatlist_full.html", context={'request': request})
    return response