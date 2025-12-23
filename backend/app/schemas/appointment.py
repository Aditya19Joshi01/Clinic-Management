from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date
from typing import Optional
from enum import Enum

class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"

class AppointmentBase(BaseModel):
    date: date
    time: str
    reason: str
    status: AppointmentStatus = AppointmentStatus.scheduled

class AppointmentCreate(AppointmentBase):
    patient_id: UUID

class AppointmentUpdate(BaseModel):
    date: Optional[date] = None
    time: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[AppointmentStatus] = None

class AppointmentRead(AppointmentBase):
    id: UUID
    patient_id: UUID
    patientName: str # Computed property in model
    company_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
