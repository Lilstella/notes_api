from fastapi.testclient import TestClient
from app.main import app
from markdown import markdown as md

client = TestClient(app)

def test_render_html():
    markdown_text = "# Hi\n this a **bold** an *italic* text"
    response = client.post("/render/", json={"text": markdown_text})

    assert response.status_code == 200
    assert response.json()["html"] == md(markdown_text)
  