from datetime import datetime

from pydantic import BaseModel


class CommentCreate(BaseModel):
    complaint: int
    comment: str
    file: str
    user: int


class CommentFetch(BaseModel):
    complaint: int
    comment: str
    file: str
    user: int
    created_on: datetime

    class Config:
        from_attributes = True