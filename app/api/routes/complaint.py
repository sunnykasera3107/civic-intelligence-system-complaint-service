import os
from datetime import datetime
import json

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from redis import Redis

from app.services.database.schemas import complaint as complaint_schema
from app.services.database.schemas import comment as comment_schema
from app.services.database.conn import SessionLocal, Base
from app.services.database.conn import engine
from app.services.database.models import complaint as complaint_model
from app.services.database.models import comment as comment_model
from app.services.email.sender import send_email
from app.utils.helper import Helper

Base.metadata.create_all(bind=engine)
router = APIRouter()
rd = Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    decode_responses=True
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register_complaint")
async def register_complaint(
    request: Request,
    complaint: complaint_schema.ComplaintCreate, 
    db: Session = Depends(get_db)
):
    # Check if complaint already exists
    existing_complaint = db.query(complaint_model.Complaint).filter(
        complaint_model.Complaint.categoryId == complaint.categoryId,
        complaint_model.Complaint.subcategoryId == complaint.subcategoryId,
        complaint_model.Complaint.latitude == complaint.latitude,
        complaint_model.Complaint.longitude == complaint.longitude,
        complaint_model.Complaint.complainerId == complaint.complainerId,
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
        complainerId=complaint.complainerId,
        officerId=complaint.officerId,
        complainer=complaint.complainer,
        officer=complaint.officer
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    
    body = {
        "latitude": complaint.latitude,
        "longitude": complaint.longitude,
        "city": complaint.city,
        "departmentId": complaint.categoryId,
        "complainerId": complaint.complainerId,
        "complaintId": new_complaint.id
    }
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)
    headers.pop("content-encoding", None)

    try:
        res = await request.app.state.httpclient.post(
            endpoint=os.getenv("USER_SERVICE_URL") + "/nearest_officer",
            payload=body,
            headers=headers
        )

        officer = json.loads(res.get("content"))    
        new_complaint.officer = officer.get("name")
        new_complaint.officerId = officer.get("id")

        db.commit()

    except Exception as e:
        print(f"{e}")

    complaints_exist = False
    if rd.exists("complaints"):
        complaints = json.loads(rd.get("complaints"))
        if len(complaints) > 0:
            new_complaint_json = Helper.to_dict(new_complaint)
            complaints.append(new_complaint_json)
            complaints_exist = True
            rd.set("complaints", json.dumps(complaints, default=str))

    if not complaints_exist:
        complaints = [new_complaint]

    return complaints


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

    complaints_exist = False
    if rd.exists("complaints"):
        complaints = json.loads(rd.get("complaints"))
        if len(complaints) > 0:
            updates = list(map(lambda item: {**item, "statusId": complaint.statusId} if item.get("id") == complaint.id else item, complaints))
            rd.set("complaints", json.dumps(updates, default=str))

    return {
        "message": "Complaint updated successfully"
    }


@router.get("/all_complaints", response_model=list[complaint_schema.ComplaintFetch])
async def all_complaints(request: Request, db: Session = Depends(get_db)):
    # Check if complaint already exists
    complaints_exist = False
    if rd.exists("complaints"):
        complaints = json.loads(rd.get("complaints"))
        if len(complaints) > 0:
            complaints_exist = False
    if not complaints_exist:
        complaints = db.query(complaint_model.Complaint).all()
        
        if len(complaints) > 0:
            complaints_json = json.dumps([
                {
                    k: v for k, v in c.__dict__.items()
                    if not k.startswith("_")
                }
                for c in complaints
            ], default=str)
            rd.set("complaints", complaints_json)

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