from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import time


#Structures de données
class Message(BaseModel):
    id : int
    time : int
    file : str
    message: str


class Thread(BaseModel):
    thread_id : int
    list_messages: list[Message]
    
    
client = MongoClient('mongodb://localhost:27017/')
db = client.test_database
collection = db.test_collection

# Partie insertion bdd
def insert_thread(thread: Thread):
    list_messages = []
    for message in thread.list_messages:
        list_messages.append({"id": message.id, "message": message.message})
    collection.insert_one({"thread_id": thread.thread_id, "list": list_messages })

def insert_message(thread_id: int ,message: Message):
    if thread_length(thread_id) == 0:
        collection.update_one({"thread_id": thread_id}, {"$push": {"list": {"id": 0,"time" : int(time.time()) ,"file":message.file, "message": message.message}}})
    else:
        collection.update_one({"thread_id": thread_id}, {"$push": {"list": {"id": thread_length(thread_id) + 1,"time": int(time.time()),"file":message.file, "message": message.message}}})

def thread_length(id: int):
    thread = collection.find_one({"thread_id": id})
    if thread is None:
        return 0
    else:
        return len(thread["list"])

#insert_thread(Thread(thread_id=3, list_messages=[Message(id=0, message="Hello"), Message(id=1, message="World")]))



#Partie API
app = FastAPI()

@app.get("/thread/{id}")
def get_thread(id: int):
    thread = collection.find_one({"thread_id": id})
    if thread is None:
        return {"message": "Thread not found"}
    else:
        return {"thread_id": thread["thread_id"], "list_messages": thread["list"]}
    
@app.get("/thread/{id}/message/{message_id}")
def get_message(id: int, message_id: int):
    thread = collection.find_one({"thread_id": id})
    if thread is None:
        return {"message": "Thread not found"}
    else:
        i = 0
        for message in thread["list"]:
            if i == message_id:
                return Message(id=message["id"], message=message["message"])
            i += 1
        return {"message": "Message not found"}

@app.post("/thread/create")
def create_thread(thread: Thread):
    insert_thread(thread)
    return {"message": "Thread created"}

@app.post("/thread/{id}/message")
def post_message(id: int, message: Message):
    insert_message(id, message)
    return {"message": "Message inserted"}