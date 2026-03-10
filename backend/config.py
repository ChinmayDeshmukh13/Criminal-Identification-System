import os
import logging
from typing import List
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Application Settings ====================
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
VERSION = "1.0.0"

# ==================== Server Configuration ====================
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_WORKERS = int(os.getenv("API_WORKERS", "4"))
API_RELOAD = os.getenv("API_RELOAD", "false").lower() == "true"

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", '["*"]')
if isinstance(CORS_ORIGINS, str):
    import json
    try:
        CORS_ORIGINS = json.loads(CORS_ORIGINS)
    except:
        CORS_ORIGINS = ["*"]

# ==================== Path Configuration ====================
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = Path(os.getenv("DATA_DIR", str(PROJECT_ROOT / "data")))
CRIMINAL_FACES_DIR = Path(os.getenv("CRIMINAL_FACES_DIR", str(DATA_DIR / "criminal_faces")))
EMBEDDINGS_DIR = Path(os.getenv("EMBEDDINGS_DIR", str(DATA_DIR / "embeddings")))
MODEL_DIR = Path(os.getenv("MODEL_DIR", str(PROJECT_ROOT / "models")))
LOG_DIR = Path(os.getenv("LOG_DIR", str(PROJECT_ROOT / "logs")))

# Create necessary directories
for directory in [DATA_DIR, CRIMINAL_FACES_DIR, EMBEDDINGS_DIR, MODEL_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
    logger.info(f"Directory ready: {directory}")

# ==================== Face Recognition Configuration ====================
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.50"))
FRAME_SKIP = int(os.getenv("FRAME_SKIP", "2"))

# Parse camera sources from environment variable
camera_sources_str = os.getenv("CAMERA_SOURCES", "[0]")
try:
    import json
    CAMERA_SOURCES = json.loads(camera_sources_str)
except:
    CAMERA_SOURCES = [0]

# Ensure CAMERA_SOURCES is a list of integers
CAMERA_SOURCES = [int(src) for src in CAMERA_SOURCES]

# ==================== Model Configuration ====================
ARCFACE_MODEL = os.getenv("ARCFACE_MODEL", "arcface.onnx")
MODEL_PATH = MODEL_DIR / ARCFACE_MODEL

# ==================== Alert Configuration ====================
ALERT_RETENTION_HOURS = int(os.getenv("ALERT_RETENTION_HOURS", "24"))
MAX_ALERTS = int(os.getenv("MAX_ALERTS", "1000"))

# ==================== File Upload Configuration ====================
ALLOWED_FILE_EXTENSIONS = os.getenv("ALLOWED_FILE_EXTENSIONS", "jpg,jpeg,png,gif").split(",")
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024

# ==================== Logging Configuration ====================
LOG_FILE = LOG_DIR / "app.log"
logger.info(f"Application initialized in {ENVIRONMENT} mode")
logger.info(f"Configuration loaded from environment variables")
