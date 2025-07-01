from datetime import datetime
from typing import Any
from pydantic import BaseModel
import uuid
from fastapi import APIRouter, Cookie, Depends, Response, Request
from db_manager import getUserByName


router = APIRouter(prefix="/auth", tags=["Auth"])

class UserSessionData(BaseModel):
    id: uuid.UUID
    username: str
    profile_pic: str
    registration_date: datetime
    last_online: datetime
    chatlist: str
    active_chat: str

COOKIES: dict[str, UserSessionData] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


def auth(username: str, password: str):
    user = getUserByName(username)
    if user != "There is no such user":
        if user.password == password:
            user = user.model_dump()
            user = UserSessionData(**user)
            return user, True
        else:
            return "Invalid Password", False
    return user, False


def generate_session_id():
    return uuid.uuid1().hex


def get_session_data(request: Request) -> dict:
    try:
        session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
        return COOKIES[session_id]
    except:
        return {"status": "Not authenticated"}



@router.post("/login")
def login(username: str, password: str, response: Response):
    user, is_ok = auth(username, password)
    if is_ok:
        session_id = generate_session_id()
        COOKIES[session_id] = user
        response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
        return "Success"
    return user


@router.get("/check-cookie")
def check_cookie(user_session_data: UserSessionData = Depends(get_session_data)):
    return user_session_data


@router.get("/logout")
def logout(response: Response, request: Request):
    try:
        session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
        COOKIES.pop(session_id)
        response.delete_cookie(COOKIE_SESSION_ID_KEY)
        return "Goodbye"
    except:
        return {"status": "Not authenticated"}
    