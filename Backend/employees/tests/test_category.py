from django.urls import reverse
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import BaseAPITestCase


class CreateCategoryAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_category_url = reverse("create-category")
        self.category_data = {"category_name": "Junior"}

        self.authenticate_admin()

    def test_successful_category_creation(self):
        # Send create request
        response = self.client.post(
            self.create_category_url, self.category_data, format="json"
        )

        # Get created activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.Category.objects.filter(category_name="Junior").exists())
        self.assertIn("added a new Category", activity_feed)
        self.assertIn("Junior", activity_feed)

    def test_empty_category(self):
        category_data_copy = self.category_data.copy()
        category_data_copy["category_name"] = ""

        # Send create request
        response = self.client.post(
            self.create_category_url, category_data_copy, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("category_name", response.data)
        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "category_name")
            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create requests
        for _ in range(13):
            response = self.client.post(
                self.create_category_url, self.category_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveCategoryAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_category_url = reverse("create-category")
        self.retrieve_category_url = reverse("retrieve-category", kwargs={"pk": 2})

        self.category_data = {"category_name": "Junior"}

        self.authenticate_admin()

    def test_retrieve_existing_category(self):
        # Send create request
        self.client.post(self.create_category_url, self.category_data, format="json")

        # Send get request
        response = self.client.get(self.retrieve_category_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("category_name", response.data)
        self.assertIn(response.data["category_name"], "Junior")

    def test_retrieve_non_existing_category(self):
        # Send get request
        response = self.client.get(self.retrieve_category_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_category_url, self.category_data, format="json")

        # Send get requests
        for _ in range(13):
            response = self.client.get(self.retrieve_category_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditCategoryAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_category_url = reverse("create-category")
        self.edit_category_url = reverse("edit-category", kwargs={"pk": 2})

        self.category_data = {"category_name": "Junior"}

        self.authenticate_admin()

    def test_edit_existing_category(self):
        edit_data = {"category_name": "Senior"}

        # Send create request
        self.client.post(self.create_category_url, self.category_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_category_url, edit_data, format="json")

        # Get created activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.Category.objects.filter(category_name="Senior").exists())
        self.assertIn("updated Category", activity_feed)
        self.assertIn("Junior → Senior", activity_feed)

    def test_edit_non_existing_category(self):
        edit_data = {"category_name": "Senior"}

        # Send edit request
        response = self.client.patch(self.edit_category_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_edit_category_as_empty(self):
        edit_data = {"category_name": ""}

        # Send create request
        self.client.post(self.create_category_url, self.category_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_category_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("category_name", response.data)
        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "category_name")
            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")
        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_throttling(self):
        edit_data = {"category_name": "Senior"}

        # Send create request
        self.client.post(self.create_category_url, self.category_data, format="json")

        # Send edit requests
        for _ in range(13):
            response = self.client.patch(
                self.edit_category_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteCategoryAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_category_url = reverse("create-category")
        self.delete_category_url = reverse("delete-category", kwargs={"pk": 2})

        self.category_data = {"category_name": "Junior"}

        self.authenticate_admin()

    def test_delete_existing_category(self):
        # Send create request
        response = self.client.post(
            self.create_category_url, self.category_data, format="json"
        )

        # Send delete request
        response = self.client.delete(self.delete_category_url)

        # Get created activity feed
        activity = "The Category(Junior) was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_category(self):
        # Send delete request
        response = self.client.delete(self.delete_category_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_delete_referenced_category(self):
        # Send delete request
        delete_category_url = reverse("delete-category", kwargs={"pk": 1})
        response = self.client.delete(delete_category_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"],
            "This record cannot be deleted because it is currently in use.",
        )
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_category_url, self.category_data, format="json")

        # Send delete requests
        for _ in range(13):
            response = self.client.delete(self.delete_category_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
