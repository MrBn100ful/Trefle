from turtle import color
from pymongo import MongoClient
import time
from objects.datastructure import Imageboard, Board, Thread, Message

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
        collection.update_one({"thread_id": thread_id}, {"$push": {"list_messages": {"message_id": get_threadlengthdb(thread_id),"time" : int(time.time()) ,"file":message.file, "message": message.message}}})

def get_threadlengthdb(thread_id: int):
    """this function is used to get the length of the thread in the database"""
    thread = collection.find_one({"thread_id": int(thread_id)})
    if thread == None:
        return -1
    else :
        return len(thread["list_messages"])

def get_imageboarddb():
    """this function is used to find all the boards"""
    boards = collection.find({"board_id": {"$exists": True}})
    if boards == None:
        return {"message": "No boards found"}
    else :
        return boards
    

def get_boarddb(board_id: int):
    board = collection.find_one({"board_id": board_id})
    if board is None:
        return {"message": "Board not found"}
    else:
        return {"board_id": board["board_id"], "board_name": board["board_name"], "board_description": board["board_description"], "list_threads": board["list_threads"]}

def get_threaddb(board_id: int, thread_id: int):
    board = get_boarddb(board_id)
    if board == {"message": "Board not found"}:
        return board
    else:
        for thread in board["list_threads"]:
            if thread_id == thread["thread_id"]:
                return 
        return {"message": "Thread not found"}

def get_messagedb(board_id: int, thread_id: int, message_id: int):
    thread = get_threaddb(board_id, thread_id)
    if thread == {"message": "Board not found"}:
        return thread
    else:
        for message in thread["list_messages"]:
            if message_id == message["message_id"]:
                return message
        return {"message": "Message not found"}
    
    
    
def init_imageboarddb():
    """this function is used to initialize the imageboard database"""
    collection.insert_one({"list_boards": [{"board_id": 0, "board_name": "b", "board_description": "a imageboard", "list_threads": []}]})
    collection.update_one({"board_id": 0}, {"$push": {"list_threads": {"thread_id": 0, "list_messages": []}}})
    collection.update_one({"board_id": 0}, {"$push": {"list_threads": {"thread_id": 1, "list_messages": []}}})
    collection.update_one({"board_id": 0}, {"$push": {"list_threads": {"thread_id": 2, "list_messages": []}}})