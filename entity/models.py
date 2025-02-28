from pydantic import BaseModel

class Information(BaseModel):
    version: str
    service: str
    author: str