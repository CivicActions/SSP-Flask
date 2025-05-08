"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""


def test_template_files_route(client):
    response = client.get("/templates")
    assert response.status_code == 200


def test_templates_files_route_content(client):
    response = client.get("/templates")
    assert '<a href="/templates/templates/appendices">appendices</a>' in response.text


def test_templates_view_file(client):
    response = client.get(
        "/templates/templates/appendices/configuration-management.md.j2"
    )
    assert response.status_code == 302


def test_templates_view_file_content(client):
    response = client.get(
        "/templates/templates/appendices/configuration-management.md.j2"
    )
    assert "Redirecting..." in response.text


def test_templates_edit_file(client):
    response = client.get(
        "/templates/edit/templates/appendices/configuration-management.md.j2"
    )
    assert "CodeMirror" in response.text
