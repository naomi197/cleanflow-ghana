from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PollutionReportBase(BaseModel):
    location: str = Field(min_length=2, max_length=255)
    pollutant_type: str = Field(min_length=2, max_length=100)
    severity: int = Field(default=1, ge=1, le=5)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    description: str | None = None


class PollutionReportCreate(PollutionReportBase):
    pass


class PollutionReportResponse(PollutionReportBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    priority_score: float
    created_at: datetime
