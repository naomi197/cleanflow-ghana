from fastapi.testclient import TestClient

from app.db.session import Base, engine
from app.main import app

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_report():
    payload = {
        "location": "Accra drainage channel",
        "pollutant_type": "chemical",
        "severity": 5,
        "latitude": 5.6037,
        "longitude": -0.1870,
        "description": "Visible chemical discharge",
    }

    response = client.post("/reports", json=payload)
    data = response.json()

    assert response.status_code == 201
    assert data["location"] == payload["location"]
    assert data["priority_score"] == 100.0
    assert data["priority_label"] == "critical"
    assert data["workflow_status"] == "open"
    assert data["is_sample"] is False


def test_list_reports():
    response = client.get("/reports")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_missing_report_returns_404():
    response = client.get("/reports/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Pollution report not found"


def test_invalid_severity_is_rejected():
    payload = {
        "location": "Accra drainage channel",
        "pollutant_type": "chemical",
        "severity": 6,
        "description": "Invalid severity value",
    }

    response = client.post("/reports", json=payload)

    assert response.status_code == 422


def test_reports_are_sorted_by_priority():
    low_priority_payload = {
        "location": "Accra residential area",
        "pollutant_type": "plastic",
        "severity": 1,
        "description": "Small amount of plastic waste",
    }
    high_priority_payload = {
        "location": "Accra industrial area",
        "pollutant_type": "chemical",
        "severity": 5,
        "description": "Severe chemical discharge",
    }

    low_response = client.post("/reports", json=low_priority_payload)
    high_response = client.post("/reports", json=high_priority_payload)

    assert low_response.status_code == 201
    assert high_response.status_code == 201
    assert low_response.json()["priority_label"] == "low"

    response = client.get("/reports")
    scores = [report["priority_score"] for report in response.json()]

    assert scores == sorted(scores, reverse=True)


def test_workflow_can_be_updated():
    created = client.post(
        "/reports",
        json={
            "location": "Tema harbour",
            "pollutant_type": "oil",
            "severity": 4,
            "description": "Oil sheen",
        },
    )
    report_id = created.json()["id"]

    updated = client.patch(f"/reports/{report_id}", json={"workflow_status": "resolved"})

    assert updated.status_code == 200
    assert updated.json()["workflow_status"] == "resolved"
    assert updated.json()["priority_label"] in {"critical", "high", "medium", "low"}

    listed = client.get("/reports", params={"workflow_status": "resolved"})
    assert any(report["id"] == report_id for report in listed.json())


def test_meta_lists_ghana_places():
    response = client.get("/reports/meta")
    names = [place["name"] for place in response.json()["places"]]

    assert response.status_code == 200
    assert "Accra" in names
    assert "Kumasi" in names
