from fastapi import FastAPI

from db_manager import readAllUsers, addUser, AddUser


app = FastAPI()


@app.get("/")
def main_page():
    return readAllUsers()


@app.post("/test/add_user")
def add_user_test(user: AddUser):
    return addUser(user)