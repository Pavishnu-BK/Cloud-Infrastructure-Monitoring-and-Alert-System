@echo off
setlocal enabledelayedexpansion
title Official Jenkins Server (Port 8085)
color 0B

cd /d "%~dp0"

set "JAVA_BIN=C:\Program Files\Java\jdk-22\bin\java.exe"
if not exist "%JAVA_BIN%" (
    where java >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        set "JAVA_BIN=java"
    ) else (
        echo [ERROR] Java not found.
        pause
        exit /b 1
    )
)

set "JENKINS_HOME=d:\DEVOPS\.jenkins"
if not exist "%JENKINS_HOME%" mkdir "%JENKINS_HOME%"

echo ===============================================================================
echo     STARTING OFFICIAL JENKINS AUTOMATION SERVER (PORT 8085)
echo     JENKINS_HOME: %JENKINS_HOME%
echo ===============================================================================
echo.

"%JAVA_BIN%" -Djenkins.install.runSetupWizard=false -jar "%~dp0jenkins.war" --enable-future-java --httpPort=8085

