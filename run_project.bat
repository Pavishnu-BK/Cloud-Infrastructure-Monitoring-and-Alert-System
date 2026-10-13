@echo off
setlocal enabledelayedexpansion
title Cloud Infrastructure Monitoring and Automated Alert System - DevOps Lab
color 0B

:: Ensure execution from the directory containing this batch file
cd /d "%~dp0"

echo ===============================================================================
echo     CLOUD INFRASTRUCTURE MONITORING AND AUTOMATED ALERT SYSTEM
echo     DevOps Automated Execution Pipeline (Pytest -^> Flask Server -^> Browser)
echo ===============================================================================
echo.

:: 1. Detect Python Executable
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

:: 2. Stage 1: Dependency Verification
echo [*] [STAGE 1/3] Checking Python Dependencies...
%PY_CMD% -c "import flask, psutil, pytest" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [*] Installing missing packages from requirements.txt...
    %PY_CMD% -m pip install -r requirements.txt
) else (
    echo [OK] All dependencies verified: Flask, psutil, pytest.
)
echo.

:: 3. Stage 2: Automated Testing with Pytest
echo ===============================================================================
echo [*] [STAGE 2/3] RUNNING PYTEST AUTOMATED TEST SUITE (11 Test Cases)
echo ===============================================================================
%PY_CMD% -m pytest test_app.py -v
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] WARNING: One or more automated tests failed!
    echo Review test output above before demonstrating to faculty.
    echo.
    pause
) else (
    echo.
    echo [OK] ALL 11 TESTS PASSED SUCCESSFULLY!
)
echo.

:: 4. Free Port 5000 if occupied by previous instance
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1

:: 5. Stage 3: Launch Web Server & Automatically Open Browser
echo ===============================================================================
echo [*] [STAGE 3/3] STARTING FLASK MONITORING WEB SERVER
echo ===============================================================================
echo [*] Monitored Target: Local Operating System / Container
echo [*] Telemetry Engine: Python psutil (CPU, RAM, Disk, Uptime)
echo [*] SQLite Database:  data\monitoring.db
echo [*] Live Dashboard:   http://localhost:5000/dashboard
echo [*] Health Check API: http://localhost:5000/health
echo.
echo [*] Automatically opening dashboard in your default browser...
start "" cmd /c "ping 127.0.0.1 -n 3 >nul & start http://localhost:5000/dashboard"

echo [*] Server is now running live! Press CTRL+C in this window anytime to stop.
echo ===============================================================================
echo.

%PY_CMD% app.py

echo.
echo [*] Server process stopped.
pause
exit /b 0
