import unittest
from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import activities, app


class UnregisterTests(unittest.TestCase):
    def setUp(self):
        self.original_activities = deepcopy(activities)
        self.client = TestClient(app)
        self.email = activities["Chess Club"]["participants"][0]
        self.url = "/activities/Chess%20Club/unregister"

    def tearDown(self):
        activities.clear()
        activities.update(self.original_activities)
        self.client.close()

    def test_unregister_removes_only_selected_participant(self):
        response = self.client.delete(self.url, params={"email": self.email})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message": f"Unregistered {self.email} from Chess Club"
        })
        expected = deepcopy(self.original_activities)
        expected["Chess Club"]["participants"].remove(self.email)
        self.assertEqual(self.client.get("/activities").json(), expected)

    def test_unknown_activity_is_rejected(self):
        response = self.client.delete(
            "/activities/Unknown/unregister", params={"email": self.email}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Activity not found")
        self.assertEqual(activities, self.original_activities)

    def test_unregistered_participant_is_rejected(self):
        response = self.client.delete(self.url, params={"email": "unknown@example.com"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"], "Student is not signed up for this activity"
        )
        self.assertEqual(activities, self.original_activities)

    def test_missing_email_is_rejected(self):
        self.assertEqual(self.client.delete(self.url).status_code, 422)
        self.assertEqual(activities, self.original_activities)

    def test_participant_can_sign_up_again_after_unregistering(self):
        self.assertEqual(
            self.client.delete(self.url, params={"email": self.email}).status_code, 200
        )
        self.assertEqual(
            self.client.delete(self.url, params={"email": self.email}).status_code, 400
        )
        response = self.client.post(
            "/activities/Chess%20Club/signup", params={"email": self.email}
        )

        self.assertEqual(response.status_code, 200)
        duplicate = self.client.post(
            "/activities/Chess%20Club/signup", params={"email": self.email}
        )
        self.assertEqual(duplicate.status_code, 400)


if __name__ == "__main__":
    unittest.main()
