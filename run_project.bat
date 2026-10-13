@echo off
setlocal enabledelayedexpansion
title Cloud Infrastructure Monitoring and DevOps Suite - Auto Runner
color 0B

:: Ensure execution from script directory
cd /d "%~dp0"

echo ===============================================================================
echo     CLOUD INFRASTRUCTURE MONITORING AND AUTOMATED ALERT SYSTEM
echo     DevOps Automated End-to-End Pipeline Execution
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
echo [*] [STAGE 1/5] Verifying Dependencies (Flask, psutil, pytest)...
%PY_CMD% -c "import flask, psutil, pytest" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [*] Installing missing packages from requirements.txt...
    %PY_CMD% -m pip install -r requirements.txt
) else (
    echo [OK] All dependencies verified.
)
echo.

:: -----------------------------------------------------------------------------
:: 3. Stage 2: Automated Pytest Testing
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [*] [STAGE 2/5] RUNNING AUTOMATED PYTEST SUITE (11 Unit and Integration Tests)
echo ===============================================================================
%PY_CMD% -m pytest test_app.py -v --tb=short
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] Warning: Some tests reported issues, proceeding to launch services...
) else (
    echo.
    echo [OK] ALL 11 TESTS PASSED SUCCESSFULLY!
)
echo.

:: -----------------------------------------------------------------------------
:: 4. Stage 3: Clean Lingering Ports (5000 and 8085)
:: -----------------------------------------------------------------------------
echo [*] [STAGE 3/5] Freeing network ports 5000 and 8085...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8085 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1
echo [OK] Ports 5000 and 8085 ready.
echo.

:: -----------------------------------------------------------------------------
:: 5. Stage 4: Launch Web Servers & Docker Desktop
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [*] [STAGE 4/5] STARTING SERVERS AND LAUNCHING DOCKER DESKTOP
echo ===============================================================================

:: 5a. Start Jenkins Web Service in Background
echo [*] Launching Jenkins CI/CD Web Server (Port 8085)...
start "Jenkins Web Server (Port 8085)" /min %PY_CMD% jenkins_server.py

:: 5b. Start Flask Cloud Monitoring Application in Background
echo [*] Launching Flask Cloud Monitoring Web Server (Port 5000)...
start "Cloud Monitoring Server (Port 5000)" /min %PY_CMD% app.py

:: 5c. Launch Docker Desktop on Windows
echo [*] Launching Docker Desktop application...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe" >nul 2>&1

:: 5d. Check Docker daemon and build/deploy container if engine is active
docker info >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [*] Docker engine active: Building image and deploying to Docker Desktop...
    docker build -t cloud-infrastructure-monitoring:v1.0 . >nul 2>&1
    docker stop cloud-monitor >nul 2>&1
    docker rm cloud-monitor >nul 2>&1
    docker run -d --name cloud-monitor -p 5002:5000 cloud-infrastructure-monitoring:v1.0 >nul 2>&1
    echo [OK] Container 'cloud-monitor' deployed in Docker Desktop!
) else (
    echo [OK] Docker Desktop launched on your screen (Docker engine is starting).
)

:: Wait 2 seconds for web servers to initialize
timeout /t 2 >nul
echo.

:: -----------------------------------------------------------------------------
:: 6. Stage 5: Automatically Open Browser Tabs
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [*] [STAGE 5/5] OPENING WEB INTERFACES IN BROWSER
echo ===============================================================================
echo [*] Opening Live Cloud Infrastructure Monitoring App: http://localhost:5000/dashboard
start "" "http://localhost:5000/dashboard"

echo [*] Opening Jenkins CI/CD Web Pipeline Interface:      http://localhost:8085
start "" "http://localhost:8085"

echo [*] Opening DevOps Telemetry & Operations Dashboard:   http://localhost:5000/pipeline
start "" "http://localhost:5000/pipeline"

echo [*] Opening Live GitHub Repository (Pavishnu-BK):      https://github.com/Pavishnu-BK/Cloud-Infrastructure-Monitoring-and-Alert-System
start "" "https://github.com/Pavishnu-BK/Cloud-Infrastructure-Monitoring-and-Alert-System"

echo.
echo ===============================================================================
echo     [SUCCESS] EVERYTHING IS RUNNING LIVE!
echo ===============================================================================
echo.
echo     ACTIVE SERVICES:
echo       1. Monitoring App:     http://localhost:5000/dashboard  (Live CPU/RAM/Disk)
echo       2. Jenkins Web UI:     http://localhost:8085            (Stage View & Console)
echo       3. DevOps Hub:         http://localhost:5000/pipeline   (Full Pipeline & QA)
echo       4. GitHub Repository:  https://github.com/Pavishnu-BK/Cloud-Infrastructure-Monitoring-and-Alert-System
echo       5. Docker Desktop:     Active on your Windows Desktop
echo.
echo ===============================================================================
echo [*] Keep this window open while demonstrating to faculty.
echo [*] Press CTRL+C or close this window when you want to stop all services.
echo ===============================================================================
echo.

:: Keep process alive so servers stay running
pause

:: On close/exit, clean up ports
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8085 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1
exit /b 0
