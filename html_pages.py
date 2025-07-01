from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["Html"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
def main_page():
    return "Ok"


@router.get("/log-in")
def log_in_page():
    return "Ok"


@router.get("/sing-up")
def sing_up_page():
    return "Ok"


@router.get("/chats")
def chats_page():
    return "Ok"


@router.get("/user/{username}")
def user_profile_page(username: str):
    return username