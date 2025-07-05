from datetime import datetime
import uuid
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from db_manager import addUser, AddUser, getChatById, addMessage, AddMessage, getUserByName, editMessageById, getMessageById, deleteMessageById, AddChat, addChat, updateUserChatlist, updateUserActiveChat, updateChatPicture

router = APIRouter(tags=["Forms"], prefix="/forms")

templates = Jinja2Templates(directory="templates")

@router.post("/create_user")
def create_user(username: str = Form(), password: str = Form()):
    if " " not in username:
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
        message = AddMessage(author=username, chat=chat_id, content=message_content, read_list=username)
        addMessage(message)
        response = templates.TemplateResponse("new_message_form.html", context={'request': request, 'id': chat_id, 'user': user})
        return response
    

@router.post("/edit_message")
def edit_message(message_id: uuid.UUID = Form(), content: str = Form()):
    message = getMessageById(message_id)
    message.content = content
    editMessageById(message_id, message)
    return RedirectResponse(url="/chats?active_chat=True", status_code=303)


@router.post("/delete_message")
def delete_message(message_id: uuid.UUID, username: str):
    message = getMessageById(message_id)
    if message.author == username:
        deleteMessageById(message_id)


@router.post("/create_chat")
async def create_chat(request: Request, username: str = Form(), chat_name: str = Form(), chat_picture: UploadFile = File(...)):
    chat = AddChat(name=chat_name, user_list=username, moderator_list=username)
    is_ok, chat = addChat(chat)
    user = getUserByName(username)
    updateUserActiveChat(username, str(chat))
    updateUserChatlist(username, user.chatlist+" "+str(chat))
    if chat_picture.size != 0:
        if chat_picture.content_type == "image/jpeg":
            photo_file = open("user_files/chat_pictures/"+str(chat)+".jpg", "wb")
            file_content = await chat_picture.read()
            photo_file.write(file_content)
            photo_file.close()
            updateChatPicture(chat, str(chat))
        else:
            return RedirectResponse(url="/photo_warning", status_code=303)
    return RedirectResponse(url="/chats?active_chat=True", status_code=303)
    # UploadFile(filename='lmao.jpg', size=29519, headers=Headers({'content-disposition': 'form-data; name="chat_picture"; filename="lmao.jpg"', 'content-type': 'image/jpeg'}))