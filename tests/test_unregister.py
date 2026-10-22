from copy import deepcopy


def test_unregister_removes_only_selected_participant(client, activity_data):
    # Arrange
    email = activity_data["Chess Club"]["participants"][0]
    expected = deepcopy(activity_data)
    expected["Chess Club"]["participants"].remove(email)

    # Act
    response = client.delete(
        "/activities/Chess%20Club/unregister", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    assert activity_data == expected


def test_unregister_rejects_unknown_activity(client, activity_data):
    # Arrange
    email = activity_data["Chess Club"]["participants"][0]
    expected = deepcopy(activity_data)

    # Act
    response = client.delete(
        "/activities/Unknown/unregister", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert activity_data == expected


def test_unregister_rejects_unregistered_participant(client, activity_data):
    # Arrange
    expected = deepcopy(activity_data)
    email = "unknown@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess%20Club/unregister", params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }
    assert activity_data == expected


def test_unregister_requires_email(client, activity_data):
    # Arrange
    expected = deepcopy(activity_data)
    url = "/activities/Chess%20Club/unregister"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 422
    assert any(
        error["loc"] == ["query", "email"] and error["type"] == "missing"
        for error in response.json()["detail"]
    )
    assert activity_data == expected


def test_unregister_rejects_repeated_removal(client, activity_data):
    # Arrange
    email = activity_data["Chess Club"]["participants"][0]
    url = "/activities/Chess%20Club/unregister"
    setup_response = client.delete(url, params={"email": email})
    assert setup_response.status_code == 200
    expected = deepcopy(activity_data)

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }
    assert activity_data == expected


def test_participant_can_sign_up_again_after_unregistering(client, activity_data):
    # Arrange
    email = activity_data["Chess Club"]["participants"][0]
    setup_response = client.delete(
        "/activities/Chess%20Club/unregister", params={"email": email}
    )
    assert setup_response.status_code == 200
    expected = deepcopy(activity_data)
    expected["Chess Club"]["participants"].append(email)

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert activity_data == expected
    assert activity_data["Chess Club"]["participants"].count(email) == 1


def test_unregister_frees_spot_for_new_signup(client, activity_data):
    # Arrange
    activity_data["Chess Club"]["participants"].append("third@mergington.edu")
    removed_email = activity_data["Chess Club"]["participants"][0]
    setup_response = client.delete(
        "/activities/Chess%20Club/unregister", params={"email": removed_email}
    )
    assert setup_response.status_code == 200
    email = "replacement@mergington.edu"
    expected = deepcopy(activity_data)
    expected["Chess Club"]["participants"].append(email)

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert activity_data == expected
    activity = activity_data["Chess Club"]
    assert len(activity["participants"]) == activity["max_participants"]
    assert removed_email not in activity["participants"]
