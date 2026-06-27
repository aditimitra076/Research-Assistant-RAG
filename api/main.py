from fastapi import FastAPI

from api.routes import router


app = FastAPI(
    title = "Research Assistant API",
    description ="RAG-based Reserach Assistant",
    verion = "1.0.0"
)

app.include_router(
    router
)

