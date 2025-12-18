from django.urls import reverse
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import BaseAPITestCase
from rest_framework.test import APITestCase


class CreateUnitAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_unit_url = reverse("create-unit")
        self.unit_data = {"unit_name": "4 BN", "city": "KUMASI"}

        self.authenticate_admin()

    def test_successful_unit_creation(self):
        # Send create request
        response = self.client.post(self.create_unit_url, self.unit_data, format="json")

        # Get created activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.Units.objects.filter(unit_name="4 BN").exists())
        self.assertIn("added a new unit", activity_feed)
        self.assertIn("4 BN", activity_feed)

    def test_empty_unit(self):
        unit_data_copy = self.unit_data.copy()
        unit_data_copy["unit_name"] = ""

        # Send create request
        response = self.client.post(self.create_unit_url, unit_data_copy, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Unit cannot be blank or is required.")
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create requests
        self.client.post(self.create_unit_url, self.unit_data, format="json")
        self.client.post(self.create_unit_url, self.unit_data, format="json")
        self.client.post(self.create_unit_url, self.unit_data, format="json")
        self.client.post(self.create_unit_url, self.unit_data, format="json")
        self.client.post(self.create_unit_url, self.unit_data, format="json")
        self.client.post(self.create_unit_url, self.unit_data, format="json")
        self.client.post(self.create_unit_url, self.unit_data, format="json")
        self.client.post(self.create_unit_url, self.unit_data, format="json")
        response = self.client.post(self.create_unit_url, self.unit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveUnitAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_unit_url = reverse("create-unit")
        self.retrieve_unit_url = reverse("retrieve-unit", kwargs={"pk": 1})

        self.unit_data = {"unit_name": "4 BN", "city": "KUMASI"}

        self.authenticate_admin()

    def test_retrieve_existing_unit(self):
        # Send create request
        self.client.post(self.create_unit_url, self.unit_data, format="json")

        # Send get request
        response = self.client.get(self.retrieve_unit_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("unit_name", response.data)
        self.assertIn(response.data["unit_name"], "4 BN")

    def test_retrieve_non_existing_unit(self):
        # Send get request
        response = self.client.get(self.retrieve_unit_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_unit_url, self.unit_data, format="json")

        # Send get requests
        response = self.client.get(self.retrieve_unit_url)
        response = self.client.get(self.retrieve_unit_url)
        response = self.client.get(self.retrieve_unit_url)
        response = self.client.get(self.retrieve_unit_url)
        response = self.client.get(self.retrieve_unit_url)
        response = self.client.get(self.retrieve_unit_url)
        response = self.client.get(self.retrieve_unit_url)
        response = self.client.get(self.retrieve_unit_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class TotalEmployeesPerUnitAPITest(APITestCase):

    def setUp(self):
        self.total_employees_url = reverse("list-employees-per-unit")

    def test_get_total_employees_per_unit(self):
        # Send get request
        response = self.client.get(self.total_employees_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)


class EditUnitAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_unit_url = reverse("create-unit")
        self.edit_unit_url = reverse("edit-unit", kwargs={"pk": 1})

        self.unit_data = {"unit_name": "4 BN", "city": "KUMASI"}

        self.authenticate_admin()

    def test_edit_existing_unit(self):
        edit_data = {"unit_name": "6 BN"}

        # Send create request
        self.client.post(self.create_unit_url, self.unit_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_unit_url, edit_data, format="json")

        # Get created activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.Units.objects.filter(unit_name="6 BN").exists())
        self.assertIn("updated unit", activity_feed)
        self.assertIn("4 BN → 6 BN", activity_feed)

    def test_edit_non_existing_unit(self):
        edit_data = {"unit_name": "6 BN"}

        # Send edit request
        response = self.client.patch(self.edit_unit_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_edit_unit_as_empty(self):
        edit_data = {"unit_name": ""}

        # Send create request
        self.client.post(self.create_unit_url, self.unit_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_unit_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Unit cannot be blank or is required.")
        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_throttling(self):
        edit_data = {"unit_name": "6 BN"}

        # Send create request
        self.client.post(self.create_unit_url, self.unit_data, format="json")

        # Send edit requests
        response = self.client.patch(self.edit_unit_url, edit_data, format="json")
        response = self.client.patch(self.edit_unit_url, edit_data, format="json")
        response = self.client.patch(self.edit_unit_url, edit_data, format="json")
        response = self.client.patch(self.edit_unit_url, edit_data, format="json")
        response = self.client.patch(self.edit_unit_url, edit_data, format="json")
        response = self.client.patch(self.edit_unit_url, edit_data, format="json")
        response = self.client.patch(self.edit_unit_url, edit_data, format="json")
        response = self.client.patch(self.edit_unit_url, edit_data, format="json")
        response = self.client.patch(self.edit_unit_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteUnitAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_unit_url = reverse("create-unit")
        self.delete_unit_url = reverse("delete-unit", kwargs={"pk": 1})

        self.unit_data = {"unit_name": "4 BN", "city": "KUMASI"}

        self.authenticate_admin()

    def test_delete_existing_unit(self):
        # Send create request
        self.client.post(self.create_unit_url, self.unit_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_unit_url)

        # Get created activity feed
        activity = "The unit '4 BN' was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_unit(self):
        # Send delete request
        response = self.client.delete(self.delete_unit_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_unit_url, self.unit_data, format="json")

        # Send delete requests
        response = self.client.delete(self.delete_unit_url)
        response = self.client.delete(self.delete_unit_url)
        response = self.client.delete(self.delete_unit_url)
        response = self.client.delete(self.delete_unit_url)
        response = self.client.delete(self.delete_unit_url)
        response = self.client.delete(self.delete_unit_url)
        response = self.client.delete(self.delete_unit_url)
        response = self.client.delete(self.delete_unit_url)
        response = self.client.delete(self.delete_unit_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
