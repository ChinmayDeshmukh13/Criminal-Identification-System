import cv2
from insightface.app import FaceAnalysis

# Initialize InsightFace once
app = FaceAnalysis(providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0, det_size=(640, 640))


def extract_face_and_embedding(img):
    """
    Used during criminal enrollment.
    Returns (face_crop, embedding) or (None, None)
    """
    if img is None:
        return None, None

    try:
        faces = app.get(img)
    except Exception as e:
        print(f"Error detecting faces: {e}")
        return None, None
    
    if not faces:
        return None, None

    # Take the largest / first face
    f = faces[0]
    x1, y1, x2, y2 = map(int, f.bbox)

    h, w = img.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    face_crop = img[y1:y2, x1:x2]
    if face_crop.size == 0:
        return None, None

    return face_crop, f.embedding


def get_embedding(face_img):
    """
    Used during real-time surveillance.
    Must NEVER crash.
    Returns embedding or None.
    """
    if face_img is None or face_img.size == 0:
        return None

    h, w = face_img.shape[:2]
    if h < 20 or w < 20:
        return None

    try:
        face_img = cv2.resize(face_img, (112, 112))
    except Exception:
        return None

    try:
        faces = app.get(face_img)
    except Exception:
        return None

    if not faces:
        return None

    return faces[0].embedding
