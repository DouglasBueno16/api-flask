import pytest
import main


@pytest.fixture(autouse=True)
def client():
    # reset in-memory storage before each test
    main.users.clear()
    main._next_id = 1
    with main.app.test_client() as c:
        yield c


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Bem-vindo" in r.get_data(as_text=True)


def test_list_users_empty(client):
    r = client.get("/users")
    assert r.status_code == 200
    assert r.get_json() == []


def test_create_user_and_get(client):
    payload = {"name": "douglas", "email": "douglas@email.com"}
    r = client.post("/users", json=payload)
    assert r.status_code == 201
    data = r.get_json()
    assert data["id"] == 1
    assert data["name"] == "douglas"
    assert data["email"] == "douglas@email.com"

    r2 = client.get(f"/users/{data['id']}")
    assert r2.status_code == 200
    assert r2.get_json() == data


def test_create_invalid_missing_fields(client):
    r = client.post("/users", json={"name": "Bob"})
    assert r.status_code == 400
    assert r.get_json().get("error")


def test_create_invalid_non_json(client):
    r = client.post("/users", data="notjson", content_type="text/plain")
    assert r.status_code == 400
    assert r.get_json().get("error") == "JSON body required"


def test_delete_user_success(client):
    # Cria um usuário para deletar
    client.post("/users", json={"name": "Douglas", "email": "douglas@email.com"})
    
    # Executa a deleção
    r = client.delete("/delete/1")
    assert r.status_code == 200
    assert r.get_json()["message"] == "Usuário 1:Douglas foi deletado"
    
    # Verifica se a lista está vazia agora
    assert len(client.get("/users").get_json()) == 0


def test_delete_user_not_found(client):
    r = client.delete("/delete/999")
    assert r.status_code == 404
    assert r.get_json()["error"] == "User not found"
