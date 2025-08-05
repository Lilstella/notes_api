import os
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_versioning_html():
    filename = "testfile_versioning_html"

    # Create file
    response = client.post(f"/file/create/{filename}", json={"text": "<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body><h1>Hello, World!</h1></body>\n</html>", "filetype": "html"})

    # Actualize file
    time.sleep(1)
    response = client.put(f"/file/edit/{filename}", json={"text": "<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body><h1>Hello, World Again!</h1></body>\n</html>", "filetype": "html"})

    time.sleep(1)
    response = client.put(f"/file/edit/{filename}", json={"text": "<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body><h1>Bye!</h1></body>\n</html>", "filetype": "html"})

    # Verify amount versions
    response = client.request(method="GET", url=f"/file/{filename}/versions", params={"file_type": "html"})
    assert response.status_code == 200
    versions = response.json()["versions"]
    assert len(versions) == 2

    # Verify content of versions
    response = client.request(method="GET", url=f"/file/{filename}/versions/{versions[0]}", params={"file_type": "html"})
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == "<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body><h1>Hello, World!</h1></body>\n</html>"

    response = client.request(method="GET", url=f"/file/{filename}/versions/{versions[1]}", params={"file_type": "html"})
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == "<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body><h1>Hello, World Again!</h1></body>\n</html>"

    # Erase file
    response = client.request(method="DELETE", url=f"/file/delete/{filename}", params={"file_type": "html"})

    # Verify that versions are deleted
    response = client.request(method="GET", url=f"/file/{filename}/versions", params={"file_type": "html"})
    assert response.status_code == 200
    assert response.json()["versions"] == []
