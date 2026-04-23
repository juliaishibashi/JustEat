def test_owner_can_update_order_status(client, get_token):
    token = get_token(client, "owner@test.com", "owner123")

    response = client.put(
        "/orders/1/status",
        json={"status": "CONFIRMED"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "CONFIRMED" 

def test_non_owner_cannot_update_order_status(client, get_token):
    token = get_token(client, "customer@test.com", "customer123")

    response = client.put(
        "/orders/1/status",
        json={"status": "CONFIRMED"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403