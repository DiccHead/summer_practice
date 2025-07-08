from datetime import datetime
from typing import Any
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uuid
from fastapi import APIRouter, Depends, Form, Response, Request
from db_manager import getUserByName, updateUserLastOnline


router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="templates")

class UserSessionData(BaseModel):
    id: uuid.UUID
    username: str
    profile_pic: str
    registration_date: datetime
    last_online: datetime
    chatlist: str
    active_chat: str
    last_logged_in: datetime

COOKIES: dict[str, UserSessionData] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


def auth(username: str, password: str):
    user = getUserByName(username)
    if user != "There is no such user":
        if user.password == password:
            now = datetime.now()
            updateUserLastOnline(name=user.username, last_online=now)
            user.last_online = now
            user = user.model_dump()
            user = UserSessionData(**user, last_logged_in=now)
            return user, True
        else:
            return "Invalid Password", False
    return user, False


def generate_session_id():
    return uuid.uuid1().hex


def get_session_data(request: Request) -> dict:
    try:
        session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
        now = datetime.now()
        user = COOKIES[session_id]
        user.last_online = now
        updateUserLastOnline(user.username, now)
        return user
    except:
        return "Guest"



@router.post("/login")
def login(username: str = Form(), password: str = Form()):
    user, is_ok = auth(username, password)
    if is_ok:
        session_id = generate_session_id()
        COOKIES[session_id] = user
        template_response = RedirectResponse(url='/', status_code=303)
        template_response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
        return template_response
    return RedirectResponse(url='/log-in?invalid_msg=Неправильное%20имя%20пользователя%20или%20пароль', status_code=303)


@router.get("/check-cookie")
def check_cookie(user_session_data: UserSessionData = Depends(get_session_data)):
    return user_session_data


@router.get("/logout", response_class=HTMLResponse)
def logout(response: Response, request: Request):
    try:
        session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
        now = datetime.now()
        updateUserLastOnline(COOKIES[session_id].username, now)
        COOKIES.pop(session_id)
        response.delete_cookie(COOKIE_SESSION_ID_KEY)
        response = templates.TemplateResponse("index.html", context={"request": request})
        response.headers["HX-Redirect"] = "/"
        return response
    except:
        return {"status": "Not authenticated"}
    