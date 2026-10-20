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
    generate_summary,
    generate_research_gaps
)

MAX_PROJECT_CONTEXT_CHARS = 12000


def _get_project_context(chunks):
    context = ""
    omitted_chunks = False

    for index, chunk in enumerate(chunks):
        context += (
            "\n"
            f"{chunk['text']}\n"
        )

        if len(context) > MAX_PROJECT_CONTEXT_CHARS:
            omitted_chunks = index < len(chunks) - 1
            break

    if omitted_chunks:
        context += (
            "\n[Additional document chunks were omitted because this generation "
            f"context is limited to approximately {MAX_PROJECT_CONTEXT_CHARS} characters. "
            "Base the response only on the context included above.]\n"
        )

    return context


def ask_project(
        project_name,
    query,
    workspace_id=None
):
    
    _, storage_path = get_project_paths(
        project_name,
        workspace_id
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
    project_name,
    workspace_id=None
):

    _, storage_path = get_project_paths(
        project_name,
        workspace_id
    )

    index, chunks = load_index(
        storage_path
    )

    if index is None:

        return (
            "No PDFs uploaded in this project."
        )

    context = _get_project_context(chunks)

    summary = generate_summary(
        context
    )

    return summary


def research_gaps_project(
    project_name,
    workspace_id=None
):

    _, storage_path = get_project_paths(
        project_name,
        workspace_id
    )

    index, chunks = load_index(
        storage_path
    )

    if index is None:

        return (
            "No PDFs uploaded in this project."
        )

    context = _get_project_context(chunks)

    gaps = generate_research_gaps(
        context
    )

    return gaps