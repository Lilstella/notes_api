import os
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_versioning_csv():
    filename = "testfile_versioning_csv"

    # Create file
    response = client.post(f"/file/create/{filename}", json={"text": "age,name", "filetype": "csv"})

    # Actualize file
    time.sleep(1)
    response = client.put(f"/file/edit/{filename}", json={"text": "id,name", "filetype": "csv"})

    time.sleep(1)
    response = client.put(f"/file/edit/{filename}", json={"text": "file,content", "filetype": "csv"})

    # Verify amount versions
    response = client.request(method="GET", url=f"/file/{filename}/versions", params={"file_type": "csv"})
    assert response.status_code == 200
    versions = response.json()["versions"]
    assert len(versions) == 2

    # Verify content of versions
    response = client.request(method="GET", url=f"/file/{filename}/versions/{versions[0]}", params={"file_type": "csv"})
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == "age,name"

    response = client.request(method="GET", url=f"/file/{filename}/versions/{versions[1]}", params={"file_type": "csv"})
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == "id,name"

    # Erase file
    response = client.request(method="DELETE", url=f"/file/delete/{filename}", params={"file_type": "csv"})

    # Verify that versions are deleted
    response = client.request(method="GET", url=f"/file/{filename}/versions", params={"file_type": "csv"})
    assert response.status_code == 200
    assert response.json()["versions"] == []
