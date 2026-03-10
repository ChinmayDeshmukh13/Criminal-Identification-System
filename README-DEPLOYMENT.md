# Intelligent Face Recognition System (IFRS)

A production-ready real-time face detection and recognition system using FastAPI, OpenCV, and deep learning.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Features

### Core Capabilities
- **🎯 Real-time Face Detection** - Live surveillance with face detection using your webcam
- **🔍 Criminal Recognition** - Match detected faces against a database of known criminals  
- **🚨 Instant Alerts** - Automatic notifications when a criminal is detected
- **📊 Database Management** - Upload, organize, and manage criminal records with photos
- **📈 System Statistics** - Real-time monitoring of detections and system health
- **🔐 Secure Processing** - Encrypted embeddings and secure file handling

### Deployment Ready
- **🐳 Docker & Docker Compose** - Instant containerized deployment
- **☁️ Cloud Deploy** - AWS, GCP, Azure compatible
- **🔒 HTTPS/SSL Support** - Production-grade security
- **📊 Health Monitoring** - Built-in health checks and monitoring
- **🚀 Auto-scaling** - Load balancer ready
- **📝 Comprehensive Logging** - Debug and production logging

## Quick Start

### Prerequisites
- **Docker & Docker Compose** (recommended)
- **Python 3.8+** (for local development)
- **Webcam/Camera device**
- **Modern web browser** (Chrome, Firefox, Edge, Safari)

### Option 1: Docker (Recommended)

#### Windows
```bash
# Double-click run-docker.bat
# Or from PowerShell
.\run-docker.bat
```

#### Linux/Mac
```bash
# Make script executable
chmod +x run-docker.sh

# Run script
./run-docker.sh
```

#### Manual Docker Compose
```bash
# Start the application
docker-compose up -d

# Access the application
# - Frontend: http://localhost
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/api/docs

# View logs
docker-compose logs -f api

# Stop the application
docker-compose down
```

### Option 2: Local Python Development

#### Windows
```bash
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the application
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000

# In another terminal, open frontend
# Open frontend/index.html in your browser
```

#### Linux/Mac
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the application
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000

# In another terminal, open frontend
# Open frontend/index.html in your browser
```

## Usage

### 1. Add Criminals to Database
1. Navigate to "Add Criminal" page
2. Enter the criminal's name
3. Upload a clear facial mugshot (JPG, PNG)
4. System will extract face and create embedding automatically

### 2. Start Surveillance
1. Go to "Surveillance" tab
2. Click "Start Surveillance"
3. System will monitor webcam feed in real-time
4. Displays detected faces with confidence scores

### 3. View Alerts
1. When a criminal is detected, an immediate alert appears
2. Go to "Alerts" tab to see all historical alerts
3. Each alert shows criminal photo and detection timestamp

### 4. Criminal Records
1. Browse all stored criminal records
2. View photos and modification dates
3. Search for specific criminals

## Project Structure

```
Criminal Identification/
├── backend/                    # FastAPI Backend
│   ├── app.py                 # Main API server
│   ├── config.py              # Configuration management
│   ├── camera_manager.py       # Camera and surveillance logic
│   ├── face_recognizer.py      # Face detection & embedding
│   ├── matcher.py              # Face matching algorithm
│   ├── database.py             # Criminal database management
│   ├── alert_manager.py        # Alert handling
│   └── requirements.txt         # Python dependencies
│
├── frontend/                   # Web Interface
│   ├── index.html             # Main page
│   ├── css/
│   │   └── style.css          # Styling
│   └── js/
│       ├── api.js             # API communication
│       ├── config.js          # Frontend config
│       ├── home.js            # Home page logic
│       ├── surveillance.js    # Surveillance page
│       ├── add-criminal.js    # Add criminal page
│       └── navigation.js      # Navigation logic
│
├── data/                       # Data Directory
│   ├── criminal_faces/        # Criminal mugshots
│   └── embeddings/            # Face embeddings cache
│
├── models/                     # Pre-trained Models
│   └── arcface.onnx           # ArcFace model
│
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Multi-container orchestration
├── nginx.conf                  # Web server configuration
├── .env.example                # Environment variables template
├── .env                        # Local environment (git-ignored)
├── DEPLOYMENT.md               # Detailed deployment guide
└── run-docker.{sh,bat}        # Docker convenience scripts
```

## API Endpoints

### Health & Status
- `GET /health` - Health check for monitoring
- `GET /` - API status
- `GET /api/info` - API information
- `GET /stats` - System statistics

### Surveillance
- `GET /start_surveillance/` - Start camera monitoring
- `GET /stop_surveillance/` - Stop camera monitoring
- `GET /surveillance_status/` - Get current status
- `GET /camera_snapshot/` - Get latest camera frame

### Criminals & Alerts
- `GET /criminals` - Get all criminals with photos
- `POST /upload_criminal/` - Add new criminal to database
- `GET /alerts` - Get all detected alerts

### Interactive Documentation
- `GET /api/docs` - Swagger UI (development only)
- `GET /api/redoc` - ReDoc documentation

## Configuration

### Environment Variables
Configure via `.env` file (see `.env.example`):

```bash
# Application
ENVIRONMENT=production        # development or production
DEBUG=false                   # Enable/disable debug mode
LOG_LEVEL=INFO               # Log level

# Server
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_RELOAD=false

# Face Recognition
SIMILARITY_THRESHOLD=0.50    # Adjust sensitivity (0.0-1.0)
FRAME_SKIP=2                 # Process every Nth frame

# Security
ALLOWED_FILE_EXTENSIONS=jpg,jpeg,png,gif
MAX_UPLOAD_SIZE_MB=10
```

## Deployment

### Docker Deployment (Production)
```bash
# Set environment to production
ENVIRONMENT=production docker-compose up -d

# Or edit docker-compose.yml and set ENVIRONMENT=production
docker-compose up -d
```

### Cloud Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides:
- **AWS EC2** with SSL/HTTPS
- **Google Cloud Platform** with Cloud Run
- **Azure Container Instances**

### Production Checklist
- ✅ Set `ENVIRONMENT=production` in `.env`
- ✅ Disable `DEBUG=false`
- ✅ Configure SSL/HTTPS certificates
- ✅ Restrict CORS origins to your domain
- ✅ Set up backups for criminal database
- ✅ Configure monitoring and logging
- ✅ Use strong authentication if added
- ✅ Regular security updates

## Troubleshooting

### Camera Not Working
```bash
# Check camera device
ls /dev/video*              # Linux
Get-PnpDevice -Class Camera # Windows

# For Docker, ensure camera access
docker run --device /dev/video0 ifrs:latest
```

### Face Not Detected
- Improve lighting conditions
- Position face clearly in frame
- Ensure face is at least 50x50 pixels
- Adjust `SIMILARITY_THRESHOLD` lower for sensitivity

### High Memory Usage
- Limit `MAX_ALERTS` in configuration
- Reduce `API_WORKERS` value
- Implement scheduled cleanup of old alerts

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000              # Linux/Mac
netstat -ano | findstr 8000 # Windows

# Change port in docker-compose.yml
ports:
  - "8080:8000"  # Use 8080 instead
```

## Performance Optimization

### For Better Detection
- Frame Skip: 1-2 (more frames processed)
- Threshold: 0.40-0.50 (more sensitive)
- Better lighting and camera quality

### For Better Performance
- Frame Skip: 2-4 (fewer frames processed)
- Threshold: 0.55-0.60 (stricter matching)
- Multiple workers: `API_WORKERS=8`

## Advanced Topics

### Custom CORS Configuration
Edit `.env`:
```bash
CORS_ORIGINS=["https://your-domain.com", "https://app.your-domain.com"]
```

### Enable HTTPS
Edit `nginx.conf` and add your SSL certificates to `certs/` directory.

### Database Backup
```bash
# Backup criminal faces and embeddings
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Restore from backup
tar -xzf backup-*.tar.gz
```

### Monitoring
```bash
# Check API health
curl http://localhost:8000/health

# View container stats
docker stats

# View logs
docker logs -f ifrs-api
```

## Security Considerations

1. **Always use HTTPS** in production
2. **Restrict CORS origins** to your domain
3. **Keep dependencies updated**: `pip install --upgrade -r backend/requirements.txt`
4. **Regular backups** of criminal database
5. **Monitor logs** for suspicious activity
6. **Use environment variables** for sensitive data
7. **Implement authentication** if exposing to public

## Technology Stack

### Backend
- **FastAPI** - Modern Python async web framework
- **OpenCV** - Computer vision library
- **InsightFace** - Face detection and recognition
- **ONNX Runtime** - Model inference engine
- **Uvicorn** - Production Python server

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **Vanilla JavaScript** - Client-side logic
- **Fetch API** - Server communication

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Orchestration
- **Nginx** - Production web server

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

For API documentation, visit http://localhost:8000/api/docs (development mode)

For issues and bug reports, please open an issue on GitHub.

---

**Version**: 1.0.0  
**Last Updated**: March 2026  
**Status**: Production Ready ✅
