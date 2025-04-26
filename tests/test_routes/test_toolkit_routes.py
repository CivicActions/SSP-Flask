"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""


def test_toolkit_render_files(client):
    response = client.get(
        "/createfiles/test/testssp/templates/appendices/configuration-management.md"
    )
    assert response.status_code == 302
