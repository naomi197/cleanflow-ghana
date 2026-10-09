# CleanFlow Ghana

A water-pollution response queue for towns in Ghana.

People record what they see. The queue ranks each incident and a response team moves it from open, to investigating, to resolved.

Developer: Alireza Sani · [alirezafazeli@live.com](mailto:alirezafazeli@live.com)

This project is prepared for the pollution-control track of the [Tech Hub Africa Hackathon 2026 on DoraHacks](https://dorahacks.io/hackathon/hackathon2026challenge/detail).

## What you can do

- File a report with a place, pollutant, severity, description, optional coordinates, and an optional contact
- See a priority score from 0 to 100 and a label: critical, high, medium, or low
- Filter the queue and change the workflow stage
- Open any mapped incident in OpenStreetMap
- Start from five sample incidents in Accra, Tema, Kumasi, Takoradi, and Tamale when the database is empty

## Priority

Severity runs from 1 to 5 and is multiplied by 12. A pollutant weight is added: chemical 25, sewage 20, oil 20, plastic 10, solid waste 8, unknown 5. That sum is scaled so a chemical discharge at severity 5 scores 100.

These weights are a triage rule for this project. They are not a Ghana EPA or WHO standard.

## Setup

```bash
git clone https://github.com/naomi197/cleanflow-ghana.git
cd cleanflow-ghana
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

On Windows PowerShell, activate the environment with `.\.venv\Scripts\Activate.ps1`.

The API is at http://127.0.0.1:8000. Interactive docs are at http://127.0.0.1:8000/docs.

The desk is in `cleanflow-ghana-frontend/`:

```bash
cd cleanflow-ghana-frontend
npm ci
npm run dev
```

The page is at http://127.0.0.1:5173.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Check that the API is running |
| GET | `/reports/meta` | Pollutants, Ghana places, and the score note |
| POST | `/reports` | Create a report and assign its priority |
| GET | `/reports` | List reports by descending priority |
| GET | `/reports/stats` | Counts by priority and workflow stage |
| PATCH | `/reports/{report_id}` | Set `workflow_status` to `open`, `investigating`, or `resolved` |
| GET | `/reports/{report_id}` | Read one report |

```json
{
  "location": "Korle Lagoon outfall, Accra",
  "pollutant_type": "sewage",
  "severity": 5,
  "latitude": 5.5376,
  "longitude": -0.2168,
  "description": "Dark discharge entering the lagoon."
}
```

## Tests

```bash
python -m pytest tests -q
```

## Author

Alireza Sani — [naomi197](https://github.com/naomi197)
