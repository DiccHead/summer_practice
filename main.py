from datetime import datetime
import uuid
from fastapi import FastAPI

from db_manager import readAllUsers, getUserById, getUserByName, addUser, editUserByName, deleteUserByName, updateUserChatlist, updateUserActiveChat, updateUserLastOnline, AddUser, readAllChats, getChatById, addChat, editChatById, deleteChatById, AddChat


app = FastAPI()


@app.get("/")
def main_page():
    return readAllUsers()


@app.post("/test/add_user")
def add_user_test(user: AddUser):
    return addUser(user)


@app.get("/test/get_user_by_id")
def get_user_by_id(id: uuid.UUID):
    return getUserById(id)


@app.get("/test/get_user_by_name")
def get_user_by_name(name: str):
    return getUserByName(name)


@app.put("/test/edit_user_by_name")
def edit_user_by_name(name: str, input: AddUser):
    return editUserByName(name, input)


@app.delete("/test/delete_user_by_name")
def delete_user_by_name(name: str):
    return deleteUserByName(name)


@app.put("/test/update_user_chatlist")
def update_user_chatlist(name: str, input: str):
    return updateUserChatlist(name, input)


@app.put("/test/update_user_active_chat")
def update_user_active_chat(name: str, input: str):
    return updateUserActiveChat(name, input)


@app.put("/test/update_user_last_online")
def update_user_last_online(name: str, input: datetime):
    return updateUserLastOnline(name, input)