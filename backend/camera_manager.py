import sys
import time
import threading
from pathlib import Path
import cv2
from backend.face_detector import detect_faces
from backend.face_recognizer import get_embedding
from backend.matcher import match_face
from backend.database import load_all_embeddings
from backend.alert_manager import send_alert
from backend.config import CAMERA_SOURCES, FRAME_SKIP, SIMILARITY_THRESHOLD

# Global for tracking surveillance state
surveillance_thread = None
LAST_FRAME = None
surveillance_running = False  # NEW: Shared flag for the thread

def process_cameras():
    """Process video from camera sources for face recognition"""
    global surveillance_running, LAST_FRAME
    
    try:
        db = load_all_embeddings()
        if not db:
            print("WARNING: No criminals in database, surveillance may not detect anything")
        
        print("Surveillance started")
        print(f"Loaded criminals: {list(db.keys())}")

        for cam_id, src in enumerate(CAMERA_SOURCES):
            # Check if we should stop
            if not surveillance_running:
                print("Surveillance stopped by user")
                break
                
            print(f"Opening camera source: {src}")
            cap = cv2.VideoCapture(src)
            
            # Set camera properties for better performance
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer
            cap.set(cv2.CAP_PROP_FPS, 15)  # Set FPS to 15
            
            if not cap.isOpened():
                print(f"Failed to open camera {src}")
                print(f"   Make sure your camera/webcam is connected and not in use")
                print(f"   Or try changing CAMERA_SOURCES in backend/config.py")
                continue

            frame_count = 0
            last_alert_time = {}  # Track last alert time per criminal
            
            try:
                while surveillance_running:
                    ret, frame = cap.read()
                    if not ret:
                        print(f"Failed to read frame from camera {src} - reconnecting...")
                        time.sleep(1)
                        continue

                    frame_count += 1
                    
                    # Skip frames based on FRAME_SKIP config
                    if frame_count % FRAME_SKIP != 0:
                        continue

                    try:
                        # Resize for faster processing
                        small_frame = cv2.resize(frame, (320, 240))

                        # Update latest frame for frontend snapshot endpoint
                        try:
                            ret_jpg, jpg = cv2.imencode('.jpg', small_frame)
                            if ret_jpg:
                                global LAST_FRAME
                                LAST_FRAME = jpg.tobytes()
                        except Exception:
                            pass
                        
                        faces = detect_faces(small_frame)
                        
                        if faces and len(faces) > 0:
                            print(f"✓ Faces detected: {len(faces)}")

                        for f in faces:
                            emb = f.embedding
                            if emb is None:
                                continue

                            name, score = match_face(emb, db)

                            print(f"MATCH -> {name}: {score:.3f} (threshold: {SIMILARITY_THRESHOLD:.2f})")

                            # Alert only if threshold met and not recently alerted
                            if score >= SIMILARITY_THRESHOLD:
                                current_time = time.time()
                                last_time = last_alert_time.get(name, 0)
                                
                                # Only alert if at least 5 seconds since last alert for this person
                                if current_time - last_time >= 5:
                                    print(f"🚨 ALERT! {name} detected with score {score:.3f}")
                                    send_alert(name, cam_id, score)
                                    last_alert_time[name] = current_time
                                    
                    except Exception as e:
                        print(f"Error processing frame: {e}")
                        continue
                        
            except KeyboardInterrupt:
                print(f"Surveillance interrupted")
                break
            except Exception as e:
                print(f"Error in surveillance loop: {e}")
            finally:
                cap.release()
                print(f"Camera {src} released")
        
        print("Surveillance stopped")
        
    except Exception as e:
        print(f"Critical error in surveillance: {e}")
        import traceback
        traceback.print_exc()
