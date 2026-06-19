from dotenv import load_dotenv


from modules.pdf_loader import load_all_pdfs
from modules.chunker import create_chunks
from modules.embedder import create_embeddings
from modules.vector_store import create_index
from modules.retriever import retrieve_chunks
from modules.generator import generate_answer

from modules.index_manager import(
    save_index,
    load_index
)

load_dotenv()

# pdf_data = load_all_pdfs(
#     "data"
# )

# chunks = create_chunks(
#     pdf_data
# )

# embeddings = create_embeddings(chunks)

# index = create_index(embeddings)

index, chunks = load_index()
if index is None:

    print(
        "Createing new index..."
    )

    pdf_data = load_all_pdfs(
        "data"
    )

    chunks = create_chunks(
        pdf_data
    )

    embeddings= create_embeddings(
        chunks
    )

    index = create_index(
        embeddings
    )

    save_index(
        index,
        chunks
    )

else:
    print(
        "Loaded saved index."
    )

print("System ready")

while True:

    query = input(
        "\nAsk any question (or type exit to exit): "
    )

    if query.lower()=="exit":
        break

    context, scores, indices = retrieve_chunks(
        query,
        index,
        chunks
    )

    print("\nTop Retrived Chunks\n")

    for score, idx in zip(scores[0], indices[0]):
        print(f"\nChunk Index: {idx}")
        print(f"Score: {score:.4f}")

        print(f"PDF: {chunks[idx]['pdf_name']}")
        print(f"Page: {chunks[idx]['page']}")
        print(f"Author:{chunks[idx]['author']}")

        print(chunks[idx]["text"][:300])

    answer = generate_answer(
        context,
        query
    )

    print("\n==ANSWER==\n")
    print (answer)

    print("\n==SOURCES==\n")

    seen = set()

    for idx in indices[0]:

        source = (
            chunks[idx]["pdf_name"],
            chunks[idx]["page"]
        )

        if source not in seen:

            print(
                f"{chunks[idx]['pdf_name']}"
                f"(Page{chunks[idx]['page']})"
            )

            seen.add(source)