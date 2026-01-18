from django.urls import reverse
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import BaseAPITestCase


class CreateBloodGroupAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_blood_group_url = reverse("create-blood-group")
        self.blood_group_data = {"blood_group_name": "O+"}

        self.authenticate_admin()

    def test_successful_blood_group_creation(self):
        # Send create request
        response = self.client.post(
            self.create_blood_group_url, self.blood_group_data, format="json"
        )

        # Get created activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            models.BloodGroup.objects.filter(blood_group_name="O+").exists()
        )
        self.assertIn("added a new Blood Group", activity_feed)
        self.assertIn("O+", activity_feed)

    def test_empty_blood_group(self):
        blood_group_data_copy = self.blood_group_data.copy()
        blood_group_data_copy["blood_group_name"] = ""

        # Send create request
        response = self.client.post(
            self.create_blood_group_url, blood_group_data_copy, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "blood_group_name")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create requests
        for _ in range(13):
            response = self.client.post(
                self.create_blood_group_url, self.blood_group_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveBloodGroupAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_blood_group_url = reverse("create-blood-group")
        self.retrieve_blood_group_url = reverse(
            "retrieve-blood-group", kwargs={"pk": 1}
        )

        self.blood_group_data = {"blood_group_name": "O+"}

        self.authenticate_admin()

    def test_retrieve_existing_blood_group(self):
        # Send create request
        self.client.post(
            self.create_blood_group_url, self.blood_group_data, format="json"
        )

        # Send get request
        response = self.client.get(self.retrieve_blood_group_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("blood_group_name", response.data)
        self.assertIn(response.data["blood_group_name"], "O+")

    def test_retrieve_non_existing_blood_group(self):
        # Send get request
        response = self.client.get(self.retrieve_blood_group_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create request
        self.client.post(
            self.create_blood_group_url, self.blood_group_data, format="json"
        )

        # Send get requests
        for _ in range(13):
            response = self.client.get(self.retrieve_blood_group_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditBloodGroupAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_blood_group_url = reverse("create-blood-group")
        self.edit_blood_group_url = reverse("edit-blood-group", kwargs={"pk": 1})

        self.blood_group_data = {"blood_group_name": "O+"}

        self.authenticate_admin()

    def test_edit_existing_blood_group(self):
        edit_data = {"blood_group_name": "A+"}

        # Send create request
        self.client.post(
            self.create_blood_group_url, self.blood_group_data, format="json"
        )

        # Send edit request
        response = self.client.patch(
            self.edit_blood_group_url, edit_data, format="json"
        )

        # Get created activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            models.BloodGroup.objects.filter(blood_group_name="A+").exists()
        )
        self.assertIn("updated Blood Group", activity_feed)
        self.assertIn("O+ → A+", activity_feed)

    def test_edit_non_existing_blood_group(self):
        edit_data = {"blood_group_name": "A+"}

        # Send edit request
        response = self.client.patch(
            self.edit_blood_group_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_edit_blood_group_as_empty(self):
        edit_data = {"blood_group_name": ""}

        # Send create request
        self.client.post(
            self.create_blood_group_url, self.blood_group_data, format="json"
        )

        # Send edit request
        response = self.client.patch(
            self.edit_blood_group_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "blood_group_name")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_throttling(self):
        edit_data = {"blood_group_name": "A+"}

        # Send create request
        self.client.post(
            self.create_blood_group_url, self.blood_group_data, format="json"
        )

        # Send edit requests
        for _ in range(13):
            response = self.client.patch(
                self.edit_blood_group_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteBloodGroupAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_blood_group_url = reverse("create-blood-group")
        self.delete_blood_group_url = reverse("delete-blood-group", kwargs={"pk": 1})

        self.blood_group_data = {"blood_group_name": "O+"}

        self.authenticate_admin()

    def test_delete_existing_blood_group(self):
        # Send create request
        self.client.post(
            self.create_blood_group_url, self.blood_group_data, format="json"
        )

        # Send delete request
        response = self.client.delete(self.delete_blood_group_url)

        # Get created activity feed
        activity = "The Blood Group(O+) was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_blood_group(self):
        # Send delete request
        response = self.client.delete(self.delete_blood_group_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create request
        self.client.post(
            self.create_blood_group_url, self.blood_group_data, format="json"
        )

        # Send delete requests
        for _ in range(13):
            response = self.client.delete(self.delete_blood_group_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
