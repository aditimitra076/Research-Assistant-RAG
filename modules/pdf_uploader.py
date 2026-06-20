#upload function

import os
import shutil


from modules.project_manager import(
    get_project_paths
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