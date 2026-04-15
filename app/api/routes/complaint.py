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
        complaint_model.Complaint.category == complaint.category,
        complaint_model.Complaint.subcategory == complaint.subcategory,
        complaint_model.Complaint.complaint == complaint.complaint,
        complaint_model.Complaint.complainer == complaint.complainer
    ).first()
    if existing_complaint:
        raise HTTPException(
            status_code=400, 
            detail="Complaint already registered"
        )

    # Create complaint
    new_complaint = complaint_model.Complaint(
        category=complaint.category,
        subcategory=complaint.subcategory,
        location=complaint.location,
        location_url=complaint.location_url,
        complaint=complaint.complaint,
        file=complaint.file,
        status=complaint.status,
        complainer=complaint.complainer,
        officer=complaint.officer
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return {
        "message": "Complaint registered successfully"
    }


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
    
    if existing_complaint.complainer == complaint.complainer :
        raise HTTPException(
            status_code=400, 
            detail="Only complainer can update status"
        )

    existing_complaint.status = complaint.status
    
    db.commit()

    return {
        "message": "Complaint registered successfully"
    }


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