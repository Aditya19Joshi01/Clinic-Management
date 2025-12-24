
from fastapi import status

def test_register_company(client):
    payload = {
        "email": "owner@newclinic.com",
        "password": "securepassword",
        "adminName": "Dr. Owner",
        "companyName": "New Clinic"
    }
    response = client.post("/api/auth/register/company", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "admin"
    assert data["user"]["company_name"] == "New Clinic"

def test_register_existing_email(client):
    # First registration
    payload = {
        "email": "duplicate@clinic.com",
        "password": "pass",
        "adminName": "Dup",
        "companyName": "Dup Clinic"
    }
    client.post("/api/auth/register/company", json=payload)
    
    # Second registration with same email
    response = client.post("/api/auth/register/company", json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT

def test_login(client, admin_a):
    payload = {
        "email": admin_a.email,
        "password": "password"
    }
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["user"]["company_id"] == str(admin_a.company_id)

def test_login_invalid_credentials(client):
    payload = {
        "email": "nonexistent@test.com",
        "password": "wrong"
    }
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
