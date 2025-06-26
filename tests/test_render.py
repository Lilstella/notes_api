from fastapi.testclient import TestClient
from app.main import app
from markdown import markdown as md

client = TestClient(app)

def test_render_html():
    markdown_text = "# Hi\n this a **bold** an *italic* text"
    response = client.post("/render/html", json={"text": markdown_text})

    assert response.status_code == 200
    html = response.json()["html"]

    assert "<h1>Hi</h1>" in html
    assert "<strong>bold</strong>" in html
    assert "<em>italic</em>" in html
  