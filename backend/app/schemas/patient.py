from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime, date
from typing import Optional

class PatientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    date_of_birth: Optional[date] = None
    address: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None

class PatientRead(PatientBase):
    id: UUID
    company_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
