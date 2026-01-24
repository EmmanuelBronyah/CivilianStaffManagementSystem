from django.urls import reverse
from ..models import FlagType
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from employees.tests.base import BaseAPITestCase


class CreateFlagTypeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_flag_type_url = reverse("create-flag-type")
        self.flag_type = {
            "flag_type": "Invalid Record",
        }

        self.authenticate_admin()

    def test_successful_flag_type_creation(self):
        # Send create request
        response = self.client.post(
            self.create_flag_type_url, self.flag_type, format="json"
        )

        # Get created activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FlagType.objects.filter(flag_type="Invalid Record").exists())
        self.assertIn("added a new Flag Type", activity_feed)
        self.assertIn("Invalid Record", activity_feed)

    def test_invalid_data(self):
        self.flag_type.update(flag_type="fisher1")
        # Send create request
        response = self.client.post(
            self.create_flag_type_url, self.flag_type, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "flag_type")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Flag Type can only contain letters and spaces.",
                )

    def test_empty_flag_type(self):
        flag_type_copy = self.flag_type.copy()
        flag_type_copy["flag_type"] = ""

        # Send create request
        response = self.client.post(
            self.create_flag_type_url, flag_type_copy, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "flag_type")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create requests
        for _ in range(13):
            response = self.client.post(
                self.create_flag_type_url, self.flag_type, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveFlagTypeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_flag_type_url = reverse("create-flag-type")
        self.retrieve_flag_type_url = reverse("retrieve-flag-type", kwargs={"pk": 1})

        self.flag_type = {
            "flag_type": "Invalid Record",
        }

        self.authenticate_admin()

    def test_retrieve_existing_flag_type(self):
        # Send create request
        self.client.post(self.create_flag_type_url, self.flag_type, format="json")

        # Send get request
        response = self.client.get(self.retrieve_flag_type_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("flag_type", response.data)
        self.assertIn(response.data["flag_type"], "Invalid Record")

    def test_retrieve_non_existing_flag_type(self):
        # Send get request
        response = self.client.get(self.retrieve_flag_type_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_flag_type_url, self.flag_type, format="json")

        # Send get requests
        for _ in range(13):
            response = self.client.get(self.retrieve_flag_type_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditFlagTypeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_flag_type_url = reverse("create-flag-type")
        self.edit_flag_type_url = reverse("edit-flag-type", kwargs={"pk": 1})

        self.flag_type = {
            "flag_type": "Invalid Record",
        }

        self.authenticate_admin()

    def test_edit_existing_flag_type(self):
        edit_data = {"flag_type": "Incomplete Record"}

        # Send create request
        self.client.post(self.create_flag_type_url, self.flag_type, format="json")

        # Send edit request
        response = self.client.patch(self.edit_flag_type_url, edit_data, format="json")

        # Get created activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(FlagType.objects.filter(flag_type="Incomplete Record").exists())
        self.assertIn("updated Flag Type", activity_feed)
        self.assertIn("Invalid Record → Incomplete Record", activity_feed)

    def test_edit_non_existing_flag_type(self):
        edit_data = {"flag_type": "Incomplete Record"}

        # Send edit request
        response = self.client.patch(self.edit_flag_type_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_invalid_data(self):
        # Send create request
        self.client.post(self.create_flag_type_url, self.flag_type, format="json")

        # Send edit request
        edit_data = {"flag_type": "fisher2"}
        response = self.client.patch(self.edit_flag_type_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "flag_type")

            for error in field_errors:
                self.assertEqual(
                    error, "Flag Type can only contain letters and spaces."
                )

    def test_edit_grade_as_empty(self):
        edit_data = {"flag_type": ""}

        # Send create request
        self.client.post(self.create_flag_type_url, self.flag_type, format="json")

        # Send edit request
        response = self.client.patch(self.edit_flag_type_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "flag_type")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_throttling(self):
        edit_data = {"flag_type": "Incomplete Record"}

        # Send create request
        self.client.post(self.create_flag_type_url, self.flag_type, format="json")

        # Send edit requests
        for _ in range(13):
            response = self.client.patch(
                self.edit_flag_type_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteFlagTypeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_flag_type_url = reverse("create-flag-type")
        self.delete_flag_type_url = reverse("delete-flag-type", kwargs={"pk": 1})

        self.flag_type = {
            "flag_type": "Invalid Record",
        }

        self.authenticate_admin()

    def test_delete_existing_flag_type(self):
        # Send create request
        self.client.post(self.create_flag_type_url, self.flag_type, format="json")

        # Send delete request
        response = self.client.delete(self.delete_flag_type_url)

        # Get created activity feed
        activity = "The Flag Type(Invalid Record) was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_flag_type(self):
        # Send delete request
        response = self.client.delete(self.delete_flag_type_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_flag_type_url, self.flag_type, format="json")

        # Send delete requests
        for _ in range(13):
            response = self.client.delete(self.delete_flag_type_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
