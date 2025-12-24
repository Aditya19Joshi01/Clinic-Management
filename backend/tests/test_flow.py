
from fastapi import status
from datetime import datetime, timedelta

def test_patient_appointment_flow(client, token_headers_a):
    # 1. Create Patient
    patient_payload = {
        "name": "Flow Patient",
        "email": "flow@test.com",
        "phone": "555-5555",
        "date_of_birth": "1985-05-05",
        "gender": "Male"
    }
    patient_resp = client.post("/api/patients/", json=patient_payload, headers=token_headers_a)
    assert patient_resp.status_code == status.HTTP_201_CREATED
    patient_id = patient_resp.json()["id"]

    # 2. Create Appointment for that Patient
    tomorrow_date = (datetime.now() + timedelta(days=1)).date().isoformat()
    appointment_payload = {
        "patient_id": patient_id,
        "date": tomorrow_date,
        "time": "10:00",
        "reason": "General Checkup",
        "status": "scheduled"
    }
    appt_resp = client.post("/api/appointments/", json=appointment_payload, headers=token_headers_a)
    assert appt_resp.status_code == status.HTTP_201_CREATED
    appt_data = appt_resp.json()
    assert appt_data["patient_id"] == patient_id
    assert appt_data["reason"] == "General Checkup"

    # 3. Verify Appointment appears in list
    list_resp = client.get("/api/appointments/", headers=token_headers_a)
    assert list_resp.status_code == status.HTTP_200_OK
    appointments = list_resp.json()
    assert len(appointments) >= 1
    assert any(a["id"] == appt_data["id"] for a in appointments)
