def create_chunks(
        pdf_data,
        chunk_size=1000,
        overlap=200
):
    chunks =[]

    for page_data in pdf_data:

        text = page_data["text"]

        page_num = page_data["page"]

        for i in range(
            0,
            len(text),
            chunk_size- overlap
        ):
            
            chunk_text = text[
                i:i+chunk_size
            ]

            chunks.append({

                "text": chunk_text,

                "chunk_id":len(chunks),

                "pdf_name":
                page_data["pdf_name"],

                "author":
                page_data["author"],

                "page":
                page_num
            })

    return chunks