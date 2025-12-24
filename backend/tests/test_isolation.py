
from fastapi import status

def test_tenant_isolation_patients(client, token_headers_a, token_headers_b):
    # 1. Create a patient for Company A
    patient_payload = {
        "name": "Alice A",
        "email": "alice@companya.com",
        "phone": "1234567890",
        "date_of_birth": "1990-01-01",
        "gender": "Female",
        "address": "123 St A",
        "emergency_contact_name": "Bob",
        "emergency_contact_phone": "0987654321"
    }
    create_response = client.post(
        "/api/patients/", 
        json=patient_payload, 
        headers=token_headers_a
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    patient_id_a = create_response.json()["id"]

    # 2. Company A should see this patient
    get_a = client.get(f"/api/patients/{patient_id_a}", headers=token_headers_a)
    assert get_a.status_code == status.HTTP_200_OK
    assert get_a.json()["id"] == patient_id_a

    # 3. Company B should NOT see this patient (404 Not Found)
    get_b = client.get(f"/api/patients/{patient_id_a}", headers=token_headers_b)
    assert get_b.status_code == status.HTTP_404_NOT_FOUND

def test_tenant_isolation_list_patients(client, token_headers_a, token_headers_b):
    # Create patient for A
    client.post(
        "/api/patients/", 
        json={"name": "P1", "email": "p1@a.com", "phone": "1", "date_of_birth": "2000-01-01", "gender": "F"}, 
        headers=token_headers_a
    )
    
    # Create patient for B
    client.post(
        "/api/patients/", 
        json={"name": "P2", "email": "p2@b.com", "phone": "2", "date_of_birth": "2000-01-01", "gender": "M"}, 
        headers=token_headers_b
    )
    
    # List for A -> Should only see P1
    list_a = client.get("/api/patients/", headers=token_headers_a).json()
    assert len(list_a) == 1
    assert list_a[0]["email"] == "p1@a.com"
    
    # List for B -> Should only see P2
    list_b = client.get("/api/patients/", headers=token_headers_b).json()
    assert len(list_b) == 1
    assert list_b[0]["email"] == "p2@b.com"
