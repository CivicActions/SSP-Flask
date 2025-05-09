"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_page(client):
    response = client.get("/")
    assert "Test Component Library" in response.text


def test_404_route(client):
    response = client.get("/not-found")
    assert response.status_code == 404


def test_404_route_title(client):
    response = client.get("/not-found")
    assert "<h2>404 error</h2>" in response.text


def test_page_docs_view(client):
    response = client.get("/docs/rendered/docs")
    assert response.status_code == 200


def test_page_docs_page_content(client):
    response = client.get("/docs/rendered/docs")
    assert '<h1 class="title">Docs</h1>' in response.text


def test_page_docx_view(client):
    response = client.get("/docx/rendered/docx")
    assert response.status_code == 200


def test_page_docx_page_content(client):
    response = client.get("/docx/rendered/docx")
    assert '<h1 class="title">Docx</h1>' in response.text
