import threading
import sys
import os
import logging
from pathlib import Path
import base64
from datetime import datetime

from fastapi import FastAPI, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np
from fastapi import UploadFile, File, Response, Form

# Add parent directory to path so we can import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Change working directory to project root for proper data path resolution
project_root = Path(__file__).parent.parent
os.chdir(project_root)

# Import configuration
from backend.config import (
    ENVIRONMENT, DEBUG, VERSION, API_HOST, API_PORT,
    CORS_ORIGINS, LOG_LEVEL, SIMILARITY_THRESHOLD
)

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Now import backend modules
from backend.database import save_criminal, load_all_embeddings
from backend.face_recognizer import extract_face_and_embedding, get_embedding
import backend.camera_manager as camera_manager
from backend.alert_manager import ALERTS

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Intelligent Face Recognition System API",
    description="Real-time face detection and criminal recognition",
    version=VERSION,
    docs_url="/api/docs" if ENVIRONMENT != "production" else None,
    redoc_url="/api/redoc" if ENVIRONMENT != "production" else None,
)

# Global surveillance state
surveillance_thread = None
app_start_time = datetime.utcnow()

# Configure CORS based on environment
cors_origins = CORS_ORIGINS if isinstance(CORS_ORIGINS, list) else ["*"]
logger.info(f"Configuring CORS with origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files if available
frontend_path = project_root / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    logger.info(f"Frontend static files mounted from {frontend_path}")

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Called when the application starts"""
    logger.info(f"Starting Intelligent Face Recognition System API (v{VERSION})")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info(f"Log level: {LOG_LEVEL}")

@app.on_event("shutdown")
async def shutdown_event():
    """Called when the application shuts down"""
    logger.info("Shutting down Intelligent Face Recognition System API")
    if camera_manager.surveillance_running:
        camera_manager.surveillance_running = False

# ==================== API ENDPOINTS ====================

@app.get("/health")
def health_check():
    """Health check endpoint for load balancers and monitoring"""
    try:
        criminals = load_all_embeddings()
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": (datetime.utcnow() - app_start_time).total_seconds(),
            "environment": ENVIRONMENT,
            "version": VERSION,
            "database": {
                "criminals_loaded": len(criminals) if criminals else 0,
                "accessible": True
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }, 503

@app.get("/")
def root():
    """Root endpoint with API info"""
    return {
        "message": "Intelligent Face Recognition System API is running",
        "version": VERSION,
        "environment": ENVIRONMENT,
        "docs": "/api/docs" if ENVIRONMENT != "production" else None,
        "health": "/health"
    }

@app.get("/api/info")
def api_info():
    """Get API information"""
    return {
        "name": "Intelligent Face Recognition System",
        "version": VERSION,
        "environment": ENVIRONMENT,
        "description": "Real-time face detection and criminal recognition system"
    }


@app.get("/stats")
def get_stats():
    """Get system statistics"""
    try:
        criminals = load_all_embeddings()
        stats = {
            "connected_cameras": 1,  # webcam for now
            "total_criminals": len(criminals) if criminals else 0,
            "faces_detected_today": len(ALERTS),
            "criminals_detected": len(ALERTS),
            "surveillance_running": camera_manager.surveillance_running
        }
        logger.info(f"Stats requested: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {
            "connected_cameras": 0,
            "total_criminals": 0,
            "faces_detected_today": 0,
            "criminals_detected": 0,
            "surveillance_running": camera_manager.surveillance_running,
            "error": str(e)
        }, 500


@app.get("/alerts")
def get_alerts():
    """Get all alerts"""
    try:
        # Enhance alerts with criminal photos
        enhanced_alerts = []
        if isinstance(ALERTS, list):
            for alert in ALERTS:
                enhanced_alert = dict(alert)
                # Try to load criminal photo
                face_path = f"data/criminal_faces/{alert.get('name', '')}.jpg"
                if os.path.exists(face_path):
                    try:
                        with open(face_path, 'rb') as f:
                            photo_data = base64.b64encode(f.read()).decode('utf-8')
                            enhanced_alert['photo'] = photo_data
                    except Exception as e:
                        logger.warning(f"Could not load photo for {alert.get('name')}: {e}")
                        enhanced_alert['photo'] = None
                else:
                    enhanced_alert['photo'] = None
                
                # Add timestamp if missing
                if 'timestamp' not in enhanced_alert:
                    enhanced_alert['timestamp'] = enhanced_alert.get('time', None)
                
                enhanced_alerts.append(enhanced_alert)
        
        logger.info(f"Alerts requested: {len(enhanced_alerts)} alerts found")
        return enhanced_alerts
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return [], 500


@app.get("/criminals")
def get_criminals():
    """Get all criminals in database with photos"""
    try:
        criminals_list = []
        embeddings = load_all_embeddings()
        
        for name in embeddings.keys():
            face_path = f"data/criminal_faces/{name}.jpg"
            criminal_data = {
                "name": name,
                "photo": None,
                "added_date": None
            }
            
            # Load criminal photo
            if os.path.exists(face_path):
                try:
                    with open(face_path, 'rb') as f:
                        photo_data = base64.b64encode(f.read()).decode('utf-8')
                        criminal_data['photo'] = photo_data
                        # Get file modification time
                        mod_time = os.path.getmtime(face_path)
                        criminal_data['added_date'] = mod_time
                except Exception as e:
                    logger.warning(f"Error reading photo for {name}: {e}")
            
            criminals_list.append(criminal_data)
        
        logger.info(f"Criminals requested: {len(criminals_list)} criminals in database")
        return criminals_list
    except Exception as e:
        logger.error(f"Error getting criminals: {e}")
        return [], 500


@app.post("/upload_criminal/")
async def upload_criminal(name: str = Form(...), file: UploadFile = File(...)):
    """Upload a criminal's face and add to database"""
    try:
        # Validate input
        if not name or not name.strip():
            logger.warning("Upload attempt with empty name")
            return {"error": "Name cannot be empty"}, 400
        
        if not file:
            logger.warning("Upload attempt without file")
            return {"error": "No file provided"}, 400

        # Read and decode image
        img_bytes = await file.read()
        img_np = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        if img is None:
            logger.warning(f"Invalid image format for {name}")
            return {"error": "Invalid image format - could not decode"}, 400

        # Check image dimensions
        if img.shape[0] < 50 or img.shape[1] < 50:
            logger.warning(f"Image too small for {name}: {img.shape}")
            return {"error": f"Image too small ({img.shape[0]}x{img.shape[1]}). Minimum 50x50 required"}, 400

        logger.info(f"Processing image for {name}: {img.shape}")
        
        # Extract face and embedding
        face, emb = extract_face_and_embedding(img)
        
        if face is None:
            logger.warning(f"Face extraction failed for {name}")
            return {"error": "No face detected in image. Please ensure the image has a clear, front-facing face with good lighting"}, 422
        
        if emb is None:
            logger.warning(f"Embedding extraction failed for {name}")
            return {"error": "Could not create face embedding. Please try a clearer image"}, 422

        logger.info(f"Face detected and embedding created for {name}")
        
        # Save to database
        save_criminal(name.strip(), face, emb)
        logger.info(f"Criminal {name} added to database successfully")

        return {
            "status": "criminal added",
            "name": name.strip()
        }, 201
    except Exception as e:
        logger.error(f"Error uploading criminal {name}: {e}", exc_info=True)
        return {"error": f"Failed to upload: {str(e)}"}, 500


@app.get("/start_surveillance/")
def start_surveillance():
    """Start surveillance monitoring"""
    global surveillance_thread

    try:
        if camera_manager.surveillance_running:
            logger.info("Surveillance already running")
            return {"status": "already running"}, 200

        logger.info("Starting surveillance")
        camera_manager.surveillance_running = True
        surveillance_thread = threading.Thread(target=camera_manager.process_cameras, daemon=True)
        surveillance_thread.start()
        logger.info("Surveillance started successfully")
        return {"status": "surveillance started"}, 200
    except Exception as e:
        logger.error(f"Error starting surveillance: {e}", exc_info=True)
        camera_manager.surveillance_running = False
        return {"error": f"Failed to start surveillance: {str(e)}"}, 500


@app.get("/stop_surveillance/")
def stop_surveillance():
    """Stop surveillance monitoring"""
    try:
        logger.info("Stopping surveillance")
        camera_manager.surveillance_running = False
        logger.info("Surveillance stopped successfully")
        return {"status": "surveillance stopped"}, 200
    except Exception as e:
        logger.error(f"Error stopping surveillance: {e}", exc_info=True)
        return {"error": str(e)}, 500


@app.get("/surveillance_status/")
def get_surveillance_status():
    """Get current surveillance status"""
    return {
        "running": camera_manager.surveillance_running,
        "alerts_count": len(ALERTS)
    }, 200


@app.get("/camera_snapshot/")
def camera_snapshot():
    """Return the latest camera frame as JPEG"""
    try:
        data = getattr(camera_manager, 'LAST_FRAME', None)
        if not data:
            logger.debug("No frame available for snapshot")
            return JSONResponse({"error": "no_frame"}, status_code=204)
        # Ensure data is bytes, set explicit Content-Length to avoid h11 errors
        if isinstance(data, bytes):
            frame_bytes = data
        else:
            frame_bytes = bytes(data)
        return Response(content=frame_bytes, media_type='image/jpeg', headers={"Content-Length": str(len(frame_bytes))})
    except Exception as e:
        logger.error(f"Error returning camera snapshot: {e}", exc_info=True)
        return JSONResponse({"error": str(e)}, status_code=500)


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    import uvicorn
    logger.info("=" * 60)
    logger.info("Starting Intelligent Face Recognition System API")
    logger.info(f"Version: {VERSION}")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Host: {API_HOST}")
    logger.info(f"Port: {API_PORT}")
    logger.info("=" * 60)
    
    if ENVIRONMENT == "development":
        logger.info("Running in DEVELOPMENT mode with auto-reload")
        uvicorn.run(
            "backend.app:app",
            host=API_HOST,
            port=API_PORT,
            reload=True,
            log_level=LOG_LEVEL.lower()
        )
    else:
        logger.info("Running in PRODUCTION mode")
        uvicorn.run(
            app,
            host=API_HOST,
            port=API_PORT,
            log_level=LOG_LEVEL.lower()
        )
