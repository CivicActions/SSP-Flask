"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""


def test_rendered_files_route(client):
    response = client.get("/rendered")
    assert response.status_code == 200


def test_rendered_view_file(client):
    response = client.get(
        "/rendered/test/testssp/rendered/appendices/configuration-management.md"
    )
    assert response.status_code == 200
