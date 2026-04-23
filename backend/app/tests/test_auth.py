def test_login_success(client):
    response = client.post("/auth/login", data={"username": "customer@test.com", "password": "customer123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_fail(client):
    response = client.post("/auth/login", data={"username": "wrong@test.com", "password": "wrongpassword"})

    assert response.status_code == 401
