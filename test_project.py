from modules.project_manager import *

create_project("TestProject")


print(
    list_projects()
)

delete_project(
    "TestProject"
)

print(
    list_projects()
    )