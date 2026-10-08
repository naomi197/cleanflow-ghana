import { FormEvent, useEffect, useState } from "react";
import {
  createReport,
  getReports,
  PollutionReport,
  PollutionReportCreate
} from "./lib/api";

function App() {
  const [reports, setReports] = useState<PollutionReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [form, setForm] = useState<PollutionReportCreate>({
    location: "",
    pollutant_type: "",
    description: "",
    severity: 3
  });

  async function loadReports() {
    try {
      setError("");
      const data = await getReports();
      setReports(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load reports");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadReports();
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    try {
      setError("");

      const payload: PollutionReportCreate = {
        location: form.location.trim(),
        pollutant_type: form.pollutant_type.trim(),
        description: form.description.trim(),
        severity: form.severity
      };

      await createReport(payload);

      setForm({
        location: "",
        pollutant_type: "",
        description: "",
        severity: 3
      });

      await loadReports();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create report");
    }
  }

  return (
    <main className="container">
      <header className="hero">
        <p className="eyebrow">CleanFlow Ghana</p>
        <h1>Pollution Reports</h1>
        <p>Monitor and report environmental pollution in your community.</p>
      </header>

      <section className="card">
        <h2>Submit a report</h2>

        <form onSubmit={handleSubmit}>
          <label>
            Location
            <input
              required
              minLength={2}
              value={form.location}
              onChange={(event) =>
                setForm({ ...form, location: event.target.value })
              }
              placeholder="Example: Accra Central"
            />
          </label>

          <label>
            Pollutant type
            <input
              required
              minLength={2}
              value={form.pollutant_type}
              onChange={(event) =>
                setForm({ ...form, pollutant_type: event.target.value })
              }
              placeholder="Example: Plastic waste"
            />
          </label>

          <label>
            Description
            <textarea
              required
              value={form.description}
              onChange={(event) =>
                setForm({ ...form, description: event.target.value })
              }
              placeholder="Describe the pollution issue"
              rows={4}
            />
          </label>

          <label>
            Severity
            <select
              value={form.severity}
              onChange={(event) =>
                setForm({
                  ...form,
                  severity: Number(event.target.value)
                })
              }
            >
              <option value={1}>1 - Very low</option>
              <option value={2}>2 - Low</option>
              <option value={3}>3 - Moderate</option>
              <option value={4}>4 - High</option>
              <option value={5}>5 - Critical</option>
            </select>
          </label>

          <button type="submit">Submit report</button>
        </form>
      </section>

      <section className="card">
        <div className="section-heading">
          <h2>Recent reports</h2>
          <button type="button" onClick={() => void loadReports()}>
            Refresh
          </button>
        </div>

        {loading && <p>Loading reports...</p>}
        {error && <p className="error">{error}</p>}

        {!loading && !error && reports.length === 0 && (
          <p>No reports found.</p>
        )}

        <div className="reports">
          {reports.map((report) => (
            <article className="report" key={report.id}>
              <div>
                <h3>{report.location}</h3>
                <p>Pollutant: {report.pollutant_type}</p>
                <p>{report.description}</p>
                <p>Status: {report.status}</p>
                <p>Priority score: {report.priority_score}</p>
              </div>

              <span className="badge">
                Severity {report.severity}
              </span>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

export default App;
