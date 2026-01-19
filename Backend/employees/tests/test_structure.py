from django.urls import reverse
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import BaseAPITestCase


class CreateStructureAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_structure_url = reverse("create-structure")
        self.structure_data = {"structure_name": "Medical"}

        self.authenticate_admin()

    def test_successful_structure_creation(self):
        # Send create request
        response = self.client.post(
            self.create_structure_url, self.structure_data, format="json"
        )

        # Get created activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            models.Structure.objects.filter(structure_name="Medical").exists()
        )
        self.assertIn("added a new Structure", activity_feed)
        self.assertIn("Medical", activity_feed)

    def test_invalid_data(self):
        structure_data_copy = self.structure_data.copy()
        structure_data_copy["structure_name"] = "iwe99"

        # Send create request
        response = self.client.post(
            self.create_structure_url, structure_data_copy, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "structure_name")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Structure can only contain letters, spaces, hyphens, and periods.",
                )

    def test_empty_structure(self):
        structure_data_copy = self.structure_data.copy()
        structure_data_copy["structure_name"] = ""

        # Send create request
        response = self.client.post(
            self.create_structure_url, structure_data_copy, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "structure_name")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create requests
        for _ in range(13):
            response = self.client.post(
                self.create_structure_url, self.structure_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveStructureAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_structure_url = reverse("create-structure")
        self.retrieve_structure_url = reverse("retrieve-structure", kwargs={"pk": 2})

        self.structure_data = {"structure_name": "Medical"}

        self.authenticate_admin()

    def test_retrieve_existing_structure(self):
        # Send create request
        self.client.post(self.create_structure_url, self.structure_data, format="json")

        # Send get request
        response = self.client.get(self.retrieve_structure_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("structure_name", response.data)
        self.assertIn(response.data["structure_name"], "Medical")

    def test_retrieve_non_existing_structure(self):
        # Send get request
        response = self.client.get(self.retrieve_structure_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_structure_url, self.structure_data, format="json")

        # Send get requests
        for _ in range(13):
            response = self.client.get(self.retrieve_structure_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditStructureAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_structure_url = reverse("create-structure")
        self.edit_structure_url = reverse("edit-structure", kwargs={"pk": 2})

        self.structure_data = {"structure_name": "Medical"}

        self.authenticate_admin()

    def test_edit_existing_structure(self):
        edit_data = {"structure_name": "Non-medical"}

        # Send create request
        self.client.post(self.create_structure_url, self.structure_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_structure_url, edit_data, format="json")

        # Get created activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            models.Structure.objects.filter(structure_name="Non-medical").exists()
        )
        self.assertIn("updated Structure", activity_feed)
        self.assertIn("Medical → Non-medical", activity_feed)

    def test_invalid_data(self):
        # Send create request
        self.client.post(self.create_structure_url, self.structure_data, format="json")

        # Send edit request
        edit_data = {"structure_name": "78r9"}
        response = self.client.patch(self.edit_structure_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "structure_name")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Structure can only contain letters, spaces, hyphens, and periods.",
                )

    def test_edit_non_existing_structure(self):
        edit_data = {"structure_name": "Non-medical"}

        # Send edit request
        response = self.client.patch(self.edit_structure_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_edit_structure_as_empty(self):
        edit_data = {"structure_name": ""}

        # Send create request
        self.client.post(self.create_structure_url, self.structure_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_structure_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "structure_name")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_throttling(self):
        edit_data = {"structure_name": "Non-medical"}

        # Send create request
        self.client.post(self.create_structure_url, self.structure_data, format="json")

        # Send edit requests
        for _ in range(13):
            response = self.client.patch(
                self.edit_structure_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteStructureAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_structure_url = reverse("create-structure")
        self.delete_structure_url = reverse("delete-structure", kwargs={"pk": 2})

        self.structure_data = {"structure_name": "Medical"}

        self.authenticate_admin()

    def test_delete_existing_structure(self):
        # Send create request
        self.client.post(self.create_structure_url, self.structure_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_structure_url)

        # Get created activity feed
        activity = "The Structure(Medical) was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_structure(self):
        # Send delete request
        response = self.client.delete(self.delete_structure_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_structure_url, self.structure_data, format="json")

        # Send delete requests
        for _ in range(13):
            response = self.client.delete(self.delete_structure_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
