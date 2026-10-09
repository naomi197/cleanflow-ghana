import { FormEvent, useEffect, useState } from "react";
import {
  createReport,
  getMeta,
  getReports,
  getStats,
  PollutionReport,
  ReportMeta,
  ReportStats,
  updateWorkflow
} from "./lib/api";

const EMPTY_FORM = {
  location: "",
  pollutant_type: "chemical",
  description: "",
  severity: 3,
  latitude: "",
  longitude: "",
  reporter_contact: ""
};

function App() {
  const [reports, setReports] = useState<PollutionReport[]>([]);
  const [meta, setMeta] = useState<ReportMeta | null>(null);
  const [stats, setStats] = useState<ReportStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [workflowFilter, setWorkflowFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");
  const [form, setForm] = useState(EMPTY_FORM);

  async function load(nextWorkflow = workflowFilter, nextPriority = priorityFilter) {
    try {
      setError("");
      const [reportRows, metaRow, statsRow] = await Promise.all([
        getReports(nextWorkflow, nextPriority),
        getMeta(),
        getStats()
      ]);
      setReports(reportRows);
      setMeta(metaRow);
      setStats(statsRow);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load reports");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  function applyPlace(name: string) {
    const place = meta?.places.find((item) => item.name === name);
    setForm((current) => ({
      ...current,
      location: name ? `${name}` : current.location,
      latitude: place ? String(place.latitude) : current.latitude,
      longitude: place ? String(place.longitude) : current.longitude
    }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      setError("");
      await createReport({
        location: form.location.trim(),
        pollutant_type: form.pollutant_type,
        description: form.description.trim(),
        severity: Number(form.severity),
        latitude: form.latitude ? Number(form.latitude) : null,
        longitude: form.longitude ? Number(form.longitude) : null,
        reporter_contact: form.reporter_contact.trim()
      });
      setForm(EMPTY_FORM);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create report");
    }
  }

  async function changeWorkflow(report: PollutionReport, workflow: PollutionReport["workflow_status"]) {
    try {
      setError("");
      await updateWorkflow(report.id, workflow);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update the report");
    }
  }

  return (
    <main className="container">
      <header className="hero">
        <p className="eyebrow">CleanFlow Ghana</p>
        <h1>Pollution response queue</h1>
        <p>
          Record a water-pollution incident, rank it, and move it from open to investigating to resolved.
        </p>
      </header>

      {stats && (
        <section className="stats">
          <Stat label="Open" value={stats.open} />
          <Stat label="Investigating" value={stats.investigating} />
          <Stat label="Resolved" value={stats.resolved} />
          <Stat label="Critical" value={stats.critical} />
        </section>
      )}

      <section className="layout">
        <section className="card">
          <h2>New report</h2>
          <form onSubmit={handleSubmit}>
            <label>
              Place in Ghana
              <select defaultValue="" onChange={(event) => applyPlace(event.target.value)}>
                <option value="">Choose a city, or type a location</option>
                {meta?.places.map((place) => (
                  <option key={place.name} value={place.name}>
                    {place.name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Location
              <input
                required
                minLength={2}
                value={form.location}
                onChange={(event) => setForm({ ...form, location: event.target.value })}
                placeholder="Korle Lagoon outfall, Accra"
              />
            </label>
            <label>
              Pollutant
              <select
                value={form.pollutant_type}
                onChange={(event) => setForm({ ...form, pollutant_type: event.target.value })}
              >
                {(meta?.pollutants ?? [{ value: "chemical", label: "Chemical" }]).map((item) => (
                  <option key={item.value} value={item.value}>
                    {item.label}
                  </option>
                ))}
              </select>
            </label>
            <label>
              What was seen
              <textarea
                required
                value={form.description}
                onChange={(event) => setForm({ ...form, description: event.target.value })}
                rows={4}
              />
            </label>
            <label>
              Severity
              <select
                value={String(form.severity)}
                onChange={(event) => setForm({ ...form, severity: Number(event.target.value) })}
              >
                <option value={1}>1 - Limited</option>
                <option value={2}>2 - Local</option>
                <option value={3}>3 - Spreading</option>
                <option value={4}>4 - Severe</option>
                <option value={5}>5 - Immediate danger</option>
              </select>
            </label>
            <div className="coords">
              <label>
                Latitude
                <input
                  value={form.latitude}
                  onChange={(event) => setForm({ ...form, latitude: event.target.value })}
                  inputMode="decimal"
                />
              </label>
              <label>
                Longitude
                <input
                  value={form.longitude}
                  onChange={(event) => setForm({ ...form, longitude: event.target.value })}
                  inputMode="decimal"
                />
              </label>
            </div>
            <label>
              Reporter contact
              <input
                value={form.reporter_contact}
                onChange={(event) => setForm({ ...form, reporter_contact: event.target.value })}
                placeholder="Optional email or phone"
              />
            </label>
            <button type="submit">Add to queue</button>
          </form>
          {meta && <p className="note">{meta.score_note}</p>}
        </section>

        <section className="card">
          <div className="section-heading">
            <h2>Queue</h2>
            <button type="button" className="secondary" onClick={() => void load()}>
              Refresh
            </button>
          </div>
          <div className="filters">
            <select
              value={workflowFilter}
              onChange={(event) => {
                setWorkflowFilter(event.target.value);
                void load(event.target.value, priorityFilter);
              }}
            >
              <option value="">All stages</option>
              <option value="open">Open</option>
              <option value="investigating">Investigating</option>
              <option value="resolved">Resolved</option>
            </select>
            <select
              value={priorityFilter}
              onChange={(event) => {
                setPriorityFilter(event.target.value);
                void load(workflowFilter, event.target.value);
              }}
            >
              <option value="">All priorities</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
          {loading && <p>Loading reports...</p>}
          {error && <p className="error">{error}</p>}
          {!loading && !error && reports.length === 0 && <p>No reports in this view.</p>}
          <div className="reports">
            {reports.map((report) => (
              <article className="report" key={report.id}>
                <div>
                  <h3>{report.location}</h3>
                  <p>
                    {report.pollutant_type.replace(/_/g, " ")} · severity {report.severity} · score{" "}
                    {report.priority_score}
                    {report.is_sample ? " · sample" : ""}
                  </p>
                  <p>{report.description}</p>
                  {report.reporter_contact && <p>Contact: {report.reporter_contact}</p>}
                  <div className="actions">
                    {(["open", "investigating", "resolved"] as const).map((stage) => (
                      <button
                        key={stage}
                        type="button"
                        className={report.workflow_status === stage ? "active" : "secondary"}
                        onClick={() => void changeWorkflow(report, stage)}
                      >
                        {stage}
                      </button>
                    ))}
                  </div>
                </div>
                <span className={`badge ${report.priority_label}`}>{report.priority_label}</span>
              </article>
            ))}
          </div>
        </section>
      </section>

      <QueueMap reports={reports} />
    </main>
  );
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <article className="stat">
      <strong>{value}</strong>
      <span>{label}</span>
    </article>
  );
}

function QueueMap({ reports }: { reports: PollutionReport[] }) {
  const mapped = reports.filter((report) => report.latitude != null && report.longitude != null);
  return (
    <section className="card">
      <h2>Mapped incidents</h2>
      {mapped.length === 0 ? (
        <p>Add a latitude and longitude to place a report on the map.</p>
      ) : (
        <ul className="map-list">
          {mapped.map((report) => (
            <li key={report.id}>
              <a
                href={`https://www.openstreetmap.org/?mlat=${report.latitude}&mlon=${report.longitude}#map=14/${report.latitude}/${report.longitude}`}
                target="_blank"
                rel="noreferrer"
              >
                {report.location}
              </a>
              <span>
                {report.priority_label} · {report.workflow_status}
              </span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default App;
