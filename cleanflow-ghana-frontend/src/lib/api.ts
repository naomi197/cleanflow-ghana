const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export type PollutionReport = {
  id: number;
  location: string;
  pollutant_type: string;
  description: string;
  severity: number;
  status: string;
  priority_score: number;
  created_at: string;
};

export type PollutionReportCreate = {
  location: string;
  pollutant_type: string;
  description: string;
  severity: number;
};

export async function getReports(): Promise<PollutionReport[]> {
  const response = await fetch(`${API_BASE_URL}/reports`);

  if (!response.ok) {
    throw new Error(`Failed to fetch reports: ${response.status}`);
  }

  return response.json();
}

export async function createReport(
  report: PollutionReportCreate
): Promise<PollutionReport> {
  const response = await fetch(`${API_BASE_URL}/reports`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(report)
  });

  if (!response.ok) {
    throw new Error(`Failed to create report: ${response.status}`);
  }

  return response.json();
}
