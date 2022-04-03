from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import time


#Structures de données
class Message(BaseModel):
    message_id : int
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
    collection.insert_one({"thread_id": thread.thread_id, "list_messages": {} })
    for message in thread.list_messages:
        insert_message(thread.thread_id, message)

def insert_message(thread_id: int ,message: Message):
    if thread_length(thread_id) == 0:
        collection.update_one({"thread_id": thread_id}, {"$push": {"list_messages": {"message_id": 0,"time" : int(time.time()) ,"file":message.file, "message": message.message}}})
    else:
        collection.update_one({"thread_id": thread_id}, {"$push": {"list_messages": {"message_id": thread_length(thread_id) + 1,"time" : int(time.time()) ,"file":message.file, "message": message.message}}})

def thread_length(id: int):
    thread = collection.find_one({"thread_id": id})
    if thread is None:
        return 0
    else:
        return len(thread["list_messages"])


#Partie API
app = FastAPI()

@app.get("/thread/{thread_id}")
def get_thread(thread_id: int):
    thread = collection.find_one({"thread_id": thread_id})
    if thread is None:
        return {"message": "Thread not found"}
    else:
        return {"thread_id": thread["thread_id"], "list_messages": thread["list_messages"]}
    
@app.get("/thread/{thread_id}/message/{message_id}")
def get_message(thread_id: int, message_id: int):
    thread = collection.find_one({"thread_id": thread_id})
    if thread is None:
        return {"message": "Thread not found"}
    else:
        i = 0
        for message in thread["list_messages"]:
            if i == message_id:
                return Message(message_id=message["message_id"], message=message["message"])
            i += 1
        return {"message": "Message not found"}

@app.post("/thread/create")
def create_thread(thread: Thread):
    #{"thread_id": 1, "list_messages": {} }
    insert_thread(thread)
    return {"message": "Thread created"}

@app.post("/thread/{thread_id}/newmessage")
def post_message(thread_id: int, message: Message):
    #{"message_id": 1, "time": 1, "file": " ", "message" : "test"}
    insert_message(thread_id, message)
    return {"message": "Message posted"}


#fonction de test
@app.get("/db")
def get_db():
    for document in collection.find():
        print(document)
    return {"message": "db"}