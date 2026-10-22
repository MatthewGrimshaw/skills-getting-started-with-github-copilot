from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def activity_data():
    original_activities = deepcopy(activities)
    try:
        activities.clear()
        activities.update({
            "Chess Club": {
                "description": "Practice chess strategies",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 3,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            "Art Studio": {
                "description": "Explore painting and drawing",
                "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
                "max_participants": 2,
                "participants": [],
            },
        })
        yield activities
    finally:
        activities.clear()
        activities.update(original_activities)


@pytest.fixture
def client(activity_data):
    with TestClient(app) as test_client:
        yield test_client
