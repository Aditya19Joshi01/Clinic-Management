import uuid
import enum
from sqlalchemy import Column, String, ForeignKey, DateTime, Date as SqlDate, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class FollowUpStatus(str, enum.Enum):
    open = "open"
    completed = "completed"

class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(SqlDate, nullable=False)
    status = Column(Enum(FollowUpStatus), default=FollowUpStatus.open, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("app.models.patient.Patient")
    company = relationship("app.models.company.Company")

    @property
    def patientName(self):
        return self.patient.name if self.patient else "Unknown"
