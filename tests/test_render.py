from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_render_html():
    markdown_text = "# Hi\n\nThis a **bold**, *italic* and ~~crossed~~ out text\n`code in line also`\n\n## Lista items\n- Item\n\n> This is a quote\n---"
    response = client.post("/render/html", json={"text": markdown_text})

    assert response.status_code == 200
    html = response.json()["html"]

    print(html)
    assert "<h1>Hi</h1>" in html
    assert "<p>This a <strong>bold</strong>, <em>italic</em> and <del>crossed</del> out text</p>"
    assert "<p><code>code in line also</code></p>"
    assert "<h2>Lista items</h2>"
    assert "<ul>" in html and "<li>Item</li>" in html
    assert "<blockquote>This is a quote</blockquote>" in html
    assert "<hr />" in html
