from pydantic import BaseModel


class Promise(BaseModel):
    promise: str
    source: str
    date: str
