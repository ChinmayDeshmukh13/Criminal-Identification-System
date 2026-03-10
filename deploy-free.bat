@echo off
REM Criminal Identification System - Free Deployment Helper (Windows)
REM This script helps you deploy to free platforms

setlocal enabledelayedexpansion

cls
echo.
echo ==================================
echo    Free Deployment Helper
echo    Criminal Identification System
echo ==================================
echo.

:menu
echo Select a platform to deploy:
echo.
echo 1. Google Cloud Run (Best - Free tier, 2M requests/month)
echo 2. Railway (Easy - $5 free credit)
echo 3. Render (Reliable free tier)
echo 4. Oracle Cloud (Always free)
echo 5. Local with Ngrok (Test online)
echo 6. View comparison
echo 7. Show help
echo 8. Exit
echo.
set /p choice="Select option (1-8): "

if "%choice%"=="1" goto google_cloud
if "%choice%"=="2" goto railway
if "%choice%"=="3" goto render
if "%choice%"=="4" goto oracle
if "%choice%"=="5" goto ngrok
if "%choice%"=="6" goto comparison
if "%choice%"=="7" goto help
if "%choice%"=="8" goto exit_script

echo Invalid option. Please try again.
echo.
goto menu

:google_cloud
cls
echo.
echo ===== Google Cloud Run Deployment =====
echo.
echo Prerequisites:
echo 1. Create Google Cloud account at https://cloud.google.com
echo 2. Install Google Cloud CLI
echo 3. Have 'gcloud' command available
echo.
echo Quick setup:
echo.
echo Step 1: Install Google Cloud SDK
echo   Download from: https://cloud.google.com/sdk/docs/install
echo.
echo Step 2: Authenticate
echo   gcloud auth login
echo.
echo Step 3: Run deployment
echo   gcloud config set project YOUR-PROJECT-ID
echo   gcloud services enable cloudbuild.googleapis.com run.googleapis.com
echo   gcloud run deploy ifrs --source . --platform managed --region us-central1 --allow-unauthenticated --memory 2Gi
echo.
echo Step 4: Access your app
echo   gcloud run services describe ifrs --region us-central1 --format='value(status.url)'
echo.
set /p ready="Ready to proceed? (yes/no): "
if /i "%ready%"=="yes" (
    echo.
    echo Opening Google Cloud Console...
    start https://cloud.google.com/sdk/docs/install
)
echo.
pause
goto menu

:railway
cls
echo.
echo ===== Railway Deployment =====
echo.
echo Railway is the easiest! Here's how:
echo.
echo Step 1: Go to https://railway.app and sign up with GitHub
echo.
echo Step 2: Create 'New Project'
echo.
echo Step 3: Select 'Deploy from GitHub'
echo.
echo Step 4: Authorize Railway and select this repository
echo.
echo Step 5: Railway auto-detects the Dockerfile
echo.
echo Step 6: Set environment variables:
echo   ENVIRONMENT = production
echo   DEBUG = false
echo.
echo Step 7: Click Deploy!
echo.
echo Your app will be live in 2-3 minutes with auto-updates!
echo.
set /p open="Open Railway.app? (yes/no): "
if /i "%open%"=="yes" (
    start https://railway.app
)
echo.
pause
goto menu

:render
cls
echo.
echo ===== Render Deployment =====
echo.
echo Step 1: Go to https://render.com and sign up with GitHub
echo.
echo Step 2: Click "New +" then "Web Service"
echo.
echo Step 3: Select "Deploy existing image" or "Deploy from GitHub"
echo.
echo Step 4: Configure:
echo   - Name: ifrs-app
echo   - Region: Choose closest to you
echo   - Plan: Free
echo.
echo Step 5: Set environment:
echo   - ENVIRONMENT = production
echo   - DEBUG = false
echo.
echo Step 6: Click "Create Web Service"
echo.
echo Your app will be live in 1-2 minutes!
echo.
set /p open="Open Render.com? (yes/no): "
if /i "%open%"=="yes" (
    start https://render.com
)
echo.
pause
goto menu

:oracle
cls
echo.
echo ===== Oracle Cloud Always Free Deployment =====
echo.
echo This option is always free - never expires!
echo.
echo Step 1: Create an account
echo   https://www.oracle.com/cloud/free/
echo.
echo Step 2: Create VM Instance
echo   - Compute ^> Instances ^> Create Instance
echo   - Image: Ubuntu 20.04 LTS (always free)
echo   - Click Create
echo.
echo Step 3: SSH to your instance
echo   ssh ubuntu^<your-instance-ip^>
echo.
echo Step 4: Install Docker
echo   sudo apt-get update
echo   sudo apt-get install -y docker.io docker-compose
echo   sudo usermod -aG docker ubuntu
echo.
echo Step 5: Deploy
echo   git clone ^<your-repo^>
echo   cd Criminal-Identification
echo   docker-compose up -d
echo.
echo Step 6: Open firewall port 80
echo   In Oracle console: add Ingress rule for port 80
echo.
echo Your app is now live forever (always free)!
echo.
set /p open="Open Oracle Cloud? (yes/no): "
if /i "%open%"=="yes" (
    start https://www.oracle.com/cloud/free/
)
echo.
pause
goto menu

:ngrok
cls
echo.
echo ===== Local Deployment with Ngrok =====
echo.
echo This lets you access your local app from anywhere!
echo.
echo Prerequisites: Docker installed and running
echo.
echo Step 1: Get ngrok
echo   Option A: Download from https://ngrok.com/download
echo   Option B: PowerShell: choco install ngrok
echo.
echo Step 2: Sign up at https://ngrok.com and get auth token
echo.
echo Step 3: Configure ngrok
echo   ngrok authtoken YOUR_TOKEN
echo.
echo Step 4: Start your app (if not running)
echo   docker-compose up -d
echo.
echo Step 5: Expose with ngrok
echo   ngrok http 80
echo.
echo Step 6: Use the provided https://xxxx.ngrok.io URL
echo.
set /p open="Open ngrok.com? (yes/no): "
if /i "%open%"=="yes" (
    start https://ngrok.com
)
echo.
pause
goto menu

:comparison
cls
echo.
echo ===== Platform Comparison =====
echo.
echo Platform          Cost              Setup Time    Best For
echo ---               ---               ---           ---
echo Google Cloud      Free (2M req)     20 min        Production
echo Railway           $5 credit/month   10 min        Quick test
echo Render            Always free       10 min        Reliable
echo Oracle Cloud      Always free       30 min        Long-term
echo Ngrok (Local)     Free              5 min         Local test
echo.
echo Recommendations:
echo - Quick test? Use Railway or Render
echo - Production? Use Google Cloud Run
echo - Always free? Use Oracle Cloud
echo.
pause
goto menu

:help
cls
echo.
echo ===== Help & Troubleshooting =====
echo.
echo Q: Which platform should I choose?
echo A: Start with Railway (easiest setup, 10 minutes)
echo    Then try Google Cloud Run (best performance)
echo.
echo Q: Why no webcam on cloud?
echo A: Cloud servers don't have cameras. Use local docker-compose
echo    for webcam features, or upload test images.
echo.
echo Q: How long is the free tier valid?
echo A: Google Cloud Run: Always free (2M req/month limit)
echo    Others: Varies (see comparison)
echo.
echo Q: Can I use my own domain?
echo A: Yes! Point domain to cloud provider in your registrar.
echo.
echo Q: How do I backup my data?
echo A: For cloud: Use cloud storage. For local: Copy ./data/ directory.
echo.
echo See these files for more info:
echo - FREE-DEPLOYMENT.md - Comprehensive guide
echo - SETUP.md - Setup instructions
echo - DEPLOYMENT.md - Advanced deployment
echo.
pause
goto menu

:exit_script
echo.
echo For more information:
echo - Read: FREE-DEPLOYMENT.md
echo - Setup help: SETUP.md
echo - Feature guide: README-DEPLOYMENT.md
echo.
echo Your app can be live in 10-20 minutes with ZERO cost!
echo.
pause
exit /b 0
