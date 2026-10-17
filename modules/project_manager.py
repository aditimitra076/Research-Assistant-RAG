import os
import shutil
import tempfile

PROJECTS_FOLDER = "projects"

def _projects_folder(workspace_id=None):
        if workspace_id is None:
                return PROJECTS_FOLDER

        return os.path.join(
                tempfile.gettempdir(),
                "research_assistant_rag",
                workspace_id
        )

def _project_path(project_name, workspace_id=None):
        if (
                not project_name
                or project_name in {".", ".."}
                or "/" in project_name
                or "\\" in project_name
        ):
                raise ValueError("Project names cannot contain path separators.")

        return os.path.join(
                _projects_folder(workspace_id),
                project_name
        )

def create_project(project_name, workspace_id=None):

        project_path = _project_path(project_name, workspace_id)
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

def list_projects(workspace_id=None):
        
        projects_folder = _projects_folder(workspace_id)

        if not os.path.exists(projects_folder):
                
                return []
        return[
                folder
                for folder in os.listdir(
                        projects_folder
                )
                if os.path.isdir(
                        os.path.join(
                                projects_folder,
                                folder
                        )
                )
        ]

def delete_project(project_name, workspace_id=None):
        
        project_path = _project_path(project_name, workspace_id)

        if os.path.exists(
                project_path
        ):
                shutil.rmtree(
                        project_path
                )

                
                print(
                        f"Project '{project_name}' deleted."
                )


def get_project_paths(project_name, workspace_id=None):
        
        project_path = _project_path(project_name, workspace_id)

        pdfs_path = os.path.join(
                project_path,
                "pdfs"
        )

        storage_path = os.path.join(
                project_path,
                "storage"
        )

        return pdfs_path, storage_path



def project_exists(project_name, workspace_id=None):
        
        return os.path.exists(
                _project_path(project_name, workspace_id)
        )