import os
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crud_markdown():
    filename = "testfile"
    content = {"text": "Hi **world**"}

    # Create file
    response = client.post(f"/markdown/{filename}", json=content)
    assert response.status_code == 200
    assert "created" in response.json()["message"]
    assert os.path.exists(f"markdown_storage/{filename}.md")

    # Read file
    response = client.get(f"/markdown/{filename}")
    assert response.status_code == 200
    assert response.json()["content"] == content["text"]
    assert response.json()["filename"] == filename
    assert os.path.exists(f"markdown_storage/{filename}.md")

    # Actualize file
    new_content = {"text": "Hola **mundo** actualizado"}
    response = client.put(f"/markdown/{filename}", json=new_content)
    assert response.status_code == 200
    assert "updated" in response.json()["message"]
    assert os.path.exists(f"markdown_storage/{filename}.md")
    
    response = client.get(f"/markdown/{filename}")
    assert response.status_code == 200
    assert response.json()["content"] == new_content["text"]
    assert response.json()["filename"] == filename

    # Erase file
    response = client.delete(f"/markdown/{filename}")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]
    assert not os.path.exists(f"markdown_storage/{filename}.md")

def test_versioning():
    filename = "testfile_versioning"

    # Create file
    response = client.post(f"/markdown/{filename}", json={"text": "First version"})
    assert response.status_code == 200

    # Actualize file
    time.sleep(1)
    response = client.put(f"/markdown/{filename}", json={"text": "Second version"})
    assert response.status_code == 200

    time.sleep(1)
    response = client.put(f"/markdown/{filename}", json={"text": "Third version"})
    assert response.status_code == 200

    # Verify amount versions
    response = client.get(f"/markdown/{filename}/versions")
    assert response.status_code == 200
    versions = response.json()["versions"]
    assert len(versions) == 2

    # Verify content of versions
    response = client.get(f"/markdown/{filename}/versions/{versions[0]}")
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == "First version"

    response = client.get(f"/markdown/{filename}/versions/{versions[1]}")
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == "Second version"

    # Erase file
    response = client.delete(f"/markdown/{filename}")
    assert response.status_code == 200

    # Verify that versions are deleted
    response = client.get(f"/markdown/{filename}/versions")
    assert response.status_code == 200
    assert response.json()["versions"] == []
