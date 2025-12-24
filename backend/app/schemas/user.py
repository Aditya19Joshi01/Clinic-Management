from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum
from typing import Optional
from datetime import datetime

class UserRole(str, Enum):
    admin = "admin"
    staff = "staff"

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    company_id: UUID
    role: UserRole

class UserRead(UserBase):
    id: UUID
    role: UserRole
    company_id: UUID
    company_name: str
    company_code: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class StaffRegister(UserBase):
    password: str
    companyCode: str

class CompanyRegister(BaseModel):
    companyName: str
    adminName: str
    email: EmailStr
    password: str
