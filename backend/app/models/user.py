import uuid
import enum
from sqlalchemy import Column, String, ForeignKey, DateTime, Enum
from app.utils.guid import GUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"

class User(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("app.models.company.Company")

    @property
    def company_name(self):
        return self.company.name if self.company else ""

    @property
    def company_code(self):
        return self.company.code if self.company else ""


