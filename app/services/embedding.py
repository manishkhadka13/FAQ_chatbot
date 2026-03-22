from functools import lru_cache
from sentence_transformers import SentenceTransformer
from app.core.config import settings

@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """Load the model once and keep it in memory forever."""
    print(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
    return SentenceTransformer(settings.EMBEDDING_MODEL)

def embed(text: str) -> list[float]:
    """Convert a string into a 384-dimensional vector."""
    model = get_model()
    vector = model.encode(text, normalize_embeddings=True)
    return vector.tolist()