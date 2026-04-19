import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.database.schemas import complaint as complaint_schema
from app.services.database.schemas import comment as comment_schema
from app.services.database.conn import SessionLocal, Base
from app.services.database.conn import engine
from app.services.database.models import complaint as complaint_model
from app.services.database.models import comment as comment_model
from app.services.email.sender import send_email

Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/comment")
async def add_comment(
    comment: comment_schema.CommentCreate, 
    db: Session = Depends(get_db)
):

    data = comment.model_dump()
    new_comment = comment_model.Comment(
        **data
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment

@router.get("/comments/{complaint_id}", response_model=list[comment_schema.CommentFetch])
def get_comments(complaint_id: int, db: Session = Depends(get_db)):
    # Check if comments already exists
    comments = db.query(comment_model.Comment).filter(
        comment_model.Comment.complaintId == complaint_id
    ).all()

    if not comments:
        raise HTTPException(
            status_code=404, 
            detail="No comments found on this complaint"
        )

    return comments or None