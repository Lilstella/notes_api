import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test bad request for GET
def test_search_wrong_extension():
    file_name = "testfile_wrong_extension"

    response = client.request(method="GET", url=f"/file/{file_name}", params={"file_type": "wrong_extension"})
    assert response.status_code == 400
    assert response.json()["detail"] == "The wrong_extension files are not available for this function"

def test_search_non_existent_file():
    file_name = "non_existent_file"

    response = client.request(method="GET", url=f"/file/{file_name}", params={"file_type": "markdown"})
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"
    assert not os.path.exists(f"storage/markdown/{file_name}.md")

# Test bad request for POST
def test_create_file_invalid_extension():
    file_name = "testfile_invalid_extension"
    content = {"text": "This is a test", "filetype": "invalid_extension"}

    response = client.post(f"/file/create/{file_name}", json=content)
    assert response.status_code == 400
    assert response.json()["detail"] == "The invalid_extension files are not available for this function"
    assert not os.path.exists(f"storage/invalid_extension/{file_name}.invalid_extension")

def test_try_create_file_that_already_exists():
    file_name = "testfile_already_exists"
    content = {"text": "This is a test", "filetype": "markdown"}

    response = client.post(f"/file/create/{file_name}", json=content)
    assert response.status_code == 201
    assert os.path.exists(f"storage/markdown/{file_name}.md")

    response = client.post(f"/file/create/{file_name}", json=content)
    assert response.status_code == 409
    assert response.json()["detail"] == f"The file {file_name} already exists"

    os.remove(f"storage/markdown/{file_name}.md")

# Test bad request for PUT
def test_update_file_invalid_extension():
    file_name = "testfile_update_invalid_extension"
    content = {"text": "This is a test", "filetype": "invalid_extension"}

    response = client.put(f"/file/edit/{file_name}", json=content)
    assert response.status_code == 400
    assert response.json()["detail"] == "The invalid_extension files are not available for this function"

def test_update_non_existent_file():
    file_name = "non_existent_file_update"
    content = {"text": "This is a test", "filetype": "markdown"}

    response = client.put(f"/file/edit/{file_name}", json=content)
    assert response.status_code == 404
    assert response.json()["detail"] == f"File not found"

# Test bad request for DELETE
def test_delete_file_invalid_extension():
    file_name = "testfile_delete_invalid_extension"
    content = {"text": "This is a test", "filetype": "invalid_extension"}

    response = client.delete(f"/file/delete/{file_name}", params={"file_type": "invalid_extension"})
    assert response.status_code == 400
    assert response.json()["detail"] == "The invalid_extension files are not available for this function"

def test_delete_non_existent_file():
    file_name = "non_existent_file_delete"
    file_type = "markdown"

    response = client.delete(f"/file/delete/{file_name}", params={"file_type": file_type})
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"
    assert not os.path.exists(f"storage/markdown/{file_name}.md")
    