from modules.project_manager import(
    get_project_paths
)

from modules.index_manager import(
    load_index
)

from modules.retriever import(
    retrieve_chunks
)

from modules.generator import(
    generate_answer
)

def ask_project(
        project_name,
        query
):
    
    _, storage_path = get_project_paths(
        project_name
    )

    index, chunks = load_index(
        storage_path
    )

    if index is None:

        return(
            "No PDFs uploaded in this project.",
            []
        )
    
    context, scores, indices = retrieve_chunks(
        query,
        index,
        chunks
    )

    answer = generate_answer(
        context,
        query
    )

    sources = []

    seen = set()

    for idx in indices[0]:

        source = (
            chunks[idx]["pdf_name"],
            chunks[idx]["page"]
        )

        if source not in seen:
            sources.append(
                f"{chunks[idx]['pdf_name']}"
                f"(Page{chunks[idx]['page']})"
            )

            seen.add(source)
            
    return answer, sources
