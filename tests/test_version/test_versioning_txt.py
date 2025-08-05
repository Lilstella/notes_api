import os
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_versioning_txt():
    filename = "testfile_versioning_txt"

    # Create file
    response = client.post(f"/file/create/{filename}", json={"text": "First version", "filetype": "txt"})

    # Actualize file
    time.sleep(1)
    response = client.put(f"/file/edit/{filename}", json={"text": "Second version", "filetype": "txt"})

    time.sleep(1)
    response = client.put(f"/file/edit/{filename}", json={"text": "Third version", "filetype": "txt"})

    # Verify amount versions
    response = client.request(method="GET", url=f"/file/{filename}/versions", params={"file_type": "txt"})
    assert response.status_code == 200
    versions = response.json()["versions"]
    assert len(versions) == 2

    # Verify content of versions
    response = client.request(method="GET", url=f"/file/{filename}/versions/{versions[0]}", params={"file_type": "txt"})
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == "First version"

    response = client.request(method="GET", url=f"/file/{filename}/versions/{versions[1]}", params={"file_type": "txt"})
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == "Second version"

    # Erase file
    response = client.request(method="DELETE", url=f"/file/delete/{filename}", params={"file_type": "txt"})

    # Verify that versions are deleted
    response = client.request(method="GET", url=f"/file/{filename}/versions", params={"file_type": "txt"})
    assert response.status_code == 200
    assert response.json()["versions"] == []
