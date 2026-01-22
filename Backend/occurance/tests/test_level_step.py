from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import BaseAPITestCase


class CreateLevelStepAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_level_step_url = reverse("create-level-step")

        self.authenticate_admin()

    def test_successful_level_step_creation(self):
        self.level_step_data = {"level_step": "18H01", "monthly_salary": 6000}
        # Send create request
        response = self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Get activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("added a new Level|Step", activity_feed)
        self.assertIn("Level|Step: 18H01 — Monthly Salary: 6000.00", activity_feed)

    def test_omit_required_field(self):
        self.level_step_data = {"level_step": "", "monthly_salary": 6000}
        # Send create request
        response = self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "level_step")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

    def test_invalid_data(self):
        self.level_step_data = {"level_step": "18H01", "monthly_salary": 990}
        # Send create request
        response = self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "monthly_salary")

            for error in field_errors:
                self.assertEqual(error, "Salary cannot be lesser than 1000.00")

    def test_throttling(self):
        self.level_step_data = {"level_step": "18H01", "monthly_salary": 6000}
        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_level_step_url, self.level_step_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditLevelStepAPITest(BaseAPITestCase):

    def setUp(self):
        self.edit_level_step_url = reverse("edit-level-step", kwargs={"pk": 1})
        self.create_level_step_url = reverse("create-level-step")

        self.level_step_data = {"level_step": "18H01", "monthly_salary": 6000}

        self.authenticate_admin()

    def test_successful_level_step_edit(self):
        edit_data = {"level_step": "25L01", "monthly_salary": "4004.89"}
        # Send create level|step request
        self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Send edit level|step request
        response = self.client.patch(self.edit_level_step_url, edit_data, format="json")

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            "Level|Step: 18H01 → 25L01 — Monthly Salary: 6000.00 → 4004.89",
            activity_feed,
        )

    def test_omit_required_field(self):
        edit_data = {"level_step": "", "monthly_salary": "4004.89"}
        # Send create level|step request
        self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Send edit level|step request
        response = self.client.patch(self.edit_level_step_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "level_step")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

    def test_invalid_data(self):
        edit_data = {"level_step": "25H01", "monthly_salary": "rtyu"}
        # Send create level|step request
        self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Send edit level|step request
        response = self.client.patch(self.edit_level_step_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "monthly_salary")

            for error in field_errors:
                self.assertEqual(error, "A valid number is required.")

    def test_throttling(self):
        edit_data = {"level_step": "25H01", "monthly_salary": "4000.89"}
        # Send create level|step request
        self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Send edit level|step request
        for _ in range(13):
            response = self.client.patch(
                self.edit_level_step_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveLevelStepAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_level_step_url = reverse("create-level-step")
        self.retrieve_level_step_url = reverse("retrieve-level-step", kwargs={"pk": 1})

        self.level_step_data = {"level_step": "18H01", "monthly_salary": 6000}

        self.authenticate_admin()

    def test_retrieve_existing_level_step(self):
        self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Send edit level|step request
        response = self.client.get(self.retrieve_level_step_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)

    def test_retrieve_non_existing_level_step(self):
        # Send edit level|step request
        response = self.client.get(self.retrieve_level_step_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Send edit level|step request
        for _ in range(13):
            response = self.client.get(self.retrieve_level_step_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteLevelStepAPITest(BaseAPITestCase):

    def setUp(self):
        self.delete_level_step_url = reverse("delete-level-step", kwargs={"pk": 1})
        self.create_level_step_url = reverse("create-level-step")

        self.level_step_data = {"level_step": "18H01", "monthly_salary": 6000}

        self.authenticate_admin()

    def test_successful_deletion(self):
        # Send create level|step request
        self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Send delete request
        response = self.client.delete(self.delete_level_step_url)

        # Get created activity feed
        activity = "The Level|Step(Level|Step: 18H01 — Monthly Salary: 6000.00) was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_level_step(self):
        # Send delete occurrence request
        response = self.client.delete(self.delete_level_step_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create level|step request
        self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Send delete level|step request
        for _ in range(13):
            response = self.client.delete(self.delete_level_step_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class CalculateAnnualSalaryAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_level_step_url = reverse("create-level-step")
        self.calculate_annual_salary_url = reverse(
            "calculate-annual-salary", kwargs={"pk": 1}
        )
        self.level_step_data = {"level_step": "18H01", "monthly_salary": 6000}

        self.authenticate_admin()

    def test_successful_calculation(self):
        # Send create level|step request
        self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Send calculate annual salary request
        response = self.client.get(self.calculate_annual_salary_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("annual_salary", response.data)
        self.assertEqual(response.data["annual_salary"], 72000)

    def test_non_existing_level_step(self):
        # Send calculate annual salary request
        response = self.client.get(self.calculate_annual_salary_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create level|step request
        self.client.post(
            self.create_level_step_url, self.level_step_data, format="json"
        )

        # Send calculate annual salary request
        for _ in range(13):
            response = self.client.get(self.calculate_annual_salary_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
