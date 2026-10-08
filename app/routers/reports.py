from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.pollution_report import PollutionReport
from app.schemas.pollution_report import (
    PollutionReportCreate,
    PollutionReportResponse,
)
from app.services.prioritization import (
    calculate_priority_score,
    priority_status,
)

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post(
    "",
    response_model=PollutionReportResponse,
    status_code=201,
)
def create_report(
    report_data: PollutionReportCreate,
    db: Session = Depends(get_db),
) -> PollutionReport:
    report = PollutionReport(**report_data.model_dump())

    report.priority_score = calculate_priority_score(report)
    report.status = priority_status(report.priority_score)

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


@router.get(
    "",
    response_model=list[PollutionReportResponse],
)
def list_reports(
    db: Session = Depends(get_db),
) -> list[PollutionReport]:
    return (
        db.query(PollutionReport)
        .order_by(PollutionReport.priority_score.desc())
        .all()
    )


@router.get("/stats")
def get_report_stats(
    db: Session = Depends(get_db),
) -> dict[str, int | float | None]:
    total_reports = db.query(func.count(PollutionReport.id)).scalar() or 0

    average_priority_score = (
        db.query(func.avg(PollutionReport.priority_score)).scalar()
    )

    status_rows = (
        db.query(
            PollutionReport.status,
            func.count(PollutionReport.id),
        )
        .group_by(PollutionReport.status)
        .all()
    )

    status_counts = {
        str(status): count
        for status, count in status_rows
    }

    return {
        "total_reports": int(total_reports),
        "average_priority_score": (
            round(float(average_priority_score), 2)
            if average_priority_score is not None
            else None
        ),
        "critical": int(status_counts.get("critical", 0)),
        "high": int(status_counts.get("high", 0)),
        "medium": int(status_counts.get("medium", 0)),
        "low": int(status_counts.get("low", 0)),
        "pending": int(status_counts.get("pending", 0)),
    }


@router.get(
    "/{report_id}",
    response_model=PollutionReportResponse,
)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
) -> PollutionReport:
    report = (
        db.query(PollutionReport)
        .filter(PollutionReport.id == report_id)
        .first()
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Pollution report not found",
        )

    return report
