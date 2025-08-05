import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_import_html():
    file_path = "tmp/test.html"
    content = "<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body><h1>Hello, World!</h1></body>\n</html>" 
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    
    response = client.post("/import", json={"file_path": file_path})
    print(response.json())
    assert response.status_code == 200
    assert "imported" in response.json()["message"]

    expected_path = os.path.join("storage", "html", "test.html")
    assert response.json()["destination_path"] == expected_path
    assert response.json()["file_name"] == "test.html"
    assert os.path.exists(file_path)

    with open(response.json()["destination_path"], "r", encoding="utf-8") as file:
        content_destination = file.read()
    assert content == content_destination
    
    client.request(method="DELETE", url="/file/delete/test", params={"file_type": "html"})
    os.remove(file_path)

def test_import_non_existent_html():
    file_path = "tmp/none.html"
    response = client.post("/import", json={"file_path": file_path})

    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"
    assert not os.path.exists("storage/html/none.html")
