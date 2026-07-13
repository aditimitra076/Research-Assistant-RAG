from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form
)

from ui.components.rag_engine import (
    ask_project,
    summarize_project,
    research_gaps_project
)

import os
import shutil

from modules.project_manager import (
    list_projects,
    create_project
)

from modules.pdf_uploader import (
    upload_pdf
)

from api.schemas import (
    ProjectRequest
)

from modules.project_manager import (
    delete_project
)

from modules.project_indexer import (
    rebuild_project_index
)


router = APIRouter()


@router.get("/")
def home():

    return {
        "message": "Research Assistant API is running."
    }


@router.get("/projects")
def get_projects():

    projects = list_projects()

    return {
        "projects": projects
    }


@router.post("/projects")
def create_new_project(
    request: ProjectRequest
):

    create_project(
        request.project_name
    )

    return {
        "message":
        f"Project '{request.project_name}' created."
    }


@router.post("/upload")
async def upload_project_pdf(

    project_name: str = Form(...),

    file: UploadFile = File(...)
):

    temp_path = file.filename

    with open(
        temp_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    upload_pdf(
        temp_path,
        project_name
    )

    os.remove(
        temp_path
    )

    return {

        "message":
        f"{file.filename} uploaded successfully."

    }


from pydantic import BaseModel


class ProjectRequest(BaseModel):
    project_name: str


class ChatRequest(BaseModel):
    project_name: str
    query: str


@router.post("/chat")
def chat(request: ChatRequest):

    answer, sources = ask_project(
        request.project_name,
        request.query
    )

    return {
        "answer": answer,
        "sources": sources
    }



@router.delete("/projects")
def delete(request: ProjectRequest):

    delete_project(
        request.project_name
    )

    return {
        "message": f"{request.project_name} deleted successfully."
    }


@router.post("/rebuild")
def rebuild(request: ProjectRequest):

    success = rebuild_project_index(
        request.project_name
    )

    if success:

        return {
            "message": "Index rebuilt successfully."
        }

    return {
        "message": "No PDFs found in this project."
    }


@router.post("/summary")
def summary(request: ProjectRequest):

    summary = summarize_project(
        request.project_name
    )

    return {
        "summary": summary
    }


@router.post("/research-gaps")
def research_gaps(request: ProjectRequest):

    gaps = research_gaps_project(
        request.project_name
    )

    return {
        "research_gaps": gaps
    }