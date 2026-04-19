from datetime import datetime

from pydantic import BaseModel


class CommentCreate(BaseModel):
    complaintId: int
    user: str
    userId: int
    comment: str
    file: str


class CommentFetch(BaseModel):
    id: int
    complaintId: int
    comment: str
    file: str
    user: str
    userId: int
    createdAt: datetime

    class Config:
        from_attributes = True