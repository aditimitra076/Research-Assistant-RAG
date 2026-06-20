from modules.project_chat import(
    chat_with_project
)

from modules.pdf_uploader import (
    upload_pdf
)

from modules.project_indexer import(
    rebuild_project_index
)

def open_project(
        project_name
):
    
    while True:
        print(
            f"==={project_name}==="
        )

        print("1.Upload PDF")
        print("2.Ask Questions")
        print("3. Rebuild index")
        print("4. Back")

        choice = input(
            "\nEnter choice: "
        )

        if choice=="1":
            pdf_path = input(
                "\nEnter PDF path: "
            ).strip().strip('"')

            upload_pdf(
                pdf_path,
                project_name
            )

        elif choice=="2":
            chat_with_project(
                project_name
            )

        elif choice=="3":
            rebuild_project_index(
                project_name
            )

        elif choice == "4":
            break