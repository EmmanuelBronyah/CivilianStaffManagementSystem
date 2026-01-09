from occurance.tests.base import BaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds


class CreateTerminationStatusAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_status_url = reverse("create-termination-status")

        self.status_data = {"termination_status": "Awol"}

        self.authenticate_admin()

    def test_successful_creation(self):
        # Send create request
        response = self.client.post(
            self.create_status_url, self.status_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["termination_status"], "Awol")
        self.assertIn("added a new Termination Status", activity_feed)

    def test_invalid_data(self):
        invalid_data = {
            "termination_status": "Awol" * 200,
        }

        # Send create request
        response = self.client.post(self.create_status_url, invalid_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Status must not have more than 100 characters."
        )

    def test_omit_required_field(self):
        # Omit required field
        self.status_data.update(termination_status="")

        # Send create request
        response = self.client.post(
            self.create_status_url,
            self.status_data,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Status cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_status_url,
                self.status_data,
                format="json",
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditTerminationStatusAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_status_url = reverse("create-termination-status")
        self.edit_status_url = reverse("edit-termination-status", kwargs={"pk": 1})

        self.status_data = {"termination_status": "Awol"}

        self.authenticate_admin()

    def test_successful_edit(self):
        # Send create Termination Status request
        self.client.post(
            self.create_status_url,
            self.status_data,
            format="json",
        )

        edit_data = {"termination_status": "Retired"}

        # Send edit Termination Status request
        response = self.client.patch(self.edit_status_url, edit_data, format="json")

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["termination_status"], "Retired")
        self.assertIn("Status: Awol → Retired", activity_feed)

    def test_invalid_data(self):
        # Send create Termination Status request
        self.client.post(
            self.create_status_url,
            self.status_data,
            format="json",
        )

        edit_data = {"termination_status": "Retired" * 200}

        # Send edit Termination Status request
        response = self.client.patch(self.edit_status_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Status must not have more than 100 characters."
        )

    def test_omit_required_field(self):
        # Send create Termination Status request
        self.client.post(
            self.create_status_url,
            self.status_data,
            format="json",
        )

        edit_data = {"termination_status": ""}

        # Send edit Termination Status request
        response = self.client.patch(self.edit_status_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Status cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create Termination Status request
        self.client.post(
            self.create_status_url,
            self.status_data,
            format="json",
        )

        edit_data = {"termination_status": "Retired"}

        # Send edit Termination Status request
        for _ in range(13):
            response = self.client.patch(self.edit_status_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteTerminationStatusAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_status_url = reverse("create-termination-status")
        self.delete_status_url = reverse("delete-termination-status", kwargs={"pk": 1})

        self.status_data = {"termination_status": "Awol"}

        self.authenticate_admin()

    def test_successful_deletion(self):
        # Send create Termination Status request
        self.client.post(
            self.create_status_url,
            self.status_data,
            format="json",
        )

        # Send delete request
        response = self.client.delete(self.delete_status_url)

        # Get created activity feed
        activity = "The Termination Status 'Awol' was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_status(self):
        # Send delete Termination Status request
        response = self.client.delete(self.delete_status_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create Termination Status request
        self.client.post(
            self.create_status_url,
            self.status_data,
            format="json",
        )

        # Send delete Termination Status request
        for _ in range(13):
            response = self.client.delete(self.delete_status_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
