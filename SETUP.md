# Setup Guide

Complete step-by-step guide to set up the Criminal Identification System in different environments.

## Table of Contents
- [Local Development (Windows, Mac, Linux)](#local-development)
- [Docker Setup (Recommended)](#docker-setup)
- [Production Checklist](#production-checklist)

---

## Local Development

### Windows

#### 1. Prerequisites
- Windows 10/11
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- Git ([Download](https://git-scm.com/))
- Webcam

#### 2. Clone Repository
```bash
# Open PowerShell in desired directory
git clone <repository-url>
cd "Criminal Identification"
```

#### 3. Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\activate
```

#### 4. Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r backend/requirements.txt

# Install development tools (optional)
pip install pytest pytest-cov black flake8
```

#### 5. Configure Environment
```bash
# Copy template
Copy-Item .env.example -Destination .env

# Edit .env with your settings (optional)
notepad .env
```

#### 6. First Run
```bash
# Start the backend server
python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

#### 7. Access Application
1. Open browser: `http://127.0.0.1:8000`
2. Allow camera access when prompted
3. Start adding criminals or surveillance

#### Troubleshooting Windows

**"Python is not recognized"**
- Check Python installation: `python --version`
- Add Python to PATH environment variable

**Camera permission denied**
- Run PowerShell as Administrator
- Settings > Privacy & Security > Camera > Allow

**Port 8000 already in use**
- Change port: `--port 8001`
- Or find process: `netstat -ano | findstr :8000`

---

### Mac

#### 1. Prerequisites
- macOS 10.14+
- Python 3.8+ 
- Git
- Webcam

#### 2. Clone Repository
```bash
git clone <repository-url>
cd Criminal\ Identification
```

#### 3. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate
```

#### 4. Install Dependencies
```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
pip install -r backend/requirements.txt

# Install development tools (optional)
pip install pytest pytest-cov black flake8
```

#### 5. Configure Environment
```bash
# Copy template
cp .env.example .env

# Edit .env (optional)
nano .env
```

#### 6. First Run
```bash
# Start the backend server
python3 -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

#### 7. Access Application
1. Open browser: `http://127.0.0.1:8000`
2. Allow camera access when prompted
3. Start using the system

#### Troubleshooting Mac

**"Permission denied" on virtual environment**
```bash
chmod +x .venv/bin/activate
```

**OpenCV/camera issues**
```bash
# Install additional dependencies
brew install opencv
pip install opencv-python-headless
```

**Port already in use**
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

---

### Linux (Ubuntu/Debian)

#### 1. Prerequisites
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3.8 python3-pip python3-venv git

# Install optional dependencies for OpenCV
sudo apt-get install -y libsm6 libxext6 libxrender-dev
```

#### 2. Clone Repository
```bash
git clone <repository-url>
cd Criminal\ Identification
```

#### 3. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

#### 5. Configure Environment
```bash
cp .env.example .env
# Edit .env
nano .env
```

#### 6. First Run
```bash
python3 -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

#### 7. Access Application
- Open browser: `http://127.0.0.1:8000`
- Allow camera access
- Start using

#### Troubleshooting Linux

**Camera permissions**
```bash
# Add user to video group
sudo usermod -a -G video $USER

# Logout and login for changes to take effect
exit
```

**Port already in use**
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

---

## Docker Setup

### Installation

#### Docker Desktop (Windows & Mac)
- Download: https://www.docker.com/products/docker-desktop
- Install and run Docker Desktop
- Verify: `docker --version` and `docker-compose --version`

#### Linux
```bash
# Install Docker
sudo apt-get install docker.io docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version
docker-compose --version
```

### Quick Start (All Platforms)

#### Method 1: Using Script (Easiest)

**Windows:**
```bash
# Run the batch file
.\run-docker.bat

# Follow the interactive menu
```

**Linux/Mac:**
```bash
# Make executable
chmod +x run-docker.sh

# Run the script
./run-docker.sh

# Follow the interactive menu
```

#### Method 2: Docker Compose (Direct)

```bash
# Start the application
docker-compose up -d

# Access:
# - Frontend: http://localhost
# - API: http://localhost:8000
# - Docs: http://localhost:8000/api/docs

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

#### Method 3: Manual Docker Commands

```bash
# Build image
docker build -t ifrs:latest .

# Run container
docker run -d \
  --name ifrs-app \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  ifrs:latest

# Check status
docker ps
docker logs ifrs-app
```

### Docker Troubleshooting

**Command not found**
```bash
# Windows PowerShell
& "C:\Program Files\Docker\Docker\resources\bin\docker" --version

# Or reinstall Docker Desktop
```

**Permission denied (Linux)**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
```

**Port already in use**
```bash
# Change port in docker-compose.yml
ports:
  - "8080:8000"

# Then docker-compose up -d
```

---

## Production Checklist

### Pre-Deployment

- [ ] Environment set to `ENVIRONMENT=production`
- [ ] Debug mode disabled: `DEBUG=false`
- [ ] CORS origins restricted to your domain
- [ ] SSL/HTTPS certificates configured
- [ ] Database backups configured
- [ ] Logging configured and tested
- [ ] Health checks verified: `curl http://localhost:8000/health`
- [ ] All dependencies updated
- [ ] Security scan passed

### Deployment

- [ ] Use Docker containers
- [ ] Use reverse proxy (Nginx)
- [ ] Enable HTTPS/SSL
- [ ] Configure firewalls
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Test failover procedures
- [ ] Document deployment process

### Post-Deployment

- [ ] Verify all endpoints working
- [ ] Test camera functionality
- [ ] Add test criminals to database
- [ ] Run surveillance test
- [ ] Check logs for errors
- [ ] Monitor performance metrics
- [ ] Set up alert notifications
- [ ] Schedule backups

### Security Hardening

```bash
# Update all dependencies
pip install --upgrade -r backend/requirements.txt

# Check for vulnerabilities
pip install safety
safety check

# Enable firewall
sudo ufw enable
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## Configuration Management

### Development Configuration
```bash
# .env file for development
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
API_RELOAD=true
CORS_ORIGINS=["*"]
SIMILARITY_THRESHOLD=0.50
```

### Production Configuration
```bash
# .env file for production
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
API_RELOAD=false
CORS_ORIGINS=["https://your-domain.com"]
SIMILARITY_THRESHOLD=0.55
ALERT_RETENTION_HOURS=72
API_WORKERS=8
```

---

## Next Steps

1. **Read** [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
2. **Check** [README.md](README.md) for features and usage
3. **Monitor** application health and logs
4. **Backup** criminal database regularly
5. **Update** dependencies regularly

---

## Support

- API Docs: `http://localhost:8000/api/docs`
- Project Issues: Check GitHub issues
- Configuration Help: See `.env.example`
- Deployment Help: See `DEPLOYMENT.md`

---

**Fresh installation should take 5-10 minutes!** ⚡
