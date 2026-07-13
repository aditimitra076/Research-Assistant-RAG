from modules.project_manager import (
    get_project_paths
)

from modules.pdf_loader import(
    load_all_pdfs
)

from modules.chunker import (
    create_chunks
)

from modules.embedder import(
    create_embeddings
)

from modules.vector_store import(
    create_index
)

from modules.index_manager import(
    save_index
)

def rebuild_project_index(project_name):

    pdfs_path, storage_path = get_project_paths(
        project_name
    )

    print(
        "\nUpdating project index..."
        )
    
    pdf_data = load_all_pdfs(
        pdfs_path
    )

    if len(pdf_data)==0:
        print(
            "No PDFs found."
        )

        return False

    chunks = create_chunks(
        pdf_data
    )

    if len(chunks)== 0:
        print(
            "No chunks created."
        )

        return False

    embeddings = create_embeddings(
        chunks
    )

    index = create_index(
        embeddings
    )

#temp
    # print("\nFirst 5 chunks\n")

    # for chunk in chunks[:5]:
    #     print("="*40)
    #     print(chunk["pdf_name"])
    #     print("page:", chunk["page"])
    #     print(chunk["text"][:300])
#temp

    save_index(
        index,
        chunks,
        storage_path
    )

    print(
        "Index updated."
    )

    return True

  