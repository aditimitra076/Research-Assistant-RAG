import numpy as np

from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def retrieve_chunks(
        query,
        index,
        chunks,
        top_k=10
):
    
    query_embedding = np.array(
        model.encode(
            query,
            normalize_embeddings=True
        )
    ).astype("float32")

    query_embedding = query_embedding.reshape(
        1,
        -1
    )


    scores, indices = index.search(
        query_embedding,
        top_k
    )

    context = "\n\n".join(
        chunks[idx]["text"]
        for idx in indices[0]
    )

    return context, scores, indices