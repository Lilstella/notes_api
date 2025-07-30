import os
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crud_markdown():
    filename = "testfile_markdown_crud"
    content = {"text": "Hi **world**", "filetype": "markdown"}

    # Create file
    response = client.post(f"/file/create/{filename}", json=content)
    assert response.status_code == 201
    assert "created" in response.json()["message"]
    assert os.path.exists(f"storage/markdown/{filename}.md")

    # Read file
    response = client.request(method="GET", url=f"/file/{filename}", params={"file_type": "markdown"})
    assert response.status_code == 200
    assert response.json()["content"] == content["text"]
    assert response.json()["filename"] == filename
    assert os.path.exists(f"storage/markdown/{filename}.md")

    # Actualize file
    new_content = {"text": "Hola **mundo** actualizado", "filetype": "markdown"}
    response = client.put(f"/file/edit/{filename}", json=new_content)
    assert response.status_code == 200
    assert "updated" in response.json()["message"]
    assert os.path.exists(f"storage/markdown/{filename}.md")
    
    response = client.request(method="GET", url=f"/file/{filename}", params={"file_type": "markdown"})
    assert response.status_code == 200
    assert response.json()["content"] == new_content["text"]
    assert response.json()["filename"] == filename

    # Erase file
    response = client.request(method="DELETE", url=f"/file/delete/{filename}", params={"file_type": "markdown"})
    print(response.json())
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]
    assert not os.path.exists(f"storage/markdown/{filename}.md")
