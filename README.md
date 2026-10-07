# CleanFlow Ghana

> A smart water-pollution reporting and prioritization API for Ghana.

CleanFlow Ghana is a FastAPI-based backend designed to help communities and response teams report, prioritize, and manage water-pollution incidents.

The project automatically calculates a priority score for each pollution report based on the pollutant type and severity level. Reports can then be sorted so that the most urgent incidents receive attention first.

## Features

- FastAPI REST API
- Pollution-report management
- Automatic priority-score calculation
- Severity validation from 1 to 5
- Priority categories:
  - `critical`
  - `high`
  - `medium`
  - `low`
- Reports sorted by priority
- SQLite database support
- Pydantic request validation
- Automated tests with pytest
- Designed for environmental response workflows in Ghana

## Project Structure
```text
cleanflow-ghana/
├── app/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── main.py
├── tests/
├── .venv/
└── README.md

## Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- Uvicorn

## Installation

Clone the repository and enter the project directory:

bash
git clone https://github.com/naomi197/cleanflow-ghana.git
cd cleanflow-ghana

Create and activate a virtual environment on Windows:

powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

Install the dependencies:

powershell
python -m pip install -r requirements.txt

## Running the API

Start the development server:

powershell
python -m uvicorn app.main:app --reload

The API will be available at:

text
http://127.0.0.1:8000

Interactive API documentation:

text
http://127.0.0.1:8000/docs

Alternative documentation:

text
http://127.0.0.1:8000/redoc

## API Endpoints

### Health Check

http
GET /health

Checks whether the API is running.

### Create a Pollution Report

http
POST /reports

Example request:

json
{
  "location": "Accra drainage channel",
  "pollutant_type": "chemical",
  "severity": 5,
  "description": "Severe chemical discharge"
}

The API calculates the priority score and assigns a priority category automatically.

### List Pollution Reports

http
GET /reports

Reports are returned in descending order of `priority_score`.

### Get a Specific Report

http
GET /reports/{report_id}

Returns the details of a single pollution report.

## Priority System

The prioritization engine combines:

1. Pollutant type
2. Severity level

The final score is normalized to a range from `0` to `100`.

Each report is assigned one of the following categories:

text
critical
high
medium
low

This allows response teams to focus first on incidents with the highest potential environmental impact.

## Running Tests

Run the complete test suite:

powershell
python -m pytest .\tests -q

Current test coverage includes:

- API health check
- Successful report creation
- Invalid severity validation
- Report listing
- Priority-based sorting
- Missing-report handling

Expected result:

text
6 passed

A Starlette/httpx deprecation warning may appear. It does not currently cause test failure.

## Hackathon Value

CleanFlow Ghana addresses a practical environmental challenge:

- Makes pollution reporting structured and consistent
- Helps prioritize limited response resources
- Provides a foundation for community-based reporting
- Supports data-driven environmental intervention
- Can be extended with geolocation, dashboards, notifications, and analytics

## Future Roadmap

- Add user authentication and role-based access
- Add GPS coordinates and map visualization
- Add image upload for pollution evidence
- Add a dashboard for authorities and NGOs
- Add email or SMS notifications for critical reports
- Add PostgreSQL support for production deployment
- Add deployment with Docker
- Add historical pollution analytics
- Add multilingual support for local communities

## Contributing

Contributions are welcome.

1. Create a feature branch.
2. Implement and test your changes.
3. Run the test suite.
4. Submit a pull request.

## License

This project is currently intended for hackathon and educational development.

## Author

**Alireza Fazeli**

Automation & Software Engineer | Python, Web3 & Computational Civil Engineering

GitHub: [@naomi197](https://github.com/naomi197)
