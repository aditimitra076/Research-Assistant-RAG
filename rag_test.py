from dotenv import load_dotenv


from modules.pdf_loader import load_pdf
from modules.chunker import create_chunks
from modules.embedder import create_embeddings
from modules.vector_store import create_index
from modules.retriever import retrieve_chunks
from modules.generator import generate_answer

load_dotenv()

text = load_pdf("data/sample.pdf")

chunks = create_chunks(text)

embeddings = create_embeddings(chunks)

index = create_index(embeddings)

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

    answer = generate_answer(
        context,
        query
    )

    print("\n==ANSWER==\n")
    print (answer)