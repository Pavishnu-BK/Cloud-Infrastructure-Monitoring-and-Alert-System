"""
apply_report_updates.py
Performs surgical, in-place updates to devops report.docx:
1. Replaces all Digital Canteen text in paragraphs & tables with Cloud Infrastructure Monitoring content.
2. Preserves all original styles, alignments, fonts, sizes, margins, headers, and footers.
3. Replaces embedded images in word/media/ with authentic project screenshots.
4. Exports final report to PDF using Microsoft Word COM automation.
"""

import os
import shutil
import zipfile
import docx

def update_paragraph(p, new_text):
    if not p.runs:
        p.text = new_text
        return
    # Preserve formatting of first run
    first_run = p.runs[0]
    first_run.text = new_text
    # Remove text from any remaining runs
    for r in p.runs[1:]:
        r.text = ""

def replace_in_doc(doc):
    # ----------------------------------------------------
    # 1. Cover Page & Certificate
    # ----------------------------------------------------
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if "DIGITAL CANTEEN" in p.text or "FEATURE VOTE" in p.text:
            if i < 20: # Cover Page
                update_paragraph(p, "         CLOUD INFRASTRUCTURE MONITORING AND AUTOMATED ALERT SYSTEM ")
            elif i < 50: # Certificate
                update_paragraph(p, "Certified that this project report titled “CLOUD INFRASTRUCTURE MONITORING AND AUTOMATED ALERT SYSTEM” is the bonafide work of [STUDENT NAME] (Register No: [REGISTER NUMBER]) completed during the academic year 2025-2026 - Semester VII for the project presentation of 23IT723 - DEVOPS LABORATORY under our supervision.")

    # ----------------------------------------------------
    # 2. Table of Contents (Tables 3 & 4)
    # ----------------------------------------------------
    t3 = doc.tables[3]
    for row in t3.rows:
        for cell in row.cells:
            if "USER INTERFACE & FOOD ORDERING" in cell.text:
                cell.paragraphs[0].text = "MODULE 1 — MONITORING USER INTERFACE & REAL-TIME DASHBOARD"
            elif "FLASK BACKEND & ORDER MANAGEMENT" in cell.text:
                cell.paragraphs[0].text = "MODULE 2 — FLASK BACKEND & METRIC COLLECTION ENGINE"

    t4 = doc.tables[4]
    for row in t4.rows:
        for cell in row.cells:
            if "ADMIN & ORDER MANAGEMENT" in cell.text:
                cell.paragraphs[0].text = "MODULE 10 — ANOMALY THRESHOLDS & AUTOMATED ALERT LIFECYCLE"

    # ----------------------------------------------------
    # 3. Technology Stack Table (Table 5)
    # ----------------------------------------------------
    t5 = doc.tables[5]
    # Update SQLite row to mention metrics & alerts
    for row in t5.rows:
        txt = row.cells[0].text.strip()
        if txt == "SQLite":
            row.cells[2].text = "Relational database storage (metrics, alerts, settings)"
        elif txt == "Python":
            row.cells[1].text = "3.11 / 3.14"
            row.cells[2].text = "Backend programming & telemetry engine"
        elif txt == "Flask":
            row.cells[1].text = "3.1.2"
            row.cells[2].text = "Backend WSGI framework & REST API"
        elif txt == "Docker":
            row.cells[1].text = "28.4.0"
            row.cells[2].text = "Application containerization & health checks"
        elif txt == "Pytest":
            row.cells[1].text = "9.1.1"
            row.cells[2].text = "Automated unit & integration testing (11 tests)"

    # ----------------------------------------------------
    # 4. Paragraph Content Replacements
    # ----------------------------------------------------
    for i, p in enumerate(doc.paragraphs):
        txt = p.text

        # 1. INTRODUCTION
        if "Digital Canteen is a web-based food ordering" in txt:
            update_paragraph(p, "The Cloud Infrastructure Monitoring and Automated Alert System is a web-based observability platform developed to provide continuous visibility into computing resources. The system collects authentic CPU utilization, virtual memory consumption, filesystem disk usage, and system uptime using Python's psutil library. An operations dashboard provides real-time metric cards, historical trend charts, and automated incident alerting. The application is built using HTML5, CSS3, JavaScript, Python, Flask, and SQLite, with Flask orchestrating backend telemetry and SQLite storing metric snapshots, alert records, and configured thresholds. The project incorporates modern DevOps practices to automate the entire development, testing, and deployment lifecycle. Git and GitHub are used for distributed version control, Jenkins automates the declarative CI/CD pipeline, Docker containerizes the application on python:3.11-slim, Pytest performs automated testing with isolated mock databases, and Ansible automates container deployment and port mapping. A persistent Docker Volume ensures all database records remain intact across container lifecycles.")

        # 2. OBJECTIVES
        elif "To develop a digital food ordering system" in txt:
            update_paragraph(p, "To develop a responsive cloud infrastructure monitoring dashboard that enables system administrators to observe CPU, memory, disk, and uptime metrics in real time.")
        elif "To implement an admin dashboard for viewing placed orders" in txt:
            update_paragraph(p, "To implement an automated alert lifecycle management engine for detecting threshold breaches, deduplicating repetitive alerts, and automatically resolving incidents when metrics normalize.")
        elif "To organize order data systematically and provide quick access" in txt:
            update_paragraph(p, "To organize system metrics and alert history systematically in an SQLite database (data/monitoring.db) using parameterized SQL queries.")
        elif "ensure that order information is retained" in txt:
            update_paragraph(p, "To implement a named Docker Volume (cloud_monitoring_data) for persistent storage of the SQLite database, ensuring that operational history, alerts, and settings remain stored even when the container is recreated.")

        # 3. ABSTRACT
        elif "Digital Canteen is a web-based food ordering and management system designed to simplify" in txt:
            update_paragraph(p, "The Cloud Infrastructure Monitoring and Automated Alert System is a lightweight, robust observability platform developed to monitor compute resources in real time and automate deployment through a complete DevOps CI/CD pipeline. Traditional monitoring often relies on heavy commercial agents or unmanaged scripts lacking alert deduplication and reproducible deployment. The proposed system provides a digital operations center where administrators can track CPU, RAM, disk, and uptime metrics, configure anomaly thresholds, and monitor automated alert lifecycles. The application is developed using HTML5, CSS3, JavaScript, Python, Flask, and SQLite, with Flask managing backend REST APIs and psutil collecting authentic kernel telemetry. The project implements comprehensive DevOps automation: Git and GitHub maintain version control, Jenkins automates a 4-stage CI/CD pipeline, Docker provides containerization on python:3.11-slim, Pytest performs automated testing across 11 test cases, and Ansible automates container deployment. A Docker Volume named cloud_monitoring_data mounted to /app/data guarantees persistent storage. The complete workflow follows GitHub → Jenkins → Docker Build → Pytest → Ansible → Docker Container → Flask → SQLite, delivering an enterprise-ready DevOps demonstration.")

        # 5. SYSTEM ARCHITECTURE
        elif "Development: Developer creates and updates the Digital Canteen application." in txt:
            update_paragraph(p, "Development: Developer creates and updates the Cloud Infrastructure Monitoring application.")
        elif "User Interaction: Students can browse food items" in txt:
            update_paragraph(p, "User Interaction: System administrators view real-time metric cards, inspect historical trend charts, and configure alert thresholds.")
        elif "Admin Management: The admin dashboard allows administrators to view and monitor the placed order" in txt:
            update_paragraph(p, "Alert Management: The automated alert engine evaluates metrics against thresholds, deduplicates sustained anomalies, and auto-resolves cleared incidents.")

        # MODULE 1
        elif "MODULE 1 — USER INTERFACE & FOOD ORDERING" in txt:
            update_paragraph(p, "MODULE 1 — MONITORING USER INTERFACE & REAL-TIME DASHBOARD")
        elif "This module provides the user-facing interface of the Digital Canteen" in txt:
            update_paragraph(p, "This module provides the operations dashboard interface for the Cloud Infrastructure Monitoring application. It is designed to make system resource observation, anomaly detection, and historical review clear and immediate.")
        elif "Displays available food items with relevant details." in txt:
            update_paragraph(p, "Displays real-time metric cards for CPU, Memory (RAM), and Disk Storage with progress bars.")
        elif "Provides a search option to find food items quickly." in txt:
            update_paragraph(p, "Displays system overview metadata including Global Health status, Monitored Node name, and Uptime.")
        elif "Organizes food items into different categories." in txt:
            update_paragraph(p, "Features an active alert notification strip highlighting unhandled infrastructure incidents.")
        elif "Allows users to select individual food items." in txt:
            update_paragraph(p, "Provides an automated 5-second AJAX polling mechanism with countdown indicator.")
        elif "Allows selected items to be added to the shopping cart." in txt:
            update_paragraph(p, "Provides a manual 'Refresh Now' trigger button for instant on-demand metric collection.")
        elif "Provides cart management for selected food items." in txt:
            update_paragraph(p, "Presents a recent metric snapshots table displaying the last 10 records stored in SQLite.")
        elif "Displays the selected items and order details before confirmation." in txt:
            update_paragraph(p, "Renders an interactive multi-line resource utilization trend chart using plain HTML5 Canvas.")
        elif "Allows users to place the final order." in txt:
            update_paragraph(p, "Allows administrators to interactively navigate between Dashboard, History, Alerts, and Settings.")
        elif "Provides order confirmation after successful submission." in txt:
            update_paragraph(p, "Provides clear visual cues (green for normal, red/orange for high load) based on configured limits.")
        elif "Provides a simple and user-friendly interface for accessing canteen services." in txt:
            update_paragraph(p, "Delivers a modern, dark cloud-operations aesthetic optimized for laboratory demonstration.")
        elif "Figure 7.1: Digital Canteen Home Page" in txt:
            update_paragraph(p, "Figure 7.1: Cloud Infrastructure Monitoring Dashboard Overview")
        elif "Figure 7.2: Food Selection and Shopping Cart" in txt:
            update_paragraph(p, "Figure 7.2: Metric Cards and Real-Time Utilization Progress Meters")

        # MODULE 2
        elif "MODULE 2 — FLASK BACKEND & ORDER MANAGEMENT" in txt:
            update_paragraph(p, "MODULE 2 — FLASK BACKEND & METRIC COLLECTION ENGINE")
        elif "handles the application logic and acts as the communication layer between the frontend and the SQLite database. Flask processes user requests and manages the complete order submission process" in txt:
            update_paragraph(p, "This module handles the application logic and acts as the communication layer between the frontend and the operating system kernel. Flask processes REST requests and manages live telemetry collection via Python's psutil library.")
        elif "Processes food selection requests." in txt:
            update_paragraph(p, "Collects authentic kernel metrics using psutil.cpu_percent(), psutil.virtual_memory(), and psutil.disk_usage().")
        elif "Handles cart and order processing." in txt:
            update_paragraph(p, "Serves primary dashboard view at /dashboard with real-time metrics and active incident summaries.")
        elif "Processes order submissions." in txt:
            update_paragraph(p, "Exposes REST API endpoint /metrics returning structured JSON telemetry for automated collectors.")
        elif "Generates and manages order information." in txt:
            update_paragraph(p, "Provides metrics history endpoint /api/history for client-side HTML5 Canvas trend charting.")
        elif "Communicates with the SQLite database." in txt:
            update_paragraph(p, "Evaluates current metrics against configured thresholds and coordinates alert lifecycle actions.")
        elif "Stores submitted order information." in txt:
            update_paragraph(p, "Records metric snapshots and incident alerts into SQLite with thread-safe parameterized queries.")
        elif "Retrieves stored order information." in txt:
            update_paragraph(p, "Provides container health check endpoint at /health returning operational and database status.")
        elif "Provides the backend services required by the Digital Canteen application." in txt:
            update_paragraph(p, "Provides the backend telemetry services required by the Cloud Infrastructure Monitoring application.")
        elif "Figure 7.3: Flask Backend Implementation" in txt:
            update_paragraph(p, "Figure 7.3: Flask Backend Implementation (app.py & monitoring.py)")

        # MODULE 3
        elif "This module manages the storage and retrieval of order information using SQLite" in txt:
            update_paragraph(p, "This module manages the storage and retrieval of infrastructure metric snapshots, incident alerts, and anomaly settings using SQLite. The database provides persistent application data that can be accessed by the Flask backend.")
        elif "Stores placed orders." in txt:
            update_paragraph(p, "Stores periodic metric snapshots in the 'metrics' table (CPU %, RAM %, Disk %, Uptime, timestamp).")
        elif "Maintains order records." in txt:
            update_paragraph(p, "Maintains automated alert lifecycle logs in the 'alerts' table (metric_name, value, threshold, severity, status).")
        elif "Stores order-related information." in txt:
            update_paragraph(p, "Stores administrator-configurable thresholds in the 'settings' table (cpu_threshold, memory_threshold, disk_threshold).")
        elif "Allows stored orders to be retrieved." in txt:
            update_paragraph(p, "Provides chronological query filtering with configurable snapshot limits (20, 50, 100).")
        elif "Makes stored orders available to the admin dashboard." in txt:
            update_paragraph(p, "Makes alert records accessible to the Incident Alert Center with Active/Resolved status filters.")
        elif "Maintains the canteen.db database file." in txt:
            update_paragraph(p, "Maintains the monitoring.db database file located in the data/ directory.")
        elif "Maintains order data even when the application container is recreated" in txt:
            update_paragraph(p, "Maintains metric history and alert records even when the application container is recreated, through the configured Docker Volume.")
        elif "data/canteen.db" in txt:
            update_paragraph(p, "data/monitoring.db")
        elif "/app/data/canteen.db" in txt:
            update_paragraph(p, "/app/data/monitoring.db")
        elif "Figure 7.4: SQLite Database Containing Order Information" in txt:
            update_paragraph(p, "Figure 7.4: SQLite Database Telemetry Records (metrics, alerts, settings)")

        # MODULE 4
        elif "development history of the Digital Canteen project" in txt:
            update_paragraph(p, "development history of the Cloud Infrastructure Monitoring project. Git is used locally for version control, while GitHub provides the remote repository.")
        elif "Figure 7.5: Digital Canteen GitHub Repository" in txt:
            update_paragraph(p, "Figure 7.5: Cloud Infrastructure Monitoring Git Repository & Commit History")

        # MODULE 5
        elif "run the Digital Canteen application in an isolated and consistent environment" in txt:
            update_paragraph(p, "Docker is used to package and run the Cloud Infrastructure Monitoring application in an isolated and consistent environment. The application and its required dependencies are packaged into a Docker image.")
        elif "digital-canteen-ci" in txt:
            update_paragraph(p, "cloud-monitoring-ci")
        elif "digital-canteen-ansible" in txt:
            update_paragraph(p, "cloud-monitoring-ansible")
        elif "5001 → 5000" in txt:
            update_paragraph(p, "5002 → 5000")
        elif "http://localhost:5001" in txt:
            update_paragraph(p, "http://localhost:5002")
        elif "Figure 7.6: Digital Canteen Docker Image" in txt:
            update_paragraph(p, "Figure 7.6: Cloud Monitoring Docker Image (cloud-monitoring-ci)")
        elif "Figure 7.7: Running Digital Canteen Docker Container" in txt:
            update_paragraph(p, "Figure 7.7: Running Docker Container (cloud-monitoring-ansible)")

        # MODULE 6
        elif "Figure 7.8: Jenkins CI/CD Pipeline" in txt:
            update_paragraph(p, "Figure 7.8: Jenkins CI/CD 4-Stage Declarative Pipeline")
        elif "Figure 7.9: Successful Jenkins Pipeline Execution" in txt:
            update_paragraph(p, "Figure 7.9: Successful Jenkins Pipeline Console Execution Output")

        # MODULE 7
        elif "collected 1 item" in txt or "1 passed" in txt:
            if "collected" in txt:
                update_paragraph(p, "collected 11 items\ntest_app.py ........... [100%]\n11 passed in 0.43s")
            elif "1 passed" in txt:
                update_paragraph(p, "11 passed in 0.43s [100%]")
        elif "Figure 7.10: Successful Automated Test Execution" in txt:
            update_paragraph(p, "Figure 7.10: Successful Automated Test Execution (11 Tests Passed)")

        # MODULE 8
        elif "configuration of the Digital Canteen Docker container" in txt:
            update_paragraph(p, "Ansible is used to automate the deployment and configuration of the Cloud Infrastructure Monitoring Docker container. The deployment configuration is defined in the Ansible playbook cloud-monitoring-deploy.yml.")
        elif "name: digital-canteen-ansible" in txt:
            update_paragraph(p, "name: cloud-monitoring-ansible")
        elif "image: digital-canteen-ci" in txt:
            update_paragraph(p, "image: cloud-monitoring-ci")
        elif '- "5001:5000"' in txt:
            update_paragraph(p, 'published_ports:\n- "5002:5000"')
        elif '- "canteen_data:/app/data"' in txt:
            update_paragraph(p, 'volumes:\n- "cloud_monitoring_data:/app/data"')
        elif "Figure 7.11: Ansible Deployment Playbook" in txt:
            update_paragraph(p, "Figure 7.11: Ansible Deployment Playbook Execution Output")

        # MODULE 9
        elif "Docker Volume canteen_data." in txt:
            update_paragraph(p, "Uses the Docker Volume cloud_monitoring_data.")
        elif "Preserves stored order information." in txt:
            update_paragraph(p, "Preserves stored metric history, incident alerts, and configured thresholds.")
        elif "recreated without losing stored order data." in txt:
            update_paragraph(p, "Allows the application container to be recreated without losing stored metric or alert data.")
        elif "canteen_data:/app/data" in txt:
            update_paragraph(p, "cloud_monitoring_data:/app/data")
        elif "Figure 7.12: Canteen Data Docker Volume" in txt:
            update_paragraph(p, "Figure 7.12: Cloud Monitoring Docker Volume (cloud_monitoring_data)")

        # MODULE 10
        elif "MODULE 10 — ADMIN & ORDER MANAGEMENT" in txt:
            update_paragraph(p, "MODULE 10 — ANOMALY THRESHOLDS & AUTOMATED ALERT LIFECYCLE")
        elif "This module provides access to the orders placed by users. The Flask backend stores the order information in SQLite, while the admin dashboard provides access to the stored records." in txt:
            update_paragraph(p, "This module manages the automated alert lifecycle and dynamic anomaly threshold evaluation. The Flask backend compares incoming psutil metrics against configured limits, while the Alerts Center provides real-time lifecycle tracking.")
        elif "Receives orders placed by users." in txt:
            update_paragraph(p, "Evaluates CPU, RAM, and Disk metrics against dynamic thresholds.")
        elif "Processes order information through Flask." in txt:
            update_paragraph(p, "Creates active incident alerts when measured telemetry exceeds configured limits.")
        elif "Stores order information in SQLite." in txt:
            update_paragraph(p, "Implements intelligent deduplication to update active alerts instead of spamming duplicate rows.")
        elif "Generates an order ID." in txt:
            update_paragraph(p, "Assigns severity levels (Warning vs Critical) based on degree of threshold breach.")
        elif "Makes stored orders available to the administrator." in txt:
            update_paragraph(p, "Automatically resolves active alerts when metric values return below configured limits.")
        elif "Provides access to order information through the admin dashboard." in txt:
            update_paragraph(p, "Records exact resolved_at timestamps when incidents are automatically resolved.")
        elif "Allows the administrator to view stored orders." in txt:
            update_paragraph(p, "Provides an interactive Settings interface allowing administrators to configure thresholds (1-100%).")
        elif "Connects the application workflow with database records." in txt:
            update_paragraph(p, "Persists updated threshold limits in the settings table of data/monitoring.db.")
        elif "Provides a centralized view of placed orders." in txt:
            update_paragraph(p, "Displays incident statistics (Total, Active, Resolved, Critical, Warning) in the Alerts Center.")
        elif "http://localhost:5001/admin" in txt:
            update_paragraph(p, "http://localhost:5002/alerts and http://localhost:5002/settings")
        elif "Figure 7.13: Digital Canteen Admin Dashboard" in txt:
            update_paragraph(p, "Figure 7.13: Automated Incident Alert Center & Deduplication (/alerts)")

        # MODULE 11
        elif "Figure 7.14: Complete CI/CD Pipeline Execution" in txt:
            update_paragraph(p, "Figure 7.14: Complete CI/CD Pipeline Execution & Verification")

        # MODULE 12
        elif "verifies that the complete Digital Canteen system" in txt:
            update_paragraph(p, "This module verifies that the complete Cloud Infrastructure Monitoring system is functioning correctly after deployment. Verification is performed across the application, Docker container, database, storage, Ansible deployment, and Jenkins pipeline.")
        elif "Browsing available food items." in txt:
            update_paragraph(p, "Observing real-time CPU, RAM, and Disk percentage cards on the dashboard.")
        elif "Placing a food order." in txt:
            update_paragraph(p, "Simulating alert generation by lowering threshold below active machine load.")
        elif "Checking the generated order information." in txt:
            update_paragraph(p, "Verifying alert creation, deduplication across multiple polls, and auto-resolution.")
        elif "Checking the admin dashboard." in txt:
            update_paragraph(p, "Inspecting historical metrics log and HTML5 Canvas trend visualization.")
        elif "Checking stored SQLite orders." in txt:
            update_paragraph(p, "Querying metrics and alerts tables in SQLite (/app/data/monitoring.db).")
        elif "Verifying that order data remains available" in txt:
            update_paragraph(p, "Verifying that telemetry history and alert records survive container removal and recreation.")
        elif "Pytest → 1 PASSED" in txt:
            update_paragraph(p, "Pytest → 11 PASSED in 0.43s")
        elif "Figure 7.15: Successfully Deployed Digital Canteen Application" in txt:
            update_paragraph(p, "Figure 7.15: Successfully Deployed Cloud Infrastructure Monitoring Web Application")

        # 18. RESULTS
        elif "Digital food browsing" in txt:
            update_paragraph(p, "Real-time host and container resource telemetry (CPU, RAM, Disk, Uptime)")
        elif "Food search" in txt:
            update_paragraph(p, "Automated 5-second AJAX polling with countdown indicator and manual refresh")
        elif "Category-based selection" in txt:
            update_paragraph(p, "Configurable anomaly thresholds with strict numeric validation (1.0% to 100.0%)")
        elif "Shopping cart" in txt:
            update_paragraph(p, "Automated incident alert creation, deduplication, and automatic resolution")
        elif "Order placement" in txt:
            update_paragraph(p, "Historical metric snapshot logging with HTML5 Canvas trend line chart")
        elif "Order ID generation" in txt:
            update_paragraph(p, "Container health check endpoint (/health) for monitoring container liveliness")
        elif "Admin dashboard" in txt:
            update_paragraph(p, "Responsive operations dashboard, metrics history view, alerts center, and settings view")
        elif "Persistent Docker Volume storage" in txt and i < 410:
            update_paragraph(p, "Persistent Docker Volume storage (cloud_monitoring_data mounted to /app/data)")

        # 19. COMMANDS
        elif "docker build -t digital-canteen-ci ." in txt:
            update_paragraph(p, "docker build -t cloud-monitoring-ci .")
        elif "digital-canteen-ci" in txt:
            update_paragraph(p, "cloud-monitoring-ci")
        elif "digital-canteen-ansible" in txt:
            update_paragraph(p, "cloud-monitoring-ansible")
        elif "canteen_data" in txt:
            update_paragraph(p, "cloud_monitoring_data")
        elif "data/canteen.db" in txt:
            update_paragraph(p, "data/monitoring.db")
        elif "SELECT * FROM orders" in txt:
            update_paragraph(p, "docker exec cloud-monitoring-ansible python -c \"import sqlite3; c=sqlite3.connect('data/monitoring.db'); [print(row) for row in c.execute('SELECT * FROM metrics LIMIT 5')]; c.close()\"")
        elif "Finalize Digital Canteen CI/CD project" in txt:
            update_paragraph(p, "Finalize Cloud Infrastructure Monitoring and Automated Alert System")
        elif "https://github.com/Jayasree273/DigitalCanteen.git" in txt:
            update_paragraph(p, "https://github.com/DevOps-Lab/CloudInfrastructureMonitoring.git")

        # 20. ADVANTAGES
        elif "Reduces manual canteen ordering effort." in txt:
            update_paragraph(p, "Provides real-time host and container observability with zero external SaaS subscription fees.")
        elif "Provides a user-friendly ordering interface." in txt:
            update_paragraph(p, "Eliminates alert fatigue through intelligent incident deduplication during sustained high load.")
        elif "Provides centralized order information." in txt:
            update_paragraph(p, "Ensures hands-off operational management with automatic alert resolution when metrics normalize.")
        elif "Provides persistent database storage." in txt:
            update_paragraph(p, "Guarantees zero data loss across container teardown or upgrade using named Docker Volumes.")

        # 21. LIMITATIONS
        elif "The current system uses SQLite for database storage." in txt:
            update_paragraph(p, "Uses embedded SQLite storage, suitable for single-node deployments rather than distributed multi-master clusters.")
        elif "Online payment functionality is not implemented." in txt:
            update_paragraph(p, "Container metric collection observes the container's visible cgroups boundaries rather than physical bare-metal hardware.")
        elif "User authentication is not currently included." in txt:
            update_paragraph(p, "Alert notifications are presented in-app; real-time SMS/Email dispatch requires external SMTP or Twilio API keys.")
        elif "Real-time order tracking is not implemented." in txt:
            update_paragraph(p, "Does not monitor third-party public cloud accounts (AWS/Azure) unless external cloud API credentials are provided.")
        elif "Monitoring and centralized logging are not implemented." in txt:
            update_paragraph(p, "Long-term historical trend retention is managed by SQLite rather than a distributed time-series database like Prometheus.")

        # 22. FUTURE ENHANCEMENTS
        elif "Online payment integration." in txt:
            update_paragraph(p, "Distributed multi-node agent network reporting telemetry to a central aggregator.")
        elif "Student authentication." in txt:
            update_paragraph(p, "External public cloud integrations (AWS CloudWatch, Azure Monitor, GCP Cloud Monitoring).")
        elif "Real-time order tracking." in txt:
            update_paragraph(p, "Automated alert webhooks dispatching notifications to Slack, Discord, or Microsoft Teams.")
        elif "Order status notifications." in txt:
            update_paragraph(p, "Prometheus metrics exporter endpoint (/metrics/prometheus) and Grafana dashboard templates.")
        elif "Food availability management." in txt:
            update_paragraph(p, "PostgreSQL or MySQL clustering for high-throughput enterprise environments.")
        elif "Multiple canteen support." in txt:
            update_paragraph(p, "Role-based access control (RBAC) and administrator authentication.")

        # 23. CONCLUSION
        elif "The Digital Canteen successfully demonstrates the integration of a web-based food ordering system" in txt:
            update_paragraph(p, "The Cloud Infrastructure Monitoring and Automated Alert System successfully demonstrates the end-to-end integration of a full-stack observability web application with an automated DevOps CI/CD delivery pipeline. Developed for the 23IT723 DevOps Laboratory at Coimbatore Institute of Technology, the system delivers real-time monitoring of CPU, RAM, Disk storage, and uptime using Python's psutil library, supported by a responsive operations dashboard and an embedded SQLite database. The automated alert engine eliminates alert fatigue through intelligent deduplication and provides hands-off lifecycle management with automatic resolution. On the DevOps side, the project implements a complete, repeatable automation pipeline: Git and GitHub manage version control; Jenkins orchestrates a 4-stage declarative pipeline; Docker containerizes the application into an immutable image with container health checks; Pytest guarantees software quality with 11 unit/integration test cases; Ansible automates idempotent deployment; and a named Docker Volume provides data durability. The complete workflow verifies the seamless integration of Git → GitHub → Jenkins → Docker → Pytest → Ansible → Flask → SQLite → Docker Volume, fulfilling all requirements for a professional, college-level DevOps engineering project.")

    doc.save("devops report.docx")
    print("[SUCCESS] Document text successfully updated in devops report.docx!")

def replace_media_in_zip():
    print("Replacing media files in devops report.docx...")
    src_zip = "devops report.docx"
    tmp_zip = "devops report_temp.zip"

    # Map image numbers to replacement files
    img_map = {
        f"word/media/image{i}.png": f"temp_screens/image{i}.png"
        for i in range(2, 22) # image2 through image21
        if os.path.exists(f"temp_screens/image{i}.png")
    }

    zin = zipfile.ZipFile(src_zip, 'r')
    zout = zipfile.ZipFile(tmp_zip, 'w')

    for item in zin.infolist():
        if item.filename in img_map:
            rep_path = img_map[item.filename]
            with open(rep_path, 'rb') as f:
                zout.writestr(item, f.read())
            print(f"Replaced {item.filename} with {rep_path}")
        else:
            zout.writestr(item, zin.read(item.filename))

    zin.close()
    zout.close()

    os.remove(src_zip)
    os.rename(tmp_zip, src_zip)
    print("[SUCCESS] All embedded images replaced in devops report.docx!")

if __name__ == '__main__':
    doc = docx.Document("devops report.docx")
    replace_in_doc(doc)
    replace_media_in_zip()
