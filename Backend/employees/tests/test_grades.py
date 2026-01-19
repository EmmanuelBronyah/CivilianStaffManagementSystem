from django.urls import reverse
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import BaseAPITestCase


class CreateGradeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_grade_url = reverse("create-grade")
        self.grade_data = {
            "grade_name": "Senior Executive Officer",
            "rank": self.rank.id,
            "structure": self.structure.id,
        }

        self.authenticate_admin()

    def test_successful_grade_creation(self):
        # Send create request
        response = self.client.post(
            self.create_grade_url, self.grade_data, format="json"
        )

        # Get created activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            models.Grades.objects.filter(grade_name="Senior Executive Officer").exists()
        )
        self.assertIn("added a new Grade", activity_feed)
        self.assertIn("Senior Executive Officer", activity_feed)

    def test_invalid_data(self):
        self.grade_data.update(grade_name="fisher1")
        # Send create request
        response = self.client.post(
            self.create_grade_url, self.grade_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "grade_name")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Grade can only contain letters, spaces, hyphens, and periods.",
                )

    def test_empty_grade(self):
        grade_data_copy = self.grade_data.copy()
        grade_data_copy["grade_name"] = ""

        # Send create request
        response = self.client.post(
            self.create_grade_url, grade_data_copy, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "grade_name")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create requests
        for _ in range(13):
            response = self.client.post(
                self.create_grade_url, self.grade_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveGradeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_grade_url = reverse("create-grade")
        self.retrieve_grade_url = reverse("retrieve-grade", kwargs={"pk": 2})

        self.grade_data = {
            "grade_name": "Senior Executive Officer",
            "rank": self.rank.id,
            "structure": self.structure.id,
        }

        self.authenticate_admin()

    def test_retrieve_existing_grade(self):
        # Send create request
        self.client.post(self.create_grade_url, self.grade_data, format="json")

        # Send get request
        response = self.client.get(self.retrieve_grade_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("grade_name", response.data)
        self.assertIn(response.data["grade_name"], "Senior Executive Officer")

    def test_retrieve_non_existing_grade(self):
        # Send get request
        response = self.client.get(self.retrieve_grade_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_grade_url, self.grade_data, format="json")

        # Send get requests
        for _ in range(13):
            response = self.client.get(self.retrieve_grade_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditGradeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_grade_url = reverse("create-grade")
        self.edit_grade_url = reverse("edit-grade", kwargs={"pk": 2})

        self.grade_data = {
            "grade_name": "Senior Executive Officer",
            "rank": self.rank.id,
            "structure": self.structure.id,
        }

        self.authenticate_admin()

    def test_edit_existing_grade(self):
        edit_data = {"grade_name": "Higher Executive Officer"}

        # Send create request
        self.client.post(self.create_grade_url, self.grade_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_grade_url, edit_data, format="json")

        # Get created activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            models.Grades.objects.filter(grade_name="Higher Executive Officer").exists()
        )
        self.assertIn("updated Grade", activity_feed)
        self.assertIn(
            "Senior Executive Officer → Higher Executive Officer", activity_feed
        )

    def test_edit_non_existing_grade(self):
        edit_data = {"grade_name": "Higher Executive Officer"}

        # Send edit request
        response = self.client.patch(self.edit_grade_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_invalid_data(self):
        # Send create request
        self.client.post(self.create_grade_url, self.grade_data, format="json")

        # Send edit request
        edit_data = {"grade_name": "fisher2"}
        response = self.client.patch(self.edit_grade_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "grade_name")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Grade can only contain letters, spaces, hyphens, and periods.",
                )

    def test_edit_grade_as_empty(self):
        edit_data = {"grade_name": ""}

        # Send create request
        self.client.post(self.create_grade_url, self.grade_data, format="json")

        # Send edit request
        response = self.client.patch(self.edit_grade_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "grade_name")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_throttling(self):
        edit_data = {"grade_name": "Higher Executive Officer"}

        # Send create request
        self.client.post(self.create_grade_url, self.grade_data, format="json")

        # Send edit requests
        for _ in range(13):
            response = self.client.patch(self.edit_grade_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteGradeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_grade_url = reverse("create-grade")
        self.delete_grade_url = reverse("delete-grade", kwargs={"pk": 2})

        self.grade_data = {
            "grade_name": "Senior Executive Officer",
            "rank": self.rank.id,
            "structure": self.structure.id,
        }

        self.authenticate_admin()

    def test_delete_existing_grade(self):
        # Send create request
        self.client.post(self.create_grade_url, self.grade_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_grade_url)

        # Get created activity feed
        activity = "The Grade(Senior Executive Officer) was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_grade(self):
        # Send delete request
        response = self.client.delete(self.delete_grade_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_grade_url, self.grade_data, format="json")

        # Send delete requests
        for _ in range(13):
            response = self.client.delete(self.delete_grade_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
