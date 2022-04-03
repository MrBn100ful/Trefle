from pydantic import BaseModel

class Message(BaseModel):
    message_id : int
    time : int
    file : str
    message: str

class Thread(BaseModel):
    board_id : int
    thread_id : int
    list_messages: list[Message]
    
class Board(BaseModel):
    board_id : int
    board_name : str
    list_threads: list[Thread]