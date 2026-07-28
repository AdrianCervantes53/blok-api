def test_notas_require_auth(client):
    assert client.get("/notas").status_code == 401
    assert client.post("/notas", json={"title": "x", "content": "y"}).status_code == 401


def test_crud_notas(client, auth_headers):
    create = client.post(
        "/notas",
        headers=auth_headers,
        json={"title": "Primera", "content": "Hola"},
    )
    assert create.status_code == 201
    note = create.json()
    assert note["title"] == "Primera"
    note_id = note["id"]

    listed = client.get("/notas", headers=auth_headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    got = client.get(f"/notas/{note_id}", headers=auth_headers)
    assert got.status_code == 200
    assert got.json()["content"] == "Hola"

    updated = client.patch(
        f"/notas/{note_id}",
        headers=auth_headers,
        json={"title": "Actualizada"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Actualizada"
    assert updated.json()["content"] == "Hola"

    deleted = client.delete(f"/notas/{note_id}", headers=auth_headers)
    assert deleted.status_code == 204
    assert client.get(f"/notas/{note_id}", headers=auth_headers).status_code == 404


def test_cannot_access_other_users_note(client, auth_headers):
    created = client.post(
        "/notas",
        headers=auth_headers,
        json={"title": "Privada", "content": "secret"},
    )
    note_id = created.json()["id"]

    other = {"email": "other@example.com", "password": "password123"}
    assert client.post("/auth/register", json=other).status_code == 201
    login = client.post("/auth/login", json=other)
    other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    assert client.get(f"/notas/{note_id}", headers=other_headers).status_code == 404
    assert (
        client.patch(
            f"/notas/{note_id}",
            headers=other_headers,
            json={"title": "hack"},
        ).status_code
        == 404
    )
    assert client.delete(f"/notas/{note_id}", headers=other_headers).status_code == 404
