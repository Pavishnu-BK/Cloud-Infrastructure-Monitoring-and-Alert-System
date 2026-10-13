@echo off
setlocal enabledelayedexpansion
title Docker Desktop Container Deployer
color 0B

cd /d "%~dp0"

echo ===============================================================================
echo     DOCKER DESKTOP LOCAL CONTAINER DEPLOYMENT
echo     Cloud Infrastructure Monitoring and Automated Alert System
echo ===============================================================================
echo.

echo [*] Checking Docker daemon connection...
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] Docker daemon is not running yet.
    echo.
    echo [*] Please ensure Docker Desktop is opened on your screen.
    echo [*] Opening Docker Desktop now...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo.
    echo [*] Waiting 15 seconds for Docker Desktop engine to initialize...
    timeout /t 15
)

echo.
echo [*] Step 1: Building Docker image 'cloud-infrastructure-monitoring:v1.0' ...
docker build -t cloud-infrastructure-monitoring:v1.0 .

echo.
echo [*] Step 2: Stopping any previous container instance...
docker stop cloud-monitor >nul 2>&1
docker rm cloud-monitor >nul 2>&1

echo.
echo [*] Step 3: Launching container in Docker Desktop...
docker run -d --name cloud-monitor -p 5000:5000 cloud-infrastructure-monitoring:v1.0

echo.
echo [*] Step 4: Verifying running container...
docker ps --filter "name=cloud-monitor"

echo.
echo ===============================================================================
echo [SUCCESS] Container 'cloud-monitor' is now active in Docker Desktop!
echo Open Docker Desktop to see the live container CPU, Memory, and Logs.
echo Web Application: http://localhost:5000/dashboard
echo ===============================================================================
pause
