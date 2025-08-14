import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crud_latex():
    filename = "testfile_latex_crud"
    content = {"text": r"\documentclass{article}\begin{document}Hello \LaTeX! $E=mc^2$\end{document}", "filetype": "latex"}

    # Create file
    response = client.post(f"/file/create/{filename}", json=content)
    assert response.status_code == 201
    assert "created" in response.json()["message"]
    assert os.path.exists(f"storage/latex/{filename}.tex")

    # Read file
    response = client.request(method="GET", url=f"/file/{filename}", params={"file_type": "latex"})
    assert response.status_code == 200
    assert response.json()["content"] == content["text"]
    assert response.json()["filename"] == filename
    assert os.path.exists(f"storage/latex/{filename}.tex")

    # Actualize file
    new_content = {"text": "name,age\nmaria,87\nclara,43", "filetype": "latex"}
    response = client.put(f"/file/edit/{filename}", json=new_content)
    assert response.status_code == 200
    assert "updated" in response.json()["message"]
    assert os.path.exists(f"storage/latex/{filename}.tex")
    
    response = client.request(method="GET", url=f"/file/{filename}", params={"file_type": "latex"})
    assert response.status_code == 200
    assert response.json()["content"] == new_content["text"]
    assert response.json()["filename"] == filename

    # Erase file
    response = client.request(method="DELETE", url=f"/file/delete/{filename}", params={"file_type": "latex"})
    print(response.json())
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]
    assert not os.path.exists(f"storage/latex/{filename}.tex")
