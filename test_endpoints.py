from datetime import datetime
import uuid
from fastapi import APIRouter

from db_manager import readAllUsers, getUserById, getUserByName, addUser, editUserByName, deleteUserByName, updateUserChatlist, updateUserActiveChat, updateUserLastOnline, AddUser, readAllChats, getChatById, addChat, editChatById, deleteChatById, updateChatUserList, getAllChatsOfUser, AddChat, readAllMessages, getMessageById, addMessage, editMessageById, deleteMessageById, readAllMessagesInChat, AddMessage

router = APIRouter(prefix="/test", tags=["Test"])

@router.get("/users")
def users_page():
    return readAllUsers()


@router.post("/add_user")
def add_user_test(user: AddUser):
    return addUser(user)


@router.get("/get_user_by_id")
def get_user_by_id(id: uuid.UUID):
    return getUserById(id)


@router.get("/get_user_by_name")
def get_user_by_name(name: str):
    return getUserByName(name)


@router.put("/edit_user_by_name")
def edit_user_by_name(name: str, input: AddUser):
    return editUserByName(name, input)


@router.delete("/delete_user_by_name")
def delete_user_by_name(name: str):
    return deleteUserByName(name)


@router.put("/update_user_chatlist")
def update_user_chatlist(name: str, input: str):
    return updateUserChatlist(name, input)


@router.put("/update_user_active_chat")
def update_user_active_chat(name: str, input: str):
    return updateUserActiveChat(name, input)


@router.put("/update_user_last_online")
def update_user_last_online(name: str, input: datetime):
    return updateUserLastOnline(name, input)


@router.get("/chats")
def chat_page():
    return readAllChats()


@router.post("/add_chat")
def add_chat_test(chat: AddChat):
    return addChat(chat)


@router.get("/get_chat_by_id")
def get_chat_by_id(id: uuid.UUID):
    return getChatById(id)


@router.put("/edit_chat_by_id")
def edit_chat_by_id(id: uuid.UUID, input: AddChat):
    return editChatById(id, input)


@router.delete("/delete_chat_by_id")
def delete_chat_by_id(id: uuid.UUID):
    return deleteChatById(id)


@router.put("/update_chat_userlist")
def update_chat_userlist(id: uuid.UUID, input: str):
    return updateChatUserList(id, input)


@router.get("/get_all_chats_of_user")
def get_all_chats_of_user(username: str):
    return getAllChatsOfUser(username)


@router.get("/messages")
def message_page():
    return readAllMessages()


@router.post("/add_message")
def add_message_test(message: AddMessage):
    return addMessage(message)


@router.get("/get_message_by_id")
def get_message_by_id(id: uuid.UUID):
    return getMessageById(id)


@router.put("/edit_message_by_id")
def edit_message_by_id(id: uuid.UUID, input: AddMessage):
    return editMessageById(id, input)


@router.delete("/delete_message_by_id")
def delete_message_by_id(id: uuid.UUID):
    return deleteMessageById(id)


@router.get("/get_all_messages_in_chat")
def get_all_messages_in_chat(id: uuid.UUID):
    return readAllMessagesInChat(id)
