import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_import_latex():
    file_path = "tmp/test.tex"
    content = r"\documentclass{article}\begin{document}Hello \LaTeX! $E=mc^2$\end{document}"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    
    response = client.post("/import", json={"file_path": file_path})
    print(response.json())
    assert response.status_code == 200
    assert "imported" in response.json()["message"]

    expected_path = os.path.join("storage", "latex", "test.tex")
    assert response.json()["destination_path"] == expected_path
    assert response.json()["file_name"] == "test.tex"
    assert os.path.exists(file_path)

    with open(response.json()["destination_path"], "r", encoding="utf-8") as file:
        content_destination = file.read()
    assert content == content_destination
    
    client.request(method="DELETE", url="/file/delete/test", params={"file_type": "latex"})
    os.remove(file_path)

def test_import_non_existent_latex():
    file_path = "tmp/none.tex"
    response = client.post("/import", json={"file_path": file_path})

    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"
    assert not os.path.exists("storage/latex/none.tex")
