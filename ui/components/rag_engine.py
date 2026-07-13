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
    generate_answer,
    generate_summary
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
    
    context, scores, indices, confidence = retrieve_chunks(
        query,
        index,
        chunks
    )

    if confidence <0.50:
        return (
            "I could not confidently find the answer in the uploaded documents.",
            []
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
                f"{chunks[idx]['pdf_name']}(Page{chunks[idx]['page']})"
                
            )
            seen.add(source)
            
    return answer, sources


def summarize_project(
        project_name
):

    _, storage_path = get_project_paths(
        project_name
    )

    index, chunks = load_index(
        storage_path
    )

    if index is None:

        return (
            "No PDFs uploaded in this project."
        )

    context = ""

    for chunk in chunks:

        context += (
            "\n"
            f"{chunk['text']}\n"
        )

        if len(context) > 12000:
            break

    summary = generate_summary(
        context
    )

    return summary