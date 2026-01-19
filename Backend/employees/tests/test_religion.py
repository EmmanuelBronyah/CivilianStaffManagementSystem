from django.urls import reverse
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import BaseAPITestCase


class CreateReligionAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_religion_url = reverse("create-religion")
        self.religion_data = {"religion_name": "Christianity"}

        self.authenticate_admin()

    def test_successful_religion_creation(self):
        # Send create request
        response = self.client.post(
            self.create_religion_url, self.religion_data, format="json"
        )

        # Get created activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            models.Religion.objects.filter(religion_name="Christianity").exists()
        )
        self.assertIn("added a new Religion", activity_feed)
        self.assertIn("Christianity", activity_feed)

    def test_invalid_data(self):
        religion_data_copy = self.religion_data.copy()
        religion_data_copy["religion_name"] = "tyu789"

        # Send create request
        response = self.client.post(
            self.create_religion_url, religion_data_copy, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "religion_name")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Religion can only contain letters, spaces, hyphens, and periods.",
                )

    def test_empty_religion(self):
        religion_data_copy = self.religion_data.copy()
        religion_data_copy["religion_name"] = ""

        # Send create request
        response = self.client.post(
            self.create_religion_url, religion_data_copy, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "religion_name")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create requests
        for _ in range(13):
            response = self.client.post(
                self.create_religion_url, self.religion_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveReligionAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_religion_url = reverse("create-religion")
        self.retrieve_religion_url = reverse("retrieve-religion", kwargs={"pk": 1})

        self.religion_data = {"religion_name": "Christianity"}

        self.authenticate_admin()

    def test_retrieve_existing_religion(self):
        # Send create request
        self.client.post(self.create_religion_url, self.religion_data, format="json")

        # Send get request
        response = self.client.get(self.retrieve_religion_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("religion_name", response.data)
        self.assertIn(response.data["religion_name"], "Christianity")

    def test_retrieve_non_existing_religion(self):
        # Send get request
        response = self.client.get(self.retrieve_religion_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_religion_url, self.religion_data, format="json")

        # Send get requests
        for _ in range(13):
            response = self.client.get(self.retrieve_religion_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditReligionAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_religion_url = reverse("create-religion")
        self.edit_religion_url = reverse("edit-religion", kwargs={"pk": 1})

        self.religion_data = {"religion_name": "Christianity"}

        self.authenticate_admin()

    def test_edit_existing_religion(self):
        edit_data = {"religion_name": "Islam"}

        # Send create request
        self.client.post(self.create_religion_url, self.religion_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_religion_url, edit_data, format="json")

        # Get created activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.Religion.objects.filter(religion_name="Islam").exists())
        self.assertIn("updated Religion", activity_feed)
        self.assertIn("Christianity → Islam", activity_feed)

    def test_invalid_data(self):
        edit_data = {"religion_name": "ke767"}

        # Send create request
        self.client.post(self.create_religion_url, self.religion_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_religion_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "religion_name")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Religion can only contain letters, spaces, hyphens, and periods.",
                )

    def test_edit_non_existing_religion(self):
        edit_data = {"religion_name": "Islam"}

        # Send edit request
        response = self.client.patch(self.edit_religion_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_edit_religion_as_empty(self):
        edit_data = {"religion_name": ""}

        # Send create request
        self.client.post(self.create_religion_url, self.religion_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_religion_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "religion_name")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

    def test_throttling(self):
        edit_data = {"religion_name": "Islam"}

        # Send create request
        self.client.post(self.create_religion_url, self.religion_data, format="json")

        # Send edit requests
        for _ in range(13):
            response = self.client.patch(
                self.edit_religion_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteReligionAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_religion_url = reverse("create-religion")
        self.delete_religion_url = reverse("delete-religion", kwargs={"pk": 1})

        self.religion_data = {"religion_name": "Christianity"}

        self.authenticate_admin()

    def test_delete_existing_religion(self):
        # Send create request
        self.client.post(self.create_religion_url, self.religion_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_religion_url)

        # Get created activity feed
        activity = "The Religion(Christianity) was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_religion(self):
        # Send delete request
        response = self.client.delete(self.delete_religion_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_religion_url, self.religion_data, format="json")

        # Send delete requests
        for _ in range(13):
            response = self.client.delete(self.delete_religion_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
