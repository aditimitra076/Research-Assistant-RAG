#upload function

import os
import shutil

from modules.project_manager import(
    get_project_paths
)

from modules.pdf_loader import load_all_pdfs
from modules.chunker import create_chunks
from modules.embedder import create_embeddings
from modules.vector_store import create_index

from modules.index_manager import(
    save_index
)


def upload_pdf(
        source_file_path,
        project_name
):
    
    pdfs_path,_ = get_project_paths(
        project_name
    )

    file_name = os.path.basename(
        source_file_path
    )

    destination = os.path.join(
        pdfs_path,
        file_name
    )


    

    shutil.copy(
        source_file_path,
        destination
    )

    print(
        f"{file_name} uploaded successfully." 
    )

    print(
        "Updating project index..."
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

    index= create_index(
        embeddings
    )

    _, storage_path = get_project_paths(
        project_name
    )

    save_index(
        index,
        chunks,
        storage_path
    )

    print(
        "Index updated."
    )