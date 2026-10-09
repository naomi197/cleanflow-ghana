from app.models.pollution_report import PollutionReport


POLLUTANT_WEIGHTS: dict[str, float] = {
    "oil": 20.0,
    "chemical": 25.0,
    "sewage": 20.0,
    "plastic": 10.0,
    "solid_waste": 8.0,
    "unknown": 5.0,
}

POLLUTANT_LABELS: dict[str, str] = {
    "chemical": "Chemical",
    "sewage": "Sewage",
    "oil": "Oil",
    "plastic": "Plastic",
    "solid_waste": "Solid waste",
    "unknown": "Unknown",
}

# Severity is 1–5, so the heaviest case is 5 * 12 + 25.
MAX_RAW_SCORE = 85.0

GHANA_PLACES: list[dict[str, float | str]] = [
    {"name": "Accra", "latitude": 5.6037, "longitude": -0.1870},
    {"name": "Tema", "latitude": 5.6698, "longitude": -0.0166},
    {"name": "Kumasi", "latitude": 6.6885, "longitude": -1.6244},
    {"name": "Takoradi", "latitude": 4.8845, "longitude": -1.7554},
    {"name": "Cape Coast", "latitude": 5.1053, "longitude": -1.2466},
    {"name": "Tamale", "latitude": 9.4034, "longitude": -0.8424},
]


def normalize_pollutant(value: str) -> str:
    key = value.strip().lower().replace("-", " ").replace(" ", "_")
    aliases = {
        "chemicals": "chemical",
        "waste": "solid_waste",
        "trash": "solid_waste",
        "solidwaste": "solid_waste",
        "rubbish": "solid_waste",
    }
    return aliases.get(key, key)


def calculate_priority_score(report: PollutionReport) -> float:
    severity_score = report.severity * 12.0
    pollutant_score = POLLUTANT_WEIGHTS.get(normalize_pollutant(report.pollutant_type), 5.0)
    raw_score = severity_score + pollutant_score
    scaled = raw_score / MAX_RAW_SCORE * 100.0
    return round(min(scaled, 100.0), 2)


def priority_status(score: float) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 35:
        return "medium"
    return "low"
