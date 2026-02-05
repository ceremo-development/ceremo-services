from app import create_app


def test_create_app_with_config(test_config):
    app = create_app(test_config)
    assert app is not None
    assert app.name == "app"


def test_create_app_without_config():
    app = create_app()
    assert app is not None
    assert app.name == "app"


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Welcome to Ceremo Services"
    assert data["status"] == "running"


def test_health_check_route(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["environment"] == "test"
    assert data["database"] == "ceremo_db"
