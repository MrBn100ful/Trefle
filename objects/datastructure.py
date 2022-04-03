from pydantic import BaseModel

class Message(BaseModel):
    """this is the structure for message"""
    message_id : int
    time : int
    file : str
    message: str

class Thread(BaseModel):
    """this is the structure for thread"""
    thread_id : int
    list_messages: list[Message]
    