import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_render_to_markdown_non_existent_file():
    file_name = "non_existent_file"

    response = client.get(f"/render/markdown/{file_name}", params={"file_type": "markdown"})
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"

def test_render_to_markdown_invalid_file_type():
    file_name = "testfile_invalid_type"
    content = {"text": "This is a test", "file_type": "invalid_type"}

    response = client.get(f"/render/markdown/{file_name}", params=content)
    assert response.status_code == 400
    assert response.json()["detail"] == "The invalid_type files are not available for this function"
    assert not os.path.exists(f"storage/invalid_type/{file_name}.invalid_type")

def test_render_csv_to_markdown():
    file_name = "test_render_csv_to_markdown"
    content = {"text": "name,age\nmariela,90", "filetype": "csv"}

    client.post(f"/file/create/{file_name}", json=content)
    response = client.request(method="GET", url=f"/render/markdown/{file_name}", params={"file_type": "csv"})

    assert response.status_code == 200
    html = response.json()["content"]

    assert "| name | age |" in html
    assert "| --- | --- |" in html
    assert "| mariela | 90 |" in html
    assert "| --- | --- |" in html
    client.request(method="DELETE", url=f"/file/delete/{file_name}", params={"file_type": "csv"})

def test_render_tsv_to_markdown():
    file_name = "test_render_tsv_to_markdown"
    content = {"text": "name\tage\nmariela\t90", "filetype": "tsv"}

    client.post(f"/file/create/{file_name}", json=content)
    response = client.request(method="GET", url=f"/render/markdown/{file_name}", params={"file_type": "tsv"})

    assert response.status_code == 200
    html = response.json()["content"]

    assert "| name | age |" in html
    assert "| --- | --- |" in html
    assert "| mariela | 90 |" in html
    assert "| --- | --- |" in html
    client.request(method="DELETE", url=f"/file/delete/{file_name}", params={"file_type": "tsv"})

def test_render_markdown_to_markdown():
    file_name = "test_render_markdown_to_markdown"
    content = {"text": "# Hi\n\nThis a **bold**, *italic* and ~~crossed~~ out text\n\n`code in line also`\n\n## Lista items\n\n- Item\n\n> This is a quote\n\n---\n\n",
               "filetype": "markdown"
               }
    
    client.post(f"/file/create/{file_name}", json=content)
    response = client.request(method="GET", url=f"/render/markdown/{file_name}", params={"file_type": "markdown"})

    assert response.status_code == 200
    markdown_content = response.json()["content"]

    assert "# Hi" in markdown_content
    assert "This a **bold**, *italic* and ~~crossed~~ out text" in markdown_content
    assert "`code in line also`" in markdown_content
    assert "## Lista items" in markdown_content
    assert "- Item" in markdown_content
    assert "> This is a quote" in markdown_content
    assert "---" in markdown_content

    client.request(method="DELETE", url=f"/file/delete/{file_name}", params={"file_type": "markdown"})

def test_render_txt_to_markdown():
    file_name = "test_render_txt_to_markdown"
    content = {"text": "This is a simple text file.", "filetype": "txt"}

    client.post(f"/file/create/{file_name}", json=content)
    response = client.request(method="GET", url=f"/render/markdown/{file_name}", params={"file_type": "txt"})

    assert response.status_code == 200
    markdown_content = response.json()["content"]

    assert "This is a simple text file." in markdown_content

    client.request(method="DELETE", url=f"/file/delete/{file_name}", params={"file_type": "txt"})

def test_render_html_to_markdown():
    file_name = "test_render_html_to_markdown"
    content = {"text": "<h1>Hi</h1><p>This a <strong>bold</strong>, <em>italic</em> and <del>crossed</del> out text</p><p><code>code in line also</code></p><h2>Lista items</h2><ul><li>Item</li></ul><blockquote>This is a quote</blockquote><hr />",
               "filetype": "html"}
    
    client.post(f"/file/create/{file_name}", json=content)
    response = client.request(method="GET", url=f"/render/markdown/{file_name}", params={"file_type": "html"})

    assert response.status_code == 200
    markdown_content = response.json()["content"]

    assert "# Hi" in markdown_content
    assert "This a **bold**, *italic* and ~~crossed~~ out text" in markdown_content
    assert "`code in line also`" in markdown_content
    assert "## Lista items" in markdown_content
    assert "- Item" in markdown_content
    assert "> This is a quote" in markdown_content
    assert "---" in markdown_content
    client.request(method="DELETE", url=f"/file/delete/{file_name}", params={"file_type": "html"})