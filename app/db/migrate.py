from sqlalchemy import inspect, text

from app.db.session import Base, DATABASE_URL, engine


def ensure_schema() -> None:
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    if "pollution_reports" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("pollution_reports")}
    statements: list[str] = []
    if "priority_label" not in columns:
        statements.append(
            "ALTER TABLE pollution_reports ADD COLUMN priority_label VARCHAR(50) DEFAULT 'low'"
        )
    if "workflow_status" not in columns:
        statements.append(
            "ALTER TABLE pollution_reports ADD COLUMN workflow_status VARCHAR(50) DEFAULT 'open'"
        )
    if "is_sample" not in columns:
        statements.append(
            "ALTER TABLE pollution_reports ADD COLUMN is_sample BOOLEAN DEFAULT 0"
        )
    if "reporter_contact" not in columns:
        statements.append(
            "ALTER TABLE pollution_reports ADD COLUMN reporter_contact VARCHAR(255)"
        )

    if not statements and DATABASE_URL.startswith("sqlite"):
        _backfill()
        return

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
    _backfill()


def _backfill() -> None:
    with engine.begin() as connection:
        rows = connection.execute(
            text("SELECT id, status, priority_label, workflow_status, priority_score FROM pollution_reports")
        ).fetchall()
        for row in rows:
            report_id, status, priority_label, workflow_status, score = row
            label = priority_label
            if status in {"critical", "high", "medium", "low"} and label in {None, "", "low"}:
                label = status
            if not label:
                label = "low"
            workflow = workflow_status or "open"
            if status in {"open", "investigating", "resolved"}:
                workflow = status
            connection.execute(
                text(
                    "UPDATE pollution_reports SET priority_label = :label, workflow_status = :workflow, status = :workflow WHERE id = :id"
                ),
                {"label": label, "workflow": workflow, "id": report_id},
            )
