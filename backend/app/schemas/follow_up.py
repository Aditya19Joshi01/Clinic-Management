from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date
from typing import Optional
from enum import Enum

class FollowUpStatus(str, Enum):
    open = "open"
    completed = "completed"

class FollowUpBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date
    status: FollowUpStatus = FollowUpStatus.open

class FollowUpCreate(FollowUpBase):
    patient_id: UUID

class FollowUpUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[FollowUpStatus] = None

class FollowUpRead(FollowUpBase):
    id: UUID
    patient_id: UUID
    patientName: str # Computed property
    company_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
