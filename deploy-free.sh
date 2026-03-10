#!/bin/bash

# Criminal Identification System - Free Deployment Helper
# This script helps you deploy to free platforms

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "=================================="
echo "   Free Deployment Helper"
echo "   Criminal Identification System"
echo "=================================="
echo ""

show_platforms() {
    echo "Which platform would you like to deploy to?"
    echo ""
    echo "1. Google Cloud Run (Best - Free tier, 2M requests/month)"
    echo "2. Railway (Easy - $5 free credit)"
    echo "3. Render (Reliable free tier)"
    echo "4. Oracle Cloud (Always free)"
    echo "5. Local with Ngrok (Test online)"
    echo "6. View comparison"
    echo "7. Exit"
    echo ""
    read -p "Select option (1-7): " choice
}

google_cloud_deploy() {
    echo ""
    echo -e "${BLUE}Google Cloud Run Deployment${NC}"
    echo ""
    echo "Prerequisites:"
    echo "1. Create Google Cloud account at https://cloud.google.com"
    echo "2. Install Google Cloud CLI"
    echo "3. Have 'gcloud' command available"
    echo ""
    
    read -p "Have you installed gcloud CLI and created a project? (yes/no): " confirm
    
    if [ "$confirm" != "yes" ]; then
        echo -e "${YELLOW}Please install gcloud first:${NC}"
        echo "Visit: https://cloud.google.com/sdk/docs/install"
        return
    fi
    
    echo ""
    echo -e "${BLUE}Starting deployment...${NC}"
    echo ""
    
    # Get project ID
    read -p "Enter your Google Cloud Project ID: " project_id
    
    # Check if gcloud is installed
    if ! command -v gcloud &> /dev/null; then
        echo -e "${RED}Error: gcloud CLI not found${NC}"
        echo "Install from: https://cloud.google.com/sdk/docs/install"
        return
    fi
    
    echo -e "${YELLOW}Configuring gcloud...${NC}"
    gcloud config set project $project_id
    
    echo -e "${YELLOW}Enabling APIs...${NC}"
    gcloud services enable cloudbuild.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable containerregistry.googleapis.com
    
    echo -e "${YELLOW}Deploying application...${NC}"
    gcloud run deploy ifrs \
        --source . \
        --platform managed \
        --region us-central1 \
        --allow-unauthenticated \
        --memory 2Gi \
        --timeout 3600
    
    echo ""
    echo -e "${GREEN}✓ Deployment complete!${NC}"
    echo ""
    echo "Get your service URL:"
    gcloud run services describe ifrs --platform managed --region us-central1 --format='value(status.url)'
    echo ""
}

railway_deploy() {
    echo ""
    echo -e "${BLUE}Railway Deployment${NC}"
    echo ""
    echo -e "${YELLOW}Manual steps (Railway handles everything):${NC}"
    echo ""
    echo "1. Go to https://railway.app"
    echo "2. Sign up with GitHub"
    echo "3. Create 'New Project'"
    echo "4. Select 'Deploy from GitHub'"
    echo "5. Authorize Railway and select this repository"
    echo "6. Railway auto-detects Dockerfile"
    echo "7. Set environment variables:"
    echo "   - ENVIRONMENT=production"
    echo "   - DEBUG=false"
    echo "8. Click Deploy!"
    echo ""
    echo "Your app will be live in 2-3 minutes with auto-updates on git push!"
    echo ""
    read -p "Ready? (yes to continue): " ready
}

render_deploy() {
    echo ""
    echo -e "${BLUE}Render Deployment${NC}"
    echo ""
    echo -e "${YELLOW}Manual steps:${NC}"
    echo ""
    echo "1. Go to https://render.com"
    echo "2. Sign up with GitHub"
    echo "3. Click 'New +' → 'Web Service'"
    echo "4. Select 'Deploy existing image'"
    echo "5. Enter Docker image: ghcr.io/your-username/ifrs:latest"
    echo "   (Or build from GitHub)"
    echo "6. Configure:"
    echo "   - Name: ifrs-app"
    echo "   - Region: Choose closest"
    echo "   - Plan: Free"
    echo "7. Set environment:"
    echo "   - ENVIRONMENT=production"
    echo "   - DEBUG=false"
    echo "8. Click 'Create Web Service'"
    echo ""
    echo "Your app will be live in 1-2 minutes!"
    echo ""
}

oracle_deploy() {
    echo ""
    echo -e "${BLUE}Oracle Cloud Always Free Deployment${NC}"
    echo ""
    echo -e "${YELLOW}Setup steps:${NC}"
    echo ""
    echo "1. Create Oracle Cloud account (always free tier):"
    echo "   https://www.oracle.com/cloud/free/"
    echo ""
    echo "2. Create VM Instance:"
    echo "   - Select: Compute > Instances > Create Instance"
    echo "   - Image: Ubuntu 20.04 LTS"
    echo "   - Shape: Ampere (always free)"
    echo "   - Click Create"
    echo ""
    echo "3. SSH into instance:"
    echo "   ssh ubuntu@<your-instance-ip>"
    echo ""
    echo "4. Install Docker:"
    echo "   sudo apt-get update"
    echo "   sudo apt-get install -y docker.io docker-compose"
    echo "   sudo usermod -aG docker ubuntu"
    echo ""
    echo "5. Clone and deploy:"
    echo "   git clone <your-repo>"
    echo "   cd Criminal\\ Identification"
    echo "   docker-compose up -d"
    echo ""
    echo "6. Open port 80 in firewall"
    echo ""
    echo "✓ Your app is now live and always free!"
    echo ""
}

ngrok_deploy() {
    echo ""
    echo -e "${BLUE}Local Deployment with Ngrok${NC}"
    echo ""
    
    # Check if docker-compose is running
    if ! docker ps > /dev/null 2>&1; then
        echo -e "${YELLOW}Docker not running. Starting docker-compose...${NC}"
        docker-compose up -d
        sleep 5
    fi
    
    echo -e "${YELLOW}Checking for ngrok...${NC}"
    if ! command -v ngrok &> /dev/null; then
        echo -e "${YELLOW}Ngrok not found. Installing...${NC}"
        echo ""
        echo "Option 1: Manual installation"
        echo "  Download from: https://ngrok.com/download"
        echo "  Extract and run: ngrok http 80"
        echo ""
        echo "Option 2: Using Homebrew (Mac)"
        echo "  brew install ngrok"
        echo "  ngrok http 80"
        echo ""
        echo "Option 3: Using apt (Linux)"
        echo "  sudo apt-get install ngrok"
        echo "  ngrok http 80"
        return
    fi
    
    echo -e "${YELLOW}Checking ngrok auth...${NC}"
    read -p "Enter your ngrok auth token (from https://dashboard.ngrok.com): " auth_token
    ngrok authtoken $auth_token
    
    echo ""
    echo -e "${GREEN}Starting ngrok...${NC}"
    echo ""
    echo "Your application will be available at the URL below:"
    echo ""
    ngrok http 80
}

show_comparison() {
    echo ""
    echo "==================== Platform Comparison ===================="
    echo ""
    printf "%-20s %-15s %-15s %-20s\n" "Platform" "Cost" "Setup Time" "Best For"
    printf "%-20s %-15s %-15s %-20s\n" "---" "---" "---" "---"
    printf "%-20s %-15s %-15s %-20s\n" "Google Cloud Run" "Free (2M req)" "20 min" "Production"
    printf "%-20s %-15s %-15s %-20s\n" "Railway" "\$5 credit/mo" "10 min" "Quick test"
    printf "%-20s %-15s %-15s %-20s\n" "Render" "Always free" "10 min" "Reliable"
    printf "%-20s %-15s %-15s %-20s\n" "Oracle Cloud" "Always free" "30 min" "Long-term"
    printf "%-20s %-15s %-15s %-20s\n" "Ngrok (Local)" "Free" "5 min" "Local test"
    printf "%-20s %-15s %-15s %-20s\n" "WSL + Docker" "Free" "10 min" "Dev/test"
    echo ""
    echo "Recommendation: Start with Railway or Render (easiest)"
    echo "For production: Google Cloud Run (best performance)"
    echo "For always free: Oracle Cloud (never expires)"
    echo ""
}

# Main loop
while true; do
    show_platforms
    
    case $choice in
        1)
            google_cloud_deploy
            ;;
        2)
            railway_deploy
            ;;
        3)
            render_deploy
            ;;
        4)
            oracle_deploy
            ;;
        5)
            ngrok_deploy
            ;;
        6)
            show_comparison
            ;;
        7)
            echo ""
            echo -e "${GREEN}For more info, check: FREE-DEPLOYMENT.md${NC}"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done
