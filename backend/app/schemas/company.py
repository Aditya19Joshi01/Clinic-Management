from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class CompanyRead(CompanyBase):
    id: UUID
    code: str
    created_at: datetime

    class Config:
        from_attributes = True
