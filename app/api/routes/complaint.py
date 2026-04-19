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


@router.post("/register_complaint")
async def register_complaint(
    complaint: complaint_schema.ComplaintCreate, 
    db: Session = Depends(get_db)
):
    # Check if complaint already exists
    existing_complaint = db.query(complaint_model.Complaint).filter(
        complaint_model.Complaint.categoryId == complaint.categoryId,
        complaint_model.Complaint.subcategoryId == complaint.subcategoryId,
        complaint_model.Complaint.latitude == complaint.latitude,
        complaint_model.Complaint.longitude == complaint.longitude,
        complaint_model.Complaint.complainer == complaint.complainer,
        complaint_model.Complaint.statusId.in_([1, 2])
    ).first()
    if existing_complaint:
        return existing_complaint

    # Create complaint
    new_complaint = complaint_model.Complaint(
        title=complaint.title,
        description=complaint.description,
        categoryId=complaint.categoryId,
        subcategoryId=complaint.subcategoryId,
        statusId=complaint.statusId,
        city=complaint.city,
        location=complaint.location,
        latitude=complaint.latitude,
        longitude=complaint.longitude,
        file_path=complaint.file_path,        
        complainer=complaint.complainer,
        officer=complaint.officer
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return new_complaint


@router.post("/update_complaint")
async def update_complaint(
    complaint: complaint_schema.ComplaintUpdate, 
    db: Session = Depends(get_db)
):
    # Check if complaint already exists
    existing_complaint = db.query(complaint_model.Complaint).filter(
        complaint_model.Complaint.id == complaint.id,
    ).first()

    if not existing_complaint:
        raise HTTPException(
            status_code=400, 
            detail="Complaint not found"
        )
    
    if existing_complaint.complainer != complaint.complainer :
        raise HTTPException(
            status_code=400, 
            detail="Only complainer can update status"
        )

    existing_complaint.statusId = complaint.statusId
    
    db.commit()

    return {
        "message": "Complaint registered successfully"
    }


@router.get("/all_complaints", response_model=list[complaint_schema.ComplaintFetch])
def all_complaints(db: Session = Depends(get_db)):
    # Check if complaint already exists
    complaints = db.query(complaint_model.Complaint).all()

    if not complaints:
        raise HTTPException(
            status_code=404, 
            detail="No complaint registered with this user account"
        )

    return complaints


@router.get("/complaints/{user_id}", response_model=list[complaint_schema.ComplaintFetch])
def get_complaints(user_id: int, db: Session = Depends(get_db)):
    # Check if complaint already exists
    complaints = db.query(complaint_model.Complaint).filter(
        complaint_model.Complaint.complainer == user_id
    ).all()

    if not complaints:
        raise HTTPException(
            status_code=404, 
            detail="No complaint registered with this user account"
        )

    return complaints

@router.get("/get_complaint/{complaint_id}", response_model=complaint_schema.ComplaintFetch)
def get_complaints(complaint_id: int, db: Session = Depends(get_db)):
    # Check if complaint already exists
    complaints = db.query(complaint_model.Complaint).filter(
        complaint_model.Complaint.id == complaint_id
    ).first()

    if not complaints:
        raise HTTPException(
            status_code=404, 
            detail="No complaint registered with this id"
        )

    return complaints