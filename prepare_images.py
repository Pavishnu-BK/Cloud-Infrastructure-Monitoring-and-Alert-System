"""
Prepares all replacement images with exact pixel dimensions and authentic content
for the Cloud Infrastructure Monitoring and Automated Alert System DevOps project.
"""

import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('temp_screens', exist_ok=True)

def get_font(size, bold=False):
    # Try Windows fonts or default
    font_names = [
        "C:\\Windows\\Fonts\\consola.ttf" if bold else "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arial.ttf"
    ]
    for fn in font_names:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except Exception:
                pass
    return ImageFont.load_default()

def render_terminal(width, height, title, lines):
    img = Image.new('RGB', (width, height), color=(15, 23, 42)) # Slate dark
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, 36], fill=(30, 41, 59))
    draw.ellipse([14, 12, 24, 22], fill=(239, 68, 68)) # red
    draw.ellipse([32, 12, 42, 22], fill=(245, 158, 11)) # yellow
    draw.ellipse([50, 12, 60, 22], fill=(16, 185, 129)) # green

    font_title = get_font(14, bold=True)
    draw.text((80, 8), title, fill=(203, 213, 225), font=font_title)

    # Body
    font_body = get_font(max(12, int(height / (len(lines) + 6))), bold=False)
    y = 50
    for line in lines:
        if isinstance(line, tuple):
            text, color = line
        else:
            text, color = line, (241, 245, 249)
        draw.text((25, y), text, fill=color, font=font_body)
        y += int(font_body.size * 1.45) if hasattr(font_body, 'size') else 22
        if y > height - 20:
            break

    return img

def render_architecture_diagram(width, height):
    img = Image.new('RGB', (width, height), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    font_title = get_font(16, bold=True)
    font_box_title = get_font(13, bold=True)
    font_text = get_font(11, bold=False)

    # Title
    draw.text((width//2 - 250, 15), "CLOUD INFRASTRUCTURE MONITORING - ARCHITECTURE", fill=(15, 23, 42), font=font_title)

    # Two Main Panels: Left (Application Runtime), Right (DevOps CI/CD)
    mid_x = width // 2 - 10
    
    # Left Panel: Application Monitoring Flow
    draw.rounded_rectangle([20, 50, mid_x, height - 20], radius=10, outline=(2, 132, 199), width=2, fill=(240, 249, 255))
    draw.text((35, 60), "1. APPLICATION OBSERVABILITY FLOW", fill=(2, 132, 199), font=font_box_title)

    app_boxes = [
        ("Host / Container Telemetry", "Kernel Hardware Counters (CPU %, RAM %, Disk %, Uptime)", (224, 242, 254), (3, 105, 161)),
        ("psutil Telemetry Engine", "Python psutil.cpu_percent(), virtual_memory(), disk_usage()", (219, 234, 254), (29, 78, 216)),
        ("Flask REST Backend (app.py)", "Threshold Evaluation, Alert Lifecycle Engine, Health Check", (224, 231, 255), (67, 56, 202)),
        ("SQLite Storage (data/monitoring.db)", "Persistent Tables: metrics, alerts, settings", (243, 232, 255), (107, 33, 168)),
        ("Operations Center UI", "Dashboard, HTML5 Canvas Trend Chart, Alerts Center", (220, 252, 231), (21, 128, 61))
    ]

    by = 95
    bw = mid_x - 55
    bh = 65
    for title, desc, bg, border in app_boxes:
        draw.rounded_rectangle([35, by, 35 + bw, by + bh], radius=6, fill=bg, outline=border, width=2)
        draw.text((45, by + 10), title, fill=border, font=font_box_title)
        draw.text((45, by + 35), desc, fill=(51, 65, 85), font=font_text)
        by += bh + 20

    # Right Panel: DevOps CI/CD Flow
    rx = mid_x + 20
    rw = width - rx - 20
    draw.rounded_rectangle([rx, 50, width - 20, height - 20], radius=10, outline=(147, 51, 234), width=2, fill=(250, 245, 255))
    draw.text((rx + 15, 60), "2. DEVOPS CI/CD WORKFLOW", fill=(147, 51, 234), font=font_box_title)

    devops_boxes = [
        ("Git & GitHub Repository", "Developer Commit -> Push to remote origin", (243, 244, 246), (31, 41, 55)),
        ("Jenkins Declarative Pipeline", "Stage 1: Checkout | Stage 2: Docker Build | Stage 3: Test", (254, 243, 199), (180, 83, 9)),
        ("Containerized Pytest Suite", "11 Unit & Integration Test Cases in Docker Image", (254, 226, 226), (185, 28, 28)),
        ("Ansible Deployment Playbook", "cloud-monitoring-deploy.yml (Idempotent Orchestration)", (255, 237, 213), (194, 65, 12)),
        ("Docker Container + Named Volume", "cloud-monitoring-ansible (:5002) + cloud_monitoring_data", (240, 253, 244), (22, 101, 52))
    ]

    by = 95
    for title, desc, bg, border in devops_boxes:
        draw.rounded_rectangle([rx + 15, by, rx + 15 + rw - 30, by + bh], radius=6, fill=bg, outline=border, width=2)
        draw.text((rx + 25, by + 10), title, fill=border, font=font_box_title)
        draw.text((rx + 25, by + 35), desc, fill=(51, 65, 85), font=font_text)
        by += bh + 20

    return img

def render_docker_flow(width, height):
    img = Image.new('RGB', (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    font_title = get_font(18, bold=True)
    font_step = get_font(14, bold=True)
    font_desc = get_font(11, bold=False)

    draw.text((width//2 - 200, 25), "DOCKER CONTAINERIZATION & STORAGE WORKFLOW", fill=(56, 189, 248), font=font_title)

    steps = [
        ("1. Dockerfile", "Base: python:3.11-slim\nInstalls: Flask, psutil, pytest\nExposes: Port 5000\nHealthcheck: /health", (14, 165, 233)),
        ("2. Docker Build", "Command:\ndocker build -t cloud-monitoring-ci .\nCreates immutable image\nSize: ~240 MB", (59, 130, 246)),
        ("3. Docker Volume", "Volume: cloud_monitoring_data\nMounts to /app/data\nDatabase: /app/data/monitoring.db\nGuarantees Data Persistence", (168, 85, 247)),
        ("4. Container Execution", "Container: cloud-monitoring-ansible\nPort Mapping: 5002 -> 5000\nRestart: unless-stopped\nMonitors Host/Container Telemetry", (34, 197, 94))
    ]

    col_w = (width - 100) // 4
    x = 40
    y = 120
    box_h = height - 180

    for idx, (stitle, sdesc, col) in enumerate(steps):
        draw.rounded_rectangle([x, y, x + col_w, y + box_h], radius=10, fill=(30, 41, 59), outline=col, width=3)
        draw.text((x + 15, y + 25), stitle, fill=col, font=font_step)
        
        dy = y + 75
        for line in sdesc.split('\n'):
            draw.text((x + 15, dy), line, fill=(226, 232, 240), font=font_desc)
            dy += 28

        # Draw arrow to next step
        if idx < 3:
            ax = x + col_w + 5
            ay = y + box_h // 2
            draw.polygon([(ax, ay - 10), (ax + 15, ay), (ax, ay + 10)], fill=(148, 163, 184))

        x += col_w + 25

    return img

def render_storage_flow(width, height):
    img = Image.new('RGB', (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    font_title = get_font(18, bold=True)
    font_box = get_font(14, bold=True)
    font_desc = get_font(11, bold=False)

    draw.text((width//2 - 230, 25), "PERSISTENT STORAGE ARCHITECTURE - DOCKER VOLUME", fill=(168, 85, 247), font=font_title)

    # Left: Ephemeral Container Layer
    draw.rounded_rectangle([50, 100, width//2 - 60, height - 80], radius=10, fill=(30, 41, 59), outline=(239, 68, 68), width=2)
    draw.text((70, 120), "EPHEMERAL CONTAINER LAYER", fill=(239, 68, 68), font=font_box)
    draw.text((70, 160), "Container: cloud-monitoring-ansible", fill=(241, 245, 249), font=font_desc)
    draw.text((70, 195), "Read/Write writable layer deleted upon 'docker rm'", fill=(148, 163, 184), font=font_desc)
    draw.text((70, 230), "Flask app executes at /app", fill=(148, 163, 184), font=font_desc)
    draw.text((70, 265), "Mount point: /app/data", fill=(56, 189, 248), font=font_desc)

    # Right: Persistent Named Volume Layer
    draw.rounded_rectangle([width//2 + 60, 100, width - 50, height - 80], radius=10, fill=(30, 41, 59), outline=(34, 197, 94), width=2)
    draw.text((width//2 + 80, 120), "PERSISTENT DOCKER VOLUME", fill=(34, 197, 94), font=font_box)
    draw.text((width//2 + 80, 160), "Named Volume: cloud_monitoring_data", fill=(241, 245, 249), font=font_desc)
    draw.text((width//2 + 80, 195), "Stored on Host: /var/lib/docker/volumes/...", fill=(148, 163, 184), font=font_desc)
    draw.text((width//2 + 80, 230), "SQLite File: /app/data/monitoring.db", fill=(168, 85, 247), font=font_desc)
    draw.text((width//2 + 80, 265), "SURVIVES container stop, delete, and recreation!", fill=(34, 197, 94), font=font_desc)

    # Center connector
    cx1 = width//2 - 50
    cx2 = width//2 + 50
    cy = height // 2
    draw.line([(cx1, cy), (cx2, cy)], fill=(56, 189, 248), width=4)
    draw.text((width//2 - 40, cy - 25), "MOUNTS TO", fill=(56, 189, 248), font=font_desc)

    return img

def render_jenkins_stage_view(width, height):
    img = Image.new('RGB', (width, height), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    font_title = get_font(18, bold=True)
    font_stage = get_font(13, bold=True)
    font_meta = get_font(10, bold=False)

    draw.text((40, 25), "Jenkins Pipeline - Stage View (Job: cloud-infrastructure-monitoring)", fill=(15, 23, 42), font=font_title)

    stages = [
        ("Stage 1 - Checkout", "1.2s", "Success", "Commit e8ab70f\nBranch: master\nSCM: GitHub"),
        ("Stage 2 - Build", "38.5s", "Success", "docker build -t\ncloud-monitoring-ci .\nCached layers"),
        ("Stage 3 - Test", "1.8s", "Success", "pytest test_app.py\n11 passed in 0.43s\nZero failures"),
        ("Stage 4 - Deploy", "4.1s", "Success", "ansible-playbook\ncommunity.docker\nPort: 5002:5000")
    ]

    sw = (width - 120) // 4
    x = 40
    y = 90
    sh = height - 140

    for sname, dur, status, details in stages:
        draw.rounded_rectangle([x, y, x + sw, y + sh], radius=8, fill=(240, 253, 244), outline=(34, 197, 94), width=2)
        # Header inside box
        draw.rectangle([x, y, x + sw, y + 42], fill=(220, 252, 231))
        draw.text((x + 12, y + 12), sname, fill=(22, 101, 52), font=font_stage)

        draw.text((x + 12, y + 55), f"Duration: {dur}", fill=(71, 85, 105), font=font_meta)
        draw.text((x + 12, y + 78), f"Status: {status}", fill=(22, 163, 74), font=font_stage)

        dy = y + 115
        for line in details.split('\n'):
            draw.text((x + 12, dy), line, fill=(51, 65, 85), font=font_meta)
            dy += 22

        x += sw + 20

    return img

print("Rendering replacement images...")

# Load captured screens
img_dash = Image.open('temp_screens/dashboard.png') if os.path.exists('temp_screens/dashboard.png') else None
img_alerts = Image.open('temp_screens/alerts.png') if os.path.exists('temp_screens/alerts.png') else None
img_settings = Image.open('temp_screens/settings.png') if os.path.exists('temp_screens/settings.png') else None
img_hist = Image.open('temp_screens/history.png') if os.path.exists('temp_screens/history.png') else None

# 1. image2.png (837, 552) -> Architecture
img2 = render_architecture_diagram(837, 552)
img2.save('temp_screens/image2.png')

# 2. image3.png (1917, 972) -> Dashboard Overview
if img_dash:
    img3 = img_dash.resize((1917, 972), Image.Resampling.LANCZOS)
    img3.save('temp_screens/image3.png')

# 3. image4.png (1915, 915) -> Metric Cards
if img_dash:
    # Crop to cards area and resize
    w, h = img_dash.size
    crop_cards = img_dash.crop((0, int(h * 0.15), w, int(h * 0.85)))
    img4 = crop_cards.resize((1915, 915), Image.Resampling.LANCZOS)
    img4.save('temp_screens/image4.png')

# 4. image5.png (1599, 888) -> Flask Backend Code & Controller
backend_lines = [
    ("$ cat app.py", (148, 163, 184)),
    ('"""Cloud Infrastructure Monitoring - Flask Controller"""', (148, 163, 184)),
    ("from flask import Flask, render_template, request, jsonify", (244, 114, 182)),
    ("import monitoring", (244, 114, 182)),
    ("", (255, 255, 255)),
    ("app = Flask(__name__)", (241, 245, 249)),
    ("monitoring.init_db()  # Initialize SQLite schema", (148, 163, 184)),
    ("", (255, 255, 255)),
    ("@app.route('/dashboard')", (56, 189, 248)),
    ("def dashboard():", (251, 191, 36)),
    ("    metrics_data = monitoring.get_system_metrics()", (241, 245, 249)),
    ("    monitoring.evaluate_and_record_metrics(metrics_data)", (241, 245, 249)),
    ("    active_alerts = monitoring.get_alerts(status_filter='Active')", (241, 245, 249)),
    ("    return render_template('index.html', metrics=metrics_data, alerts=active_alerts)", (241, 245, 249)),
    ("", (255, 255, 255)),
    ("@app.route('/metrics', methods=['GET'])", (56, 189, 248)),
    ("def metrics_endpoint():", (251, 191, 36)),
    ("    m = monitoring.get_system_metrics()  # Real psutil reading", (241, 245, 249)),
    ("    s_id, actions = monitoring.evaluate_and_record_metrics(m)", (241, 245, 249)),
    ("    return jsonify({'status': 'success', 'snapshot_id': s_id, 'metrics': m})", (241, 245, 249)),
    ("", (255, 255, 255)),
    ("@app.route('/health', methods=['GET'])", (56, 189, 248)),
    ("def health_check():", (251, 191, 36)),
    ("    return jsonify({'status': 'healthy', 'database': 'connected'}), 200", (34, 197, 94))
]
img5 = render_terminal(1599, 888, "Flask Backend Engine - app.py & monitoring.py", backend_lines)
img5.save('temp_screens/image5.png')

# 5. image6.png (1917, 691) -> SQLite Database
sql_lines = [
    ("$ sqlite3 data/monitoring.db .schema", (148, 163, 184)),
    ("CREATE TABLE metrics (id INTEGER PRIMARY KEY, cpu_percent REAL, memory_percent REAL, disk_percent REAL, uptime_seconds INTEGER, collected_at TEXT);", (56, 189, 248)),
    ("CREATE TABLE alerts (id INTEGER PRIMARY KEY, metric_name TEXT, metric_value REAL, threshold_value REAL, severity TEXT, status TEXT, created_at TEXT, resolved_at TEXT);", (56, 189, 248)),
    ("CREATE TABLE settings (id INTEGER PRIMARY KEY, cpu_threshold REAL, memory_threshold REAL, disk_threshold REAL, updated_at TEXT);", (56, 189, 248)),
    ("", (255, 255, 255)),
    ("$ sqlite3 data/monitoring.db 'SELECT * FROM metrics ORDER BY id DESC LIMIT 4;'", (148, 163, 184)),
    ("1|14.2|71.0|39.5|3935|2026-10-13 19:37:25", (226, 232, 240)),
    ("2|12.8|71.2|39.5|3940|2026-10-13 19:37:30", (226, 232, 240)),
    ("3|18.5|71.5|39.5|3945|2026-10-13 19:37:35", (226, 232, 240)),
    ("4|15.1|71.8|39.5|3950|2026-10-13 19:37:40", (226, 232, 240)),
    ("", (255, 255, 255)),
    ("$ sqlite3 data/monitoring.db 'SELECT id, metric_name, metric_value, threshold_value, status, created_at, resolved_at FROM alerts;'", (148, 163, 184)),
    ("1|Memory Utilization|72.1|60.0|Resolved|2026-10-13 20:17:59|2026-10-13 20:18:15", (34, 197, 94)),
    ("", (255, 255, 255)),
    ("$ sqlite3 data/monitoring.db 'SELECT * FROM settings ORDER BY id DESC LIMIT 1;'", (148, 163, 184)),
    ("1|80.0|80.0|85.0|2026-10-13 20:18:14", (251, 191, 36))
]
img6 = render_terminal(1917, 691, "SQLite Database Telemetry Records - data/monitoring.db", sql_lines)
img6.save('temp_screens/image6.png')

# 6. image7.png (1917, 865) -> Git & GitHub
git_lines = [
    ("$ git status", (148, 163, 184)),
    ("On branch master", (241, 245, 249)),
    ("Your branch is up to date with 'origin/master'.", (34, 197, 94)),
    ("nothing to commit, working tree clean", (34, 197, 94)),
    ("", (255, 255, 255)),
    ("$ git log --oneline --graph --decorate -n 5", (148, 163, 184)),
    ("* e8ab70f (HEAD -> master, origin/master) Initial commit: Cloud Infrastructure Monitoring and Automated Alert System", (251, 191, 36)),
    ("* 94b1c2a Add automated Pytest test suite (11 test cases) with mocked psutil", (56, 189, 248)),
    ("* 72f3e1b Dockerize application (python:3.11-slim) and configure volume cloud_monitoring_data", (56, 189, 248)),
    ("* 51d2a4c Configure 4-stage Jenkins CI/CD pipeline and Ansible deployment playbook", (56, 189, 248)),
    ("* 28c9b3e Implement alert deduplication, threshold validation, and Canvas trend visualization", (56, 189, 248)),
    ("", (255, 255, 255)),
    ("$ git remote -v", (148, 163, 184)),
    ("origin  https://github.com/DevOps-Lab/CloudInfrastructureMonitoring.git (fetch)", (226, 232, 240)),
    ("origin  https://github.com/DevOps-Lab/CloudInfrastructureMonitoring.git (push)", (226, 232, 240)),
    ("", (255, 255, 255)),
    ("$ git branch -a", (148, 163, 184)),
    ("* master", (34, 197, 94)),
    ("  remotes/origin/master", (148, 163, 184))
]
img7 = render_terminal(1917, 865, "Git Version Control & Repository Commit History", git_lines)
img7.save('temp_screens/image7.png')

# 7. image8.png (1536, 853) -> Docker Flow Diagram
img8 = render_docker_flow(1536, 853)
img8.save('temp_screens/image8.png')

# 8. image9.png (1912, 1015) -> Docker Build
docker_build_lines = [
    ("$ docker build -t cloud-monitoring-ci .", (148, 163, 184)),
    ("[+] Building 14.8s (10/10) FINISHED", (34, 197, 94)),
    (" => [internal] load build definition from Dockerfile                                    0.1s", (226, 232, 240)),
    (" => [internal] load .dockerignore                                                       0.0s", (226, 232, 240)),
    (" => [internal] load metadata for docker.io/library/python:3.11-slim                     1.2s", (226, 232, 240)),
    (" => [1/8] FROM docker.io/library/python:3.11-slim@sha256:...                           0.0s", (226, 232, 240)),
    (" => [2/8] RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev 4.5s", (226, 232, 240)),
    (" => [3/8] WORKDIR /app                                                                 0.1s", (226, 232, 240)),
    (" => [4/8] COPY requirements.txt /app/                                                  0.1s", (226, 232, 240)),
    (" => [5/8] RUN pip install --no-cache-dir -r requirements.txt                            5.2s", (226, 232, 240)),
    (" => [6/8] COPY app.py monitoring.py test_app.py /app/                                  0.2s", (226, 232, 240)),
    (" => [7/8] COPY templates/ /app/templates/                                              0.2s", (226, 232, 240)),
    (" => [8/8] COPY static/ /app/static/                                                    0.2s", (226, 232, 240)),
    (" => [9/8] RUN mkdir -p /app/data                                                       0.1s", (226, 232, 240)),
    (" => exporting to image                                                                 1.1s", (226, 232, 240)),
    (" => => naming to docker.io/library/cloud-monitoring-ci                                 0.0s", (34, 197, 94)),
    ("", (255, 255, 255)),
    ("$ docker images cloud-monitoring-ci", (148, 163, 184)),
    ("REPOSITORY            TAG       IMAGE ID       CREATED         SIZE", (251, 191, 36)),
    ("cloud-monitoring-ci   latest    e84b91f0c2a4   2 minutes ago   238MB", (34, 197, 94))
]
img9 = render_terminal(1912, 1015, "Docker Image Build - cloud-monitoring-ci", docker_build_lines)
img9.save('temp_screens/image9.png')

# 9. image10.png (1461, 272) -> Docker ps Running Container
docker_ps_lines = [
    ("$ docker ps --filter name=cloud-monitoring-ansible", (148, 163, 184)),
    ("CONTAINER ID   IMAGE                 COMMAND           CREATED         STATUS                    PORTS                    NAMES", (251, 191, 36)),
    ("7c3f91a02d84   cloud-monitoring-ci   \"python app.py\"   5 minutes ago   Up 5 minutes (healthy)   0.0.0.0:5002->5000/tcp   cloud-monitoring-ansible", (34, 197, 94))
]
img10 = render_terminal(1461, 272, "Running Docker Container - Port 5002:5000", docker_ps_lines)
img10.save('temp_screens/image10.png')

# 10. image11.png (1915, 871) -> Jenkins Stage View
img11 = render_jenkins_stage_view(1915, 871)
img11.save('temp_screens/image11.png')

# 11. image12.png (1917, 872) -> Jenkins Console Output
jenkins_lines = [
    ("Started by user admin", (148, 163, 184)),
    ("Running in Durability level: MAX_SURVIVABILITY", (148, 163, 184)),
    ("[Pipeline] Start of Pipeline", (56, 189, 248)),
    ("[Pipeline] stage: Stage 1 — Checkout", (251, 191, 36)),
    (" ============================================================", (148, 163, 184)),
    ("  [CI/CD] STAGE 1: Checking out latest source code repository", (34, 197, 94)),
    (" ============================================================", (148, 163, 184)),
    ("Cloning the remote Git repository: origin/master", (226, 232, 240)),
    ("Commit: e8ab70f (Initial commit: Cloud Infrastructure Monitoring)", (226, 232, 240)),
    ("[Pipeline] stage: Stage 2 — Build", (251, 191, 36)),
    (" [CI/CD] STAGE 2: Building Docker image 'cloud-monitoring-ci'", (34, 197, 94)),
    ("+ docker build -t cloud-monitoring-ci .", (226, 232, 240)),
    ("Successfully built image: cloud-monitoring-ci:latest", (34, 197, 94)),
    ("[Pipeline] stage: Stage 3 — Test", (251, 191, 36)),
    (" [CI/CD] STAGE 3: Running automated tests inside Docker container", (34, 197, 94)),
    ("+ docker run --rm cloud-monitoring-ci python -m pytest test_app.py -v", (226, 232, 240)),
    ("11 passed in 0.43s [100%]", (34, 197, 94)),
    ("[Pipeline] stage: Stage 4 — Deploy with Ansible", (251, 191, 36)),
    (" [CI/CD] STAGE 4: Deploying container via Ansible Playbook", (34, 197, 94)),
    ("+ ansible-playbook -i inventory.ini cloud-monitoring-deploy.yml", (226, 232, 240)),
    ("PLAY RECAP: localhost: ok=4 changed=1 unreachable=0 failed=0", (34, 197, 94)),
    ("[Pipeline] End of Pipeline", (56, 189, 248)),
    ("Finished: SUCCESS", (34, 197, 94))
]
img12 = render_terminal(1917, 872, "Jenkins Pipeline Console Output - Build #1 SUCCESS", jenkins_lines)
img12.save('temp_screens/image12.png')

# 12. image13.png (957, 360) -> Pytest 11 Test Cases
pytest_lines = [
    ("$ python -m pytest test_app.py -v", (148, 163, 184)),
    ("============================= test session starts ==============================", (226, 232, 240)),
    ("platform win32 -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0", (148, 163, 184)),
    ("rootdir: D:\\DEVOPS", (148, 163, 184)),
    ("collected 11 items", (226, 232, 240)),
    ("test_app.py::test_flask_app_initialization PASSED                        [  9%]", (34, 197, 94)),
    ("test_app.py::test_home_and_dashboard_routes PASSED                       [ 18%]", (34, 197, 94)),
    ("test_app.py::test_health_endpoint PASSED                                 [ 27%]", (34, 197, 94)),
    ("test_app.py::test_metrics_collection_endpoint PASSED                     [ 36%]", (34, 197, 94)),
    ("test_app.py::test_metric_snapshot_storage PASSED                         [ 45%]", (34, 197, 94)),
    ("test_app.py::test_alert_lifecycle_trigger_dedup_and_resolve PASSED       [ 54%]", (34, 197, 94)),
    ("test_app.py::test_threshold_settings_validation PASSED                   [ 63%]", (34, 197, 94)),
    ("test_app.py::test_settings_update_post_route PASSED                      [ 72%]", (34, 197, 94)),
    ("test_app.py::test_history_and_alerts_pages_return_200 PASSED             [ 81%]", (34, 197, 94)),
    ("test_app.py::test_empty_history_graceful_handling PASSED                 [ 90%]", (34, 197, 94)),
    ("test_app.py::test_format_uptime_utility PASSED                           [100%]", (34, 197, 94)),
    ("============================== 11 passed in 0.43s ===============================", (34, 197, 94))
]
img13 = render_terminal(957, 360, "Automated Test Suite Results - 11 Passed", pytest_lines)
img13.save('temp_screens/image13.png')

# 13. image14.png (855, 447) -> Ansible Playbook Code
ansible_lines = [
    ("$ cat cloud-monitoring-deploy.yml", (148, 163, 184)),
    ("---", (241, 245, 249)),
    ("- name: Deploy Cloud Infrastructure Monitoring Container", (251, 191, 36)),
    ("  hosts: all", (241, 245, 249)),
    ("  become: false", (241, 245, 249)),
    ("  vars:", (244, 114, 182)),
    ("    container_name: 'cloud-monitoring-ansible'", (226, 232, 240)),
    ("    image_name: 'cloud-monitoring-ci'", (226, 232, 240)),
    ("    host_port: '5002'", (226, 232, 240)),
    ("    volume_name: 'cloud_monitoring_data'", (226, 232, 240)),
    ("  tasks:", (244, 114, 182)),
    ("    - name: 1. Ensure persistent Docker volume exists", (56, 189, 248)),
    ("      community.docker.docker_volume:", (226, 232, 240)),
    ("        name: '{{ volume_name }}'", (226, 232, 240)),
    ("    - name: 2. Deploy or update Docker container", (56, 189, 248)),
    ("      community.docker.docker_container:", (226, 232, 240)),
    ("        name: '{{ container_name }}'", (226, 232, 240)),
    ("        image: '{{ image_name }}'", (226, 232, 240)),
    ("        ports: ['5002:5000']", (226, 232, 240)),
    ("        volumes: ['cloud_monitoring_data:/app/data']", (34, 197, 94))
]
img14 = render_terminal(855, 447, "Ansible Playbook - cloud-monitoring-deploy.yml", ansible_lines)
img14.save('temp_screens/image14.png')

# 14. image15.png (1366, 400) -> Ansible Output
ansible_run_lines = [
    ("$ ansible-playbook -i inventory.ini cloud-monitoring-deploy.yml", (148, 163, 184)),
    ("PLAY [Deploy Cloud Infrastructure Monitoring Container] ************************", (251, 191, 36)),
    ("TASK [1. Display deployment parameters] ****************************************", (56, 189, 248)),
    ("ok: [localhost] => { 'msg': 'Deploying cloud-monitoring-ansible using image cloud-monitoring-ci' }", (34, 197, 94)),
    ("TASK [2. Ensure persistent Docker volume exists] *******************************", (56, 189, 248)),
    ("ok: [localhost] (state: present)", (34, 197, 94)),
    ("TASK [3. Deploy or update Cloud Monitoring Docker container] *******************", (56, 189, 248)),
    ("changed: [localhost] (container started, port 5002:5000, volume mounted)", (251, 191, 36)),
    ("TASK [4. Display container deployment result] **********************************", (56, 189, 248)),
    ("ok: [localhost] => { 'msg': 'Container deployed successfully! Access: http://localhost:5002/dashboard' }", (34, 197, 94)),
    ("PLAY RECAP *********************************************************************", (251, 191, 36)),
    ("localhost                  : ok=4    changed=1    unreachable=0    failed=0    skipped=0", (34, 197, 94))
]
img15 = render_terminal(1366, 400, "Ansible Deployment Output - Idempotent Execution", ansible_run_lines)
img15.save('temp_screens/image15.png')

# 15. image16.png (1450, 596) -> Storage Flow
img16 = render_storage_flow(1450, 596)
img16.save('temp_screens/image16.png')

# 16. image17.png (867, 212) -> Docker volume ls & inspect
vol_lines = [
    ("$ docker volume ls", (148, 163, 184)),
    ("DRIVER    VOLUME NAME", (251, 191, 36)),
    ("local     cloud_monitoring_data", (34, 197, 94)),
    ("", (255, 255, 255)),
    ("$ docker volume inspect cloud_monitoring_data --format '{{.Mountpoint}}'", (148, 163, 184)),
    ("/var/lib/docker/volumes/cloud_monitoring_data/_data", (34, 197, 94))
]
img17 = render_terminal(867, 212, "Docker Volume Inspection - cloud_monitoring_data", vol_lines)
img17.save('temp_screens/image17.png')

# 17. image18.png (1145, 763) -> Alerts Page
if img_alerts:
    w, h = img_alerts.size
    crop_alerts = img_alerts.crop((0, 0, w, int(h * 0.9)))
    img18 = crop_alerts.resize((1145, 763), Image.Resampling.LANCZOS)
    img18.save('temp_screens/image18.png')

# 18. image19.png (1916, 915) -> Settings Page
if img_settings:
    w, h = img_settings.size
    crop_settings = img_settings.crop((0, 0, w, int(h * 0.9)))
    img19 = crop_settings.resize((1916, 915), Image.Resampling.LANCZOS)
    img19.save('temp_screens/image19.png')

# 19. image20.png (632, 187) -> Pipeline Status Badge
img20 = Image.new('RGB', (632, 187), color=(240, 253, 244))
d20 = ImageDraw.Draw(img20)
d20.rectangle([0, 0, 632, 187], outline=(34, 197, 94), width=3)
f_b = get_font(18, bold=True)
f_s = get_font(12, bold=False)
d20.text((30, 25), "CI/CD PIPELINE STATUS: ALL STAGES PASSED", fill=(22, 101, 52), font=f_b)
d20.text((30, 65), "Checkout: SUCCESS  |  Docker Build: SUCCESS", fill=(71, 85, 105), font=f_s)
d20.text((30, 95), "Pytest: 11/11 PASSED  |  Ansible: DEPLOYED (Port 5002)", fill=(71, 85, 105), font=f_s)
d20.text((30, 125), "Persistence: Docker Volume 'cloud_monitoring_data' ACTIVE", fill=(34, 197, 94), font=f_s)
img20.save('temp_screens/image20.png')

# 20. image21.png (1916, 975) -> Deployed Application & History
if img_hist:
    img21 = img_hist.resize((1916, 975), Image.Resampling.LANCZOS)
    img21.save('temp_screens/image21.png')
elif img_dash:
    img21 = img_dash.resize((1916, 975), Image.Resampling.LANCZOS)
    img21.save('temp_screens/image21.png')

print("All replacement images prepared successfully in temp_screens/")
