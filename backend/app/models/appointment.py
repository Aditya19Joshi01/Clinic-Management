import uuid
import enum
from sqlalchemy import Column, String, ForeignKey, DateTime, Date as SqlDate, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    date = Column(SqlDate, nullable=False)
    time = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("app.models.patient.Patient")
    company = relationship("app.models.company.Company")

    @property
    def patientName(self):
        return self.patient.name if self.patient else "Unknown"
