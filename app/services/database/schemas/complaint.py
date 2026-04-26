from datetime import datetime

from pydantic import BaseModel

class ComplaintCreate(BaseModel):
    title: str
    description: str
    categoryId: int
    subcategoryId: int
    statusId: int
    city: str
    location: str
    latitude: float
    longitude: float
    file_path: str
    complainerId: int
    officerId: int
    complainer: str
    officer: str


class ComplaintFetch(BaseModel):
    id: int
    title: str
    description: str
    categoryId: int
    subcategoryId: int
    statusId: int
    location: str
    latitude: float
    longitude: float
    file_path: str
    complainerId: int
    officerId: int
    complainer: str
    officer: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class ComplaintUpdate(BaseModel):
    id: int
    statusId: int
    complainerId: int