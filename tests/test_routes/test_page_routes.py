def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200


def test_404_route(client):
    response = client.get("/not-found")
    assert response.status_code == 404


def test_404_route_title(client):
    response = client.get("/not-found")
    assert "<h2>404 error</h2>" in response.text
