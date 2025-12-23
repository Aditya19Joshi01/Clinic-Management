from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import User, Patient, Note, Appointment, FollowUp
from app.schemas import patient as patient_schema
from app.schemas import note as note_schema
from app.utils import security

router = APIRouter(prefix="/api/patients", tags=["patients"])

@router.get("/", response_model=List[patient_schema.PatientRead])
def get_patients(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Patient).filter(Patient.company_id == current_user.company_id)
    
    if search:
        search_filter = or_(
            Patient.name.ilike(f"%{search}%"),
            Patient.email.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
        
    patients = query.offset(skip).limit(limit).all()
    return patients

@router.post("/", response_model=patient_schema.PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient: patient_schema.PatientCreate,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    # Check for existing email within the company? Optional business logic.
    # Allowing duplicate emails for now unless unique constraint exists.
    
    new_patient = Patient(
        **patient.model_dump(),
        company_id=current_user.company_id
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

@router.get("/{patient_id}", response_model=patient_schema.PatientRead)
def get_patient(
    patient_id: UUID,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id, 
        Patient.company_id == current_user.company_id
    ).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{patient_id}", response_model=patient_schema.PatientRead)
def update_patient(
    patient_id: UUID,
    patient_update: patient_schema.PatientUpdate,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id, 
        Patient.company_id == current_user.company_id
    ).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_data = patient_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(patient, key, value)
        
    db.commit()
    db.refresh(patient)
    return patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: UUID,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id, 
        Patient.company_id == current_user.company_id
    ).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Optional: Check if patient has appointments/followups and block delete or cascade?
    # SQLAlchemy relationships might handle cascade if configured, currently manual.
    # For now, we just delete.
    db.delete(patient)
    db.commit()
    return None

# --- NOTES SUB-RESOURCE ---

@router.get("/{patient_id}/notes", response_model=List[note_schema.NoteRead])
def get_patient_notes(
    patient_id: UUID,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    # Verify patient exists and belongs to company
    patient = db.query(Patient).filter(
        Patient.id == patient_id, 
        Patient.company_id == current_user.company_id
    ).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    notes = db.query(Note).filter(
        Note.patient_id == patient_id,
        Note.company_id == current_user.company_id
    ).order_by(Note.created_at.desc()).all()
    return notes

@router.post("/{patient_id}/notes", response_model=note_schema.NoteRead)
def create_patient_note(
    patient_id: UUID,
    note: note_schema.NoteCreate,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id, 
        Patient.company_id == current_user.company_id
    ).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    new_note = Note(
        content=note.content,
        patient_id=patient_id,
        created_by_user_id=current_user.id,
        company_id=current_user.company_id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note
