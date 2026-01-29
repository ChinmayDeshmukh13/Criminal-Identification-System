import numpy as np

def match_face(live_embedding, db_embeddings):
    """
    Find the best matching criminal based on cosine similarity of embeddings.
    Uses NumPy for cross-platform compatibility (avoids sklearn multiprocessing issues on Windows)
    """
    best_name = None
    best_score = -1

    for name, db_emb in db_embeddings.items():
        # Calculate cosine similarity manually using NumPy
        # cosine_similarity = (A·B) / (||A|| * ||B||)
        dot_product = np.dot(live_embedding, db_emb)
        norm_live = np.linalg.norm(live_embedding)
        norm_db = np.linalg.norm(db_emb)
        
        if norm_live > 0 and norm_db > 0:
            score = dot_product / (norm_live * norm_db)
        else:
            score = 0

        if score > best_score:
            best_score = score
            best_name = name

    return best_name, best_score
