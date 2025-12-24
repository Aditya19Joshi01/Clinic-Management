from typing import List, Optional
from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import User, Appointment, Patient
from app.schemas import appointment as appointment_schema
from app.utils import security

router = APIRouter(prefix="/api/appointments", tags=["appointments"])

@router.get("/", response_model=List[appointment_schema.AppointmentRead])
def get_appointments(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None,
    limit: int = 100,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Appointment).options(joinedload(Appointment.patient)).filter(Appointment.company_id == current_user.company_id)
    
    if start_date:
        query = query.filter(Appointment.date >= start_date)
    if end_date:
        query = query.filter(Appointment.date <= end_date)
    if status:
        query = query.filter(Appointment.status == status)
        
    appointments = query.order_by(Appointment.date.asc(), Appointment.time.asc()).limit(limit).all()
    return appointments

@router.post("/", response_model=appointment_schema.AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment: appointment_schema.AppointmentCreate,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    # Verify patient exists
    patient = db.query(Patient).filter(
        Patient.id == appointment.patient_id,
        Patient.company_id == current_user.company_id
    ).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    new_appointment = Appointment(
        **appointment.model_dump(),
        company_id=current_user.company_id
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

@router.patch("/{appointment_id}", response_model=appointment_schema.AppointmentRead)
def update_appointment(
    appointment_id: UUID,
    appointment_update: appointment_schema.AppointmentUpdate,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.company_id == current_user.company_id
    ).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
        
    update_data = appointment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(appointment, key, value)
        
    db.commit()
    db.refresh(appointment)
    return appointment
