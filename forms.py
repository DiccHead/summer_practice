from datetime import datetime
from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse
from db_manager import addUser, AddUser

router = APIRouter(tags=["Forms"], prefix="/forms")

@router.post("/create_user")
def create_user(username: str = Form(), password: str = Form()):
    if " " not in username:
        new_user = AddUser(username=username, password=password, last_online=datetime.now())
        answer = addUser(new_user)
        if answer != "That username is already taken!":
            return RedirectResponse(url="/", status_code=303)
        return RedirectResponse(url="/sing-up?invalid_msg=Имя%20пользователя%20уже%20занято", status_code=303)
    return RedirectResponse(url="/sing-up?invalid_msg=Имя%20пользователя%20не%20должно%20содержать%20пробелов", status_code=303)


