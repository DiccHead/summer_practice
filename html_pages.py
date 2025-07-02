from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from auth import get_session_data, UserSessionData


router = APIRouter(tags=["Html"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
def main_page(request: Request, user: UserSessionData = Depends(get_session_data)):
    if user == "Guest":
        response = RedirectResponse(url='/log-in', status_code=303)
        return response
    response = RedirectResponse(url='/chats', status_code=303)
    return response


@router.get("/log-in", response_class=HTMLResponse)
def log_in_page(request: Request):
    response = templates.TemplateResponse("index.html", context={'request': request, 'page_name': 'log in'})
    return response


@router.get("/sing-up", response_class=HTMLResponse)
def sing_up_page(request: Request):
    response = templates.TemplateResponse("index.html", context={'request': request, 'page_name': 'sing up'})
    return response


@router.get("/chats", response_class=HTMLResponse)
def chats_page(request: Request, user: UserSessionData = Depends(get_session_data)):
    if user == "Guest":
        response = RedirectResponse(url='/log-in', status_code=303)
        return response
    response = templates.TemplateResponse("index.html", context={'request': request, 'page_name': 'chats'})
    return response


@router.get("/user/{username}", response_class=HTMLResponse)
def user_profile_page(request: Request, username: str, user: UserSessionData = Depends(get_session_data)):
    if user == "Guest":
        response = RedirectResponse(url='/log-in', status_code=303)
        return response
    response = templates.TemplateResponse("index.html", context={'request': request, 'page_name': username})
    return response