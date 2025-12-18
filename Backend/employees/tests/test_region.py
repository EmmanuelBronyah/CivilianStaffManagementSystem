from django.urls import reverse
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import BaseAPITestCase


class CreateRegionAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_region_url = reverse("create-region")
        self.region_data = {"region_name": "ACCRA"}

        self.authenticate_admin()

    def test_successful_region_creation(self):
        # Send create request
        response = self.client.post(
            self.create_region_url, self.region_data, format="json"
        )

        # Get created activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.Region.objects.filter(region_name="ACCRA").exists())
        self.assertIn("added a new region", activity_feed)
        self.assertIn("ACCRA", activity_feed)

    def test_empty_region(self):
        region_data_copy = self.region_data.copy()
        region_data_copy["region_name"] = ""

        # Send create request
        response = self.client.post(
            self.create_region_url, region_data_copy, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "Region cannot be blank or is required."
        )
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create requests
        self.client.post(self.create_region_url, self.region_data, format="json")
        self.client.post(self.create_region_url, self.region_data, format="json")
        self.client.post(self.create_region_url, self.region_data, format="json")
        self.client.post(self.create_region_url, self.region_data, format="json")
        self.client.post(self.create_region_url, self.region_data, format="json")
        self.client.post(self.create_region_url, self.region_data, format="json")
        self.client.post(self.create_region_url, self.region_data, format="json")
        self.client.post(self.create_region_url, self.region_data, format="json")
        response = self.client.post(
            self.create_region_url, self.region_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveRegionAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_region_url = reverse("create-region")
        self.retrieve_region_url = reverse("retrieve-region", kwargs={"pk": 1})

        self.region_data = {"region_name": "ACCRA"}

        self.authenticate_admin()

    def test_retrieve_existing_region(self):
        # Send create request
        self.client.post(self.create_region_url, self.region_data, format="json")

        # Send get request
        response = self.client.get(self.retrieve_region_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("region_name", response.data)
        self.assertIn(response.data["region_name"], "ACCRA")

    def test_retrieve_non_existing_region(self):
        # Send get request
        response = self.client.get(self.retrieve_region_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_region_url, self.region_data, format="json")

        # Send get requests
        response = self.client.get(self.retrieve_region_url)
        response = self.client.get(self.retrieve_region_url)
        response = self.client.get(self.retrieve_region_url)
        response = self.client.get(self.retrieve_region_url)
        response = self.client.get(self.retrieve_region_url)
        response = self.client.get(self.retrieve_region_url)
        response = self.client.get(self.retrieve_region_url)
        response = self.client.get(self.retrieve_region_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditRegionAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_region_url = reverse("create-region")
        self.edit_region_url = reverse("edit-region", kwargs={"pk": 1})

        self.region_data = {"region_name": "ACCRA"}

        self.authenticate_admin()

    def test_edit_existing_region(self):
        edit_data = {"region_name": "KUMASI"}

        # Send create request
        self.client.post(self.create_region_url, self.region_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_region_url, edit_data, format="json")

        # Get created activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.Region.objects.filter(region_name="KUMASI").exists())
        self.assertIn("updated region", activity_feed)
        self.assertIn("ACCRA → KUMASI", activity_feed)

    def test_edit_non_existing_region(self):
        edit_data = {"region_name": "KUMASI"}

        # Send edit request
        response = self.client.patch(self.edit_region_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_edit_region_as_empty(self):
        edit_data = {"region_name": ""}

        # Send create request
        self.client.post(self.create_region_url, self.region_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_region_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "Region cannot be blank or is required."
        )
        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_throttling(self):
        edit_data = {"region_name": "KUMASI"}

        # Send create request
        self.client.post(self.create_region_url, self.region_data, format="json")

        # Send edit requests
        response = self.client.patch(self.edit_region_url, edit_data, format="json")
        response = self.client.patch(self.edit_region_url, edit_data, format="json")
        response = self.client.patch(self.edit_region_url, edit_data, format="json")
        response = self.client.patch(self.edit_region_url, edit_data, format="json")
        response = self.client.patch(self.edit_region_url, edit_data, format="json")
        response = self.client.patch(self.edit_region_url, edit_data, format="json")
        response = self.client.patch(self.edit_region_url, edit_data, format="json")
        response = self.client.patch(self.edit_region_url, edit_data, format="json")
        response = self.client.patch(self.edit_region_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteRegionAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_region_url = reverse("create-region")
        self.delete_region_url = reverse("delete-region", kwargs={"pk": 1})

        self.region_data = {"region_name": "ACCRA"}

        self.authenticate_admin()

    def test_delete_existing_region(self):
        # Send create request
        self.client.post(self.create_region_url, self.region_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_region_url)

        # Get created activity feed
        activity = "The region 'ACCRA' was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_region(self):
        # Send delete request
        response = self.client.delete(self.delete_region_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_region_url, self.region_data, format="json")

        # Send delete requests
        response = self.client.delete(self.delete_region_url)
        response = self.client.delete(self.delete_region_url)
        response = self.client.delete(self.delete_region_url)
        response = self.client.delete(self.delete_region_url)
        response = self.client.delete(self.delete_region_url)
        response = self.client.delete(self.delete_region_url)
        response = self.client.delete(self.delete_region_url)
        response = self.client.delete(self.delete_region_url)
        response = self.client.delete(self.delete_region_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
