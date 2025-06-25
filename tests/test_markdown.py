import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_y_leer_markdown():
    filename = "testfile"
    content = {"text": "Hola **mundo**"}

    # Crear archivo
    response = client.post(f"/markdown/{filename}", json=content)
    assert response.status_code == 200
    assert "created" in response.json()["message"]
    assert os.path.exists(f"markdown_storage/{filename}.md")

    # Leer archivo
    response = client.get(f"/markdown/{filename}")
    assert response.status_code == 200
    assert response.json()["content"] == content["text"]
    assert response.json()["filename"] == filename
    assert os.path.exists(f"markdown_storage/{filename}.md")

    # Actualizar archivo
    new_content = {"text": "Hola **mundo** actualizado"}
    response = client.put(f"/markdown/{filename}", json=new_content)
    assert response.status_code == 200
    assert "updated" in response.json()["message"]
    assert os.path.exists(f"markdown_storage/{filename}.md")
    
    response = client.get(f"/markdown/{filename}")
    assert response.status_code == 200
    assert response.json()["content"] == new_content["text"]
    assert response.json()["filename"] == filename

    # Limpiar borrando el archivo
    response = client.delete(f"/markdown/{filename}")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]
    assert not os.path.exists(f"markdown_storage/{filename}.md")
