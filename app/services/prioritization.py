from app.models.pollution_report import PollutionReport


POLLUTANT_WEIGHTS: dict[str, float] = {
    "oil": 20.0,
    "chemical": 25.0,
    "sewage": 20.0,
    "plastic": 10.0,
    "solid_waste": 8.0,
    "unknown": 5.0,
}


def calculate_priority_score(report: PollutionReport) -> float:
    severity_score = report.severity * 12.0

    pollutant_key = report.pollutant_type.strip().lower().replace(" ", "_")
    pollutant_score = POLLUTANT_WEIGHTS.get(pollutant_key, 5.0)

    score = severity_score + pollutant_score
    return round(min(score, 100.0), 2)


def priority_status(score: float) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 35:
        return "medium"
    return "low"
