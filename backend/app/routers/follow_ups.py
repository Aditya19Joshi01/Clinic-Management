from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import User, FollowUp, Patient
from app.schemas import follow_up as follow_up_schema
from app.utils import security

router = APIRouter(prefix="/api/followups", tags=["followups"])

@router.get("/", response_model=List[follow_up_schema.FollowUpRead])
def get_followups(
    status: Optional[str] = None,
    limit: int = 100,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(FollowUp).options(joinedload(FollowUp.patient)).filter(FollowUp.company_id == current_user.company_id)
    
    if status:
        query = query.filter(FollowUp.status == status)
        
    follow_ups = query.order_by(FollowUp.due_date.asc()).limit(limit).all()
    return follow_ups

@router.post("/", response_model=follow_up_schema.FollowUpRead, status_code=status.HTTP_201_CREATED)
def create_followup(
    followup: follow_up_schema.FollowUpCreate,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == followup.patient_id,
        Patient.company_id == current_user.company_id
    ).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    new_followup = FollowUp(
        **followup.model_dump(),
        company_id=current_user.company_id
    )
    db.add(new_followup)
    db.commit()
    db.refresh(new_followup)
    return new_followup

@router.patch("/{followup_id}", response_model=follow_up_schema.FollowUpRead)
def update_followup(
    followup_id: UUID,
    followup_update: follow_up_schema.FollowUpUpdate,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    followup = db.query(FollowUp).filter(
        FollowUp.id == followup_id,
        FollowUp.company_id == current_user.company_id
    ).first()
    if not followup:
        raise HTTPException(status_code=404, detail="FollowUp not found")
    
    update_data = followup_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(followup, key, value)
        
    db.commit()
    db.refresh(followup)
    return followup
