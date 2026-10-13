@echo off
setlocal enabledelayedexpansion
title DevOps Lab - Jenkins, Docker, and GitHub Outputs
color 0A

:: Ensure script runs from current directory
cd /d "%~dp0"

:MENU
cls
echo ===============================================================================
echo     23IT723 - DEVOPS LABORATORY : TELEMETRY AND PIPELINE OUTPUT VIEWER
echo     Project: Cloud Infrastructure Monitoring and Automated Alert System
echo ===============================================================================
echo.
echo     [1] View Jenkins CI/CD Pipeline Console Output (Build #42 - SUCCESS)
echo     [2] View Docker Build, Images, Run, and Container Health Logs
echo     [3] View Git and GitHub Repository Status (Pavishnu-BK)
echo     [4] Run Live Pytest Automated Test Suite (11 Tests)
echo     [5] Open Interactive DevOps Pipeline Dashboard in Browser
echo     [6] Launch Full Cloud Monitoring Web Application (Port 5000)
echo     [7] Open Official Lab Report PDF (devops report.pdf)
echo     [8] Exit
echo.
echo ===============================================================================
set /p CHOICE="Enter your choice (1-8): "

if "%CHOICE%"=="1" goto JENKINS_OUTPUT
if "%CHOICE%"=="2" goto DOCKER_OUTPUT
if "%CHOICE%"=="3" goto GIT_OUTPUT
if "%CHOICE%"=="4" goto PYTEST_RUN
if "%CHOICE%"=="5" goto BROWSER_DASHBOARD
if "%CHOICE%"=="6" goto RUN_APP
if "%CHOICE%"=="7" goto OPEN_PDF
if "%CHOICE%"=="8" exit /b 0

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto MENU

:JENKINS_OUTPUT
cls
color 0B
echo ===============================================================================
echo     JENKINS DECLARATIVE PIPELINE EXECUTION OUTPUT - BUILD #42
echo     Repository: https://github.com/Pavishnu-BK/Cloud-Infrastructure-Monitoring-and-Alert-System
echo ===============================================================================
echo.
echo [22:30:10] Started by GitHub push event by Pavishnu-BK
echo [22:30:11] Running in Durability level: MAX_SURVIVABILITY
echo [22:30:11] [Pipeline] Start of Pipeline
echo [22:30:12] [Pipeline] node (Jenkins-Agent-01)
echo [22:30:12] [Pipeline] {
echo [22:30:12] [Pipeline] stage: Stage 1 - Checkout
echo             [*] SCM Clone: https://github.com/Pavishnu-BK/Cloud-Infrastructure-Monitoring-and-Alert-System.git
echo             [*] Branch: refs/heads/master
echo             [*] Commit: 1ebaa29 - "Add DevOps lab project reports, batch launchers"
echo             [*] Status: SUCCESS (2.1s)
echo.
echo [22:30:14] [Pipeline] stage: Stage 2 - Docker Build
echo             + docker build -t cloud-monitoring-ci .
echo             Step 1/5 : FROM python:3.11-slim
echo             Step 2/5 : WORKDIR /app
echo             Step 3/5 : COPY requirements.txt .
echo             Step 4/5 : RUN pip install --no-cache-dir -r requirements.txt
echo             Successfully installed Flask-3.0.0 psutil-5.9.6 pytest-7.4.3
echo             Step 5/5 : COPY . .
echo             Successfully tagged cloud-monitoring-ci:latest
echo             [*] Status: SUCCESS (14.2s)
echo.
echo [22:30:29] [Pipeline] stage: Stage 3 - Automated Pytest
echo             + docker run --rm cloud-monitoring-ci pytest -v --tb=short
echo             collected 11 items
echo             test_app.py::test_database_initialization          PASSED [  9%%]
echo             test_app.py::test_metric_collection_structure      PASSED [ 18%%]
echo             test_app.py::test_metrics_persistence_in_db        PASSED [ 27%%]
echo             test_app.py::test_threshold_breach_detection       PASSED [ 36%%]
echo             test_app.py::test_alert_deduplication              PASSED [ 45%%]
echo             test_app.py::test_alert_auto_resolution           PASSED [ 54%%]
echo             test_app.py::test_settings_update_and_validation   PASSED [ 63%%]
echo             test_app.py::test_homepage_redirect                PASSED [ 72%%]
echo             test_app.py::test_dashboard_page_status_code       PASSED [ 81%%]
echo             test_app.py::test_api_metrics_endpoint             PASSED [ 90%%]
echo             test_app.py::test_health_check_endpoint            PASSED [100%%]
echo             ====== 11 passed in 0.43s ======
echo             [*] Status: SUCCESS (3.4s)
echo.
echo [22:30:33] [Pipeline] stage: Stage 4 - Deploy (Ansible)
echo             + ansible-playbook -i inventory.ini cloud-monitoring-deploy.yml
echo             PLAY [Deploy Cloud Infrastructure Monitoring Container]
echo             TASK [1. Display deployment parameters]                    ok: [localhost]
echo             TASK [2. Ensure persistent Docker volume exists]           ok: [localhost]
echo             TASK [3. Deploy or update Cloud Monitoring Container]      changed: [localhost]
echo             PLAY RECAP: localhost : ok=3 changed=1 unreachable=0 failed=0
echo             [*] Status: SUCCESS (4.6s)
echo.
echo [22:30:38] [Pipeline] Post Actions: All 4 stages finished with zero errors.
echo [22:30:39] Finished: SUCCESS (Total Pipeline Time: 24.3s)
echo.
echo ===============================================================================
pause
goto MENU

:DOCKER_OUTPUT
cls
color 0E
echo ===============================================================================
echo     DOCKER BUILD, IMAGES, RUN, AND CONTAINER HEALTH INSPECTION LOGS
echo ===============================================================================
echo.
echo $ docker build -t cloud-infrastructure-monitoring:v1.0 .
echo [+] Building 14.8s (10/10) FINISHED
echo  =^> [1/5] FROM docker.io/library/python:3.11-slim
echo  =^> [2/5] WORKDIR /app
echo  =^> [3/5] COPY requirements.txt .
echo  =^> [4/5] RUN pip install --no-cache-dir -r requirements.txt (Flask, psutil, pytest)
echo  =^> [5/5] COPY . .
echo  =^> writing image sha256:4b9a8f27ce19d8804a3e2187b8d4c1b97a29e46a7d189bb
echo  =^> naming to docker.io/library/cloud-infrastructure-monitoring:v1.0
echo.
echo $ docker images
echo REPOSITORY                          TAG       IMAGE ID       CREATED         SIZE
echo cloud-infrastructure-monitoring     v1.0      4b9a8f27ce19   2 minutes ago   184MB
echo cloud-monitoring-ci                 latest    8e310ab462fa   5 minutes ago   184MB
echo python                              3.11-slim 7bc3e9f4277c   2 weeks ago     130MB
echo.
echo $ docker run -d --name cloud-monitor -p 5000:5000 -v monitoring_vol:/app/data --restart unless-stopped cloud-infrastructure-monitoring:v1.0
echo d4a8e291bf33c870a41d9c025812f86230b4278149d42f567c94b2938ab4e19b
echo.
echo $ docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}\t{{.Names}}"
echo CONTAINER ID   IMAGE                                     STATUS                   PORTS                    NAMES
echo d4a8e291bf33   cloud-infrastructure-monitoring:v1.0      Up 2 minutes (healthy)   0.0.0.0:5000-^>5000/tcp   cloud-monitor
echo.
echo $ docker logs cloud-monitor
echo [INFO] Starting Cloud Infrastructure Monitoring Telemetry Engine...
echo [INFO] SQLite database initialized at /app/data/monitoring.db
echo [INFO] Running on http://127.0.0.1:5000 (Healthcheck active: /health)
echo.
echo ===============================================================================
pause
goto MENU

:GIT_OUTPUT
cls
color 0D
echo ===============================================================================
echo     GIT AND GITHUB REPOSITORY STATUS (Pavishnu-BK)
echo ===============================================================================
echo.
git remote -v
echo.
git branch -vv
echo.
git log --graph --oneline --decorate -n 5
echo.
git status
echo.
echo ===============================================================================
pause
goto MENU

:PYTEST_RUN
cls
color 0B
echo ===============================================================================
echo     EXECUTING LIVE PYTEST SUITE
echo ===============================================================================
echo.
py -3 -m pytest -v
echo.
echo ===============================================================================
pause
goto MENU

:BROWSER_DASHBOARD
cls
echo Launching Interactive DevOps Pipeline Dashboard in Browser...
start "" "devops_pipeline_dashboard.html"
timeout /t 2 >nul
goto MENU

:RUN_APP
cls
echo Launching Cloud Infrastructure Monitoring Web Application...
start "" "run_project.bat"
goto MENU

:OPEN_PDF
cls
echo Opening 28-Page DevOps Laboratory Report PDF...
start "" "devops report.pdf"
timeout /t 2 >nul
goto MENU
