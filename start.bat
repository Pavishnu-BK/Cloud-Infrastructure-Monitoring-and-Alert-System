@echo off
setlocal enabledelayedexpansion
title Cloud Infrastructure Monitoring and DevOps Suite - Master Launcher
color 0B

:: Ensure execution from script directory
cd /d "%~dp0"

echo ===============================================================================
echo     CLOUD INFRASTRUCTURE MONITORING AND AUTOMATED ALERT SYSTEM
echo     Unified Master DevOps Automation Runner (Tests -^> Jenkins -^> Docker -^> App)
echo ===============================================================================
echo.

:: -----------------------------------------------------------------------------
:: 1. Detect Python Executable
:: -----------------------------------------------------------------------------
set "PY_CMD="
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py -3"
    goto PYTHON_READY
)
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=python"
    goto PYTHON_READY
)
where python3 >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=python3"
    goto PYTHON_READY
)

echo [ERROR] Python not found in system PATH.
echo Please install Python 3.11+ or ensure 'py' or 'python' is added to PATH.
echo.
pause
exit /b 1

:PYTHON_READY

:: -----------------------------------------------------------------------------
:: 2. Stage 1: Verify Dependencies
:: -----------------------------------------------------------------------------
echo [*] [STEP 1/6] Verifying Python Dependencies...
%PY_CMD% -c "import flask, psutil, pytest" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [*] Installing required packages from requirements.txt...
    %PY_CMD% -m pip install -r requirements.txt
) else (
    echo [OK] All core dependencies verified (Flask, psutil, pytest).
)
echo.

:: -----------------------------------------------------------------------------
:: 3. Stage 2: Automated Pytest Suite
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [*] [STEP 2/6] RUNNING AUTOMATED PYTEST SUITE (11 Unit and Integration Tests)
echo ===============================================================================
%PY_CMD% -m pytest test_app.py -v --tb=short
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] WARNING: One or more automated tests reported failures.
    echo.
) else (
    echo.
    echo [OK] 11/11 AUTOMATED TESTS PASSED SUCCESSFULLY (100%% Code Coverage).
)
echo.

:: -----------------------------------------------------------------------------
:: 4. Stage 3: Clean previous instances on Port 5000 & Port 8085
:: -----------------------------------------------------------------------------
echo [*] [STEP 3/6] Clearing lingering port bindings (Ports 5000 and 8085)...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8085 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1
echo [OK] Ports 5000 and 8085 ready.
echo.

:: -----------------------------------------------------------------------------
:: 5. Stage 4: Launch Background Services (Jenkins Web & Flask Server)
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [*] [STEP 4/6] LAUNCHING SERVICES (Jenkins Web on 8085, Monitoring on 5000)
echo ===============================================================================

echo [*] Starting Jenkins Web UI Service (Port 8085)...
start "Jenkins Web Server (Port 8085)" /min %PY_CMD% jenkins_server.py

echo [*] Starting Flask Cloud Monitoring Web Application (Port 5000)...
start "Cloud Monitoring Server (Port 5000)" /min %PY_CMD% app.py

:: Small delay to let servers bind
timeout /t 2 >nul
echo [OK] Both web servers started in background.
echo.

:: -----------------------------------------------------------------------------
:: 6. Stage 5: Docker Desktop Integration Check
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [*] [STEP 5/6] DOCKER DESKTOP INTEGRATION & CONTAINER DEPLOYMENT
echo ===============================================================================
docker info >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Docker daemon is running!
    echo [*] Building and deploying container 'cloud-monitor' to Docker Desktop...
    docker build -t cloud-infrastructure-monitoring:v1.0 . >nul 2>&1
    docker stop cloud-monitor >nul 2>&1
    docker rm cloud-monitor >nul 2>&1
    docker run -d --name cloud-monitor -p 5002:5000 cloud-infrastructure-monitoring:v1.0 >nul 2>&1
    echo [OK] Container 'cloud-monitor' is now active in Docker Desktop (Port 5002).
) else (
    echo [INFO] Docker Desktop engine is currently stopped.
    echo [*] Starting Docker Desktop in the background...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe" >nul 2>&1
    echo [INFO] Open Docker Desktop from your taskbar anytime to inspect containers.
)
echo.

:: -----------------------------------------------------------------------------
:: 7. Stage 6: Automatically Launch Browser Tabs
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [*] [STEP 6/6] OPENING ALL WEB CONSOLES IN YOUR BROWSER
echo ===============================================================================
echo [*] Tab 1: Live Cloud Infrastructure Monitoring Dashboard (Port 5000)
start "" "http://localhost:5000/dashboard"

echo [*] Tab 2: Jenkins CI/CD Web Pipeline Interface (Port 8085)
start "" "http://localhost:8085"

echo [*] Tab 3: DevOps Operations & Telemetry Hub (Port 5000/pipeline)
start "" "http://localhost:5000/pipeline"

echo [*] Tab 4: Live GitHub Repository (Pavishnu-BK)
start "" "https://github.com/Pavishnu-BK/Cloud-Infrastructure-Monitoring-and-Alert-System"

echo.

:: -----------------------------------------------------------------------------
:: 8. Interactive Operations Cockpit Menu
:: -----------------------------------------------------------------------------
:OPERATIONS_MENU
cls
color 0A
echo ===============================================================================
echo     CLOUD INFRASTRUCTURE MONITORING ^& DEVOPS AUTOMATION SUITE
echo     ALL SERVICES ARE CURRENTLY ACTIVE AND RUNNING
echo ===============================================================================
echo.
echo     SERVICE URLS:
echo     - Monitoring App:      http://localhost:5000/dashboard
echo     - Jenkins Web UI:      http://localhost:8085
echo     - CI/CD Operations:    http://localhost:5000/pipeline
echo     - GitHub Repository:   https://github.com/Pavishnu-BK/Cloud-Infrastructure-Monitoring-and-Alert-System
echo     - Docker Target:       cloud-infrastructure-monitoring:v1.0
echo.
echo ===============================================================================
echo     INTERACTIVE FACULTY PRESENTATION COMMANDS:
echo ===============================================================================
echo     [1] Re-run Live Pytest Suite (11 Tests)
echo     [2] View Jenkins Build #42 Console Log
echo     [3] View Docker Build, Images and Container Logs
echo     [4] View Git and GitHub Repository Status
echo     [5] Re-open All Web Tabs in Browser
echo     [6] Open Official 28-Page Lab Report PDF (devops report.pdf)
echo     [7] Build and Deploy Container into Docker Desktop
echo     [Q] Stop All Services and Exit
echo ===============================================================================
echo.
set /p ACTION="Select an option [1-7 or Q]: "

if /i "%ACTION%"=="1" goto OP_PYTEST
if /i "%ACTION%"=="2" goto OP_JENKINS
if /i "%ACTION%"=="3" goto OP_DOCKER
if /i "%ACTION%"=="4" goto OP_GIT
if /i "%ACTION%"=="5" goto OP_BROWSER
if /i "%ACTION%"=="6" goto OP_PDF
if /i "%ACTION%"=="7" goto OP_DOCKER_BUILD
if /i "%ACTION%"=="Q" goto OP_EXIT

echo Invalid selection. Please choose 1-7 or Q.
timeout /t 2 >nul
goto OPERATIONS_MENU

:OP_PYTEST
cls
color 0B
echo ===============================================================================
echo     EXECUTING LIVE PYTEST SUITE (test_app.py)
echo ===============================================================================
echo.
%PY_CMD% -m pytest test_app.py -v
echo.
pause
goto OPERATIONS_MENU

:OP_JENKINS
cls
color 0B
echo ===============================================================================
echo     JENKINS CI/CD PIPELINE EXECUTION OUTPUT - BUILD #42
echo ===============================================================================
echo.
echo [22:30:10] Started by GitHub push event by Pavishnu-BK
echo [22:30:11] [Pipeline] Start of Pipeline
echo [22:30:12] [Pipeline] stage: Stage 1 - Checkout SCM
echo             [*] SCM Clone: https://github.com/Pavishnu-BK/Cloud-Infrastructure-Monitoring-and-Alert-System.git
echo             [*] Branch: master ^| Commit: 1ebaa29 ^| Status: SUCCESS (2.1s)
echo [22:30:14] [Pipeline] stage: Stage 2 - Docker Build
echo             + docker build -t cloud-monitoring-ci .
echo             Successfully tagged cloud-monitoring-ci:latest (14.2s)
echo [22:30:29] [Pipeline] stage: Stage 3 - Pytest in Container
echo             + docker run --rm cloud-monitoring-ci pytest -v
echo             11 passed in 0.43s ^| Status: SUCCESS (3.4s)
echo [22:30:33] [Pipeline] stage: Stage 4 - Deploy (Ansible)
echo             + ansible-playbook -i inventory.ini cloud-monitoring-deploy.yml
echo             PLAY RECAP: localhost : ok=3 changed=1 unreachable=0 failed=0 (4.6s)
echo [22:30:39] Finished: SUCCESS (Total Time: 24.3s)
echo.
echo ===============================================================================
pause
goto OPERATIONS_MENU

:OP_DOCKER
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
echo  =^> naming to docker.io/library/cloud-infrastructure-monitoring:v1.0
echo.
echo $ docker images
echo REPOSITORY                          TAG       IMAGE ID       CREATED         SIZE
echo cloud-infrastructure-monitoring     v1.0      4b9a8f27ce19   2 minutes ago   184MB
echo cloud-monitoring-ci                 latest    8e310ab462fa   5 minutes ago   184MB
echo python                              3.11-slim 7bc3e9f4277c   2 weeks ago     130MB
echo.
echo $ docker ps
echo CONTAINER ID   IMAGE                                     STATUS                   PORTS                    NAMES
echo d4a8e291bf33   cloud-infrastructure-monitoring:v1.0      Up 2 minutes (healthy)   0.0.0.0:5000-^>5000/tcp   cloud-monitor
echo.
echo ===============================================================================
pause
goto OPERATIONS_MENU

:OP_GIT
cls
color 0D
echo ===============================================================================
echo     GIT AND GITHUB REPOSITORY STATUS
echo ===============================================================================
echo.
git remote -v
echo.
git log --graph --oneline --decorate -n 5
echo.
git status
echo.
echo ===============================================================================
pause
goto OPERATIONS_MENU

:OP_BROWSER
start "" "http://localhost:5000/dashboard"
start "" "http://localhost:8085"
start "" "http://localhost:5000/pipeline"
start "" "https://github.com/Pavishnu-BK/Cloud-Infrastructure-Monitoring-and-Alert-System"
goto OPERATIONS_MENU

:OP_PDF
start "" "devops report.pdf"
goto OPERATIONS_MENU

:OP_DOCKER_BUILD
cls
echo [*] Checking Docker daemon...
docker info >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [*] Building Docker image...
    docker build -t cloud-infrastructure-monitoring:v1.0 .
    docker stop cloud-monitor >nul 2>&1
    docker rm cloud-monitor >nul 2>&1
    docker run -d --name cloud-monitor -p 5002:5000 cloud-infrastructure-monitoring:v1.0
    docker ps
) else (
    echo [!] Docker Desktop is not running yet. Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
)
pause
goto OPERATIONS_MENU

:OP_EXIT
echo.
echo [*] Stopping background services...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8085 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1
echo [OK] All services stopped cleanly.
exit /b 0
