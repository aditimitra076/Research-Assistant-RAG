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

    chunks = create_chunks(
        pdf_data
    )

    embeddings = create_embeddings(
        chunks
    )

    index = create_index(
        embeddings
    )

    save_index(
        index,
        chunks,
        storage_path
    )

    print(
        "INdex updated."
    )