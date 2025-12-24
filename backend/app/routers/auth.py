import random
import string
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import User, Company
from app.schemas import user as user_schema
from app.schemas import token as token_schema
from app.utils import security

router = APIRouter(prefix="/api/auth", tags=["auth"])

def generate_company_code():
    return "CLINIC" + "".join(random.choices(string.digits, k=3))

class LoginRequest(user_schema.BaseModel):
    email: str
    password: str

@router.post("/login", response_model=token_schema.Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).options(joinedload(User.company)).filter(User.email == credentials.email).first()
    if not user or not security.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": str(user.id), "company_id": str(user.company_id), "role": user.role})
    
    user_read = user_schema.UserRead(
        email=user.email,
        name=user.name,
        id=user.id,
        role=user.role,
        company_id=user.company_id,
        company_name=user.company.name,
        company_code=user.company.code
    )

    return {"access_token": access_token, "token_type": "bearer", "user": user_read}


@router.post("/register/company", response_model=token_schema.Token)
def register_company(data: user_schema.CompanyRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    
    company_code = generate_company_code()
    while db.query(Company).filter(Company.code == company_code).first():
        company_code = generate_company_code()
        
    new_company = Company(name=data.companyName, code=company_code)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    
    hashed_password = security.get_password_hash(data.password)
    new_user = User(
        email=data.email,
        password_hash=hashed_password,
        name=data.adminName,
        role="admin",
        company_id=new_company.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = security.create_access_token(data={"sub": str(new_user.id), "company_id": str(new_company.id), "role": "admin"})
    
    user_read = user_schema.UserRead(
        email=new_user.email,
        name=new_user.name,
        id=new_user.id,
        role=new_user.role,
        company_id=new_company.id,
        company_name=new_company.name,
        company_code=new_company.code
    )
    
    return {"access_token": access_token, "token_type": "bearer", "user": user_read}


@router.post("/register/staff", response_model=token_schema.Token)
def register_staff(data: user_schema.StaffRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    
    company = db.query(Company).filter(Company.code == data.companyCode).first()
    if not company:
        raise HTTPException(status_code=404, detail="Invalid company code")
        
    hashed_password = security.get_password_hash(data.password)
    new_user = User(
        email=data.email,
        password_hash=hashed_password,
        name=data.name,
        role="staff",
        company_id=company.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = security.create_access_token(data={"sub": str(new_user.id), "company_id": str(company.id), "role": "staff"})
    
    user_read = user_schema.UserRead(
        email=new_user.email,
        name=new_user.name,
        id=new_user.id,
        role=new_user.role,
        company_id=company.id,
        company_name=company.name,
        company_code=company.code
    )
    
    return {"access_token": access_token, "token_type": "bearer", "user": user_read}


@router.post("/logout")
def logout(current_user: User = Depends(security.get_current_user_dependency_placeholder)):
    # Since we use stateless JWTs, "logout" is mostly a frontend action (deleting the token).
    # However, to be thorough, we could add token blacklisting here in the future.
    # For now, we return a success message.
    return {"message": "Successfully logged out"}
