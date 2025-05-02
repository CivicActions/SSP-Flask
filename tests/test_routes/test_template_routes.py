"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""


def test_template_files_route(client):
    response = client.get("/templates")
    assert response.status_code == 200


def test_templates_files_route_content(client):
    response = client.get("/templates")
    assert "<td>appendices</td>" in response.text


def test_templates_view_file(client):
    response = client.get(
        "/templates/templates/appendices/configuration-management.md.j2"
    )
    assert response.status_code == 200


def test_templates_view_file_content(client):
    response = client.get(
        "/templates/templates/appendices/configuration-management.md.j2"
    )
    assert "<h2>Overview</h2>" in response.text
