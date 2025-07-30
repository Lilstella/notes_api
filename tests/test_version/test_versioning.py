import os
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

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
