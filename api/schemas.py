
from pydantic import BaseModel

class ProjectRequest(
    BaseModel
):
    project_name: str


class ChatRequest(BaseModel):
    project_name: str
    query: str