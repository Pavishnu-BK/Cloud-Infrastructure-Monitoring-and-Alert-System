# COIMBATORE INSTITUTE OF TECHNOLOGY
*(Government Aided Autonomous Institution Affiliated to Anna University)*  
**COIMBATORE - 641 014**

---

### **23IT723 – DEVOPS LABORATORY PROJECT REPORT**

# **CLOUD INFRASTRUCTURE MONITORING AND AUTOMATED ALERT SYSTEM**

**OCTOBER 2026**

**Submitted by:**  
**[STUDENT NAME]**  
**Register No: [REGISTER NUMBER]**  
**Department of Information Technology**

---

## **BONAFIDE CERTIFICATE**

Certified that this project report titled **“CLOUD INFRASTRUCTURE MONITORING AND AUTOMATED ALERT SYSTEM”** is the bonafide work of **[STUDENT NAME]** (Register No: **[REGISTER NUMBER]**) completed during the academic year 2025–2026 – Semester VII for the project presentation of **23IT723 – DEVOPS LABORATORY** under our supervision.

Certified that the candidate was examined during the laboratory project evaluation examination.

**Review Members:**  
1. Dr. M. Sangeetha  
2. Dr. E. Arul  

**Faculty Evaluator I** &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **Faculty Evaluator II**

---

## **23IT723 – DEVOPS LABORATORY EVALUATION SCHEME**

| S.No. | Evaluation Component | Key Verification Points | Marks |
|---|---|---|:---:|
| 1 | Problem Definition & Planning | Problem statement, objectives, requirements, module identification, technology selection. | 10 |
| 2 | Git Repository & Version Control | Repository creation, meaningful commits, README, .gitignore, remote operations, commit history. | 15 |
| 3 | Branching & Collaboration | Feature branches, parallel development, merging, clean commit organization. | 10 |
| 4 | Application Development & Build | Working Flask app, psutil telemetry, project structure, dependencies, successful execution. | 15 |
| 5 | Jenkins Continuous Integration | Jenkinsfile configuration, automated checkout, image build, test pipeline, execution logs. | 15 |
| 6 | Docker / Containerization | Dockerfile, image creation, container run, port mapping, health checks, environment handling. | 10 |
| 7 | Automation / Configuration (Ansible) | Ansible playbook (`cloud-monitoring-deploy.yml`), idempotency, container deployment. | 5 |
| 8 | Testing & Verification | Pytest suite (11 test cases), automated validation, error handling, mock testing evidence. | 5 |
| 9 | Documentation & Presentation | Architecture diagrams, commands, screenshots, results, troubleshooting, viva guide. | 5 |
| 10 | Final Demonstration & Viva-Voce | Live demonstration, alert lifecycle, volume persistence proof, technical understanding. | 10 |
| **TOTAL** | | | **100** |

---

## **TABLE OF CONTENTS**

1. [INTRODUCTION](#1-introduction)
2. [OBJECTIVES](#2-objectives)
3. [ABSTRACT](#3-abstract)
4. [TECHNOLOGY STACK](#4-technology-stack)
5. [SYSTEM ARCHITECTURE](#5-system-architecture)
6. [MODULE 1 — MONITORING USER INTERFACE & REAL-TIME DASHBOARD](#6-module-1--monitoring-user-interface--real-time-dashboard)
7. [MODULE 2 — FLASK BACKEND & METRIC COLLECTION ENGINE](#7-module-2--flask-backend--metric-collection-engine)
8. [MODULE 3 — SQLITE DATABASE PERSISTENCE](#8-module-3--sqlite-database-persistence)
9. [MODULE 4 — GIT & GITHUB SOURCE CONTROL](#9-module-4--git--github-source-control)
10. [MODULE 5 — DOCKER CONTAINERIZATION & HEALTH CHECKS](#10-module-5--docker-containerization--health-checks)
11. [MODULE 6 — JENKINS CI/CD PIPELINE](#11-module-6--jenkins-cicd-pipeline)
12. [MODULE 7 — AUTOMATED TESTING (PYTEST)](#12-module-7--automated-testing-pytest)
13. [MODULE 8 — ANSIBLE DEPLOYMENT AUTOMATION](#13-module-8--ansible-deployment-automation)
14. [MODULE 9 — PERSISTENT STORAGE (DOCKER VOLUME)](#14-module-9--persistent-storage-docker-volume)
15. [MODULE 10 — ANOMALY THRESHOLDS & AUTOMATED ALERT LIFECYCLE](#15-module-10--anomaly-thresholds--automated-alert-lifecycle)
16. [MODULE 11 — CI/CD INTEGRATION & PIPELINE ORCHESTRATION](#16-module-11--cicd-integration--pipeline-orchestration)
17. [MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION](#17-module-12--application--deployment-verification)
18. [RESULTS AND OUTPUT](#18-results-and-output)
19. [COMMANDS USED](#19-commands-used)
20. [ADVANTAGES](#20-advantages)
21. [LIMITATIONS](#21-limitations)
22. [FUTURE ENHANCEMENTS](#22-future-enhancements)
23. [CONCLUSION](#23-conclusion)

---

## 1. INTRODUCTION

The **Cloud Infrastructure Monitoring and Automated Alert System** is a lightweight, robust DevOps engineering project developed to address the critical need for continuous observability, resource tracking, and automated anomaly detection across modern compute infrastructure. In distributed computing environments, unhandled CPU spikes, memory leaks, and disk exhaustion can quickly lead to cascading service outages and degraded user experiences. Traditional monitoring often relies on heavyweight commercial agents or unmanaged scripts lacking alert deduplication and reproducible continuous deployment.

The application is engineered using HTML5, CSS3, JavaScript, Python, Flask, and SQLite. Flask powers the backend REST controller, while Python’s `psutil` library interfaces directly with the host/container operating system kernel to collect authentic telemetry (CPU utilization %, virtual memory %, mounted filesystem disk utilization %, and system uptime). SQLite serves as the persistent relational database, cleanly segregated under `data/monitoring.db`.

Furthermore, the project implements modern DevOps automation best practices across the entire software delivery lifecycle:
- **Git & GitHub** manage distributed version control and collaborative development.
- **Jenkins** orchestrates a 4-stage declarative CI/CD pipeline.
- **Docker** packages the application into an immutable container image.
- **Pytest** performs automated testing with isolated temporary databases.
- **Ansible** provisions and deploys the container idempotently.
- A **Docker Volume** (`cloud_monitoring_data`) guarantees persistent storage surviving container recreation.

---

## 2. OBJECTIVES

1. To develop a responsive web-based infrastructure monitoring dashboard providing real-time visibility into CPU, Memory, Disk, and System Uptime.
2. To interface with the operating system kernel using Python’s `psutil` library for authentic, non-fabricated telemetry collection.
3. To establish an SQLite database schema (`data/monitoring.db`) storing periodic metric snapshots, incident alert logs, and configurable thresholds using parameterized SQL queries.
4. To engineer an automated alert lifecycle management engine that dynamically evaluates metrics against thresholds, performs alert deduplication to prevent notification fatigue, and automatically resolves alerts when metrics normalize.
5. To implement version control and team collaboration workflows using Git and GitHub with strict `.gitignore` rules.
6. To package the Flask application into a lightweight, portable Docker container based on `python:3.11-slim` with embedded health check polling.
7. To configure persistent data storage using a named Docker Volume (`cloud_monitoring_data`) mounted to `/app/data` so that metrics, alerts, and settings survive container deletion.
8. To integrate an automated Pytest test suite (11 test cases) executing deterministically with isolated temporary databases and mocked kernel telemetry.
9. To construct a declarative 4-stage Jenkins CI/CD pipeline (Checkout → Docker Build → Containerized Pytest → Ansible Deployment).
10. To automate idempotent container configuration and deployment using an Ansible playbook (`cloud-monitoring-deploy.yml`).

---

## 3. ABSTRACT

The Cloud Infrastructure Monitoring and Automated Alert System is a self-contained, enterprise-inspired operations center developed to monitor compute resources in real time and automate deployment through a complete DevOps CI/CD pipeline. Modern infrastructure operations require continuous observability without the overhead of complex, bloated external frameworks. The proposed solution features a responsive HTML5/CSS3/JavaScript operations dashboard connected to a Python Flask backend. The backend leverages the `psutil` library to record authentic CPU, memory, and filesystem telemetry directly into an SQLite database. 

A central innovation of the application is its automated alert engine: when metrics breach configured thresholds, an alert is logged; subsequent high-load readings are gracefully deduplicated to avoid database spamming; and once values drop back within nominal bounds, the active alert is automatically transitioned to 'Resolved' with exact timestamps.

From a DevOps perspective, the application follows a robust automated pipeline: code committed to GitHub triggers a Jenkins declarative pipeline which builds the Docker container (`cloud-monitoring-ci`), runs automated Pytest validation inside the container image, and invokes an Ansible playbook to idempotently deploy the container (`cloud-monitoring-ansible`) with port mapping `5002:5000`. Persistent storage is guaranteed using a dedicated Docker Volume (`cloud_monitoring_data` mounted to `/app/data`), ensuring that historical data and alert records remain completely preserved even across container restarts or image upgrades. The project successfully demonstrates the synergy between operational software engineering and automated DevOps infrastructure management.

---

## 4. TECHNOLOGY STACK

| Technology | Version / Tool | Purpose in Project |
|---|---|---|
| **HTML5** | W3C Standard | Responsive user interface structure, tables, and modal cards. |
| **CSS3** | Vanilla CSS Design System | Modern dark DevOps operations theme, status indicators, and badges. |
| **JavaScript** | Vanilla ES6+ | 5-second AJAX polling, countdown indicator, and HTML5 Canvas trend charting. |
| **Python** | 3.11 / 3.14 | Core backend application programming and telemetry orchestration. |
| **Flask** | 3.1.2 | Lightweight WSGI web framework and REST API routing. |
| **psutil** | 7.2.2 | Cross-platform system telemetry library (CPU, RAM, Disk, Uptime). |
| **SQLite** | 3.x (Embedded) | Thread-safe relational database storage for metrics, alerts, and settings. |
| **Git** | 2.x | Distributed version control, atomic commits, and repository management. |
| **GitHub** | Cloud Repository | Centralized remote Git repository hosting and CI/CD source. |
| **Jenkins** | 2.x Declarative Pipeline | CI/CD server automating Checkout, Image Build, Testing, and Deployment. |
| **Docker** | 28.4.0 Engine | Application containerization with health checks and isolated runtime. |
| **Docker Volume** | `cloud_monitoring_data` | Named persistent volume mounted to `/app/data` for database preservation. |
| **Pytest** | 9.1.1 | Automated unit and integration test suite executing 11 isolated test cases. |
| **Ansible** | 2.x Playbook | Automated idempotent container configuration and lifecycle deployment. |

---

## 5. SYSTEM ARCHITECTURE

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
|   GitHub Repository                                                               |
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

## 6. MODULE 1 — MONITORING USER INTERFACE & REAL-TIME DASHBOARD

This module provides the operations dashboard for infrastructure observability:
- **Metric Cards**: Real-time percentage meters and progress bars for CPU, Memory, and Disk.
- **System Overview Bar**: Displays Global Health status (Healthy, Warning, Critical), Monitored Node name, OS, Filesystem Mount, and Uptime.
- **Active Alert Banner**: Prominently highlights unhandled infrastructure anomalies requiring administrator attention.
- **Recent Snapshot Log**: Displays the last 10 metric readings stored in SQLite with nominal/exceeded badges.
- **Dual Refresh Controls**: 5-second auto-refresh countdown toggle and a manual "Refresh Now" trigger button.
- **Native Canvas Trend Visualization**: Renders dynamic multi-line charts (CPU cyan, Memory purple, Disk green) using HTML5 Canvas.

---

## 7. MODULE 2 — FLASK BACKEND & METRIC COLLECTION ENGINE

Module 2 encompasses the backend controller (`app.py`) and core telemetry engine (`monitoring.py`):
- `GET /` & `/dashboard`: Serves the primary monitoring dashboard populated with live telemetry and active alert summaries.
- `GET /metrics`: RESTful endpoint returning structured JSON containing metric readings, alert actions, and health states for polling clients.
- `GET /history` & `/api/history`: Fetches historical metric records with query limit options (20, 50, 100) for tabular and Canvas rendering.
- `GET /alerts`: Displays active and resolved incident logs with severity categorization and filtering.
- `GET /settings` & `POST /update_settings`: Validates and persists administrator-configured anomaly limits.
- `GET /health`: Container health check endpoint verifying database connectivity and operational status.
- `psutil` Engine: Interfaces with `psutil.cpu_percent()`, `psutil.virtual_memory()`, and `psutil.disk_usage()`.

---

## 8. MODULE 3 — SQLITE DATABASE PERSISTENCE

Module 3 manages data storage using SQLite embedded at `data/monitoring.db`:
- **Table `metrics`**: Columns: `id` (PK), `cpu_percent` (REAL), `memory_percent` (REAL), `disk_percent` (REAL), `uptime_seconds` (INT), `collected_at` (TEXT).
- **Table `alerts`**: Columns: `id` (PK), `metric_name` (TEXT), `metric_value` (REAL), `threshold_value` (REAL), `severity` (TEXT), `status` (TEXT), `created_at` (TEXT), `resolved_at` (TEXT).
- **Table `settings`**: Columns: `id` (PK), `cpu_threshold` (REAL), `memory_threshold` (REAL), `disk_threshold` (REAL), `updated_at` (TEXT). Default: 80%, 80%, 85%.
- **Auto-Initialization**: Tables and initial threshold rows are automatically created upon startup via `monitoring.init_db()`.

---

## 9. MODULE 4 — GIT & GITHUB SOURCE CONTROL

Version control and code collaboration are managed through Git locally and GitHub remotely:
- **Repository Hygiene**: Strict `.gitignore` excluding `data/monitoring.db`, `*.pyc`, `__pycache__`, `.venv`, and `.pytest_cache`.
- **Commit History**: Meaningful atomic commits tracking application logic, Docker configuration, Jenkinsfile, and test suites.
- **Branching & Merging**: Supports feature-branch workflows integrated with Jenkins SCM checkout.

---

## 10. MODULE 5 — DOCKER CONTAINERIZATION & HEALTH CHECKS

Module 5 packages the application into an immutable container based on `python:3.11-slim` defined in `Dockerfile`:
- **Lightweight Base**: Built on Debian-slim with Python 3.11 runtime, optimizing image footprint.
- **Directory Structure**: Application code copied to `/app` with persistent data directory `/app/data`.
- **Port Configuration**: Exposes port `5000` internally; mapped to host port `5002` in production deployment.
- **Built-in Healthcheck**: Periodically queries `/health` using Python urllib to verify container liveliness.

---

## 11. MODULE 6 — JENKINS CI/CD PIPELINE

Jenkins automates the Continuous Integration and Continuous Deployment pipeline using a declarative `Jenkinsfile` comprising 4 sequential stages:
- **Stage 1 — Checkout**: Clones source code from Git repository into Jenkins workspace.
- **Stage 2 — Build**: Executes `docker build -t cloud-monitoring-ci .` to create the application image.
- **Stage 3 — Test**: Runs `docker run --rm cloud-monitoring-ci python -m pytest test_app.py -v`. If any test fails, the pipeline terminates.
- **Stage 4 — Deploy with Ansible**: Executes `ansible-playbook -i inventory.ini cloud-monitoring-deploy.yml` for deployment.

---

## 12. MODULE 7 — AUTOMATED TESTING (PYTEST)

Module 7 implements automated testing via `test_app.py`, ensuring comprehensive test coverage across 11 test cases:
1. `test_flask_app_initialization`: Verifies application factory initialization.
2. `test_home_and_dashboard_routes`: Validates root 302 redirection and dashboard 200 response.
3. `test_health_endpoint`: Tests container health check returning HTTP 200 and healthy JSON status.
4. `test_metrics_collection_endpoint`: Validates `/metrics` telemetry collection and JSON serialization.
5. `test_metric_snapshot_storage`: Verifies accurate insertion and retrieval in SQLite metrics table.
6. `test_alert_lifecycle_trigger_dedup_and_resolve`: Tests alert creation on threshold breach, deduplication on continued load, and auto-resolution when metrics normalize.
7. `test_threshold_settings_validation`: Enforces 1.0% to 100.0% numeric validation and rejects invalid inputs.
8. `test_settings_update_post_route`: Tests `POST /update_settings` form processing and flash feedback.
9. `test_history_and_alerts_pages_return_200`: Confirms rendering of all ancillary views.
10. `test_empty_history_graceful_handling`: Validates zero-state handling when database contains no prior records.
11. `test_format_uptime_utility`: Validates human-readable conversion of uptime seconds.

---

## 13. MODULE 8 — ANSIBLE DEPLOYMENT AUTOMATION

Ansible provides automated, idempotent container configuration through `cloud-monitoring-deploy.yml`:
- **Idempotency**: Uses `community.docker.docker_container` module; verifies running container state and updates only when configuration differs.
- **Container Configuration**: Container name `cloud-monitoring-ansible`, image `cloud-monitoring-ci`, port `5002:5000`, restart policy `unless-stopped`.
- **Volume Attachment**: Mounts `cloud_monitoring_data:/app/data` ensuring zero data loss during automated redeployments.

---

## 14. MODULE 9 — PERSISTENT STORAGE (DOCKER VOLUME)

To guarantee that operational history, alerts, and settings survive container deletion, persistent storage is implemented using a Docker Volume:
- **Volume Name**: `cloud_monitoring_data`.
- **Mount Point**: `/app/data` inside the container.
- **Database Path**: `/app/data/monitoring.db`.
- **Persistence Verification**: Container can be stopped and removed (`docker rm -f`); launching a new container with the same volume restores all historical data.

---

## 15. MODULE 10 — ANOMALY THRESHOLDS & AUTOMATED ALERT LIFECYCLE

This module governs the alert lifecycle to prevent alert fatigue and provide deterministic incident management:
- **Threshold Configuration**: Administrators can adjust CPU, RAM, and Disk limits between 1.0% and 100.0% through `/settings`.
- **Alert Creation**: An active alert is created when a reading exceeds its configured threshold, classified as Warning or Critical.
- **Deduplication**: If a metric continues to exceed the threshold across polling cycles, the existing active alert is updated rather than creating duplicate rows.
- **Auto-Resolution**: Once metric values drop back below the threshold, the alert status automatically transitions to 'Resolved' with an exact `resolved_at` timestamp.

---

## 16. MODULE 11 — CI/CD INTEGRATION & PIPELINE ORCHESTRATION

Module 11 harmonizes the individual DevOps tools into an integrated pipeline:
$$\text{Git} \longrightarrow \text{GitHub} \longrightarrow \text{Jenkins} \longrightarrow \text{Docker} \longrightarrow \text{Pytest} \longrightarrow \text{Ansible} \longrightarrow \text{Docker Volume} \longrightarrow \text{Flask} \longrightarrow \text{SQLite}$$
- **Automated Gatekeeping**: Jenkins prevents deployment if any Pytest test case fails.
- **Repeatability**: Entire infrastructure deployment can be reproduced identically on any Docker host.

---

## 17. MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION

Verification confirms the health and reliability of all project subsystems:
- **Application Verification**: Verified live dashboard, `/metrics` API, canvas trend chart, and threshold update form.
- **Docker Verification**: Verified image creation, container health checks, and volume inspection.
- **Pytest Verification**: 11 of 11 tests passed in 0.43s.
- **Ansible Verification**: Playbook executed with 0 failures.

---

## 18. RESULTS AND OUTPUT

The completed system successfully delivers:
1. Real-time host and container observability with live CPU, Memory, Disk, and Uptime meters.
2. Automated 5-second AJAX polling with countdown timer and manual on-demand refresh.
3. Incident alert management with automated trigger, deduplication, and auto-resolution.
4. Configurable threshold management with validated range enforcement (1.0% to 100.0%).
5. Historical metrics logging with interactive plain HTML5 Canvas trend visualization.
6. Isolated containerized deployment on Docker with persistent SQLite storage via Docker Volume.
7. Automated test validation with 11 passing Pytest cases.
8. Automated CI/CD pipeline orchestrated via Jenkins and deployed via Ansible.

---

## 19. COMMANDS USED

### A. Local Application & Testing Commands
```bash
# Run Pytest test suite
python -m pytest test_app.py -v

# Start Flask application locally
python app.py

# Access Dashboard
http://localhost:5000/dashboard
```

### B. Docker Commands
```bash
# Create Persistent Volume
docker volume create cloud_monitoring_data

# Build Docker Image
docker build -t cloud-monitoring-ci .

# Run Container with Persistent Volume Mounted
docker run -d --name cloud-monitoring-ansible -p 5002:5000 -v cloud_monitoring_data:/app/data cloud-monitoring-ci

# Check Container Status & Health
docker ps

# Inspect Container Logs
docker logs cloud-monitoring-ansible

# Inspect Volume Configuration
docker volume inspect cloud_monitoring_data
```

### C. Ansible Deployment Commands
```bash
# Execute Deployment Playbook
ansible-playbook -i inventory.ini cloud-monitoring-deploy.yml
```

### D. SQLite Database Verification Commands
```bash
# Query Metrics Table inside Container
docker exec cloud-monitoring-ansible python -c "import sqlite3; c=sqlite3.connect('data/monitoring.db'); [print(row) for row in c.execute('SELECT * FROM metrics LIMIT 5')]; c.close()"

# Query Alerts Table inside Container
docker exec cloud-monitoring-ansible python -c "import sqlite3; c=sqlite3.connect('data/monitoring.db'); [print(row) for row in c.execute('SELECT * FROM alerts')]; c.close()"
```

### E. Git Commands
```bash
# Check Status
git status

# View Commit History
git log --oneline --graph

# Stage and Commit
git add .
git commit -m "Finalize Cloud Infrastructure Monitoring and Automated Alert System"
```

---

## 20. ADVANTAGES

1. **Zero Cost & Lightweight**: Uses open-source technologies (Python, Flask, SQLite, psutil) without expensive third-party SaaS fees.
2. **Eliminates Alert Fatigue**: Built-in alert deduplication prevents repeated notification flooding during sustained load.
3. **Automated Auto-Resolution**: Eliminates stale alerts by automatically resolving incidents when metrics return below thresholds.
4. **Data Durability**: Docker Volume guarantees zero data loss across container teardown, rebuild, or recreation.
5. **Automated Quality Assurance**: Integrated Pytest suite halts broken builds in Jenkins prior to production deployment.
6. **Repeatable Infrastructure**: Ansible playbook ensures consistent, idempotent deployments across developer and production hosts.

---

## 21. LIMITATIONS

1. **Host/Container Scope**: In an unprivileged Docker container, `psutil` observes the container's visible cgroups and virtualized boundaries rather than an entire multi-node cluster.
2. **Embedded SQLite Database**: SQLite is designed for lightweight single-server deployments; high-concurrency enterprise clusters require PostgreSQL or MySQL.
3. **Local Demonstration Focus**: Default alert delivery is in-app; real-time SMS/Email dispatch requires configured external SMTP or Twilio API keys.

---

## 22. FUTURE ENHANCEMENTS

1. **Multi-Node Agent Network**: Implementing distributed lightweight telemetry agents reporting to a centralized aggregator.
2. **External Cloud Integrations**: Ingesting AWS CloudWatch, Azure Monitor, and Google Cloud telemetry via official SDKs.
3. **External Incident Webhooks**: Dispatching automated alert webhooks to Slack, Discord, PagerDuty, or Microsoft Teams.
4. **Time-Series Database Migration**: Integrating Prometheus and Grafana for long-term time-series indexing and custom dashboards.

---

## 23. CONCLUSION

The **Cloud Infrastructure Monitoring and Automated Alert System** successfully demonstrates the end-to-end integration of a full-stack observability web application with an automated DevOps CI/CD delivery pipeline. Developed for the 23IT723 DevOps Laboratory at Coimbatore Institute of Technology, the system delivers real-time monitoring of CPU, RAM, Disk storage, and uptime using Python’s `psutil` library, supported by a responsive operations dashboard and an embedded SQLite database. The automated alert engine eliminates alert fatigue through intelligent deduplication and provides hands-off lifecycle management with automatic resolution.

On the DevOps side, the project implements a complete, repeatable automation pipeline: Git and GitHub manage version control; Jenkins orchestrates a 4-stage declarative pipeline; Docker containerizes the application into an immutable image with container health checks; Pytest guarantees software quality with 11 unit/integration test cases; Ansible automates idempotent deployment; and a named Docker Volume provides data durability. The complete workflow verifies the seamless integration of:
$$\text{Git} \longrightarrow \text{GitHub} \longrightarrow \text{Jenkins} \longrightarrow \text{Docker} \longrightarrow \text{Pytest} \longrightarrow \text{Ansible} \longrightarrow \text{Flask} \longrightarrow \text{SQLite} \longrightarrow \text{Docker Volume}$$
fulfilling all requirements for a professional, college-level DevOps engineering project.
