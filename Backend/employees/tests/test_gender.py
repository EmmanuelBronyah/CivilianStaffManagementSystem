from django.urls import reverse
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import BaseAPITestCase
from rest_framework.test import APITestCase


class CreateGenderAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_gender_url = reverse("create-gender")
        self.gender_data = {"sex": "Male"}

        self.authenticate_admin()

    def test_successful_gender_creation(self):
        # Send create request
        response = self.client.post(
            self.create_gender_url, self.gender_data, format="json"
        )

        # Get created activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.Gender.objects.filter(sex="Male").exists())
        self.assertIn("added a new gender", activity_feed)
        self.assertIn("Male", activity_feed)

    def test_empty_gender(self):
        gender_data_copy = self.gender_data.copy()
        gender_data_copy["sex"] = ""

        # Send create request
        response = self.client.post(
            self.create_gender_url, gender_data_copy, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Sex cannot be blank or is required.")
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create requests
        self.client.post(self.create_gender_url, self.gender_data, format="json")
        self.client.post(self.create_gender_url, self.gender_data, format="json")
        self.client.post(self.create_gender_url, self.gender_data, format="json")
        self.client.post(self.create_gender_url, self.gender_data, format="json")
        self.client.post(self.create_gender_url, self.gender_data, format="json")
        self.client.post(self.create_gender_url, self.gender_data, format="json")
        self.client.post(self.create_gender_url, self.gender_data, format="json")
        self.client.post(self.create_gender_url, self.gender_data, format="json")
        response = self.client.post(
            self.create_gender_url, self.gender_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveGenderAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_gender_url = reverse("create-gender")
        self.retrieve_gender_url = reverse("retrieve-gender", kwargs={"pk": 1})

        self.gender_data = {"sex": "Male"}

        self.authenticate_admin()

    def test_retrieve_existing_gender(self):
        # Send create request
        self.client.post(self.create_gender_url, self.gender_data, format="json")

        # Send get request
        response = self.client.get(self.retrieve_gender_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("sex", response.data)
        self.assertIn(response.data["sex"], "Male")

    def test_retrieve_non_existing_gender(self):
        # Send get request
        response = self.client.get(self.retrieve_gender_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_gender_url, self.gender_data, format="json")

        # Send get requests
        response = self.client.get(self.retrieve_gender_url)
        response = self.client.get(self.retrieve_gender_url)
        response = self.client.get(self.retrieve_gender_url)
        response = self.client.get(self.retrieve_gender_url)
        response = self.client.get(self.retrieve_gender_url)
        response = self.client.get(self.retrieve_gender_url)
        response = self.client.get(self.retrieve_gender_url)
        response = self.client.get(self.retrieve_gender_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class TotalMaleAndFemaleAPITest(APITestCase):

    def setUp(self):
        self.total_gender_url = reverse("total-gender")

    def test_get_total_males_and_females(self):
        # Send get request
        response = self.client.get(self.total_gender_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)


class EditGenderAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_gender_url = reverse("create-gender")
        self.edit_gender_url = reverse("edit-gender", kwargs={"pk": 1})

        self.gender_data = {"sex": "Male"}

        self.authenticate_admin()

    def test_edit_existing_gender(self):
        edit_data = {"sex": "Female"}

        # Send create request
        self.client.post(self.create_gender_url, self.gender_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_gender_url, edit_data, format="json")

        # Get created activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.Gender.objects.filter(sex="Female").exists())
        self.assertIn("updated gender", activity_feed)
        self.assertIn("Male → Female", activity_feed)

    def test_edit_non_existing_gender(self):
        edit_data = {"sex": "Female"}

        # Send edit request
        response = self.client.patch(self.edit_gender_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_edit_gender_as_empty(self):
        edit_data = {"sex": ""}

        # Send create request
        self.client.post(self.create_gender_url, self.gender_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_gender_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Sex cannot be blank or is required.")
        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_throttling(self):
        edit_data = {"sex": "Female"}

        # Send create request
        self.client.post(self.create_gender_url, self.gender_data, format="json")

        # Send edit requests
        response = self.client.patch(self.edit_gender_url, edit_data, format="json")
        response = self.client.patch(self.edit_gender_url, edit_data, format="json")
        response = self.client.patch(self.edit_gender_url, edit_data, format="json")
        response = self.client.patch(self.edit_gender_url, edit_data, format="json")
        response = self.client.patch(self.edit_gender_url, edit_data, format="json")
        response = self.client.patch(self.edit_gender_url, edit_data, format="json")
        response = self.client.patch(self.edit_gender_url, edit_data, format="json")
        response = self.client.patch(self.edit_gender_url, edit_data, format="json")
        response = self.client.patch(self.edit_gender_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteGenderAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_gender_url = reverse("create-gender")
        self.delete_gender_url = reverse("delete-gender", kwargs={"pk": 1})

        self.gender_data = {"sex": "Male"}

        self.authenticate_admin()

    def test_delete_existing_gender(self):
        # Send create request
        self.client.post(self.create_gender_url, self.gender_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_gender_url)

        # Get created activity feed
        activity = "The gender 'Male' was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_gender(self):
        # Send delete request
        response = self.client.delete(self.delete_gender_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_gender_url, self.gender_data, format="json")

        # Send delete requests
        response = self.client.delete(self.delete_gender_url)
        response = self.client.delete(self.delete_gender_url)
        response = self.client.delete(self.delete_gender_url)
        response = self.client.delete(self.delete_gender_url)
        response = self.client.delete(self.delete_gender_url)
        response = self.client.delete(self.delete_gender_url)
        response = self.client.delete(self.delete_gender_url)
        response = self.client.delete(self.delete_gender_url)
        response = self.client.delete(self.delete_gender_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
