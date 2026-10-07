from fastapi import APIRouter, Depends, HTTPException
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
