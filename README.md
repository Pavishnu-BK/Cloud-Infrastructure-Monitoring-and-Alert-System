# Cloud Infrastructure Monitoring and Automated Alert System

A lightweight, robust DevOps laboratory project demonstrating a full-stack Python Flask monitoring application backed by SQLite, integrated with a complete continuous integration and deployment (CI/CD) lifecycle using Git, Docker, Pytest, Jenkins, and Ansible.

---

## 1. Project Overview & Problem Statement

### 1.1 Problem Statement
Modern distributed systems require continuous visibility into compute resources (CPU, Memory, Disk) to prevent service degradation and unhandled resource exhaustion. System administrators need deterministic automated alerting that detects anomalous conditions without flooding alert feeds with duplicate notifications or false positives. Additionally, deploying and managing such systems requires an automated, repeatable DevOps pipeline guaranteeing that code passes testing before reaching production.

### 1.2 Objectives
1. **Real-time Observability**: Collect real host/container metrics (CPU %, RAM %, Monitored Disk %, Uptime) using Python's `psutil` library.
2. **Automated Alerting**: Evaluate metrics against configurable thresholds, implementing alert deduplication and automatic incident resolution.
3. **Data Persistence**: Store chronological snapshots, alerts, and settings in an SQLite database mounted on a persistent Docker Volume.
4. **Automated CI/CD Pipeline**: Implement an end-to-end DevOps automation flow: Checkout &rarr; Docker Build &rarr; Automated Pytest Execution &rarr; Ansible Deployment.
5. **Laboratory Demonstration Readiness**: Provide an intuitive web interface with clear controls to simulate, verify, and resolve alerts for academic laboratory evaluations and viva examinations.

---

## 2. Technology Stack

| Domain | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript | Responsive Operations Center UI, live AJAX auto-refresh, and HTML5 Canvas trend visualization (No external bloated JS frameworks). |
| **Backend** | Python 3.11, Flask | Lightweight WSGI web framework, REST API routes, and metric evaluation logic. |
| **System Metrics** | `psutil` library | Direct host/container telemetry (CPU, virtual memory, disk usage, and boot time). |
| **Database** | SQLite 3 (`data/monitoring.db`) | Embedded relational database with parameterized queries for metrics, alerts, and settings. |
| **Automated Testing** | Pytest | Unit and integration test suite executing with isolated in-memory/temporary test databases and mocked metrics. |
| **Containerization** | Docker (`python:3.11-slim`) | Containerized runtime with health checks, exposing port `5000`. |
| **Persistent Storage** | Docker Volume (`cloud_monitoring_data`) | Mounts to `/app/data` to ensure database persistence across container restarts or replacements. |
| **CI Automation** | Jenkins (`Jenkinsfile`) | 4-stage pipeline orchestrating Checkout, Image Build, Automated Testing, and Ansible Deployment. |
| **CD Automation** | Ansible (`cloud-monitoring-deploy.yml`) | Declarative, idempotent container deployment using `community.docker.docker_container`. |

---

## 3. High-Level Architecture & Separation of Concerns

### 3.1 Architectural Separation
> **CRITICAL ARCHITECTURAL PRINCIPLE**: Application monitoring operations are strictly decoupled from DevOps CI/CD operations.
> - A user viewing or polling the dashboard **does NOT trigger Jenkins**.
> - Jenkins executes **only** when code is updated or pushed to source control (Developer &rarr; Git).
> - Alert creation and resolution is an **application runtime responsibility**, not a Jenkins build job.

```
+-----------------------------------------------------------------------------------+
|                            APPLICATION RUNTIME FLOW                               |
|                                                                                   |
|  [Host / Container Engine]                                                        |
|             |                                                                     |
|             v (Telemetric Poll)                                                   |
|      [psutil Library]                                                             |
|             |                                                                     |
|             v (Raw Metric Readings)                                               |
|      [Flask Backend: app.py / monitoring.py]                                      |
|             |                                                                     |
|             +---> [Threshold Evaluation Engine]                                   |
|             |             |                                                       |
|             |             +---> Trigger New Alert (Exceeded Threshold)            |
|             |             +---> Deduplicate Alert (Continuously High Load)        |
|             |             +---> Auto-Resolve Alert (Metric Drops Below Threshold) |
|             v                                                                     |
|  [SQLite Database: /app/data/monitoring.db] <======== [Docker Volume Mount]       |
|             |                                                                     |
|             v                                                                     |
|  [Web UI Dashboard, Metrics History, Alerts Center, Settings Page]                |
+-----------------------------------------------------------------------------------+

+-----------------------------------------------------------------------------------+
|                              DEVOPS CI/CD WORKFLOW                                |
|                                                                                   |
|   Developer                                                                       |
|       | (git push)                                                                |
|       v                                                                           |
|   GitHub / Git Repository                                                         |
|       | (Webhook / SCM Poll)                                                      |
|       v                                                                           |
|   Jenkins CI/CD Pipeline                                                          |
|       |                                                                           |
|       +---> Stage 1: Checkout (Pull latest source tree)                           |
|       +---> Stage 2: Docker Build (Build image: cloud-monitoring-ci)              |
|       +---> Stage 3: Pytest (Run tests inside container image)                    |
|       +---> Stage 4: Deploy with Ansible (Invoke cloud-monitoring-deploy.yml)     |
|                   |                                                               |
|                   v                                                               |
|   Target Host (Docker Engine)                                                     |
|       |                                                                           |
|       +---> Container: cloud-monitoring-ansible (Port 5002 -> 5000)               |
|       +---> Persistent Volume: cloud_monitoring_data -> /app/data                 |
+-----------------------------------------------------------------------------------+
```

---

## 4. Application Workflows

### 4.1 Live Metric & Monitoring Flow
1. User loads `/dashboard` or client JS polls `/metrics`.
2. Flask backend invokes `monitoring.get_system_metrics()`.
3. `psutil` reads current CPU %, memory %, root/disk filesystem % and system boot time.
4. `monitoring.evaluate_and_record_metrics()` stores a new snapshot in the `metrics` table.
5. The readings are evaluated against dynamic thresholds stored in the `settings` table.
6. Alert state transitions are computed and persisted in the `alerts` table.
7. Structured telemetry and health status are rendered to the HTML view or returned via JSON.

### 4.2 Metrics History Flow
1. Metric snapshots are stored with an auto-incrementing ID and ISO timestamp.
2. Visiting `/history` queries the `metrics` table with configurable limits (20, 50, 100).
3. The page renders both a structured HTML table and an interactive HTML5 Canvas trend chart.
4. If no history exists, a clean fallback state is displayed.

### 4.3 Automated Alert Lifecycle Flow
```
        [Metric Measurement Received]
                     |
         Is Value > Configured Threshold?
                    / \
             YES   /   \   NO
                  /     \
    [Active Alert Exists?]    [Active Alert Exists?]
            /     \                   /     \
      YES  /       \  NO        YES  /       \  NO
          /         \               /         \
  [Deduplicate]  [Create Alert]  [Auto-Resolve] [No Action]
  (Update value, (status=Active, (status=Resolved,
  keep 1 active) severity=Warn/  resolved_at=NOW)
                 Critical)
```

---

## 5. Database Schema & Tables

The application automatically creates all necessary tables in `data/monitoring.db` upon startup. All queries use parameterized SQL to prevent SQL injection.

### Table: `metrics`
Stores periodic system utilization samples.
```sql
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpu_percent REAL NOT NULL,
    memory_percent REAL NOT NULL,
    disk_percent REAL NOT NULL,
    uptime_seconds INTEGER,
    collected_at TEXT NOT NULL
);
```

### Table: `alerts`
Stores alert records throughout their lifecycle.
```sql
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    threshold_value REAL NOT NULL,
    severity TEXT NOT NULL,         -- 'Warning' or 'Critical'
    status TEXT NOT NULL,           -- 'Active' or 'Resolved'
    created_at TEXT NOT NULL,
    resolved_at TEXT                -- Nullable until resolved
);
```

### Table: `settings`
Stores configurable anomaly thresholds.
```sql
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpu_threshold REAL NOT NULL,    -- Default: 80.0
    memory_threshold REAL NOT NULL, -- Default: 80.0
    disk_threshold REAL NOT NULL,   -- Default: 85.0
    updated_at TEXT NOT NULL
);
```

---

## 6. Project Structure

```
d:/DEVOPS/
├── app.py                      # Flask web application & REST routes
├── monitoring.py               # Telemetry collection, SQLite DAO, & alert evaluation
├── requirements.txt            # Python dependencies (Flask, psutil, pytest)
├── Dockerfile                  # Containerfile (python:3.11-slim, volume mount, healthcheck)
├── Jenkinsfile                 # Declarative 4-stage Jenkins CI/CD pipeline
├── cloud-monitoring-deploy.yml # Ansible playbook for container deployment
├── inventory.ini               # Ansible inventory configuration
├── test_app.py                 # Pytest automated test suite (11 test cases)
├── .gitignore                  # Ignores database files, caches, environments
├── README.md                   # Complete architectural & operational guide
├── templates/
│   ├── base.html               # Shared layout, navigation, status badge, notifications
│   ├── index.html              # Monitoring dashboard, metric cards, recent samples
│   ├── history.html            # Tabular snapshot log and HTML5 Canvas trend chart
│   ├── alerts.html             # Active & resolved alerts list, severity badges
│   └── settings.html           # Threshold configuration form & laboratory demo guide
├── static/
│   ├── style.css               # Modern operations dark theme design system
│   └── script.js               # Client AJAX polling, countdown timer, Canvas chart
└── data/
    └── .gitkeep                # Git tracking placeholder for persistent directory
```

---

## 7. How to Run Locally (Native Python)

### Prerequisites
- Python 3.11+ installed.
- Git.

### Setup Instructions
1. Clone the repository and navigate into the project directory:
   ```bash
   git clone <repository-url>
   cd DEVOPS
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows PowerShell
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application in your browser:
   - **Dashboard**: `http://localhost:5000/dashboard`
   - **Metrics History**: `http://localhost:5000/history`
   - **Alerts Center**: `http://localhost:5000/alerts`
   - **Settings**: `http://localhost:5000/settings`
   - **Health API**: `http://localhost:5000/health`

---

## 8. How to Run Automated Tests (Pytest)

The test suite tests the application in isolation using temporary test databases and mocked system metrics.

Run Pytest locally:
```bash
python -m pytest test_app.py -v
```

### What is tested:
1. `test_flask_app_initialization`: Verifies application factory and configuration.
2. `test_home_and_dashboard_routes`: Validates root redirection and dashboard HTTP 200.
3. `test_health_endpoint`: Ensures `/health` returns HTTP 200 with JSON status `healthy`.
4. `test_metrics_collection_endpoint`: Checks `/metrics` collection, persistence, and JSON output.
5. `test_metric_snapshot_storage`: Verifies SQLite insertion and retrieval in the `metrics` table.
6. `test_alert_lifecycle_trigger_dedup_and_resolve`:
   - Validates alert creation when threshold is exceeded.
   - Validates alert deduplication (continuous high values do not produce duplicate rows).
   - Validates auto-resolution when metrics drop below threshold.
7. `test_threshold_settings_validation`: Ensures thresholds accept valid ranges (1–100%) and reject negative, zero, >100%, and non-numeric inputs.
8. `test_settings_update_post_route`: Tests POST `/update_settings` form submission and flash feedback.
9. `test_history_and_alerts_pages_return_200`: Ensures all HTML views render HTTP 200.
10. `test_empty_history_graceful_handling`: Validates zero-state UX handling without exceptions.
11. `test_format_uptime_utility`: Verifies human-readable formatting of uptime seconds.

---

## 9. How to Build & Run with Docker and Persistent Volume

### 9.1 Build the Docker Image
```bash
docker build -t cloud-monitoring-ci .
```

### 9.2 Create the Docker Volume
Create a named Docker volume to store the SQLite database independently of the container lifecycle:
```bash
docker volume create cloud_monitoring_data
```

### 9.3 Run the Container with the Volume Mounted
```bash
docker run -d \
  --name cloud-monitoring-ansible \
  -p 5002:5000 \
  -v cloud_monitoring_data:/app/data \
  cloud-monitoring-ci
```

### 9.4 Verify Persistence Across Container Re-creation
To demonstrate that metric history and alerts persist when the container is deleted:
1. Access `http://localhost:5002/dashboard` and refresh a few times.
2. Stop and remove the running container:
   ```bash
   docker stop cloud-monitoring-ansible
   docker rm cloud-monitoring-ansible
   ```
3. Re-run a brand new container with the same volume mounted:
   ```bash
   docker run -d \
     --name cloud-monitoring-ansible \
     -p 5002:5000 \
     -v cloud_monitoring_data:/app/data \
     cloud-monitoring-ci
   ```
4. Refresh `http://localhost:5002/dashboard` &mdash; notice that **all historical snapshots, alert logs, and configured settings remain completely intact**!

---

## 10. How Jenkins CI/CD Works

The `Jenkinsfile` implements a 4-stage declarative pipeline:

```groovy
pipeline {
    agent any
    environment {
        IMAGE_NAME = "cloud-monitoring-ci"
        CONTAINER_NAME = "cloud-monitoring-ansible"
        HOST_PORT = "5002"
    }
    stages {
        stage('Stage 1 — Checkout') { ... }
        stage('Stage 2 — Build') { ... }
        stage('Stage 3 — Test') { ... }
        stage('Stage 4 — Deploy with Ansible') { ... }
    }
}
```

### Pipeline Stages Explained:
1. **Stage 1 &mdash; Checkout**: Clones the latest revision from the configured Git branch into the Jenkins agent workspace.
2. **Stage 2 &mdash; Build**: Executes `docker build -t cloud-monitoring-ci .` to compile the application container.
3. **Stage 3 &mdash; Test**: Runs the automated test suite inside the newly built Docker image:
   ```bash
   docker run --rm cloud-monitoring-ci python -m pytest test_app.py -v
   ```
   If any test fails, the pipeline halts immediately, preventing broken code from deploying.
4. **Stage 4 &mdash; Deploy with Ansible**: Executes the Ansible playbook to deploy the container:
   ```bash
   ansible-playbook -i inventory.ini cloud-monitoring-deploy.yml
   ```

---

## 11. How Ansible Deploys the Application

The playbook `cloud-monitoring-deploy.yml` utilizes Ansible's `community.docker.docker_container` module for declarative, idempotent container lifecycle management.

### Key Ansible Features:
- **Idempotency**: If the container is already running with the correct image, port, and volume configurations, Ansible makes no changes (`ok`). If configurations differ or a new image was built, it performs a seamless replacement (`changed`).
- **Data Protection**: Normal redeployment touches only the container layer; it **never** deletes or wipes the named volume `cloud_monitoring_data`.
- **Command to Execute**:
  ```bash
  ansible-playbook -i inventory.ini cloud-monitoring-deploy.yml
  ```

### Ansible Prerequisites:
To execute Ansible on the deployment controller or Jenkins runner:
```bash
ansible-galaxy collection install community.docker
pip install docker
```

---

## 12. College DevOps Demonstration (Viva / CAT Guide)

### How to Demonstrate an Automated Alert in 60 Seconds:
1. **Open the Settings View**:
   - Navigate to `http://localhost:5000/settings` (or `http://localhost:5002/settings` if running in Docker).
   - Observe the current CPU utilization on the dashboard (e.g., ~15-25%).
2. **Lower the Threshold**:
   - Change the **CPU Utilization Threshold** from `80.0%` to `5.0%`.
   - Click **Save & Apply Thresholds**.
3. **Trigger the Alert**:
   - Return to the **Dashboard** and click **Refresh Now**.
   - Notice that the CPU card immediately transitions to a red/warning **High Load** state.
   - An active alert banner appears on top of the dashboard.
4. **Demonstrate Alert Deduplication**:
   - Click **Refresh Now** 3 to 5 times.
   - Navigate to the **Alerts** tab (`/alerts`).
   - Point out to the evaluator that **only 1 Active Alert** exists for CPU. The system did **not** spam 5 separate alerts into the database; it gracefully updated the reading of the active alert.
5. **Demonstrate Auto-Resolution**:
   - Return to **Settings** and set the CPU threshold back to `80.0%`.
   - Click **Save & Apply Thresholds**.
   - Return to the **Dashboard** and click **Refresh Now**.
   - Go to the **Alerts** tab: the alert has automatically transitioned to <span style="color:#10b981;font-weight:bold;">Resolved</span> with an exact `resolved_at` timestamp!

---

## 13. System Monitoring Scope & Limitations

1. **What is Monitored**:
   - CPU utilization percentage of the operating environment.
   - Virtual memory (RAM) utilization percentage.
   - Disk space utilization percentage for the mounted root/primary filesystem.
   - System boot time and calculated uptime in seconds.
2. **Container Scope Limitations**:
   - Inside an unprivileged Docker container, `psutil` reads values constrained by the container's cgroups and namespace virtualization.
   - Metrics represent the container's visible execution environment rather than an entire multi-node cluster or hypervisor host.
3. **External Cloud Limitations**:
   - This application is self-contained and intentionally does not connect to third-party public cloud providers (AWS CloudWatch, Azure Monitor, GCP Cloud Monitoring) unless external cloud API credentials and SDKs are explicitly supplied.

---

## 14. Troubleshooting & FAQ

| Problem | Root Cause | Solution |
|---|---|---|
| `docker build` fails with connection error | Docker Desktop daemon is not running on host machine. | Start Docker Desktop application and wait for the engine to initialize. |
| `sqlite3.OperationalError: unable to open database file` | Directory `data/` does not exist or permissions are insufficient. | The application creates `data/` automatically; verify write permissions on the directory or Docker volume. |
| Port 5002 already in use | Previous container or process is bound to port 5002. | Stop existing container with `docker stop cloud-monitoring-ansible` or edit port in `inventory.ini` / `cloud-monitoring-deploy.yml`. |
| Ansible fails with `community.docker` not found | Missing Ansible Galaxy collection on controller. | Run `ansible-galaxy collection install community.docker` and `pip install docker`. |
| Alert does not auto-resolve | Metric reading still exceeds configured threshold. | Verify current metric reading on dashboard and ensure threshold in `/settings` is set higher than that value. |
