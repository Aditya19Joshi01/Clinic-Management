import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from app.utils.guid import GUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    patient_id = Column(GUID(), ForeignKey("patients.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_by_user_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("app.models.patient.Patient")
    created_by_user = relationship("app.models.user.User")
    company = relationship("app.models.company.Company")

    @property
    def createdBy(self):
        return self.created_by_user.name if self.created_by_user else "Unknown"
