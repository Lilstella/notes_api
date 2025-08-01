import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crud_csv():
    filename = "testfile_csv_crud"
    content = {"text": "name,age\nmaria,87", "filetype": "csv"}

    # Create file
    response = client.post(f"/file/create/{filename}", json=content)
    assert response.status_code == 201
    assert "created" in response.json()["message"]
    assert os.path.exists(f"storage/csv/{filename}.csv")

    # Read file
    response = client.request(method="GET", url=f"/file/{filename}", params={"file_type": "csv"})
    assert response.status_code == 200
    assert response.json()["content"] == content["text"]
    assert response.json()["filename"] == filename
    assert os.path.exists(f"storage/csv/{filename}.csv")

    # Actualize file
    new_content = {"text": "name,age\nmaria,87\nclara,43", "filetype": "csv"}
    response = client.put(f"/file/edit/{filename}", json=new_content)
    assert response.status_code == 200
    assert "updated" in response.json()["message"]
    assert os.path.exists(f"storage/csv/{filename}.csv")
    
    response = client.request(method="GET", url=f"/file/{filename}", params={"file_type": "csv"})
    assert response.status_code == 200
    assert response.json()["content"] == new_content["text"]
    assert response.json()["filename"] == filename

    # Erase file
    response = client.request(method="DELETE", url=f"/file/delete/{filename}", params={"file_type": "csv"})
    print(response.json())
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]
    assert not os.path.exists(f"storage/csv/{filename}.csv")
