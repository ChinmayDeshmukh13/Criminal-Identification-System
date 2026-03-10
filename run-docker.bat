@echo off
REM Criminal Identification System - Docker Build and Run Script for Windows
REM This script builds and runs the application using Docker

setlocal enabledelayedexpansion

REM Colors (Windows doesn't support ANSI by default, so we use simple messaging)
echo.
echo ====================================
echo Criminal Identification System
echo Docker Build and Run Script
echo ====================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker Compose is not installed
    echo Please install Docker Desktop which includes Docker Compose
    pause
    exit /b 1
)

echo Docker and Docker Compose are installed
echo.

REM Menu
:menu
echo Select operation:
echo 1. Start application (docker-compose up)
echo 2. Stop application (docker-compose down)
echo 3. Build image (docker build)
echo 4. View logs (docker-compose logs)
echo 5. Restart services (docker-compose restart)
echo 6. Remove all and clean up
echo 7. Exit

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto start
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto build
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto restart
if "%choice%"=="6" goto cleanup
if "%choice%"=="7" goto exit

echo Invalid choice. Please try again.
echo.
goto menu

:start
echo.
echo Starting Criminal Identification System with Docker Compose...
docker-compose up -d
if errorlevel 1 (
    echo Error starting services
    pause
    goto menu
)
echo.
echo Application started successfully!
echo.
echo Access the application at:
echo - Frontend: http://localhost
echo - API: http://localhost:8000
echo - API Docs: http://localhost:8000/api/docs (development only)
echo.
echo View logs with: docker-compose logs -f
pause
goto menu

:stop
echo.
echo Stopping Criminal Identification System...
docker-compose down
echo Application stopped
echo.
pause
goto menu

:build
echo.
echo Building Docker image...
docker build -t ifrs:latest .
if errorlevel 1 (
    echo Error building image
    pause
    goto menu
)
echo Image built successfully: ifrs:latest
echo.
pause
goto menu

:logs
echo.
echo Showing logs (Press Ctrl+C to stop)...
docker-compose logs -f
echo.
pause
goto menu

:restart
echo.
echo Restarting services...
docker-compose restart
echo Services restarted
echo.
pause
goto menu

:cleanup
echo.
echo WARNING: This will remove all containers, images, and volumes!
set /p confirm="Are you sure? (yes/no): "
if /i "%confirm%"=="yes" (
    echo Cleaning up...
    docker-compose down -v
    docker rmi ifrs:latest
    echo Cleanup complete
) else (
    echo Cleanup cancelled
)
echo.
pause
goto menu

:exit
echo.
echo Exiting...
exit /b 0
