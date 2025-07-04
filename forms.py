from datetime import datetime
import uuid
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from db_manager import addUser, AddUser, getChatById, addMessage, AddMessage, getUserByName

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
        # return RedirectResponse(url="/chats?active_chat=True", status_code=303)
        response = templates.TemplateResponse("new_message_form.html", context={'request': request, 'id': chat_id, 'user': user})
        return response