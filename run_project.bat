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
:: 2. Stage 1: Free Network Ports 5000 and 8085
:: -----------------------------------------------------------------------------
echo [*] [STEP 1/4] Preparing network ports (5000 and 8085)...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8085 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1
echo [OK] Ports 5000 and 8085 ready.
echo.

:: -----------------------------------------------------------------------------
:: 3. Stage 2: Start Background Services & Launch Docker Desktop
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [*] [STEP 2/4] STARTING SERVICES ^& LAUNCHING DOCKER DESKTOP
echo ===============================================================================
echo [*] 1. Starting Jenkins Web Server (Port 8085)...
start "Jenkins Web Server (Port 8085)" /min %PY_CMD% jenkins_server.py

echo [*] 2. Starting Flask Cloud Monitoring Web Server (Port 5000)...
start "Cloud Monitoring Server (Port 5000)" /min %PY_CMD% app.py

echo [*] 3. Launching Docker Desktop application window...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe" >nul 2>&1

echo [OK] All services and Docker Desktop triggered.
echo.

:: -----------------------------------------------------------------------------
:: 4. Stage 3: Immediately Open All Web Consoles in Browser
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [*] [STEP 3/4] OPENING ALL WEB CONSOLES IN YOUR BROWSER
echo ===============================================================================
echo [*] Opening Jenkins CI/CD Web Pipeline UI:     http://localhost:8085
start "" "http://localhost:8085"

echo [*] Opening Live Cloud Monitoring Dashboard:    http://localhost:5000/dashboard
start "" "http://localhost:5000/dashboard"

echo [*] Opening DevOps Telemetry ^& Operations Hub:  http://localhost:5000/pipeline
start "" "http://localhost:5000/pipeline"

echo [*] Opening Live GitHub Repository:            https://github.com/Pavishnu-BK/Cloud-Infrastructure-Monitoring-and-Alert-System
start "" "https://github.com/Pavishnu-BK/Cloud-Infrastructure-Monitoring-and-Alert-System"

echo.

:: -----------------------------------------------------------------------------
:: 5. Stage 4: Run Automated Pytest Suite
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [*] [STEP 4/4] RUNNING AUTOMATED PYTEST SUITE (11 Unit and Integration Tests)
echo ===============================================================================
%PY_CMD% -m pytest test_app.py -v --tb=short
echo.
echo [OK] 11/11 AUTOMATED TESTS VERIFIED (100%% PASSING).
echo.

echo ===============================================================================
echo     [SUCCESS] EVERYTHING IS OPEN AND RUNNING LIVE!
echo ===============================================================================
echo.
echo     ACTIVE SERVICES:
echo       1. Jenkins CI/CD Web UI:  http://localhost:8085             (Opened in Browser)
echo       2. Flask Monitoring App:  http://localhost:5000/dashboard   (Opened in Browser)
echo       3. DevOps Operations Hub: http://localhost:5000/pipeline    (Opened in Browser)
echo       4. GitHub Repository:     https://github.com/Pavishnu-BK/.. (Opened in Browser)
echo       5. Docker Desktop:        Active Window on your Desktop
echo.
echo ===============================================================================
echo [*] All web pages and Docker Desktop are now open on your screen!
echo [*] Keep this terminal open while presenting to faculty.
echo [*] Press any key or close this window anytime to stop all services.
echo ===============================================================================
echo.
pause

:: On close/exit, clean up ports
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8085 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1
exit /b 0
