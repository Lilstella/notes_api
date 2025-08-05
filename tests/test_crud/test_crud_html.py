import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crud_html():
    filename = "testfile_html_crud"
    content = {"text": "<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body><h1>Hello, World!</h1></body>\n</html>", "filetype": "html"}

    # Create file
    response = client.post(f"/file/create/{filename}", json=content)
    assert response.status_code == 201
    assert "created" in response.json()["message"]
    assert os.path.exists(f"storage/html/{filename}.html")

    # Read file
    response = client.request(method="GET", url=f"/file/{filename}", params={"file_type": "html"})
    assert response.status_code == 200
    assert response.json()["content"] == content["text"]
    assert response.json()["filename"] == filename
    assert os.path.exists(f"storage/html/{filename}.html")

    # Actualize file
    new_content = {"text": "<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body><h1>Hello, World Again!</h1></body>\n</html>", "filetype": "html"}
    response = client.put(f"/file/edit/{filename}", json=new_content)
    assert response.status_code == 200
    assert "updated" in response.json()["message"]
    assert os.path.exists(f"storage/html/{filename}.html")
    
    response = client.request(method="GET", url=f"/file/{filename}", params={"file_type": "html"})
    assert response.status_code == 200
    assert response.json()["content"] == new_content["text"]
    assert response.json()["filename"] == filename

    # Erase file
    response = client.request(method="DELETE", url=f"/file/delete/{filename}", params={"file_type": "html"})
    print(response.json())
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]
    assert not os.path.exists(f"storage/html/{filename}.html")
