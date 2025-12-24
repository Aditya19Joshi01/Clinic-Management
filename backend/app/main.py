from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, patients, appointments, follow_ups, dashboard, staff
from app.database import engine, Base
from app.config import settings

# Create tables (for development only; production usage should rely on Alembic)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clinic Management System", version="1.0.0")

# CORS Configuration
origins = settings.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"],
)

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(follow_ups.router)
app.include_router(dashboard.router)
app.include_router(staff.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Clinic Management API"}