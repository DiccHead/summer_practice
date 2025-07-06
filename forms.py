from datetime import datetime
import os
import uuid
from fastapi import APIRouter, File, Form, Request, UploadFile, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from database import User
from db_manager import addUser, AddUser, deleteChatById, editChatById, getChatById, addMessage, AddMessage, getUserByName, editMessageById, getMessageById, deleteMessageById, AddChat, addChat, updateUserChatlist, updateUserActiveChat, updateChatPicture, updateChatUserList, updateChatModeratorList, user_search
from auth import UserSessionData, get_session_data
import pathlib

router = APIRouter(tags=["Forms"], prefix="/forms")

templates = Jinja2Templates(directory="templates")

@router.post("/create_user")
def create_user(username: str = Form(), password: str = Form()):
    if " " not in username:
        if password == "":
            return RedirectResponse(url="/sing-up?invalid_msg=Пароль%20не%20должен%20быть%20пустым", status_code=303)
        new_user = AddUser(username=username, password=password, last_online=datetime.now())
        answer = addUser(new_user)
        if answer != "That username is already taken!":
            return RedirectResponse(url="/", status_code=303)
        return RedirectResponse(url="/sing-up?invalid_msg=Имя%20пользователя%20уже%20занято", status_code=303)
    return RedirectResponse(url="/sing-up?invalid_msg=Имя%20пользователя%20не%20должно%20содержать%20пробелов", status_code=303)


@router.post("/new_message", response_class=HTMLResponse)
def new_message(request: Request, username: str = Form(), chat_id: uuid.UUID = Form(), message_content: str = Form()):
    chat = getChatById(chat_id)
    user = getUserByName(username)
    user_list = chat.user_list.split()
    if username in user_list:
        if message_content != '':
            message = AddMessage(author=username, chat=chat_id, content=message_content, read_list=username)
            addMessage(message)
        response = templates.TemplateResponse("new_message_form.html", context={'request': request, 'id': chat_id, 'user': user})
        return response
    

@router.post("/edit_message")
def edit_message(message_id: uuid.UUID = Form(), content: str = Form()):
    message = getMessageById(message_id)
    message.content = content
    editMessageById(message_id, message)
    return RedirectResponse(url="/chats", status_code=303)


@router.post("/delete_message")
def delete_message(message_id: uuid.UUID, username: str):
    message = getMessageById(message_id)
    if message.author == username:
        deleteMessageById(message_id)


@router.post("/create_chat")
async def create_chat(request: Request, username: str = Form(), chat_name: str = Form(), chat_picture: UploadFile = File(...)):
    try:
        if chat_picture.size != 0:
            if 'image' in chat_picture.content_type.split('/'):
                chat = AddChat(name=chat_name, user_list=username, moderator_list=username)
                is_ok, chat = addChat(chat)
                photo_file = open("user_files/chat_pictures/"+str(chat)+".jpg", "wb")
                file_content = await chat_picture.read()
                photo_file.write(file_content)
                photo_file.close()
                user = getUserByName(username)
                updateUserActiveChat(username, str(chat))
                updateUserChatlist(username, user.chatlist+" "+str(chat))
                updateChatPicture(chat, str(chat))
            else:
                return RedirectResponse(url="/warning?error=Файл%20должен%20быть%20изображением", status_code=303)
        else:
            chat = AddChat(name=chat_name, user_list=username, moderator_list=username)
            is_ok, chat = addChat(chat)
            user = getUserByName(username)
            updateUserActiveChat(username, str(chat))
            updateUserChatlist(username, user.chatlist+" "+str(chat))
        return RedirectResponse(url="/chats", status_code=303)
    except:
        return RedirectResponse(url="/warning?error=Файл%20должен%20быть%20изображением", status_code=303)
    # UploadFile(filename='lmao.jpg', size=29519, headers=Headers({'content-disposition': 'form-data; name="chat_picture"; filename="lmao.jpg"', 'content-type': 'image/jpeg'}))


@router.post("/leave_chat")
def leave_chat(chat_id: uuid.UUID, user: UserSessionData = Depends(get_session_data)):
    user = getUserByName(user.username)
    leave_chat_f(chat_id, user)
    return RedirectResponse(url="/chats", status_code=303)


@router.post("/delete_chat")
def delete_chat(chat_id: uuid.UUID, user: UserSessionData = Depends(get_session_data)):
    user = getUserByName(user.username)
    chat = getChatById(chat_id)
    user_list = chat.user_list.split()
    moderator_list = chat.moderator_list.split()
    if user.username in moderator_list:
        for i in user_list:
            leave_chat_f(chat_id, getUserByName(i))
        deleteChatById(chat_id)
        return RedirectResponse(url="/chats", status_code=303)


def leave_chat_f(chat_id: uuid.UUID, user: User):
    chat_list = user.chatlist.split()
    chat_list.remove(str(chat_id))
    chat_list = " ".join(chat_list)
    chat = getChatById(chat_id)
    username = user.username
    user_list = chat.user_list.split()
    moderator_list = chat.moderator_list.split()
    if username in moderator_list:
        moderator_list.remove(username)
    user_list.remove(username)
    user_list = " ".join(user_list)
    moderator_list = " ".join(moderator_list)
    updateUserChatlist(username, chat_list)
    updateChatUserList(chat_id, user_list)
    updateChatModeratorList(chat_id, moderator_list)


@router.post("/edit_chat")
async def edit_chat(request: Request, name: str = Form(), user_list: str = Form(), moderator_list: str = Form(), chat_picture: UploadFile = File(...), chat_id: uuid.UUID = Form(), user: UserSessionData = Depends(get_session_data)):
    for i in user_list.split():
        if i in moderator_list.split():
            return RedirectResponse(url="/warning?error=Админы%20не%20должны%20быть%20указаны%20в%20раздееле%20обычных%20пользователей%20(и%20наоборот)", status_code=303)
    try:
        print(chat_picture)
        if chat_picture.size != 0:
            if 'image' in chat_picture.content_type.split('/'):
                user = getUserByName(user.username)
                chat = getChatById(chat_id)
                old_user_list = chat.user_list.split()
                user_list = user_list.split() + moderator_list.split()
                moderator_list = moderator_list.split()
                if user.username in old_user_list:
                    for i in user_list:
                        if i not in old_user_list:
                            chat_list = getUserByName(i).chatlist.split()
                            chat_list.append(str(chat_id))
                            chat_list = " ".join(chat_list)
                            updateUserChatlist(i, chat_list)
                    for i in old_user_list:
                        if i not in user_list:
                            chat_list = getUserByName(i).chatlist.split()
                            chat_list.remove(str(chat_id))
                            chat_list = " ".join(chat_list)
                            updateUserChatlist(i, chat_list)
                    user_list = " ".join(user_list)
                    moderator_list = " ".join(moderator_list)
                    if user.username in chat.moderator_list.split():
                        new_chat = AddChat(name=name, user_list=user_list, moderator_list=moderator_list, picture=str(chat_id))
                    else:
                        new_chat = AddChat(name=name, user_list=user_list, moderator_list=chat.moderator_list, picture=str(chat_id))
                    editChatById(chat_id, new_chat)
                    if chat.picture != 'Default':
                        photo_file = open("user_files/chat_pictures/"+str(chat.picture)+"0"+".jpg", "wb")
                        updateChatPicture(chat_id, str(chat.picture)+"0")
                    else:
                        photo_file = open("user_files/chat_pictures/"+str(chat.id)+".jpg", "wb")
                        updateChatPicture(chat_id, str(chat.id))
                    file_content = await chat_picture.read()
                    photo_file.write(file_content)
                    photo_file.close()
            else:
                return RedirectResponse(url="/warning?error=Файл%20должен%20быть%20изображением", status_code=303)
        else:
            user = getUserByName(user.username)
            chat = getChatById(chat_id)
            old_user_list = chat.user_list.split()
            user_list = user_list.split() + moderator_list.split()
            moderator_list = moderator_list.split()
            if user.username in old_user_list:
                for i in user_list:
                    if i not in old_user_list:
                        chat_list = getUserByName(i).chatlist.split()
                        chat_list.append(str(chat_id))
                        chat_list = " ".join(chat_list)
                        updateUserChatlist(i, chat_list)
                for i in old_user_list:
                    if i not in user_list:
                        chat_list = getUserByName(i).chatlist.split()
                        chat_list.remove(str(chat_id))
                        chat_list = " ".join(chat_list)
                        updateUserChatlist(i, chat_list)
                user_list = " ".join(user_list)
                moderator_list = " ".join(moderator_list)
                if user.username in chat.moderator_list.split():
                    new_chat = AddChat(name=name, user_list=user_list, moderator_list=moderator_list, picture=chat.picture)
                else:
                    new_chat = AddChat(name=name, user_list=user_list, moderator_list=chat.moderator_list, picture=chat.picture)
                editChatById(chat_id, new_chat)
        return RedirectResponse(url="/chats", status_code=303)
    except:
        return RedirectResponse(url="/warning?error=Файл%20должен%20быть%20изображением", status_code=303)


@router.get("/search_user", response_class=HTMLResponse)
def search_user(request: Request, search_request: str):
    result = user_search(search_request)
    if result != []:
        return templates.TemplateResponse("/user_list.html", context={'request': request, 'users': result, 'nothing': False})
    else:
        return templates.TemplateResponse("/user_list.html", context={'request': request, 'users': result, 'nothing': True})