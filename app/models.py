from pydantic import BaseModel

class Quote(BaseModel):
    text: str
    author: str