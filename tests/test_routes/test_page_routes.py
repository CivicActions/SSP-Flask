"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200


def test_404_route(client):
    response = client.get("/not-found")
    assert response.status_code == 404


def test_404_route_title(client):
    response = client.get("/not-found")
    assert "<h2>404 error</h2>" in response.text
