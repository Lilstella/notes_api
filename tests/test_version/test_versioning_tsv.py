import os
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_versioning_tsv():
    filename = "testfile_versioning_tsv"

    # Create file
    response = client.post(f"/file/create/{filename}", json={"text": "name\tage\nhugo\t67", "filetype": "tsv"})

    # Actualize file
    time.sleep(1)
    response = client.put(f"/file/edit/{filename}", json={"text": "name\tage\nhugo\t68", "filetype": "tsv"})

    time.sleep(1)
    response = client.put(f"/file/edit/{filename}", json={"text": "name\tage\nhugo\t69", "filetype": "tsv"})

    # Verify amount versions
    response = client.request(method="GET", url=f"/file/{filename}/versions", params={"file_type": "tsv"})
    assert response.status_code == 200
    versions = response.json()["versions"]
    assert len(versions) == 2

    # Verify content of versions
    response = client.request(method="GET", url=f"/file/{filename}/versions/{versions[0]}", params={"file_type": "tsv"})
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == "name\tage\nhugo\t67"

    response = client.request(method="GET", url=f"/file/{filename}/versions/{versions[1]}", params={"file_type": "tsv"})
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == "name\tage\nhugo\t68"

    # Erase file
    response = client.request(method="DELETE", url=f"/file/delete/{filename}", params={"file_type": "tsv"})

    # Verify that versions are deleted
    response = client.request(method="GET", url=f"/file/{filename}/versions", params={"file_type": "tsv"})
    assert response.status_code == 200
    assert response.json()["versions"] == []
