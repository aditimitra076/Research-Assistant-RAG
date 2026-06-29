# from fastapi import APTRoute

# from modules.project_manager import (
#     list_projects,
#     create_project
# )

# from api.schemas import (
#     ProjectRequest
# )

# router = APIRouter()

# @router.get("/")
# def home():
#     return {
#         "message": "Research Assistant API is running."
#     }

# @router.get("/projects")
# def get_projects():

#     projects = list_projects()

#     return {
#         "projects":projects
#     }

# @router.post("/projects")
# def create_new_project(
#     request:ProjectRequest
# ):
    
#     create_project(
#         request.project_name
#     )

#     return {
#         "message":
#         f"Project '{request.project_name}' created."
#     }

from pydantic import BaseModel

class ProjectRequest(
    BaseModel
):
    project_name: str