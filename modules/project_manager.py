import os
import shutil

PROJECTS_FOLDER = "projects"

def create_project(project_name):

    
        project_path= os.path.join(
            PROJECTS_FOLDER,
            project_name
        )


        os.makedirs(
            os.path.join(
                    project_path,
                    "pdfs"
            ),
            exist_ok=True
        )

        os.makedirs(
            os.path.join(
                    project_path,
                    "storage"
            ),
            exist_ok= True
        )

        print(
            f"Project '{project_name}'created. "
        )

def list_projects():
        
        if not os.path.exists(
                PROJECTS_FOLDER
        ):
                
                return []
        return[
                folder
                for folder in os.listdir(
                        PROJECTS_FOLDER
                )
                if os.path.isdir(
                        os.path.join(
                                PROJECTS_FOLDER,
                                folder
                        )
                )
        ]

def delete_project(project_name):
        
        project_path = os.path.join(
                PROJECTS_FOLDER,
                project_name
        )

        if os.path.exists(
                project_path
        ):
                shutil.rmtree(
                        project_path
                )

                
                print(
                        f"Project '{project_name}' deleted."
                )


def get_project_paths(project_name):
        
        project_path = os.path.join(
                PROJECTS_FOLDER,
                project_name
        )

        pdfs_path = os.path.join(
                project_path,
                "pdfs"
        )

        storage_path = os.path.join(
                project_path,
                "storage"
        )

        return pdfs_path, storage_path



def project_exists(project_name):
        
        return os.path.exists(
                os.path.join(
                        PROJECTS_FOLDER,
                        project_name
                )
        )