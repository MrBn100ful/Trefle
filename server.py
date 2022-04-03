from fastapi import FastAPI
from  objects.datastructure import Thread, Message
from database.dbmanager import insert_messagedb, insert_threaddb, get_threaddb, get_messagedb

app = FastAPI()

@app.get("/thread/{thread_id}")
def get_thread(thread_id: int):
    """this function is used to get a thread"""
    return get_threaddb(thread_id)
    
@app.get("/thread/{thread_id}/message/{message_id}")
def get_message(thread_id: int, message_id: int):
    """this function is used to get a message from a thread"""
    return get_messagedb(thread_id,message_id)

@app.post("/thread/create")
def create_thread(thread: Thread):
    """this function is used to create a thread"""
    #{"thread_id": 1, "list_messages": {} }
    insert_threaddb(thread)
    return {"message": "Thread created"}

@app.post("/thread/{thread_id}/newmessage")
def post_message(thread_id: int, message: Message):
    """this function is used to post a message in a thread"""
    #{"message_id": 1, "time": 1, "file": " ", "message" : "test"}
    insert_messagedb(thread_id, message)
    return {"message": "Message posted"}