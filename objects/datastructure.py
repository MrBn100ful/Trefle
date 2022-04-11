from pydantic import BaseModel

class Message(BaseModel):
    message_id : int
    time : int
    file : str
    message: str

class Thread(BaseModel):
    thread_id : int
    list_messages: list[Message]
    
class Board(BaseModel):
    board_id : int
    board_name : str
    board_description : str
    list_threads: list[Thread]
    
class Imageboard(BaseModel):
    list_boards: list[Board]