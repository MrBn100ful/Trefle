from pymongo import MongoClient
import time
from objects.datastructure import Thread, Message

client = MongoClient('mongodb://localhost:27017/')
db = client.test_database
collection = db.test_collection

def insert_threaddb(thread: Thread):
    """this function is used to insert a thread in the database"""
    collection.insert_one({"thread_id": thread.thread_id, "list_messages": {} })
    for message in thread.list_messages:
        insert_messagedb(thread.thread_id, message)

def insert_messagedb(thread_id: int ,message: Message):
    """this function is used to insert a message in the thread database"""
    if get_threadlengthdb(thread_id) == -1:
        collection.update_one({"thread_id": thread_id}, {"$push": {"list_messages": {"message_id": 0,"time" : int(time.time()) ,"file":message.file, "message": message.message}}})
    else:
        collection.update_one({"thread_id": thread_id}, {"$push": {"list_messages": {"message_id": thread_length(thread_id),"time" : int(time.time()) ,"file":message.file, "message": message.message}}})

def get_threadlengthdb(thread_id: int):
    """this function is used to get the length of the thread in the database"""
    thread = collection.find_one({"thread_id": int(thread_id)})
    if thread == None:
        return -1
    else :
        return len(thread["list_messages"])

def get_threaddb(thread_id: int):
    thread = collection.find_one({"thread_id": thread_id})
    if thread is None:
        return {"message": "Thread not found"}
    else:
        return {"thread_id": thread["thread_id"], "list_messages": thread["list_messages"]}

def get_messagedb(thread_id: int, message_id: int):
    thread = collection.find_one({"thread_id": thread_id})
    if thread is None:
        return {"message": "Thread not found"}
    else:
        i = 0
        for message in thread["list_messages"]:
            if message_id == i:
                return message
            i += 1
        return {"message": "Message not found"}