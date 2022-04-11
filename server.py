from fastapi import FastAPI
from  objects.datastructure import Thread, Message
from database.dbmanager import insert_messagedb, insert_threaddb, get_imageboarddb ,get_boarddb, get_threaddb, get_messagedb, init_imageboarddb

app = FastAPI()

#init_imageboarddb()

@app.get("/boards/")
def get_boards():
    """this function is used to get all the boards"""
    return get_imageboarddb()
    
@app.get("/boards/{board_id}/")
def get_board(board_id: int):
    """this function is used to get a board"""
    return get_boarddb(board_id)

@app.get("boards/{board_id}/threads/{thread_id}")
def get_thread(board_id: int ,thread_id: int):
    """this function is used to get a thread"""
    return get_threaddb(board_id,thread_id)
    
@app.get("boards/{board_id}/threads/{thread_id}/messages/{message_id}")
def get_message(board_id: int,thread_id: int, message_id: int):
    """this function is used to get a message from a thread"""
    return get_messagedb(thread_id,message_id)

@app.post("boards/{board_id}/threads/post")
def create_thread(board_id: int,thread: Thread):
    """this function is used to create a thread"""
    #{"thread_id": 1, "list_messages": {} }
    insert_threaddb(thread)
    return {"message": "Thread created"}

@app.post("boards/{board_id}/threads/{thread_id}/post")
def post_message(board_id: int, thread_id: int, message: Message):
    """this function is used to post a message in a thread"""
    #{"message_id": 1, "time": 1, "file": " ", "message" : "test"}
    insert_messagedb(thread_id, message)
    return {"message": "Message posted"}