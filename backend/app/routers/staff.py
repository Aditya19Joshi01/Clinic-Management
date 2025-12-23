from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import user as user_schema
from app.utils import security

router = APIRouter(prefix="/api/staff", tags=["staff"])

@router.get("/", response_model=List[user_schema.UserRead])
def get_staff(
    current_admin: User = Depends(security.get_current_admin_user),
    db: Session = Depends(get_db)
):
    # Only admins can see this list (enforced by dependency)
    # List all users in the company
    staff_members = db.query(User).filter(User.company_id == current_admin.company_id).all()
    return staff_members

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_staff(
    user_id: UUID,
    current_admin: User = Depends(security.get_current_admin_user),
    db: Session = Depends(get_db)
):
    # Ensure not deleting self
    if user_id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove yourself"
        )
    
    user_to_remove = db.query(User).filter(
        User.id == user_id,
        User.company_id == current_admin.company_id
    ).first()
    
    if not user_to_remove:
        raise HTTPException(status_code=404, detail="Staff member not found")
        
    db.delete(user_to_remove)
    db.commit()
    return None
