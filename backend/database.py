import os
import cv2
import numpy as np

FACE_DIR = "data/criminal_faces"
EMB_DIR = "data/embeddings"

os.makedirs(FACE_DIR, exist_ok=True)
os.makedirs(EMB_DIR, exist_ok=True)

def save_criminal(name, face_img, embedding):
    cv2.imwrite(f"{FACE_DIR}/{name}.jpg", face_img)
    np.save(f"{EMB_DIR}/{name}.npy", embedding)

def load_all_embeddings():
    db = {}
    for file in os.listdir(EMB_DIR):
        if file.endswith(".npy"):
            name = file.replace(".npy", "")
            db[name] = np.load(f"{EMB_DIR}/{file}")
    return db
