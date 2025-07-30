import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_import_invalid_extension():
    file_path = "tmp/invalid.doc"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("ohara")
        
    response = client.post("/import", json={"file_path": file_path})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file extension"

    os.remove(file_path)

def test_import_invalid_json():
    response = client.post("/import", json={"file_path": True})
    assert response.status_code == 422

    response = client.post("/import", json={"file_path": 233})
    assert response.status_code == 422

    response = client.post("/import", json={"file_path": []})
    assert response.status_code == 422

    response = client.post("/import", json={})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "file_path"]

    response = client.post("/import", json={"file_path": ""})
    assert response.status_code == 422

def test_import_file_alredy_exists():
    os.makedirs("storage/markdown", exist_ok=True)

    file_path = "tmp/alredy_exists.md"
    destination_path = "storage/markdown/alredy_exists.md"
    with open(destination_path, "w", encoding="utf-8") as file_1, open(file_path, "w", encoding="utf-8") as file_2:
        file_1.write("original")
        file_2.write("new")

    response = client.post("/import", json={"file_path": file_path})
    print(response.json())
    assert response.status_code == 409
    assert response.json()["detail"] == "File already exists"

    os.remove(file_path)
    os.remove(destination_path)
