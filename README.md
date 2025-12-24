# Clinic Management System

A robust, multi-tenant Clinic Management System built with a modern tech stack. It enables clinics to manage patients, appointments, staff, and follow-ups efficiently with strict data isolation between different companies.

## Features

-   **Multi-Tenancy**: Strict data isolation between clinics (Companies).
-   **Role-Based Access Control (RBAC)**: Admin and Staff roles with specific permissions.
-   **Patient Management**: Create, view, update, and delete patient records.
-   **Appointment Scheduling**: Schedule and manage appointments with status tracking.
-   **Clinical Notes & Follow-ups**: Record patient notes and schedule follow-up actions.
-   **Secure Authentication**: JWT-based authentication with password hashing.
-   **Modern Frontend**: Responsive UI built with React and TypeScript.
-   **Containerized**: Fully Dockerized for easy deployment.
-   **CI/CD**: GitHub Actions pipeline for automated backend testing.

## Tech Stack Choices & Rationale

### Backend
-   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11) (async, auto-docs, type safety)
-   **Database**: PostgreSQL (reliable, supports complex queries)
-   **ORM**: SQLAlchemy (mature, flexible)
-   **Migrations**: Alembic (database schema management)
-   **Testing**: Pytest, Httpx (In-memory SQLite for tests) (unit testing, integration testing)
-   **Authentication**: OAuth2 with JWT (stateless, scalable)

### Frontend
-   **Framework**: [React](https://react.dev/) (Vite) (modern, fast, component-based)
-   **Language**: TypeScript (type safety, component reuse)
-   **HTTP Client**: Axios (modern, type-safe)
-   **Styling**: CSS / Tailwind (responsive, modern, customizable)

### DevOps
-   **Containerization**: Docker & Docker Compose (easy local dev, production-ready)
-   **CI**: GitHub Actions (automated testing, deployment)

## System Architecture

![System Architecture](/images/architecture.png)

## Feature Roadmap

## Feature Roadmap

### MVP (Week 1-2) - Foundation & Core Operations [Completed]
- [x] **Authentication & Multi-Tenancy**: Secure JWT login, strict company-level data isolation, and Admin/Staff RBAC.
- [x] **Comprehensive Patient Management**: CRUD, Search, and Detailed Profiles with Clinical Notes.
- [x] **Appointment Workflow**: Scheduling, Status Tracking (Scheduled/Completed/Cancelled), and Calendar Views.
- [x] **Operational Tools**: Task management via Follow-ups and a Real-time Staff Dashboard for daily overviews.
- [x] **Backend Assurance**: Full test suite with CI/CD integration.

### V1 (Week 3-4) - Revenue & Advanced Workflow
- [ ] **Billing & Invoicing Module**: Generate professional invoices, track payment status (Paid/Pending), and export PDFs.
- [ ] **Prescription Management**: Digital prescription creator with customizable medicine templates and print layout.
- [ ] **Patient Communication Layer**: Automated email/SMS triggers for appointment confirmations and reminders (AWS SES / Twilio).
- [ ] **Granular Access Control**: Custom permission sets (e.g., "Front Desk" vs "Nurse" vs "Doctor").

### V2 (Future) - Scale & Ecosystem
- [ ] **Patient Self-Service Portal**: Dedicated secure view for patients to book appointments, view history, and pay bills online.
- [ ] **Telemedicine Integration**: Embedded secure video conferencing for remote consultations (WebRTC).
- [ ] **Lab & Pharmacy Integrations**: Standardized data exchange (HL7/FHIR) with external providers.
- [ ] **AI-Driven Analytics**: Revenue forecasting, "No-Show" prediction models, and intelligent scheduling optimization.

## Deployment Strategy & Cost Estimates (GBP)

### Strategy A: Serverless (Startups & Variable Load)
Ideal for initial launch or clinics with variable patient volume.
-   **Architecture**:
    -   **Frontend**: AWS S3 + CloudFront (Global CDN).
    -   **Backend**: AWS API Gateway + Lambda (Python runtime).
    -   **Database**: AWS Aurora Serverless (PostgreSQL).
-   **Pros**: Zero idle costs, automatic scaling, low maintenance.
-   **Estimated Cost**: ~£15-£25/month (Free Tier eligible for first year).

### Strategy B: Dedicated Containers (Enterprise/High Compliance)
Recommended for clinics with high, predictable daily volume or strict compliance requirements.
-   **Architecture**:
    -   **Orchestration**: AWS ECS (Fargate) or EKS (Kubernetes) for full control.
    -   **Containerization**: Dockerized services for Backend and Frontend.
    -   **Database**: Amazon RDS for PostgreSQL (Provisioned).
-   **Pros**: Consistent performance, easier debugging, simpler networking for microservices.
-   **Estimated Cost**: ~£60-£100/month (depending on instance types and redundancy).

### Cost Breakdown (Estimated)
| Service | Serverless (Monthly) | Dedicated (Monthly) |
| :--- | :--- | :--- |
| **Compute** | £5 (variable) | £40 (2x t3.medium) |
| **Database** | £10 (Aurora v2) | £35 (RDS db.t3.medium) |
| **Storage/CDN** | £2 | £5 |
| **Load Balancer** | £0 (Included in APIGW) | £15 (ALB) |
| **Total** | **~£17** | **~£95** |

### Cost Reduction Strategies
-   **Open-Source Stack**: Utilizing Linux, Python, and React eliminates expensive software licensing fees common in legacy medical software (e.g., Windows Server, proprietary DBs).
    -   *Potential Saving*: **£300+ per month** in licensing avoidance compared to enterprise commercial stacks.
-   **Modular Design**: The architecture allows enabling resource-heavy features (like AI analytics) only for premium (paying) clients, preventing "bloat costs" from eating into margins.
    -   *Potential Saving*: **Avoids ~£80/month** in premature over-provisioning by sticking to Serverless for early stages.
-   **Docker Containerization**: Standardized deployment reduces DevOps overhead and allows seamless migration to cheaper hosting providers (e.g., DigitalOcean or Hetzner) if AWS costs rise.
    -   *Potential Saving*: **40-60% reduction** in infrastructure costs by having the flexibility to switch providers without code refactoring.
-   **PostgreSQL**: Provides enterprise-grade reliability (ACID compliance, Row-Level Security) without the per-core licensing model of Oracle or SQL Server.
    -   *Potential Saving*: **£1,000s annually** in database licensing fees.

## Prerequisites

-   Docker & Docker Compose
-   Node.js (for local frontend dev)
-   Python 3.11+ (for local backend dev)

## Getting Started

### Option 1: Docker (Recommended)

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Aditya19Joshi01/Clinic-Management.git
    cd Clinic-Management
    ```

2.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    This will start:
    -   Backend API at `http://localhost:8000`
    -   Frontend at `http://localhost:7000` (mapped port)
    -   PostgreSQL Database

### Option 2: Local Development

#### Backend Setup
1.  Navigate to `backend`:
    ```bash
    cd backend
    ```
2.  Create virtual environment and install dependencies:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    
    pip install -r requirements.txt
    ```
3.  Set up Environment Variables:
    -   Copy `.env.example` to `.env`.
    -   Update `DATABASE_URL` if running a local Postgres instance (or use Docker for just the DB).
4.  Run Migrations:
    ```bash
    alembic upgrade head
    ```
5.  Start Server:
    ```bash
    uvicorn app.main:app --reload
    ```

#### Frontend Setup
1.  Navigate to `frontend`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Set up Environment Variables:
    -   Copy `.env.example` to `.env`.
    -   Set `VITE_API_URL=http://localhost:8000/api`.
4.  Start Dev Server:
    ```bash
    npm run dev
    ```

## Testing

The backend includes a comprehensive test suite using `pytest` and an in-memory SQLite database to ensure tenant isolation and workflow correctness.

Run tests locally:
```bash
cd backend
# Windows
$env:PYTHONPATH='backend'; .venv\Scripts\pytest backend/tests

# Linux/Mac
PYTHONPATH=. pytest tests
```

## Environment Variables

### Backend (`backend/.env`)
| Variable | Description | Default (Dev) |
| :--- | :--- | :--- |
| `DATABASE_URL` | Connection string for PostgreSQL | `postgresql://...` |
| `SECRET_KEY` | Key for signing JWTs | `supersecretkey` |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token validity duration | `10080` |
| `CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:5173", ...]` |

### Frontend (`frontend/.env`)
| Variable | Description |
| :--- | :--- |
| `VITE_API_URL` | Base URL of the backend API |

## Project Structure

```
Clinic-Management/
├── .github/              # GitHub Actions workflows
├── alembic/              # Database migration scripts
├── backend/              # Python FastAPI Backend
│   ├── app/
│   │   ├── models/       # SQLAlchemy Models
│   │   ├── routers/      # API Endpoints
│   │   ├── schemas/      # Pydantic Schemas
│   │   └── utils/        # Utilities (Security, GUID)
│   ├── tests/            # Pytest Test Suite
│   └── ...
├── frontend/             # React TypeScript Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── lib/          # API Client
│   └── ...
├── Dockerfiles/          # Docker build files
└── docker-compose.yml    # Orchestration
```
