from fastapi import FastAPI
from app.routes import crud, version, render, images, importer

app = FastAPI(
    title="Markdown Editor API", description="API for manage MArkdowns", version="1.0.0"
)

# Routers
app.include_router(crud.router, prefix="/file", tags=["Crud"])
app.include_router(version.router, prefix="/file", tags=["Version"])
app.include_router(render.router, prefix="/render", tags=["Render"])
app.include_router(importer.router, prefix="/import", tags=["Import"])
app.include_router(images.router, prefix="/images", tags=["Image"])
