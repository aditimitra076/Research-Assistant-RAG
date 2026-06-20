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

from modules.project_manager import(
    create_project,
    list_projects,
    delete_project
)

from modules.project_chat import(
    chat_with_project
)

from modules.project_workspace import(
    open_project
)

from modules.pdf_uploader import upload_pdf


from modules.project_indexer import(
    rebuild_project_index
)


load_dotenv()


while True:

    print("\n===PROJECT MENU===\n")
    print("1. Create Project")
    print("2. Select Project")
    print("3. Delete Project")
    print("4. Exit")

    choice = input("\nEnter choice:")

    if choice =="1":

        project_name = input(
            "Project name:"
        )

        create_project(
            project_name
        )

    elif choice =="2":

        projects = list_projects()

        print("\nProjects:")

        for project in projects:
            print(project)
        
        selected_project = input(
            "\nSelect Project: "
        )

        open_project(
            selected_project
        )
    
    elif choice=="3":
        projects = list_projects()

        print("\nProjects: ")

        for project in projects:
            print(project)
            
        project_name= input(
            "\nDelete Project: "
        )

        delete_project(
            project_name
        )

    elif choice =="4":

        break


