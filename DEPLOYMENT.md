# Deployment Guide

This document provides comprehensive instructions for deploying the Intelligent Face Recognition System (IFRS) to production.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Production Configuration](#production-configuration)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **CPU:** Multi-core processor (4+ cores recommended)
- **RAM:** 4GB minimum (8GB+ recommended for production)
- **Storage:** 20GB free space (for criminal database and logs)
- **GPU:** NVIDIA GPU optional (for faster face processing)

### Software Requirements
- **Python:** 3.8 or higher
- **Docker:** 20.10+ (for containerized deployment)
- **Docker Compose:** 1.29+ (for multi-container deployment)

### Network Requirements
- Port 80 (HTTP)
- Port 443 (HTTPS - for production)
- Port 8000 (Backend API - for development)

---

## Local Development Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Criminal\ Identification
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
pip install python-dotenv
```

### 4. Configure Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# Set ENVIRONMENT=development for local testing
```

### 5. Run the Application
```bash
# Start backend server
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000

# In another terminal, open frontend
# Open frontend/index.html in your web browser
# Access at http://localhost:8000
```

---

## Docker Deployment

### 1. Build Docker Image
```bash
# Build the image
docker build -t ifrs:latest .

# Or with a specific version tag
docker build -t ifrs:v1.0 .
```

### 2. Run Single Container
```bash
# Run with environment variables
docker run -d \
  --name ifrs-app \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -e ENVIRONMENT=production \
  -e DEBUG=false \
  ifrs:latest

# Check logs
docker logs -f ifrs-app
```

### 3. Docker Compose (Recommended)
```bash
# Start the stack with Nginx and API
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the stack
docker-compose down

# Backup data before stopping
docker-compose exec api tar -czf /app/backup.tar.gz /app/data
```

### Environment Configuration for Docker
Edit environment variables in `docker-compose.yml`:
```yaml
environment:
  - ENVIRONMENT=production
  - DEBUG=false
  - LOG_LEVEL=INFO
  - API_WORKERS=4
  - SIMILARITY_THRESHOLD=0.50
```

---

## Cloud Deployment

### AWS EC2 Deployment

#### 1. Launch EC2 Instance
- AMI: Ubuntu 20.04 LTS
- Instance Type: t3.medium (minimum)
- Security Groups: Allow ports 80, 443, 22

#### 2. Install Docker
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
```

#### 3. Deploy Application
```bash
# Clone repository
git clone <repository-url> && cd Criminal\ Identification

# Start with Docker Compose
docker-compose up -d

# Ensure Nginx is running
docker-compose ps
```

#### 4. Configure SSL Certificate
```bash
# Using Let's Encrypt
sudo apt-get install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates to certs directory
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./certs/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./certs/key.pem

# Update nginx.conf HTTPS block with your domain
# Uncomment HTTPS configuration and restart
docker-compose restart nginx
```

### Google Cloud Platform

#### 1. Create Cloud VM
- OS: Ubuntu 20.04 LTS
- Machine Type: e2-medium

#### 2. Deploy via Cloud Run
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/ifrs

# Deploy
gcloud run deploy ifrs \
  --image gcr.io/PROJECT_ID/ifrs \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production
```

### Azure Deployment

#### 1. Create Container Instance
```bash
# Create resource group
az group create --name ifrs-rg --location eastus

# Deploy container
az container create \
  --resource-group ifrs-rg \
  --name ifrs-api \
  --image ifrs:latest \
  --cpu 2 --memory 4 \
  --environment-variables ENVIRONMENT=production
```

---

## Production Configuration

### 1. Environment Variables
Create a `.env` file in the project root:
```bash
# Application
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Server
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_RELOAD=false

# CORS (restrict to your domain in production)
CORS_ORIGINS=["https://your-domain.com"]

# Face Recognition
SIMILARITY_THRESHOLD=0.50
FRAME_SKIP=2
CAMERA_SOURCES=[0]

# Database
DATA_DIR=/app/data
CRIMINAL_FACES_DIR=/app/data/criminal_faces
EMBEDDINGS_DIR=/app/data/embeddings

# Security
ALLOWED_FILE_EXTENSIONS=jpg,jpeg,png,gif
MAX_UPLOAD_SIZE_MB=10
```

### 2. SSL/HTTPS Configuration
Edit `nginx.conf` to enable HTTPS:
```nginx
# Uncomment and configure the server block with SSL
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/certs/cert.pem;
    ssl_certificate_key /etc/nginx/certs/key.pem;
    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### 3. Performance Tuning
- **Worker Processes:** `API_WORKERS=4` (or 2 per CPU core)
- **Frame Skip:** Increase to 3-4 for faster processing, decrease for accuracy
- **Similarity Threshold:** Adjust 0.40-0.60 based on false positive rate

### 4. Database Backups
```bash
# Backup data directory
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# In Docker
docker-compose exec api tar -czf backup.tar.gz data/
docker cp ifrs-api:/app/backup.tar.gz ./
```

---

## Monitoring and Maintenance

### 1. Health Checks
```bash
# Check API health
curl http://localhost:8000/health

# Docker health status
docker-compose ps

# View logs
docker-compose logs -f api
```

### 2. Performance Monitoring
```bash
# Monitor CPU and memory usage
docker stats

# View API logs for errors
docker logs ifrs-api | grep ERROR
```

### 3. Regular Maintenance
- **Daily:** Monitor logs for errors
- **Weekly:** Backup criminal database
- **Monthly:** Review and optimize similarity threshold
- **Quarterly:** Update dependencies and models

### 4. Scaling
```bash
# Horizontal scaling with multiple workers
# Increase API_WORKERS in docker-compose.yml
API_WORKERS: 8

# Or scale with multiple containers (with load balancer)
docker-compose up -d --scale api=3
```

---

## Troubleshooting

### API Won't Start
```bash
# Check logs
docker logs ifrs-api

# Verify ports are available
netstat -tulpn | grep 8000

# Restart container
docker-compose restart api
```

### Camera Not Working
- **Issue:** "No camera connected" error
- **Solution:** 
  - Check `CAMERA_SOURCES` in `.env`
  - For Docker, add: `--device /dev/video0:/dev/video0`
  - Test camera access directly

### Face Detection Not Working
- **Issue:** Faces not being detected
- **Solution:**
  - Improve lighting conditions
  - Try different image sizes
  - Lower `SIMILARITY_THRESHOLD` in config
  - Check model files exist in `models/` directory

### High Memory Usage
- **Issue:** Memory usage keeps increasing
- **Solution:**
  - Limit `MAX_ALERTS` in configuration
  - Restart API: `docker-compose restart api`
  - Implement alert cleanup: `ALERT_RETENTION_HOURS=24`

### Nginx Port Already in Use
```bash
# Find process using port 80
lsof -i :80

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8080:80"  # Use 8080 instead
```

---

## Security Best Practices

1. **Always use HTTPS in production**
2. **Restrict CORS origins** to your domain
3. **Use strong passwords** for any admin access
4. **Keep dependencies updated:**
   ```bash
   pip install --upgrade -r backend/requirements.txt
   ```
5. **Regular backups** of criminal database
6. **Monitor logs** for suspicious activity
7. **Use environment variables** for sensitive data
8. **Keep Docker images updated:**
   ```bash
   docker pull python:3.11-slim
   docker build --no-cache .
   ```

---

## Support and Troubleshooting

For detailed logs:
```bash
# Enable debug logging
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# Check specific component logs
docker logs ifrs-api | grep "face_recognizer"
docker logs ifrs-api | grep "camera_manager"
```

For the API documentation:
```
http://your-domain.com/api/docs
```

---

Happy Deployment! 🚀
