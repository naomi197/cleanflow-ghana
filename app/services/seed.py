from sqlalchemy.orm import Session

from app.models.pollution_report import PollutionReport
from app.services.prioritization import calculate_priority_score, priority_status


SAMPLE_REPORTS = [
    {
        "location": "Korle Lagoon outfall, Accra",
        "pollutant_type": "sewage",
        "severity": 5,
        "latitude": 5.5376,
        "longitude": -0.2168,
        "description": "Dark discharge entering the lagoon beside the drain.",
        "workflow_status": "open",
    },
    {
        "location": "Tema fishing harbour",
        "pollutant_type": "oil",
        "severity": 4,
        "latitude": 5.6333,
        "longitude": 0.0167,
        "description": "Oil sheen along the inner harbour wall.",
        "workflow_status": "investigating",
    },
    {
        "location": "Subin River, Kumasi",
        "pollutant_type": "chemical",
        "severity": 5,
        "latitude": 6.6901,
        "longitude": -1.6145,
        "description": "Strong chemical odour and discoloured water downstream of the market.",
        "workflow_status": "open",
    },
    {
        "location": "Sekondi beach drain, Takoradi",
        "pollutant_type": "plastic",
        "severity": 3,
        "latitude": 4.9340,
        "longitude": -1.7137,
        "description": "Plastic waste collecting where the storm drain meets the beach.",
        "workflow_status": "open",
    },
    {
        "location": "Tamale central market gutter",
        "pollutant_type": "solid_waste",
        "severity": 2,
        "latitude": 9.4075,
        "longitude": -0.8530,
        "description": "Blocked gutter with solid waste after rainfall.",
        "workflow_status": "resolved",
    },
]


def seed_samples_if_empty(db: Session) -> None:
    existing = db.query(PollutionReport).count()
    if existing:
        return

    for item in SAMPLE_REPORTS:
        report = PollutionReport(
            location=item["location"],
            pollutant_type=item["pollutant_type"],
            severity=item["severity"],
            latitude=item["latitude"],
            longitude=item["longitude"],
            description=item["description"],
            workflow_status=item["workflow_status"],
            status=item["workflow_status"],
            is_sample=True,
        )
        report.priority_score = calculate_priority_score(report)
        report.priority_label = priority_status(report.priority_score)
        db.add(report)
    db.commit()
