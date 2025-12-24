from typing import List
from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.database import get_db
from app.models import User, Patient, Appointment, FollowUp
from app.schemas import appointment as appointment_schema
from app.schemas import follow_up as follow_up_schema
from app.utils import security
from pydantic import BaseModel

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

class DashboardStats(BaseModel):
    totalPatients: int
    todayAppointments: int
    openFollowUps: int
    upcomingAppointments: List[appointment_schema.AppointmentRead]
    openFollowUpsList: List[follow_up_schema.FollowUpRead]

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    today = date.today()
    company_id = current_user.company_id
    
    total_patients = db.query(Patient).filter(Patient.company_id == company_id).count()
    
    today_appointments_count = db.query(Appointment).filter(
        Appointment.company_id == company_id,
        Appointment.date == today,
        Appointment.status == "scheduled"
    ).count()
    
    open_followups_query = db.query(FollowUp).options(joinedload(FollowUp.patient)).filter(
        FollowUp.company_id == company_id,
        FollowUp.status == "open"
    )
    open_followups_count = open_followups_query.count()
    open_followups_list = open_followups_query.order_by(FollowUp.due_date.asc()).limit(5).all()
    
    upcoming_appointments = db.query(Appointment).options(joinedload(Appointment.patient)).filter(
        Appointment.company_id == company_id,
        Appointment.date >= today,
        Appointment.status == "scheduled"
    ).order_by(Appointment.date.asc(), Appointment.time.asc()).limit(5).all()
    
    return DashboardStats(
        totalPatients=total_patients,
        todayAppointments=today_appointments_count,
        openFollowUps=open_followups_count,
        upcomingAppointments=upcoming_appointments,
        openFollowUpsList=open_followups_list
    )
