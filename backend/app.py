import threading
import sys
import os
from pathlib import Path
import base64

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import cv2
import numpy as np
from fastapi import UploadFile, File, Response, Form

# Add parent directory to path so we can import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Change working directory to project root for proper data path resolution
project_root = Path(__file__).parent.parent
os.chdir(project_root)

# Now import backend modules
from backend.database import save_criminal, load_all_embeddings
from backend.face_recognizer import extract_face_and_embedding, get_embedding
import backend.camera_manager as camera_manager
from backend.alert_manager import ALERTS

# Initialize FastAPI app
app = FastAPI()

# Global surveillance state
surveillance_thread = None

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== API ENDPOINTS ====================

@app.get("/")
def root():
    """Root endpoint with API info"""
    return {
        "message": "Intelligent Face Recognition System API is running",
        "docs": "http://127.0.0.1:8000/docs"
    }


@app.get("/stats")
def get_stats():
    """Get system statistics"""
    try:
        criminals = load_all_embeddings()
        return {
            "connected_cameras": 1,  # webcam for now
            "total_criminals": len(criminals),
            "faces_detected_today": len(ALERTS),
            "criminals_detected": len(ALERTS),
            "surveillance_running": camera_manager.surveillance_running
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {
            "connected_cameras": 0,
            "total_criminals": 0,
            "faces_detected_today": 0,
            "criminals_detected": 0,
            "surveillance_running": camera_manager.surveillance_running,
            "error": str(e)
        }


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
                    except:
                        enhanced_alert['photo'] = None
                else:
                    enhanced_alert['photo'] = None
                
                # Add timestamp if missing
                if 'timestamp' not in enhanced_alert:
                    enhanced_alert['timestamp'] = enhanced_alert.get('time', None)
                
                enhanced_alerts.append(enhanced_alert)
        
        return enhanced_alerts
    except Exception as e:
        print(f"Error getting alerts: {e}")
        return []


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
                    print(f"Error reading photo for {name}: {e}")
            
            criminals_list.append(criminal_data)
        
        return criminals_list
    except Exception as e:
        print(f"Error getting criminals: {e}")
        return []


@app.post("/upload_criminal/")
async def upload_criminal(name: str = Form(...), file: UploadFile = File(...)):
    """Upload a criminal's face and add to database"""
    try:
        # Validate input
        if not name or not name.strip():
            return {"error": "Name cannot be empty"}
        
        if not file:
            return {"error": "No file provided"}

        # Read and decode image
        img_bytes = await file.read()
        img_np = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        if img is None:
            return {"error": "Invalid image format - could not decode"}

        # Check image dimensions
        if img.shape[0] < 50 or img.shape[1] < 50:
            return {"error": f"Image too small ({img.shape[0]}x{img.shape[1]}). Minimum 50x50 required"}

        print(f"Attempting to extract face from image: {img.shape}")
        
        # Extract face and embedding
        face, emb = extract_face_and_embedding(img)
        
        if face is None:
            print(f"❌ Face extraction failed for {name}")
            return {"error": "No face detected in image. Please ensure the image has a clear, front-facing face with good lighting"}
        
        if emb is None:
            print(f"❌ Embedding extraction failed for {name}")
            return {"error": "Could not create face embedding. Please try a clearer image"}

        print(f"✓ Face detected and embedding created for {name}")
        
        # Save to database
        save_criminal(name.strip(), face, emb)
        print(f"✓ Criminal {name} added to database")

        return {
            "status": "criminal added",
            "name": name.strip()
        }
    except Exception as e:
        print(f"❌ Error uploading criminal: {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"Failed to upload: {str(e)}"}


@app.get("/start_surveillance/")
def start_surveillance():
    """Start surveillance monitoring"""
    global surveillance_thread

    try:
        if camera_manager.surveillance_running:
            return {"status": "already running"}

        camera_manager.surveillance_running = True
        surveillance_thread = threading.Thread(target=camera_manager.process_cameras, daemon=True)
        surveillance_thread.start()
        return {"status": "surveillance started"}
    except Exception as e:
        print(f"Error starting surveillance: {e}")
        camera_manager.surveillance_running = False
        return {"error": f"Failed to start surveillance: {str(e)}"}


@app.get("/stop_surveillance/")
def stop_surveillance():
    """Stop surveillance monitoring"""
    try:
        camera_manager.surveillance_running = False
        return {"status": "surveillance stopped"}
    except Exception as e:
        print(f"Error stopping surveillance: {e}")
        return {"error": str(e)}


@app.get("/surveillance_status/")
def get_surveillance_status():
    """Get current surveillance status"""
    return {
        "running": camera_manager.surveillance_running,
        "alerts_count": len(ALERTS)
    }


@app.get("/camera_snapshot/")
def camera_snapshot():
    """Return the latest camera frame as JPEG"""
    try:
        data = getattr(camera_manager, 'LAST_FRAME', None)
        if not data:
            return JSONResponse({"error": "no_frame"}, status_code=204)
        # Ensure data is bytes, set explicit Content-Length to avoid h11 errors
        if isinstance(data, bytes):
            frame_bytes = data
        else:
            frame_bytes = bytes(data)
        return Response(content=frame_bytes, media_type='image/jpeg', headers={"Content-Length": str(len(frame_bytes))})
    except Exception as e:
        print(f"Error returning camera snapshot: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    import uvicorn
    print("Starting Intelligent Face Recognition System API...")
    print("API Docs: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)