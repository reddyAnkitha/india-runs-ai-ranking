from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer(
    "sentence-transformers/paraphrase-MiniLM-L3-v2"
)

print("Model loaded successfully!")