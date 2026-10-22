def test_root_redirects_to_homepage(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_destination_loads(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=True)

    # Assert
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"
    assert len(response.history) == 1
    assert response.headers["content-type"].startswith("text/html")
    assert 'id="activities-list"' in response.text
    assert 'id="signup-form"' in response.text
