def test_rendered_files_route(client):
    response = client.get("/rendered")
    assert response.status_code == 200


def test_rendered_view_file(client):
    response = client.get(
        "/rendered/test/testssp/rendered/appendices/configuration-management.md"
    )
    assert response.status_code == 200
