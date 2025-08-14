import os
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_versioning_latex():
    filename = "testfile_versioning_latex"

    # Create file
    response = client.post(f"/file/create/{filename}", json={"text": r"\documentclass{article}\begin{document}Hello \LaTeX! $E=mc^2$\end{document}", "filetype": "latex"})

    # Actualize file
    time.sleep(1)
    response = client.put(f"/file/edit/{filename}", json={"text": r"\documentclass{article}\begin{document}Hello There \LaTeX! $E=mc^2$\end{document}", "filetype": "latex"})

    time.sleep(1)
    response = client.put(f"/file/edit/{filename}", json={"text": r"\documentclass{article}\begin{document}Bye \LaTeX! $E=mc^2$\end{document}", "filetype": "latex"})

    # Verify amount versions
    response = client.request(method="GET", url=f"/file/{filename}/versions", params={"file_type": "latex"})
    assert response.status_code == 200
    versions = response.json()["versions"]
    assert len(versions) == 2

    # Verify content of versions
    response = client.request(method="GET", url=f"/file/{filename}/versions/{versions[0]}", params={"file_type": "latex"})
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == r"\documentclass{article}\begin{document}Hello \LaTeX! $E=mc^2$\end{document}"

    response = client.request(method="GET", url=f"/file/{filename}/versions/{versions[1]}", params={"file_type": "latex"})
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == r"\documentclass{article}\begin{document}Hello There \LaTeX! $E=mc^2$\end{document}"

    # Erase file
    response = client.request(method="DELETE", url=f"/file/delete/{filename}", params={"file_type": "latex"})

    # Verify that versions are deleted
    response = client.request(method="GET", url=f"/file/{filename}/versions", params={"file_type": "latex"})
    assert response.status_code == 200
    assert response.json()["versions"] == []
