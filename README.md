# Intelligent Face Recognition System (IFRS)

A real-time face detection and recognition system using FastAPI and OpenCV.

## 🚀 Quick Start

### Deploy for FREE (10 minutes)

**Windows:**
```bash
deploy-free.bat
```

**Linux/Mac:**
```bash
chmod +x deploy-free.sh
./deploy-free.sh
```

Or read [FREE-DEPLOYMENT.md](FREE-DEPLOYMENT.md) for detailed free deployment options.

### Using Docker (Local)

**Windows:**
```bash
.\run-docker.bat
```

**Linux/Mac:**
```bash
chmod +x run-docker.sh
./run-docker.sh
```

**Or manually:**
```bash
docker-compose up -d
# Access at http://localhost
```

### Local Development

1. Clone repository:
```bash
git clone <repository-url>
cd Criminal\ Identification
```

2. Windows setup:
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

2. Linux/Mac setup:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python3 -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

3. Open `frontend/index.html` in your web browser
4. Access API at: http://127.0.0.1:8000

## Prerequisites

- Python 3.8+
- Webcam or camera device
- Modern web browser
- Docker & Docker Compose (for containerized deployment)

## Features

- **Real-time Surveillance** - Live face detection using your webcam
- **Criminal Recognition** - Match detected faces against a database of criminals
- **Alert System** - Get alerted when a criminal is detected
- **Add Criminals** - Upload criminal mugshots to the database
- **View Records** - Browse all criminal records with photos
- **Production Ready** - Docker, HTTPS, monitoring, and scaling ready
- **Free Deployment** - Deploy to cloud for free with no upfront costs

## Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── app.py              # Main API server
│   ├── camera_manager.py   # Camera and surveillance logic
│   ├── face_recognizer.py  # Face detection & embedding
│   ├── matcher.py          # Face matching algorithm
│   ├── database.py         # Criminal database management
│   ├── alert_manager.py    # Alert handling
│   └── requirements.txt    # Python dependencies
├── frontend/               # Web interface
│   ├── index.html         # Main page
│   ├── js/                # JavaScript files
│   └── css/               # Stylesheets
├── data/                   # Data directory
│   ├── criminal_faces/    # Criminal mugshots
│   └── embeddings/        # Face embeddings cache
├── models/                # Pre-trained models
│   └── arcface.onnx       # ArcFace model
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker orchestration
├── nginx.conf             # Production web server config
└── docs/                  # Documentation
```

## API Endpoints

### Surveillance
- `GET /start_surveillance/` - Start camera monitoring
- `GET /stop_surveillance/` - Stop camera monitoring
- `GET /surveillance_status/` - Get current status
- `GET /camera_snapshot/` - Get latest camera frame

### Alerts & Data
- `GET /alerts` - Get all detected alerts
- `GET /criminals` - Get all criminals in database
- `POST /upload_criminal/` - Add new criminal to database
- `GET /stats` - Get system statistics

### System
- `GET /health` - Health check endpoint
- `GET /` - API status
- `GET /api/docs` - Interactive API documentation (dev only)

## Configuration

See `.env.example` for all available configuration options.

Key settings:
```bash
ENVIRONMENT=development|production
DEBUG=true|false
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
SIMILARITY_THRESHOLD=0.50     # Adjust sensitivity (0.0-1.0)
FRAME_SKIP=2                  # Process every Nth frame
API_WORKERS=4                 # For production
```

## Documentation

- **[FREE-DEPLOYMENT.md](FREE-DEPLOYMENT.md)** - Deploy for free on cloud platforms
- **[SETUP.md](SETUP.md)** - Complete setup guide for all platforms
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[README-DEPLOYMENT.md](README-DEPLOYMENT.md)** - Comprehensive feature documentation

## Troubleshooting

### Camera Not Opening
- Ensure your webcam is connected and not being used by another application
- Try changing `CAMERA_SOURCES` in `.env`

### Face Not Detected
- Ensure good lighting
- Keep face clearly visible to camera
- Faces must be reasonably sized (not too far away)

### Port 8000 Already in Use

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -i :8000
kill -9 <PID>
```

### Docker Issues

```bash
# View logs
docker-compose logs -f api

# Rebuild image
docker-compose build --no-cache

# Clean up and restart
docker-compose down -v
docker-compose up -d
```

## Free Cloud Deployment

Get your app online for FREE in 10-20 minutes:

| Platform | Cost | Time | Best For |
|----------|------|------|----------|
| **Google Cloud Run** | Free (2M req/month) | 20 min | Production |
| **Railway** | $5 credit/month | 10 min | Quick test |
| **Render** | Always free | 10 min | Reliable |
| **Oracle Cloud** | Always free | 30 min | Long-term |

See [FREE-DEPLOYMENT.md](FREE-DEPLOYMENT.md) for step-by-step guides.

## Production Deployment

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md) for:
- AWS EC2, Google Cloud, Azure setup
- SSL/HTTPS configuration
- Performance optimization
- Monitoring and scaling
- Security best practices

## Security Best Practices

1. Always use HTTPS in production
2. Restrict CORS origins to your domain
3. Keep dependencies updated: `pip install --upgrade -r backend/requirements.txt`
4. Regular backups of criminal database
5. Monitor logs for suspicious activity

## Technology Stack

- **Backend:** FastAPI, OpenCV, InsightFace, ONNX Runtime
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **DevOps:** Docker, Docker Compose, Nginx

## License

This project is licensed under the MIT License.

## Support

- **Free Deployment:** See [FREE-DEPLOYMENT.md](FREE-DEPLOYMENT.md)
- **Setup help:** See [SETUP.md](SETUP.md)
- **Deployment help:** See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Features:** See [README-DEPLOYMENT.md](README-DEPLOYMENT.md)
- **API docs:** http://localhost:8000/api/docs (development)

---

**Version:** 1.0.0 | **Status:** Production Ready ✅ | **Deploy for Free:** 🚀

- Lower the `SIMILARITY_THRESHOLD` in `backend/config.py` if threshold is too high (default: 0.65)

## Configuration

Edit `backend/config.py` to customize:
- `SIMILARITY_THRESHOLD` - How similar faces must be to trigger alert (0-1, default: 0.65)
- `FRAME_SKIP` - Skip frames for better performance (default: 5)
- `CAMERA_SOURCES` - Camera device IDs (default: [0])

## Notes

- The system uses ArcFace embeddings for robust face recognition
- MTCNN is used for real-time face detection
- Face embeddings are cached for faster matching
- Alerts prevent duplicate detections within 5 seconds

## License

This project is provided as-is for educational and research purposes.
