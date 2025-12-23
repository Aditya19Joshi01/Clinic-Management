import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Date as SqlDate, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    date_of_birth = Column(SqlDate, nullable=True) # Changed to nullable as it might optionally be empty string in frontend
    address = Column(Text, nullable=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("app.models.company.Company")
