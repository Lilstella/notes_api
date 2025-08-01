import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_render_to_html_non_existent_file():
    file_name = "non_existent_file"

    response = client.get(f"/render/html/{file_name}", params={"file_type": "markdown"})
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"

def test_render_to_html_invalid_file_type():
    file_name = "testfile_invalid_type"
    content = {"text": "This is a test", "file_type": "invalid_type"}

    response = client.request(method="GET", url=f"/render/html/{file_name}", params=content)
    assert response.status_code == 400
    assert response.json()["detail"] == "The invalid_type files are not available for this function"

def test_render_markdown_to_html():
    file_name = "test_render_markdown_to_html"
    content = {"text": "# Hi\n\nThis a **bold**, *italic* and ~~crossed~~ out text\n\n`code in line also`\n\n## Lista items\n\n- Item\n\n> This is a quote\n\n---\n\n",
               "filetype": "markdown"
               }
    
    client.post(f"/file/create/{file_name}", json=content)
    response = client.request(method="GET", url=f"/render/html/{file_name}", params={"file_type": "markdown"})

    assert response.status_code == 200
    html = response.json()["content"]

    assert "<h1>Hi</h1>" in html
    assert "<p>This a <strong>bold</strong>, <em>italic</em> and <del>crossed</del> out text</p>" in html
    assert "<p><code>code in line also</code></p>" in html
    assert "<h2>Lista items</h2>" in html
    assert "<ul>" in html and "<li>Item</li>" in html
    assert "<blockquote>This is a quote</blockquote>" in html
    assert "<hr />" in html

    client.request(method="DELETE", url=f"/file/delete/{file_name}", params={"file_type": "markdown"})

def test_render_csv_to_html():
    file_name = "test_render_csv_to_html"
    content = {"text": "name,age,country\nLouis,43,Ven\nAlbert,80,Arg", "filetype": "csv"}

    client.post(f"/file/create/{file_name}", json=content)
    response = client.request(method="GET", url=f"/render/html/{file_name}", params={"file_type": "csv"})

    assert response.status_code == 200
    html = response.json()["content"]

    assert "<table>" in html
    assert "<tr><th>name</th><th>age</th><th>country</th></tr>" in html
    assert "<tr><td>Louis</td><td>43</td><td>Ven</td></tr>" in html
    assert "<tr><td>Albert</td><td>80</td><td>Arg</td></tr>" in html
    assert "</table>" in html

    client.request(method="DELETE", url=f"/file/delete/{file_name}", params={"file_type": "csv"})

def test_render_txt_to_html():
    file_name = "test_render_txt_to_html"
    content = {"text": "This is a simple text file.", "filetype": "txt"}

    client.post(f"/file/create/{file_name}", json=content)
    response = client.request(method="GET", url=f"/render/html/{file_name}", params={"file_type": "txt"})

    assert response.status_code == 200
    html = response.json()["content"]

    assert "<pre>This is a simple text file.</pre>" in html

    client.request(method="DELETE", url=f"/file/delete/{file_name}", params={"file_type": "txt"})