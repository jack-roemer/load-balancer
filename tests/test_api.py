from fastapi.testclient import TestClient

from api import create_app


client = TestClient(create_app())

def test_list_servers():

    response = client.get("/servers")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert all("id" in server for server in data)

def test_get_server_by_id():

    response = client.get("/servers/s1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "s1"
    assert "address" in data

def test_get_missing_server_returns_404():
    response = client.get("/servers/does-not-exist")

    assert response.status_code == 404

def test_handle_request_returns_503_when_no_healthy_servers():

    client.patch("/servers/s1/state", json={"state": "unhealthy"})
    client.patch("/servers/s2/state", json={"state": "draining"})

    response = client.post(
        "/handle_request",
        json={
            "client_id": "user-123",
            "path": "/home",
            "headers": {},
        },
    )

    assert response.status_code == 503

def test_create_server():
    response = client.post(
        "/servers",
        json={
            "id": "s3",
            "host": "localhost",
            "port": 8003,
            "weight": 2,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "created successfully" in data["message"]

def test_create_duplicate_server_returns_400():

    client.post(
        "/servers",
        json={
            "id": "dup1",
            "host": "localhost",
            "port": 9001,
            "weight": 1,
        },
    )

    response = client.post(
        "/servers",
        json={
            "id": "dup1",
            "host": "localhost",
            "port": 9002,
            "weight": 1,
        },
    )

    assert response.status_code == 400

def test_update_server_state():

    response = client.patch(
        "/servers/s1/state",
        json={"state": "draining"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "draining" in data["message"]

def test_handle_request_returns_server():

    client.patch("/servers/s1/state", json={"state": "healthy"})
    client.patch("/servers/s2/state", json={"state": "healthy"})

    response = client.post(
        "/handle_request",
        json={
            "client_id": "user-123",
            "path": "/home",
            "headers": {"x-test": "1"},
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "server_id" in data
    assert "address" in data

def test_get_metrics():

    client.patch("/servers/s1/state", json={"state": "healthy"})
    client.patch("/servers/s2/state", json={"state": "healthy"})

    client.post("/handle_request", json={"client_id": "a", "path": "/", "headers": {}})
    client.post("/handle_request", json={"client_id": "b", "path": "/", "headers": {}})

    response = client.get("/metrics")

    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data
    assert "failed_requests" in data
    assert "requests_per_server" in data

def test_update_strategy():

    response = client.patch(
        "/strategy",
        json={"strategy": "least_connections"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "least_connections" in data["message"]

def test_update_strategy_invalid_returns_400():

    response = client.patch(
        "/strategy",
        json={"strategy": "not_a_real_strategy"},
    )

    assert response.status_code == 400