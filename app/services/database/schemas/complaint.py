from datetime import datetime

from pydantic import BaseModel

class ComplaintCreate(BaseModel):
    category: int
    subcategory: int
    location: str
    location_url: str
    complaint: str
    file: str
    status: int
    complainer: int
    officer: int


class ComplaintFetch(BaseModel):
    category: int
    subcategory: int
    location: str
    location_url: str
    complaint: str
    file: str
    status: int
    complainer: int
    officer: int
    created_on: datetime
    updated_on: datetime

    class Config:
        from_attributes = True


class ComplaintUpdate(BaseModel):
    id: int
    status: int
    complainer: int