from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class NoteBase(BaseModel):
    content: str

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: UUID
    patient_id: UUID
    created_by_user_id: UUID
    createdBy: str # Computed property
    created_at: datetime

    class Config:
        from_attributes = True
