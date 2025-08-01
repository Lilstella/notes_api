import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crud_txt():
    filename = "testfile_txt_crud"
    content = {"text": "Hi world", "filetype": "txt"}

    # Create file
    response = client.post(f"/file/create/{filename}", json=content)
    assert response.status_code == 201
    assert "created" in response.json()["message"]
    assert os.path.exists(f"storage/txt/{filename}.txt")

    # Read file
    response = client.request(method="GET", url=f"/file/{filename}", params={"file_type": "txt"})
    assert response.status_code == 200
    assert response.json()["content"] == content["text"]
    assert response.json()["filename"] == filename
    assert os.path.exists(f"storage/txt/{filename}.txt")

    # Actualize file
    new_content = {"text": "Hola mundo actualizado", "filetype": "txt"}
    response = client.put(f"/file/edit/{filename}", json=new_content)
    assert response.status_code == 200
    assert "updated" in response.json()["message"]
    assert os.path.exists(f"storage/txt/{filename}.txt")
    
    response = client.request(method="GET", url=f"/file/{filename}", params={"file_type": "txt"})
    assert response.status_code == 200
    assert response.json()["content"] == new_content["text"]
    assert response.json()["filename"] == filename

    # Erase file
    response = client.request(method="DELETE", url=f"/file/delete/{filename}", params={"file_type": "txt"})
    print(response.json())
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]
    assert not os.path.exists(f"storage/txt/{filename}.txt")
