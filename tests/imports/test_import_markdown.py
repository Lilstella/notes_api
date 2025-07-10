import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_import_markdown():
    file_path = "tests/test.md"
    content = "# Hi world\n\nThis is a markdown type file." 
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    
    response = client.post("/import", json={"file_path": file_path})
    assert response.status_code == 200
    assert "imported" in response.json()["message"]
    assert response.json()["destination_path"] == "storage/markdown/test.md"
    assert response.json()["file_name"] == "test.md"
    assert os.path.exists(file_path)

    with open(response.json()["destination_path"], "r", encoding="utf-8") as file:
        content_destination = file.read()
    assert content == content_destination
    
    client.delete("/markdown/test")
    os.remove(file_path)

def test_import_non_existent_markdown():
    file_path = "tests/none.md"
    response = client.post("/import", json={"file_path": file_path})

    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"
    assert not os.path.exists("storage/markdown/none.md")
