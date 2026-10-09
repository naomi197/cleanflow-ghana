from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.pollution_report import PollutionReport
from app.schemas.pollution_report import (
    PollutionReportCreate,
    PollutionReportResponse,
    WorkflowUpdate,
)
from app.services.prioritization import (
    GHANA_PLACES,
    POLLUTANT_LABELS,
    POLLUTANT_WEIGHTS,
    calculate_priority_score,
    priority_status,
)

router = APIRouter(prefix="/reports", tags=["Reports"])

WORKFLOW_STATUSES = ("open", "investigating", "resolved")
PRIORITY_LABELS = ("critical", "high", "medium", "low")


@router.get("/meta")
def report_meta() -> dict[str, object]:
    return {
        "pollutants": [
            {
                "value": key,
                "label": POLLUTANT_LABELS[key],
                "weight": POLLUTANT_WEIGHTS[key],
            }
            for key in POLLUTANT_LABELS
        ],
        "places": GHANA_PLACES,
        "workflow_statuses": list(WORKFLOW_STATUSES),
        "priority_labels": list(PRIORITY_LABELS),
        "score_note": (
            "A severity of 5 for a chemical discharge scores 100. "
            "The weights are a triage rule for this project, not a Ghana EPA standard."
        ),
    }


@router.post("", response_model=PollutionReportResponse, status_code=201)
def create_report(
    report_data: PollutionReportCreate,
    db: Session = Depends(get_db),
) -> PollutionReport:
    report = PollutionReport(**report_data.model_dump())
    report.priority_score = calculate_priority_score(report)
    report.priority_label = priority_status(report.priority_score)
    report.workflow_status = "open"
    report.status = "open"
    report.is_sample = False
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@router.get("", response_model=list[PollutionReportResponse])
def list_reports(
    workflow_status: str | None = Query(default=None),
    priority_label: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[PollutionReport]:
    query = db.query(PollutionReport)
    if workflow_status:
        if workflow_status not in WORKFLOW_STATUSES:
            raise HTTPException(status_code=422, detail="Unknown workflow status")
        query = query.filter(PollutionReport.workflow_status == workflow_status)
    if priority_label:
        if priority_label not in PRIORITY_LABELS:
            raise HTTPException(status_code=422, detail="Unknown priority label")
        query = query.filter(PollutionReport.priority_label == priority_label)
    return query.order_by(PollutionReport.priority_score.desc(), PollutionReport.id.desc()).all()


@router.get("/stats")
def get_report_stats(db: Session = Depends(get_db)) -> dict[str, int | float | None]:
    total_reports = db.query(func.count(PollutionReport.id)).scalar() or 0
    average_priority_score = db.query(func.avg(PollutionReport.priority_score)).scalar()
    label_rows = (
        db.query(PollutionReport.priority_label, func.count(PollutionReport.id))
        .group_by(PollutionReport.priority_label)
        .all()
    )
    workflow_rows = (
        db.query(PollutionReport.workflow_status, func.count(PollutionReport.id))
        .group_by(PollutionReport.workflow_status)
        .all()
    )
    labels = {str(label): count for label, count in label_rows}
    workflows = {str(status): count for status, count in workflow_rows}
    return {
        "total_reports": int(total_reports),
        "average_priority_score": (
            round(float(average_priority_score), 2) if average_priority_score is not None else None
        ),
        "critical": int(labels.get("critical", 0)),
        "high": int(labels.get("high", 0)),
        "medium": int(labels.get("medium", 0)),
        "low": int(labels.get("low", 0)),
        "open": int(workflows.get("open", 0)),
        "investigating": int(workflows.get("investigating", 0)),
        "resolved": int(workflows.get("resolved", 0)),
    }


@router.patch("/{report_id}", response_model=PollutionReportResponse)
def update_workflow(
    report_id: int,
    update: WorkflowUpdate,
    db: Session = Depends(get_db),
) -> PollutionReport:
    report = db.query(PollutionReport).filter(PollutionReport.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Pollution report not found")
    report.workflow_status = update.workflow_status
    report.status = update.workflow_status
    db.commit()
    db.refresh(report)
    return report


@router.get("/{report_id}", response_model=PollutionReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)) -> PollutionReport:
    report = db.query(PollutionReport).filter(PollutionReport.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Pollution report not found")
    return report
