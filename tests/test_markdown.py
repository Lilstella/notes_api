from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_y_leer_markdown():
    filename = "testfile"
    content = {"text": "Hola **mundo**"}

    # Crear archivo
    response = client.post(f"/markdown/{filename}", json=content)
    assert response.status_code == 200
    assert "created" in response.json()["message"].lower()

    # Leer archivo
    response = client.get(f"/markdown/{filename}")
    assert response.status_code == 200
    assert response.json()["content"] == content["text"]

    

    # Limpiar borrando el archivo
    response = client.delete(f"/markdown/{filename}")
    assert response.status_code == 200
