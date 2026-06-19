def create_chunks(
        text,
        chunk_size=1000,
        overlap=200
):
    chunks =[]

    for i in range(
        0,
        len(text),
        chunk_size - overlap
    ):
        chunk = text[i: i+chunk_size]

        chunks.append({
            "text": chunk,
            "chunk_id": len(chunks)
        })

    return chunks