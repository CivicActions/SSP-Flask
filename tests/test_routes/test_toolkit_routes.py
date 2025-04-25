def test_toolkit_render_files(client):
    response = client.get(
        "/createfiles/test/testssp/templates/appendices/configuration-management.md"
    )
    assert response.status_code == 302
