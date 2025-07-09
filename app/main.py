from fastapi import FastAPI
from app.routes import markdown, render, images, importer

app = FastAPI(
    title="Markdown Editor API",
    description="API for manage MArkdowns",
    version="1.0.0"
)

# Routers
app.include_router(markdown.router, prefix="/markdown", tags=["Markdown"])
app.include_router(render.router, prefix="/render", tags=["Render"])
app.include_router(importer.router, prefix="/import", tags=["Import"])
app.include_router(images.router, prefix="/images", tags=["Images"])
