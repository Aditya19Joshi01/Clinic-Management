
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import AsyncGenerator, Generator

from app.database import Base, get_db
from app.main import app
from app.utils import security
from app.models import User, Company

# Use in-memory SQLite database for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator:
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    # Override the get_db dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    
    # Use TestClient as context manager or simply allow requests
    # Since we are using httpx AsyncClient for async tests or TestClient for sync?
    # The routers seem sync (def root()...), so TestClient is simpler.
    # However, httpx is standard for modern fastapi testing.
    # Let's use TestClient for sync endpoints for simplicity, or stick to httpx.
    # The user asked for tests, I'll use TestClient approach via httpx for consistence.
    
    from fastapi.testclient import TestClient
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()

@pytest.fixture
def company_a(db_session):
    company = Company(name="Company A", code="COMPA")
    db_session.add(company)
    db_session.commit()
    db_session.refresh(company)
    return company

@pytest.fixture
def company_b(db_session):
    company = Company(name="Company B", code="COMPB")
    db_session.add(company)
    db_session.commit()
    db_session.refresh(company)
    return company

@pytest.fixture
def admin_a(db_session, company_a):
    user = User(
        email="admin@companya.com",
        password_hash=security.get_password_hash("password"),
        name="Admin A",
        role="admin",
        company_id=company_a.id
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def admin_b(db_session, company_b):
    user = User(
        email="admin@companyb.com",
        password_hash=security.get_password_hash("password"),
        name="Admin B",
        role="admin",
        company_id=company_b.id
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def token_headers_a(admin_a):
    access_token = security.create_access_token(
        data={"sub": str(admin_a.id), "company_id": str(admin_a.company_id), "role": admin_a.role}
    )
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def token_headers_b(admin_b):
    access_token = security.create_access_token(
        data={"sub": str(admin_b.id), "company_id": str(admin_b.company_id), "role": admin_b.role}
    )
    return {"Authorization": f"Bearer {access_token}"}
