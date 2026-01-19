from django.urls import reverse
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import BaseAPITestCase


class CreateMaritalStatusAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_marital_status_url = reverse("create-marital-status")
        self.marital_status_data = {"marital_status_name": "Single"}

        self.authenticate_admin()

    def test_successful_marital_status_creation(self):
        # Send create request
        response = self.client.post(
            self.create_marital_status_url, self.marital_status_data, format="json"
        )

        # Get created activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            models.MaritalStatus.objects.filter(marital_status_name="Single").exists()
        )
        self.assertIn("added a new Marital Status", activity_feed)
        self.assertIn("Single", activity_feed)

    def test_invalid_data(self):
        # Send create request
        self.marital_status_data.update(marital_status_name="32321")
        response = self.client.post(
            self.create_marital_status_url, self.marital_status_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "marital_status_name")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Marital Status can only contain letters, spaces, hyphens, and periods.",
                )

    def test_empty_marital_status(self):
        marital_status_data_copy = self.marital_status_data.copy()
        marital_status_data_copy["marital_status_name"] = ""

        # Send create request
        response = self.client.post(
            self.create_marital_status_url, marital_status_data_copy, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "marital_status_name")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create requests
        for _ in range(13):
            response = self.client.post(
                self.create_marital_status_url, self.marital_status_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveMaritalStatusAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_marital_status_url = reverse("create-marital-status")
        self.retrieve_marital_status_url = reverse(
            "retrieve-marital-status", kwargs={"pk": 1}
        )

        self.marital_status_data = {"marital_status_name": "Single"}

        self.authenticate_admin()

    def test_retrieve_existing_marital_status(self):
        # Send create request
        self.client.post(
            self.create_marital_status_url, self.marital_status_data, format="json"
        )

        # Send get request
        response = self.client.get(self.retrieve_marital_status_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("marital_status_name", response.data)
        self.assertIn(response.data["marital_status_name"], "Single")

    def test_retrieve_non_existing_marital_status(self):
        # Send get request
        response = self.client.get(self.retrieve_marital_status_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create request
        self.client.post(
            self.create_marital_status_url, self.marital_status_data, format="json"
        )

        # Send get requests
        for _ in range(13):
            response = self.client.get(self.retrieve_marital_status_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditMaritalStatusAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_marital_status_url = reverse("create-marital-status")
        self.edit_marital_status_url = reverse("edit-marital-status", kwargs={"pk": 1})

        self.marital_status_data = {"marital_status_name": "Single"}

        self.authenticate_admin()

    def test_edit_existing_marital_status(self):
        edit_data = {"marital_status_name": "Married"}

        # Send create request
        self.client.post(
            self.create_marital_status_url, self.marital_status_data, format="json"
        )

        # Send edit request
        response = self.client.patch(
            self.edit_marital_status_url, edit_data, format="json"
        )

        # Get created activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            models.MaritalStatus.objects.filter(marital_status_name="Married").exists()
        )
        self.assertIn("updated Marital Status", activity_feed)
        self.assertIn("Single → Married", activity_feed)

    def test_edit_non_existing_marital_status(self):
        edit_data = {"marital_status_name": "Married"}

        # Send edit request
        response = self.client.patch(
            self.edit_marital_status_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_invalid_data(self):
        edit_data = {"marital_status_name": "35tt2"}

        # Send create request
        self.client.post(
            self.create_marital_status_url, self.marital_status_data, format="json"
        )

        # Send edit request
        response = self.client.patch(
            self.edit_marital_status_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "marital_status_name")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Marital Status can only contain letters, spaces, hyphens, and periods.",
                )

    def test_edit_marital_status_as_empty(self):
        edit_data = {"marital_status_name": ""}

        # Send create request
        self.client.post(
            self.create_marital_status_url, self.marital_status_data, format="json"
        )

        # Send edit request
        response = self.client.patch(
            self.edit_marital_status_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "marital_status_name")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

    def test_throttling(self):
        edit_data = {"marital_status_name": "Married"}

        # Send create request
        self.client.post(
            self.create_marital_status_url, self.marital_status_data, format="json"
        )

        # Send edit requests
        for _ in range(13):
            response = self.client.patch(
                self.edit_marital_status_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteMaritalStatusAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_marital_status_url = reverse("create-marital-status")
        self.delete_marital_status_url = reverse(
            "delete-marital-status", kwargs={"pk": 1}
        )

        self.marital_status_data = {"marital_status_name": "Single"}

        self.authenticate_admin()

    def test_delete_existing_marital_status(self):
        # Send create request
        self.client.post(
            self.create_marital_status_url, self.marital_status_data, format="json"
        )

        # Send delete request
        response = self.client.delete(self.delete_marital_status_url)

        # Get created activity feed
        activity = "The Marital Status(Single) was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_marital_status(self):
        # Send delete request
        response = self.client.delete(self.delete_marital_status_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create request
        self.client.post(
            self.create_marital_status_url, self.marital_status_data, format="json"
        )

        # Send delete requests
        for _ in range(13):
            response = self.client.delete(self.delete_marital_status_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
