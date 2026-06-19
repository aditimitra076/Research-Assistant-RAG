from sentence_transformers import SentenceTransformer

import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def create_embeddings(chunks):

    chunk_texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        chunk_texts,
        normalize_embeddings=True
    )

    embeddings = np.array(
        embeddings
    ).astype("float32")

    return embeddings