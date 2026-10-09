const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export type PollutionReport = {
  id: number;
  location: string;
  pollutant_type: string;
  description: string | null;
  severity: number;
  latitude: number | null;
  longitude: number | null;
  reporter_contact: string | null;
  workflow_status: "open" | "investigating" | "resolved";
  priority_label: "critical" | "high" | "medium" | "low";
  priority_score: number;
  is_sample: boolean;
  created_at: string;
};

export type PollutionReportCreate = {
  location: string;
  pollutant_type: string;
  description: string;
  severity: number;
  latitude?: number | null;
  longitude?: number | null;
  reporter_contact?: string;
};

export type ReportMeta = {
  pollutants: { value: string; label: string; weight: number }[];
  places: { name: string; latitude: number; longitude: number }[];
  workflow_statuses: string[];
  priority_labels: string[];
  score_note: string;
};

export type ReportStats = {
  total_reports: number;
  average_priority_score: number | null;
  critical: number;
  high: number;
  medium: number;
  low: number;
  open: number;
  investigating: number;
  resolved: number;
};

async function readJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`Request failed (${response.status})`);
  }
  return response.json();
}

export function getReports(workflowStatus = "", priorityLabel = ""): Promise<PollutionReport[]> {
  const params = new URLSearchParams();
  if (workflowStatus) params.set("workflow_status", workflowStatus);
  if (priorityLabel) params.set("priority_label", priorityLabel);
  const query = params.toString();
  return fetch(`${API_BASE_URL}/reports${query ? `?${query}` : ""}`).then((response) =>
    readJson<PollutionReport[]>(response)
  );
}

export function getMeta(): Promise<ReportMeta> {
  return fetch(`${API_BASE_URL}/reports/meta`).then((response) => readJson<ReportMeta>(response));
}

export function getStats(): Promise<ReportStats> {
  return fetch(`${API_BASE_URL}/reports/stats`).then((response) => readJson<ReportStats>(response));
}

export function createReport(report: PollutionReportCreate): Promise<PollutionReport> {
  return fetch(`${API_BASE_URL}/reports`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(report)
  }).then((response) => readJson<PollutionReport>(response));
}

export function updateWorkflow(
  reportId: number,
  workflowStatus: PollutionReport["workflow_status"]
): Promise<PollutionReport> {
  return fetch(`${API_BASE_URL}/reports/${reportId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ workflow_status: workflowStatus })
  }).then((response) => readJson<PollutionReport>(response));
}
