@echo off
setlocal enabledelayedexpansion
title Jenkins CI/CD Web Service (Port 8085)
color 0B

cd /d "%~dp0"

echo ===============================================================================
echo     JENKINS CI/CD AUTOMATION WEB SERVICE - PORT 8085
echo     Cloud Infrastructure Monitoring and Automated Alert System
echo ===============================================================================
echo.

set "PY_CMD="
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py -3"
    goto START_JENKINS
)
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=python"
    goto START_JENKINS
)
echo [ERROR] Python not found in system PATH.
pause
exit /b 1

:START_JENKINS
echo [*] Starting Jenkins Web UI on http://localhost:8085 ...
start "" http://localhost:8085
%PY_CMD% jenkins_server.py

pause
