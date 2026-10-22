from copy import deepcopy


def test_get_activities_returns_activity_details(client, activity_data):
    # Arrange
    expected = deepcopy(activity_data)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected
    assert activity_data == expected
    for activity in response.json().values():
        assert set(activity) == {
            "description", "schedule", "max_participants", "participants"
        }


def test_get_activities_returns_empty_dictionary_when_no_activities_exist(
    client, activity_data
):
    # Arrange
    activity_data.clear()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {}
    assert activity_data == {}
