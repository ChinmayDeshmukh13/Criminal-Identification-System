# Intelligent Face Recognition System (IFRS)

A real-time face detection and recognition system using FastAPI and OpenCV.

## Quick Start

### Windows
1. Double-click `START.bat` to start the server
2. Open `frontend/index.html` in your web browser
3. The API will be available at http://127.0.0.1:8000

### Linux/Mac
1. Run `./start.sh` to start the server
2. Open `frontend/index.html` in your web browser
3. The API will be available at http://127.0.0.1:8000

## Prerequisites

- Python 3.8+
- Webcam or camera device
- Modern web browser

## Features

- **Real-time Surveillance**: Live face detection using your webcam
- **Criminal Recognition**: Match detected faces against a database of criminals
- **Alert System**: Get alerted when a criminal is detected
- **Add Criminals**: Upload criminal mugshots to the database
- **View Records**: Browse all criminal records with photos

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
└── models/                # Pre-trained models
    └── arcface.onmx       # ArcFace model for embeddings

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
- `GET /` - API status
- `GET /docs` - Interactive API documentation

## Setup

### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Add a Criminal

Use the web interface to upload a criminal's photo:
1. Go to "Add Criminal" page
2. Enter name and upload mugshot
3. The system will extract face and create embedding automatically

## Troubleshooting

### Camera Not Opening
- Ensure your webcam is connected and not being used by another application
- Try changing `CAMERA_SOURCES` in `backend/config.py`

### Face Not Detected
- Ensure good lighting
- Keep face clearly visible to camera
- Faces must be reasonably sized (not too far away)

### No Alerts After Detection
- Check that criminals are added to the database
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
