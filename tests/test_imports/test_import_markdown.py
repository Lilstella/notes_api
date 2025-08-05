import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_import_markdown():
    file_path = "tmp/test.md"
    content = "# Hi world\n\nThis is a markdown type file." 
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    
    response = client.post("/import", json={"file_path": file_path})
    print(response.json())
    assert response.status_code == 200
    assert "imported" in response.json()["message"]

    expected_path = os.path.join("storage", "markdown", "test.md")
    assert response.json()["destination_path"] == expected_path
    assert response.json()["file_name"] == "test.md"
    assert os.path.exists(file_path)

    with open(response.json()["destination_path"], "r", encoding="utf-8") as file:
        content_destination = file.read()
    assert content == content_destination
    
    client.request(method="DELETE", url="/file/delete/test", params={"file_type": "markdown"})
    os.remove(file_path)

def test_import_non_existent_markdown():
    file_path = "tmp/none.md"
    response = client.post("/import", json={"file_path": file_path})

    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"
    assert not os.path.exists("storage/markdown/none.md")
