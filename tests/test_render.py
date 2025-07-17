import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_render_html():
    file_name = "test_render_html"
    content = {"text": "# Hi\n\nThis a **bold**, *italic* and ~~crossed~~ out text\n\n`code in line also`\n\n## Lista items\n\n- Item\n\n> This is a quote\n\n---\n\n"}
    
    client.post(f"/markdown/{file_name}", json=content)
    response = client.get(f"/render/html/{file_name}")

    assert response.status_code == 200
    html = response.json()["content"]

    assert "<h1>Hi</h1>" in html
    assert "<p>This a <strong>bold</strong>, <em>italic</em> and <del>crossed</del> out text</p>" in html
    assert "<p><code>code in line also</code></p>" in html
    assert "<h2>Lista items</h2>" in html
    assert "<ul>" in html and "<li>Item</li>" in html
    assert "<blockquote>This is a quote</blockquote>" in html
    assert "<hr />" in html

    client.delete(f"/markdown/{file_name}")

def test_render_csv():
    file_path = "tests/test_render.csv"
    csv_text = "name,age,country\nLouis,43,Ven\nAlbert,80,Arg"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(csv_text)
    
    client.post("/import", json={"file_path": file_path})
    response = client.post("/render/csv/test_render")
    
    assert response.status_code == 200
    markdown = response.json()["content"]
    assert markdown == "| name | age | country |\n| --- | --- | --- |\n| Louis | 43 | Ven |\n| Albert | 80 | Arg |\n"

    os.remove(file_path)
    os.remove("storage/csv/test_render.csv")
