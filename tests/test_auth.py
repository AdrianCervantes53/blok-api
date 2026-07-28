def test_register_and_login(client):
    payload = {"email": "alice@example.com", "password": "password123"}

    register = client.post("/auth/register", json=payload)
    assert register.status_code == 201
    body = register.json()
    assert body["email"] == payload["email"]
    assert "id" in body

    login = client.post("/auth/login", json=payload)
    assert login.status_code == 200
    token = login.json()
    assert token["token_type"] == "bearer"
    assert token["access_token"]


def test_register_duplicate_email(client):
    payload = {"email": "dup@example.com", "password": "password123"}
    assert client.post("/auth/register", json=payload).status_code == 201
    assert client.post("/auth/register", json=payload).status_code == 409


def test_login_wrong_password(client):
    payload = {"email": "bob@example.com", "password": "password123"}
    client.post("/auth/register", json=payload)
    response = client.post(
        "/auth/login",
        json={"email": payload["email"], "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_me_requires_auth(client):
    assert client.get("/auth/me").status_code == 401


def test_me_with_token(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"
