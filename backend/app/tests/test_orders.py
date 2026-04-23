
def test_create_order(client, get_token):
    token = get_token(client, "customer@test.com", "customer123")

    response = client.post(
        "/orders",
        json={
            "restaurant_id": 1,
            "items": [
                {"menu_id": 1, "quantity": 2},
            ],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert "total_price" in response.json()



def test_get_my_orders(client, get_token):
    token = get_token(client, "customer@test.com", "customer123")

    response = client.get("/orders/my", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert isinstance(response.json(), list)