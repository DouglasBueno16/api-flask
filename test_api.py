import pytest
from main import app, db, User

@pytest.fixture
def client():
    # Configura o app para teste
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_index(client):
    """Teste da rota inicial"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Bem-vindo" in response.data

def test_health(client):
    """Teste da rota de saúde"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_create_user(client):
    """Teste de criação de usuário"""
    data = {"name": "Teste User", "email": "teste@example.com"}
    response = client.post('/users', json=data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["name"] == "Teste User"
    assert json_data["email"] == "teste@example.com"
    assert "id" in json_data

def test_create_user_duplicate_email(client):
    """Teste de erro ao criar usuário com email duplicado"""
    data = {"name": "User 1", "email": "duplicado@example.com"}
    client.post('/users', json=data)
    
    response = client.post('/users', json=data)
    assert response.status_code == 400
    assert response.get_json()["error"] == "Email already exists"

def test_list_users(client):
    """Teste de listagem de usuários"""
    # Adiciona um usuário primeiro
    client.post('/users', json={"name": "User 1", "email": "u1@example.com"})
    
    response = client.get('/users')
    assert response.status_code == 200
    # O endpoint atual em main.py retorna User.query.all(), 200 (que pode não ser serializável se não usar jsonify)
    # Mas no seu main.py você mudou para return User.query.all(), 200 sem o jsonify/to_dict
    # Se der erro de serialização no app, o teste falhará aqui.
    
def test_get_user(client):
    """Teste de busca de usuário por ID"""
    post_res = client.post('/users', json={"name": "User 1", "email": "u1@example.com"})
    user_id = post_res.get_json()["id"]
    
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.get_json()["name"] == "User 1"

def test_get_user_not_found(client):
    """Teste de usuário não encontrado"""
    response = client.get('/users/999')
    assert response.status_code == 404

def test_delete_user(client):
    """Teste de deleção de usuário"""
    post_res = client.post('/users', json={"name": "Deletar", "email": "del@example.com"})
    user_id = post_res.get_json()["id"]
    
    response = client.delete(f'/delete/{user_id}')
    assert response.status_code == 200
    assert b"foi deletado" in response.data
    
    # Verifica se foi deletado mesmo
    get_res = client.get(f'/users/{user_id}')
    assert get_res.status_code == 404
