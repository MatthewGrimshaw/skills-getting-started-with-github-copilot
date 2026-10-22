from copy import deepcopy

import pytest


@pytest.mark.parametrize("email", [
    "student@mergington.edu",
    "student+art@mergington.edu",
])
def test_signup_adds_participant_once(client, activity_data, email):
    # Arrange
    expected = deepcopy(activity_data)
    expected["Art Studio"]["participants"].append(email)

    # Act
    response = client.post(
        "/activities/Art%20Studio/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Art Studio"}
    assert activity_data == expected
    assert activity_data["Art Studio"]["participants"].count(email) == 1


def test_signup_accepts_last_available_spot(client, activity_data):
    # Arrange
    email = "new@mergington.edu"
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


def test_signup_rejects_duplicate_participant(client, activity_data):
    # Arrange
    email = activity_data["Chess Club"]["participants"][0]
    expected = deepcopy(activity_data)

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }
    assert activity_data == expected


def test_signup_rejects_full_activity(client, activity_data):
    # Arrange
    activity_data["Chess Club"]["participants"].append("third@mergington.edu")
    expected = deepcopy(activity_data)

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup", params={"email": "fourth@mergington.edu"}
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Activity is full"}
    assert activity_data == expected


def test_signup_rejects_unknown_activity(client, activity_data):
    # Arrange
    expected = deepcopy(activity_data)
    email = "student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Unknown/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert activity_data == expected


def test_signup_requires_email(client, activity_data):
    # Arrange
    expected = deepcopy(activity_data)
    url = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 422
    assert any(
        error["loc"] == ["query", "email"] and error["type"] == "missing"
        for error in response.json()["detail"]
    )
    assert activity_data == expected
