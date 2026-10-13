"""
Script to generate the official college project report in .docx format:
23IT723_Cloud_Infrastructure_Monitoring_Report.docx
Following Coimbatore Institute of Technology 23IT723 DevOps Laboratory format.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = Document()

    # Set 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base font
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # ==========================================
    # 1. TITLE PAGE
    # ==========================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("COIMBATORE INSTITUTE OF TECHNOLOGY\n")
    r_inst.bold = True
    r_inst.font.size = Pt(16)
    r_sub = p_inst.add_run("(Government Aided Autonomous Institution Affiliated to Anna University)\nCOIMBATORE - 641 014\n\n")
    r_sub.font.size = Pt(12)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c = p_course.add_run("23IT723 - DEVOPS LABORATORY\nPROJECT REPORT\n\n\n")
    r_c.bold = True
    r_c.font.size = Pt(14)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("CLOUD INFRASTRUCTURE MONITORING AND AUTOMATED ALERT SYSTEM\n\n\n")
    r_t.bold = True
    r_t.font.size = Pt(18)
    r_t.font.color.rgb = RGBColor(16, 44, 87)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_date.add_run("OCTOBER 2026\n\n\n")
    r_d.bold = True
    r_d.font.size = Pt(12)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.add_run("Submitted by\n\n").font.size = Pt(12)
    r_stud = p_sub.add_run("[STUDENT NAME]\n[REGISTER NUMBER]\n\nDEPARTMENT OF INFORMATION TECHNOLOGY")
    r_stud.bold = True
    r_stud.font.size = Pt(13)

    doc.add_page_break()

    # ==========================================
    # 2. BONAFIDE CERTIFICATE
    # ==========================================
    p_cert_inst = doc.add_paragraph()
    p_cert_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ci = p_cert_inst.add_run("COIMBATORE INSTITUTE OF TECHNOLOGY\n")
    r_ci.bold = True
    r_ci.font.size = Pt(14)
    p_cert_inst.add_run("(Government Aided Autonomous Institution Affiliated to Anna University)\nCOIMBATORE - 641 014\n\n").font.size = Pt(11)

    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ct = p_cert_title.add_run("BONAFIDE CERTIFICATE\n\n")
    r_ct.bold = True
    r_ct.font.size = Pt(15)

    p_cert_body = doc.add_paragraph()
    p_cert_body.paragraph_format.line_spacing = 1.5
    p_cert_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert_body.add_run(
        "Certified that this project report titled “CLOUD INFRASTRUCTURE MONITORING AND AUTOMATED ALERT SYSTEM” "
        "is the bonafide work of [STUDENT NAME] (Register No: [REGISTER NUMBER]) completed during the academic "
        "year 2025-2026 - Semester VII for the project presentation of 23IT723 - DEVOPS LABORATORY under our supervision.\n\n"
        "Certified that the candidate was examined during the laboratory project evaluation examination.\n\n\n\n"
    )

    p_rev = doc.add_paragraph()
    p_rev.add_run("Review Members:\n\n").bold = True
    p_rev.add_run("1. Dr. M. Sangeetha\n2. Dr. E. Arul\n\n\n\n")
    p_rev.add_run("Faculty Evaluator I                                                    Faculty Evaluator II")

    doc.add_page_break()

    # ==========================================
    # 3. EVALUATION SCHEME
    # ==========================================
    h_eval = doc.add_paragraph()
    h_eval.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_he = h_eval.add_run("23IT723 – DEVOPS LABORATORY\nFINAL MINI PROJECT – EVALUATION SCHEME\n")
    r_he.bold = True
    r_he.font.size = Pt(13)

    p_eval_desc = doc.add_paragraph()
    p_eval_desc.paragraph_format.line_spacing = 1.15
    p_eval_desc.add_run(
        "The final mini project requires students to integrate major DevOps practices covered in the laboratory. "
        "The project demonstrates practical implementation of version control, automated testing, Continuous Integration, "
        "containerization, persistent storage, and automated deployment with proper execution evidence."
    )

    table_rubric = doc.add_table(rows=11, cols=4)
    table_rubric.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_rubric.autofit = False

    rubric_headers = ["S.No.", "Evaluation Component", "Key Verification Points", "Marks"]
    for i, h in enumerate(rubric_headers):
        cell = table_rubric.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "E2E8F0")

    rubric_data = [
        ("1", "Problem Definition & Planning", "Problem statement, objectives, requirements, module identification, technology selection.", "10"),
        ("2", "Git Repository & Version Control", "Repository creation, meaningful commits, README, .gitignore, remote operations, commit history.", "15"),
        ("3", "Branching & Collaboration", "Feature branches, parallel development, merging, clean commit organization.", "10"),
        ("4", "Application Development & Build", "Working Flask app, psutil telemetry, project structure, dependencies, successful execution.", "15"),
        ("5", "Jenkins Continuous Integration", "Jenkinsfile configuration, automated checkout, image build, test pipeline, execution logs.", "15"),
        ("6", "Docker / Containerization", "Dockerfile, image creation, container run, port mapping, health checks, environment handling.", "10"),
        ("7", "Automation / Configuration (Ansible)", "Ansible playbook (cloud-monitoring-deploy.yml), idempotency, container deployment.", "5"),
        ("8", "Testing & Verification", "Pytest suite (11 test cases), automated validation, error handling, mock testing evidence.", "5"),
        ("9", "Documentation & Presentation", "Architecture diagrams, commands, screenshots, results, troubleshooting, viva guide.", "5"),
        ("10", "Final Demonstration & Viva-Voce", "Live demonstration, alert lifecycle, volume persistence proof, technical understanding.", "10"),
    ]

    for row_idx, data in enumerate(rubric_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table_rubric.rows[row_idx].cells[col_idx]
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)

    p_tot = doc.add_paragraph()
    p_tot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_tot.add_run("TOTAL: 100 MARKS\n").bold = True

    doc.add_page_break()

    # ==========================================
    # 4. TABLE OF CONTENTS
    # ==========================================
    h_toc = doc.add_paragraph()
    h_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_htoc = h_toc.add_run("TABLE OF CONTENTS\n")
    r_htoc.bold = True
    r_htoc.font.size = Pt(14)

    toc_items = [
        ("1", "INTRODUCTION", "05"),
        ("2", "OBJECTIVES", "05"),
        ("3", "ABSTRACT", "06"),
        ("4", "TECHNOLOGY STACK", "06"),
        ("5", "SYSTEM ARCHITECTURE", "07"),
        ("6", "MODULE 1 — MONITORING USER INTERFACE & REAL-TIME DASHBOARD", "08"),
        ("7", "MODULE 2 — FLASK BACKEND & METRIC COLLECTION ENGINE", "09"),
        ("8", "MODULE 3 — SQLITE DATABASE PERSISTENCE", "10"),
        ("9", "MODULE 4 — GIT & GITHUB SOURCE CONTROL", "11"),
        ("10", "MODULE 5 — DOCKER CONTAINERIZATION & HEALTH CHECKS", "12"),
        ("11", "MODULE 6 — JENKINS CI/CD PIPELINE", "14"),
        ("12", "MODULE 7 — AUTOMATED TESTING (PYTEST)", "15"),
        ("13", "MODULE 8 — ANSIBLE DEPLOYMENT AUTOMATION", "17"),
        ("14", "MODULE 9 — PERSISTENT STORAGE (DOCKER VOLUME)", "18"),
        ("15", "MODULE 10 — ANOMALY THRESHOLDS & AUTOMATED ALERT LIFECYCLE", "19"),
        ("16", "MODULE 11 — CI/CD INTEGRATION & PIPELINE ORCHESTRATION", "20"),
        ("17", "MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION", "21"),
        ("18", "RESULTS AND OUTPUT", "22"),
        ("19", "COMMANDS USED", "23"),
        ("20", "ADVANTAGES", "27"),
        ("21", "LIMITATIONS", "27"),
        ("22", "FUTURE ENHANCEMENTS", "28"),
        ("23", "CONCLUSION", "28"),
    ]

    toc_table = doc.add_table(rows=len(toc_items) + 1, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_table.rows[0].cells[0].text = "S.NO."
    toc_table.rows[0].cells[1].text = "CONTENT"
    toc_table.rows[0].cells[2].text = "PAGE NO."
    for c in toc_table.rows[0].cells:
        c.paragraphs[0].runs[0].bold = True
        set_cell_background(c, "E2E8F0")

    for idx, item in enumerate(toc_items, start=1):
        for col_idx, val in enumerate(item):
            c = toc_table.rows[idx].cells[col_idx]
            c.text = val
            c.paragraphs[0].runs[0].font.size = Pt(10)
            set_cell_margins(c, top=40, bottom=40, left=60, right=60)

    doc.add_page_break()

    # ==========================================
    # HELPER FOR REPORT SECTIONS
    # ==========================================
    def add_section_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(16, 44, 87)
        return p

    def add_body_paragraph(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(6)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run(text)
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        p.add_run(text)
        return p

    # ==========================================
    # 1. INTRODUCTION
    # ==========================================
    add_section_header("1. INTRODUCTION")
    add_body_paragraph(
        "The Cloud Infrastructure Monitoring and Automated Alert System is a lightweight, robust DevOps engineering "
        "project developed to address the critical need for continuous visibility, resource tracking, and automated anomaly "
        "detection across modern computing infrastructure. In cloud environments and distributed clusters, unhandled CPU exhaustion, "
        "memory leaks, or storage bottlenecks can lead to severe service downtime and degraded user experience. Traditional system "
        "monitoring often relies on monolithic commercial agents or unmanaged scripts that lack clean alert lifecycle management "
        "and reproducible continuous deployment."
    )
    add_body_paragraph(
        "The application is engineered using HTML5, CSS3, JavaScript, Python, Flask, and SQLite. Flask powers the backend REST "
        "controller, while Python’s psutil library interfaces directly with the host/container kernel to collect authentic telemetry "
        "(CPU utilization percentage, virtual memory percentage, mounted filesystem disk utilization percentage, and system uptime). "
        "SQLite is utilized as the persistent relational database, cleanly segregated into data/monitoring.db."
    )
    add_body_paragraph(
        "Furthermore, the project embodies modern DevOps automation best practices across the entire software delivery lifecycle. "
        "Git and GitHub provide distributed version control and branch collaboration; Jenkins drives an automated Continuous "
        "Integration and Continuous Deployment (CI/CD) pipeline; Docker packages the application into an immutable container image; "
        "Pytest performs rigorous automated testing with isolated mock databases; Ansible provisions and deploys the container idempotently; "
        "and a Docker Volume ensures persistent database storage surviving container recreation. The project delivers a completely functional "
        "monitoring system while demonstrating end-to-end DevOps automation."
    )

    # ==========================================
    # 2. OBJECTIVES
    # ==========================================
    add_section_header("2. OBJECTIVES")
    add_bullet("To develop a responsive web-based infrastructure monitoring dashboard providing real-time visibility into CPU, Memory, Disk, and System Uptime.")
    add_bullet("To interface with the host/container operating system kernel using Python’s psutil library for authentic, non-fabricated telemetry collection.")
    add_bullet("To establish an SQLite database schema (data/monitoring.db) to store periodic metric snapshots, incident alert logs, and configurable thresholds using parameterized queries.")
    add_bullet("To engineer an automated alert lifecycle management engine that dynamically evaluates metrics against thresholds, performs alert deduplication to prevent notification fatigue, and automatically resolves alerts when metrics normalize.")
    add_bullet("To implement version control and team collaboration workflows using Git and GitHub with a strict .gitignore policy.")
    add_bullet("To package the Flask application into a lightweight, portable Docker container based on python:3.11-slim with embedded health check polling.")
    add_bullet("To configure persistent data storage using a named Docker Volume (cloud_monitoring_data) mounted to /app/data so that metrics, alerts, and settings survive container deletion.")
    add_bullet("To integrate an automated Pytest test suite (11 test cases) executing deterministically with isolated temporary databases and mocked kernel telemetry.")
    add_bullet("To construct a declarative 4-stage Jenkins CI/CD pipeline (Checkout → Docker Build → Containerized Pytest → Ansible Deployment).")
    add_bullet("To automate idempotent container configuration and deployment using an Ansible playbook (cloud-monitoring-deploy.yml).")

    # ==========================================
    # 3. ABSTRACT
    # ==========================================
    add_section_header("3. ABSTRACT")
    add_body_paragraph(
        "The Cloud Infrastructure Monitoring and Automated Alert System is a self-contained, enterprise-inspired operations center "
        "developed to monitor compute resources in real time and automate deployment through a complete DevOps CI/CD pipeline. "
        "Modern infrastructure operations require continuous observability without the overhead of complex, bloated external frameworks. "
        "The proposed solution features a responsive HTML5/CSS3/JavaScript operations dashboard connected to a Python Flask backend. "
        "The backend leverages the psutil library to record authentic CPU, memory, and filesystem telemetry directly into an SQLite database. "
        "A central innovation of the application is its automated alert engine: when metrics breach configured thresholds, an alert is logged; "
        "subsequent high-load readings are gracefully deduplicated to avoid database spamming; and once values drop back within nominal bounds, "
        "the active alert is automatically transitioned to 'Resolved' with exact timestamps."
    )
    add_body_paragraph(
        "From a DevOps perspective, the application follows a robust automated pipeline: code committed to GitHub triggers a Jenkins declarative "
        "pipeline which builds the Docker container (cloud-monitoring-ci), runs automated Pytest validation inside the container image, and invokes "
        "an Ansible playbook to idempotently deploy the container (cloud-monitoring-ansible) with port mapping 5002:5000. Persistent storage is "
        "guaranteed using a dedicated Docker Volume (cloud_monitoring_data mounted to /app/data), ensuring that historical data and alert records "
        "remain completely preserved even across container restarts or image upgrades. The project successfully demonstrates the synergy between "
        "operational software engineering and automated DevOps infrastructure management."
    )

    # ==========================================
    # 4. TECHNOLOGY STACK
    # ==========================================
    add_section_header("4. TECHNOLOGY STACK")
    tech_table = doc.add_table(rows=14, cols=3)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tech_table.rows[0].cells[0].text = "Technology"
    tech_table.rows[0].cells[1].text = "Version / Tool"
    tech_table.rows[0].cells[2].text = "Purpose in Project"
    for c in tech_table.rows[0].cells:
        c.paragraphs[0].runs[0].bold = True
        set_cell_background(c, "E2E8F0")

    tech_data = [
        ("HTML5", "W3C Semantic Standard", "Responsive user interface structure, tables, and modal cards."),
        ("CSS3", "Pure Vanilla CSS Design System", "Modern dark DevOps operations theme, status indicators, and badges."),
        ("JavaScript", "Vanilla ES6+", "5-second AJAX polling, countdown indicator, and HTML5 Canvas trend charting."),
        ("Python", "3.11 / 3.14", "Core backend application programming and telemetry orchestration."),
        ("Flask", "3.1.2", "Lightweight WSGI web framework and REST API routing."),
        ("psutil", "7.2.2", "Cross-platform process and system monitoring library (CPU, RAM, Disk, Uptime)."),
        ("SQLite", "3.x (Embedded)", "Thread-safe relational database storage for metrics, alerts, and settings."),
        ("Git", "2.x", "Distributed version control, atomic commits, and repository management."),
        ("GitHub", "Cloud Repository", "Centralized remote Git repository hosting and CI/CD webhook source."),
        ("Jenkins", "2.x Declarative Pipeline", "CI/CD server automating Checkout, Image Build, Testing, and Deployment."),
        ("Docker", "28.4.0 Engine", "Application containerization with health checks and isolated runtime."),
        ("Docker Volume", "cloud_monitoring_data", "Named persistent volume mounted to /app/data for database preservation."),
        ("Pytest", "9.1.1", "Automated unit and integration test suite executing 11 isolated test cases."),
    ]

    for r_idx, (t, v, p) in enumerate(tech_data, start=1):
        row = tech_table.rows[r_idx]
        row.cells[0].text = t
        row.cells[1].text = v
        row.cells[2].text = p
        for c in row.cells:
            c.paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_margins(c, top=40, bottom=40, left=60, right=60)

    # ==========================================
    # 5. SYSTEM ARCHITECTURE
    # ==========================================
    add_section_header("5. SYSTEM ARCHITECTURE")
    add_body_paragraph(
        "A foundational principle of this project is the strict architectural separation of concerns between Application Runtime "
        "Monitoring and the DevOps CI/CD Lifecycle. A user browsing or polling the dashboard interacts solely with the Flask WSGI "
        "server and SQLite database; viewing metrics does NOT trigger Jenkins builds. Jenkins is activated exclusively during the code "
        "delivery phase."
    )
    add_body_paragraph("A. Application Runtime Observability Flow:")
    add_bullet("1. Client Browser: Requests /dashboard or triggers automated 5-second AJAX polling to /metrics.")
    add_bullet("2. Flask Controller: Dispatches request to monitoring.get_system_metrics() in monitoring.py.")
    add_bullet("3. Kernel Telemetry: psutil queries hardware counters for CPU %, virtual memory %, disk %, and boot time.")
    add_bullet("4. Snapshot Persistence: Telemetry values are validated and inserted into the metrics table in data/monitoring.db.")
    add_bullet("5. Threshold Evaluation: Current readings are compared against active limits stored in the settings table.")
    add_bullet("6. Alert Lifecycle: If a threshold is exceeded, a new alert is generated or deduplicated. When values return to normal, active alerts auto-resolve.")
    add_bullet("7. Presentation: The updated telemetry, system health badge, and active incident strips are returned via JSON/HTML.")

    add_body_paragraph("B. DevOps CI/CD Delivery Pipeline:")
    add_bullet("1. Developer: Commits code changes and pushes to GitHub repository.")
    add_bullet("2. Jenkins Stage 1 (Checkout): Jenkins agent clones the latest source code revision.")
    add_bullet("3. Jenkins Stage 2 (Docker Build): Executes 'docker build -t cloud-monitoring-ci .' creating the immutable container image.")
    add_bullet("4. Jenkins Stage 3 (Automated Testing): Executes 'docker run --rm cloud-monitoring-ci python -m pytest test_app.py -v'. If tests fail, the pipeline aborts.")
    add_bullet("5. Jenkins Stage 4 (Ansible Deployment): Triggers Ansible playbook 'cloud-monitoring-deploy.yml' to deploy the container.")
    add_bullet("6. Target Container Execution: Runs container 'cloud-monitoring-ansible' on port 5002:5000 with volume 'cloud_monitoring_data:/app/data'.")

    # ==========================================
    # 6. MODULE 1 - USER INTERFACE
    # ==========================================
    add_section_header("6. MODULE 1 — MONITORING USER INTERFACE & REAL-TIME DASHBOARD")
    add_body_paragraph(
        "This module delivers the operations dashboard for infrastructure observability. Designed with a dark cloud-operations aesthetic, "
        "it presents system telemetry with clarity, avoiding complex dependencies."
    )
    add_bullet("Metric Cards: Visual cards for CPU, Memory, and Disk Storage with colored progress meters and real-time percentages.")
    add_bullet("System Overview Bar: Displays Global Health status (Healthy, Warning, Critical), Monitored Node name, Operating System, Filesystem Mount, and Uptime.")
    add_bullet("Active Alert Banner: Prominently highlights unhandled infrastructure anomalies requiring administrator attention.")
    add_bullet("Recent Snapshot Log: Displays the last 10 metric readings stored in the SQLite database with nominal/exceeded badges.")
    add_bullet("Dual Refresh Controls: Provides a 5-second auto-refresh countdown toggle and a manual 'Refresh Now' trigger button.")
    add_bullet("Native Canvas Trend Visualization: Renders dynamic multi-line charts (CPU cyan, Memory purple, Disk green) using HTML5 Canvas.")

    # ==========================================
    # 7. MODULE 2 - FLASK BACKEND
    # ==========================================
    add_section_header("7. MODULE 2 — FLASK BACKEND & METRIC COLLECTION ENGINE")
    add_body_paragraph(
        "Module 2 encompasses the backend controller (app.py) and core telemetry engine (monitoring.py). It mediates communication between "
        "the frontend client, operating system kernel, and SQLite persistence layer."
    )
    add_bullet("GET / & /dashboard: Serves the primary monitoring dashboard populated with live telemetry and active alert summaries.")
    add_bullet("GET /metrics: RESTful endpoint returning structured JSON containing metric readings, alert actions, and health states for polling clients.")
    add_bullet("GET /history & /api/history: Fetches historical metric records with query limit options (20, 50, 100) for tabular and Canvas rendering.")
    add_bullet("GET /alerts: Displays active and resolved incident logs with severity categorization and filtering.")
    add_bullet("GET /settings & POST /update_settings: Validates and persists administrator-configured anomaly limits.")
    add_bullet("GET /health: Container health check endpoint verifying database connectivity and operational status.")
    add_bullet("psutil Engine: Interfaces with psutil.cpu_percent(), psutil.virtual_memory(), and psutil.disk_usage() safely handling exceptions.")

    # ==========================================
    # 8. MODULE 3 - SQLITE DATABASE
    # ==========================================
    add_section_header("8. MODULE 3 — SQLITE DATABASE PERSISTENCE")
    add_body_paragraph(
        "This module manages data storage using SQLite embedded at data/monitoring.db. All SQL statements use parameterized bindings "
        "to prevent SQL injection vulnerabilities and enforce thread-safe database access."
    )
    add_bullet("Table 'metrics': Columns: id (PK), cpu_percent (REAL), memory_percent (REAL), disk_percent (REAL), uptime_seconds (INT), collected_at (TEXT).")
    add_bullet("Table 'alerts': Columns: id (PK), metric_name (TEXT), metric_value (REAL), threshold_value (REAL), severity (TEXT), status (TEXT), created_at (TEXT), resolved_at (TEXT).")
    add_bullet("Table 'settings': Columns: id (PK), cpu_threshold (REAL), memory_threshold (REAL), disk_threshold (REAL), updated_at (TEXT). Default: 80%, 80%, 85%.")
    add_bullet("Auto-Initialization: Automatically generates tables and initial threshold rows on application boot via monitoring.init_db().")

    # ==========================================
    # 9. MODULE 4 - GIT & GITHUB
    # ==========================================
    add_section_header("9. MODULE 4 — GIT & GITHUB SOURCE CONTROL")
    add_body_paragraph(
        "Version control and code collaboration are managed through Git locally and GitHub remotely."
    )
    add_bullet("Repository Hygiene: Complete .gitignore file excluding data/monitoring.db, *.pyc, __pycache__, .venv, and .pytest_cache.")
    add_bullet("Commit History: Meaningful atomic commits tracking application logic, Docker configuration, Jenkinsfile, and test suites.")
    add_bullet("Branching & Merging: Supports trunk-based or feature-branch workflows integrated with Jenkins SCM checkout.")

    # ==========================================
    # 10. MODULE 5 - DOCKER CONTAINERIZATION
    # ==========================================
    add_section_header("10. MODULE 5 — DOCKER CONTAINERIZATION & HEALTH CHECKS")
    add_body_paragraph(
        "Module 5 packages the application into an immutable container based on python:3.11-slim defined in Dockerfile."
    )
    add_bullet("Lightweight Base: Built on Debian-slim with Python 3.11 runtime, optimizing image footprint.")
    add_bullet("Directory Structure: Application code copied to /app with persistent data directory /app/data.")
    add_bullet("Port Configuration: Exposes port 5000 internally; mapped to host port 5002 in production deployment.")
    add_bullet("Built-in Healthcheck: Periodically queries /health using Python urllib to verify container liveliness.")

    # ==========================================
    # 11. MODULE 6 - JENKINS CI/CD PIPELINE
    # ==========================================
    add_section_header("11. MODULE 6 — JENKINS CI/CD PIPELINE")
    add_body_paragraph(
        "Jenkins automates the Continuous Integration and Continuous Deployment pipeline using a declarative Jenkinsfile comprising 4 sequential stages:"
    )
    add_bullet("Stage 1 — Checkout: Clones source code from Git repository into Jenkins workspace.")
    add_bullet("Stage 2 — Build: Executes 'docker build -t cloud-monitoring-ci .' to create the application image.")
    add_bullet("Stage 3 — Test: Runs 'docker run --rm cloud-monitoring-ci python -m pytest test_app.py -v'. If any test fails, the pipeline terminates.")
    add_bullet("Stage 4 — Deploy with Ansible: Executes 'ansible-playbook -i inventory.ini cloud-monitoring-deploy.yml' for deployment.")

    # ==========================================
    # 12. MODULE 7 - AUTOMATED TESTING (PYTEST)
    # ==========================================
    add_section_header("12. MODULE 7 — AUTOMATED TESTING (PYTEST)")
    add_body_paragraph(
        "Module 7 implements automated testing via test_app.py, ensuring comprehensive test coverage across 11 test cases:"
    )
    add_bullet("1. test_flask_app_initialization: Verifies application factory initialization.")
    add_bullet("2. test_home_and_dashboard_routes: Validates root 302 redirection and dashboard 200 response.")
    add_bullet("3. test_health_endpoint: Tests container health check returning HTTP 200 and healthy JSON status.")
    add_bullet("4. test_metrics_collection_endpoint: Validates /metrics telemetry collection and JSON serialization.")
    add_bullet("5. test_metric_snapshot_storage: Verifies accurate insertion and retrieval in SQLite metrics table.")
    add_bullet("6. test_alert_lifecycle_trigger_dedup_and_resolve: Tests alert creation on threshold breach, deduplication on continued load, and auto-resolution when metrics normalize.")
    add_bullet("7. test_threshold_settings_validation: Enforces 1.0% to 100.0% numeric validation and rejects invalid inputs.")
    add_bullet("8. test_settings_update_post_route: Tests POST /update_settings form processing and flash feedback.")
    add_bullet("9. test_history_and_alerts_pages_return_200: Confirms rendering of all ancillary views.")
    add_bullet("10. test_empty_history_graceful_handling: Validates zero-state handling when database contains no prior records.")
    add_bullet("11. test_format_uptime_utility: Validates human-readable conversion of uptime seconds.")

    # ==========================================
    # 13. MODULE 8 - ANSIBLE DEPLOYMENT
    # ==========================================
    add_section_header("13. MODULE 8 — ANSIBLE DEPLOYMENT AUTOMATION")
    add_body_paragraph(
        "Ansible provides automated, idempotent container configuration through cloud-monitoring-deploy.yml."
    )
    add_bullet("Idempotency: Uses community.docker.docker_container module; verifies running container state and updates only when configuration differs.")
    add_bullet("Container Configuration: Container name 'cloud-monitoring-ansible', image 'cloud-monitoring-ci', port '5002:5000', restart policy 'unless-stopped'.")
    add_bullet("Volume Attachment: Mounts 'cloud_monitoring_data:/app/data' ensuring zero data loss during automated redeployments.")

    # ==========================================
    # 14. MODULE 9 - PERSISTENT STORAGE
    # ==========================================
    add_section_header("14. MODULE 9 — PERSISTENT STORAGE (DOCKER VOLUME)")
    add_body_paragraph(
        "To guarantee that operational history, alerts, and settings survive container deletion, persistent storage is implemented using a Docker Volume."
    )
    add_bullet("Volume Name: cloud_monitoring_data.")
    add_bullet("Mount Point: /app/data inside the container.")
    add_bullet("Database Path: /app/data/monitoring.db.")
    add_bullet("Persistence Verification: Container can be stopped and removed ('docker rm -f'); launching a new container with the same volume restores all historical data.")

    # ==========================================
    # 15. MODULE 10 - ALERT LIFECYCLE
    # ==========================================
    add_section_header("15. MODULE 10 — ANOMALY THRESHOLDS & AUTOMATED ALERT LIFECYCLE")
    add_body_paragraph(
        "This module governs the alert lifecycle to prevent alert fatigue and provide deterministic incident management."
    )
    add_bullet("Threshold Configuration: Administrators can adjust CPU, RAM, and Disk limits between 1.0% and 100.0% through /settings.")
    add_bullet("Alert Creation: An active alert is created when a reading exceeds its configured threshold, classified as Warning or Critical.")
    add_bullet("Deduplication: If a metric continues to exceed the threshold across polling cycles, the existing active alert is updated rather than creating duplicate rows.")
    add_bullet("Auto-Resolution: Once metric values drop back below the threshold, the alert status automatically transitions to 'Resolved' with an exact resolved_at timestamp.")

    # ==========================================
    # 16. MODULE 11 - CI/CD INTEGRATION
    # ==========================================
    add_section_header("16. MODULE 11 — CI/CD INTEGRATION & PIPELINE ORCHESTRATION")
    add_body_paragraph(
        "Module 11 harmonizes the individual DevOps tools into an integrated pipeline: Git → GitHub → Jenkins → Docker → Pytest → Ansible → Docker Volume → Flask → SQLite."
    )
    add_bullet("Automated Gatekeeping: Jenkins prevents deployment if any Pytest test case fails.")
    add_bullet("Repeatability: Entire infrastructure deployment can be reproduced identically on any Docker host.")

    # ==========================================
    # 17. MODULE 12 - VERIFICATION
    # ==========================================
    add_section_header("17. MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION")
    add_body_paragraph(
        "Verification confirms the health and reliability of all project subsystems:"
    )
    add_bullet("Application Verification: Verified live dashboard, /metrics API, canvas trend chart, and threshold update form.")
    add_bullet("Docker Verification: Verified image creation, container health checks, and volume inspection.")
    add_bullet("Pytest Verification: 11 of 11 tests passed in 0.43s.")
    add_bullet("Ansible Verification: Playbook executed with 0 failures.")

    # ==========================================
    # 18. RESULTS AND OUTPUT
    # ==========================================
    add_section_header("18. RESULTS AND OUTPUT")
    add_body_paragraph(
        "The completed Cloud Infrastructure Monitoring and Automated Alert System successfully delivers:"
    )
    add_bullet("Real-time host and container observability with live CPU, Memory, Disk, and Uptime meters.")
    add_bullet("Automated 5-second AJAX polling with countdown timer and manual on-demand refresh.")
    add_bullet("Incident alert management with automated trigger, deduplication, and auto-resolution.")
    add_bullet("Configurable threshold management with validated range enforcement (1.0% to 100.0%).")
    add_bullet("Historical metrics logging with interactive plain HTML5 Canvas trend visualization.")
    add_bullet("Isolated containerized deployment on Docker with persistent SQLite storage via Docker Volume.")
    add_bullet("Automated test validation with 11 passing Pytest cases.")
    add_bullet("Automated CI/CD pipeline orchestrated via Jenkins and deployed via Ansible.")

    # ==========================================
    # 19. COMMANDS USED
    # ==========================================
    add_section_header("19. COMMANDS USED")
    add_body_paragraph("A. Local Application & Testing Commands:")
    add_bullet("Run Pytest suite: python -m pytest test_app.py -v")
    add_bullet("Start Flask application: python app.py")
    add_bullet("Access Dashboard: http://localhost:5000/dashboard")

    add_body_paragraph("B. Docker Commands:")
    add_bullet("Create Persistent Volume: docker volume create cloud_monitoring_data")
    add_bullet("Build Docker Image: docker build -t cloud-monitoring-ci .")
    add_bullet("Run Container with Volume: docker run -d --name cloud-monitoring-ansible -p 5002:5000 -v cloud_monitoring_data:/app/data cloud-monitoring-ci")
    add_bullet("List Running Containers: docker ps")
    add_bullet("View Container Logs: docker logs cloud-monitoring-ansible")
    add_bullet("Inspect Volume: docker volume inspect cloud_monitoring_data")

    add_body_paragraph("C. Ansible Deployment Commands:")
    add_bullet("Run Ansible Playbook: ansible-playbook -i inventory.ini cloud-monitoring-deploy.yml")

    add_body_paragraph("D. SQLite Verification Commands:")
    add_bullet("Query Metrics Table: docker exec cloud-monitoring-ansible python -c \"import sqlite3; c=sqlite3.connect('data/monitoring.db'); [print(row) for row in c.execute('SELECT * FROM metrics LIMIT 5')]; c.close()\"")
    add_bullet("Query Alerts Table: docker exec cloud-monitoring-ansible python -c \"import sqlite3; c=sqlite3.connect('data/monitoring.db'); [print(row) for row in c.execute('SELECT * FROM alerts')]; c.close()\"")

    add_body_paragraph("E. Git Version Control Commands:")
    add_bullet("Check Status: git status")
    add_bullet("View Commit History: git log --oneline --graph")
    add_bullet("Commit and Push: git add . && git commit -m \"Finalize DevOps Monitoring project\" && git push origin master")

    # ==========================================
    # 20. ADVANTAGES
    # ==========================================
    add_section_header("20. ADVANTAGES")
    add_bullet("Zero Cost & Lightweight: Uses open-source technologies (Python, Flask, SQLite, psutil) without expensive third-party SaaS fees.")
    add_bullet("Eliminates Alert Fatigue: Built-in alert deduplication prevents repeated notification flooding during sustained load.")
    add_bullet("Automated Auto-Resolution: Eliminates stale alerts by automatically resolving incidents when metrics return below thresholds.")
    add_bullet("Data Durability: Docker Volume guarantees zero data loss across container teardown, rebuild, or recreation.")
    add_bullet("Automated Quality Assurance: Integrated Pytest suite halts broken builds in Jenkins prior to production deployment.")
    add_bullet("Repeatable Infrastructure: Ansible playbook ensures consistent, idempotent deployments across developer and production hosts.")

    # ==========================================
    # 21. LIMITATIONS
    # ==========================================
    add_section_header("21. LIMITATIONS")
    add_bullet("Host/Container Scope: In an unprivileged Docker container, psutil observes the container's visible cgroups and virtualized boundaries rather than an entire multi-node cluster.")
    add_bullet("Embedded SQLite Database: SQLite is designed for lightweight single-server deployments; high-concurrency enterprise clusters require PostgreSQL or MySQL.")
    add_bullet("Local Demonstration Focus: Default alert delivery is in-app; real-time SMS/Email dispatch requires configured external SMTP or Twilio API keys.")

    # ==========================================
    # 22. FUTURE ENHANCEMENTS
    # ==========================================
    add_section_header("22. FUTURE ENHANCEMENTS")
    add_bullet("Multi-Node Agent Network: Implementing distributed lightweight telemetry agents reporting to a centralized aggregator.")
    add_bullet("External Cloud Integrations: Ingesting AWS CloudWatch, Azure Monitor, and Google Cloud telemetry via official SDKs.")
    add_bullet("External Incident Webhooks: Dispatching automated alert webhooks to Slack, Discord, PagerDuty, or Microsoft Teams.")
    add_bullet("Time-Series Database Migration: Integrating Prometheus and Grafana for long-term time-series indexing and custom dashboards.")

    # ==========================================
    # 23. CONCLUSION
    # ==========================================
    add_section_header("23. CONCLUSION")
    add_body_paragraph(
        "The Cloud Infrastructure Monitoring and Automated Alert System successfully demonstrates the end-to-end integration of a full-stack "
        "observability web application with an automated DevOps CI/CD delivery pipeline. Developed for the 23IT723 DevOps Laboratory at Coimbatore "
        "Institute of Technology, the system delivers real-time monitoring of CPU, RAM, Disk storage, and uptime using Python’s psutil library, "
        "supported by a responsive operations dashboard and an embedded SQLite database. The automated alert engine eliminates alert fatigue through "
        "intelligent deduplication and provides hands-off lifecycle management with automatic resolution."
    )
    add_body_paragraph(
        "On the DevOps side, the project implements a complete, repeatable automation pipeline: Git and GitHub manage version control; Jenkins orchestrates "
        "a 4-stage declarative pipeline; Docker containerizes the application into an immutable image with container health checks; Pytest guarantees "
        "software quality with 11 unit/integration test cases; Ansible automates idempotent deployment; and a named Docker Volume provides data durability. "
        "The complete workflow verifies the seamless integration of Git → GitHub → Jenkins → Docker → Pytest → Ansible → Flask → SQLite → Docker Volume, "
        "fulfilling all requirements for a professional, college-level DevOps engineering project."
    )

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "23IT723_Cloud_Infrastructure_Monitoring_Report.docx")
    doc.save(output_path)
    print(f"[SUCCESS] Report successfully generated at: {output_path}")

if __name__ == '__main__':
    create_report()
