from pydantic import BaseModel
class Question(BaseModel):
    question:str
    #differentiate user
    uuid:int
