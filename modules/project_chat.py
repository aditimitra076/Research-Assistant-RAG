from modules.project_manager import(
    get_project_paths
)

from modules.index_manager import (
    load_index
)

from modules.retriever import (
    retrieve_chunks
)

from modules.generator import (
    generate_answer
)

def chat_with_project(
        project_name
):
    _, storage_path = get_project_paths(
        project_name
    )

    index, chunks = load_index(
        storage_path
    )

    if index is None:

        print(
            "\nNo PDFs uploaded in this project."
        )

        return
    
    print(
        "\nProject Ready."
    )

    while True:

        query = input(
            "\nAsk Question (exit to quit): "
        )

        if query.lower()== "exit":
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
        print(answer)

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
                    f"(Page {chunks[idx]['page']})"
                )

                seen.add(source)