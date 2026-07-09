---

# Data Extraction Service API

A robust, production-ready REST API built with **Django** and **Django REST Framework (DRF)** designed to handle asynchronous data extraction workflows. This service initializes extraction jobs, tracks execution lifecycles, exposes endpoints for result compilation, and enforces reliable error-handling guards against common API edge cases.

---

## Architecture & Workflow

Because data extraction operations can take time, this service is architected asynchronously.

```
[Client App] ---> (POST /scan/start) ---> [Django API Engine] ---> [SQLite Database]
                                                    │                   │
                                             (Accepts Job)        (Saves PENDING)
                                                    │
                                                    ▼
                                         [Immediate 202 Response]

```

1. **Job Initialization**: The client requests a new scan by providing an authentication token. The API instantly spins up an isolated `PENDING` job database entry and returns a unique `job_id` via a `202 ACCEPTED` status code.
2. **Polling & Tracking**: The client polls the status using the assigned `job_id`.
3. **Data Integrity Guards**: The service prevents common sequence flaws (e.g., blocking requests to read results of a job that is still processing).

---

##  Getting Started

### 1. Environment Setup

Clone the repository and navigate into the workspace:

```bash
cd FINAL-BACKEND-PROJECT

```

Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

```

### 2. Install Dependencies

```bash
pip install django djangorestframework

```

### 3. Database Migrations

Initialize the local SQLite database structural schemas:

```bash
python manage.py makemigrations
python manage.py migrate

```

### 4. Run the Server

```bash
python manage.py runserver

```

The application will be accessible locally at `http://127.0.0.1:8000/`.

---

##  API Endpoints Reference

All application endpoints are prefixed with `/api/v1/`.

| Endpoint | Method | Expected Payload | Success Status | Description |
| --- | --- | --- | --- | --- |
| `scan/start` | **POST** | `{"token": "string"}` | `202 Accepted` | Initiates a fresh extraction task. |
| `scan/status/<uuid:job_id>` | **GET** | *None* | `200 OK` | Retrieves current job progress metrics. |
| `scan/result/<uuid:job_id>` | **GET** | *None* | `200 OK` | Compiles extracted data structures. |
| `scan/cancel/<uuid:job_id>` | **POST** | *None* | `200 OK` | Halts a pending or running job. |
| `scan/remove/<uuid:job_id>` | **DELETE** | *None* | `200 OK` | Wipes target job data records from DB. |
| `jobs/jobs` | **GET** | *None* | `200 OK` | Lists all historical job records. |

---

##  Implemented Edge-Case Guards

* **Token Validation**: Returns `400 Bad Request` if the initialization payload lacks a valid string token.
* **Route Type-Safety**: Utilizes route parameter casting (`<uuid:job_id>`) to filter and block invalid input patterns before hitting database layers.
* **Resource Separation**: Rejects data compilation calls with a `400 Bad Request` if a client requests results from a job that is still `PENDING` or `IN_PROGRESS`.
* **State Mutation Integrity**: Blocks attempts to cancel jobs that are already marked as `COMPLETED`, `FAILED`, or `CANCELLED`.
