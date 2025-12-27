from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import BaseAPITestCase


class CreateSalaryAdjustmentPercentageAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_percentage_adjustment_url = reverse("create-percentage-adjustment")

        self.authenticate_admin()

    def test_successful_percentage_adjustment_creation(self):
        self.percentage_adjustment_data = {"percentage_adjustment": "10"}
        # Send create request
        response = self.client.post(
            self.create_percentage_adjustment_url,
            self.percentage_adjustment_data,
            format="json",
        )

        # Get activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("added a new Salary Adjustment Percentage", activity_feed)
        self.assertIn("10%", activity_feed)

    def test_omit_required_field(self):
        self.percentage_adjustment_data = {"percentage_adjustment": ""}
        # Send create request
        response = self.client.post(
            self.create_percentage_adjustment_url,
            self.percentage_adjustment_data,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"],
            "Invalid format for Salary Percentage Adjustment.",
        )

    def test_invalid_data(self):
        self.percentage_adjustment_data = {"percentage_adjustment": "t" * 300}
        # Send create request
        response = self.client.post(
            self.create_percentage_adjustment_url,
            self.percentage_adjustment_data,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "Invalid format for Salary Percentage Adjustment."
        )

    def test_throttling(self):
        self.percentage_adjustment_data = {"percentage_adjustment": "10"}
        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_percentage_adjustment_url,
                self.percentage_adjustment_data,
                format="json",
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditSalaryAdjustmentPercentageAPITest(BaseAPITestCase):

    def setUp(self):
        self.edit_percentage_adjustment_url = reverse(
            "edit-percentage-adjustment", kwargs={"pk": 1}
        )
        self.create_percentage_adjustment_url = reverse("create-percentage-adjustment")

        self.percentage_adjustment_data = {"percentage_adjustment": "10"}

        self.authenticate_admin()

    def test_successful_percentage_adjustment_edit(self):
        edit_data = {"percentage_adjustment": "23"}
        # Send create percentage adjustment request
        self.client.post(
            self.create_percentage_adjustment_url,
            self.percentage_adjustment_data,
            format="json",
        )

        # Send edit percentage adjustment request
        response = self.client.patch(
            self.edit_percentage_adjustment_url, edit_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Percentage Adjustment: 10% → 23%", activity_feed)

    def test_omit_required_field(self):
        edit_data = {"percentage_adjustment": ""}
        # Send create percentage adjustment request
        self.client.post(
            self.create_percentage_adjustment_url,
            self.percentage_adjustment_data,
            format="json",
        )

        # Send edit percentage adjustment request
        response = self.client.patch(
            self.edit_percentage_adjustment_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn(
            "Invalid format for Salary Percentage Adjustment.", response.data["error"]
        )

    def test_invalid_data(self):
        edit_data = {"percentage_adjustment": "t" * 300}
        # Send create percentage adjustment request
        self.client.post(
            self.create_percentage_adjustment_url,
            self.percentage_adjustment_data,
            format="json",
        )

        # Send edit percentage adjustment request
        response = self.client.patch(
            self.edit_percentage_adjustment_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "Invalid format for Salary Percentage Adjustment."
        )

    def test_throttling(self):
        edit_data = {"percentage_adjustment": "10"}
        # Send create percentage adjustment request
        self.client.post(
            self.create_percentage_adjustment_url,
            self.percentage_adjustment_data,
            format="json",
        )

        # Send edit percentage adjustment request
        for _ in range(13):
            response = self.client.patch(
                self.edit_percentage_adjustment_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveSalaryAdjustmentPercentageAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_percentage_adjustment_url = reverse("create-percentage-adjustment")
        self.retrieve_percentage_adjustment_url = reverse(
            "retrieve-percentage-adjustment", kwargs={"pk": 1}
        )

        self.percentage_adjustment_data = {"percentage_adjustment": "10"}

        self.authenticate_admin()

    def test_retrieve_existing_percentage_adjustment(self):
        self.client.post(
            self.create_percentage_adjustment_url,
            self.percentage_adjustment_data,
            format="json",
        )

        # Send edit percentage adjustment request
        response = self.client.get(self.retrieve_percentage_adjustment_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)

    def test_retrieve_non_existing_percentage_adjustment(self):
        # Send edit percentage adjustment request
        response = self.client.get(self.retrieve_percentage_adjustment_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        self.client.post(
            self.create_percentage_adjustment_url,
            self.percentage_adjustment_data,
            format="json",
        )

        # Send edit percentage adjustment request
        for _ in range(13):
            response = self.client.get(self.retrieve_percentage_adjustment_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteSalaryAdjustmentPercentageAPITest(BaseAPITestCase):

    def setUp(self):
        self.delete_percentage_adjustment_url = reverse(
            "delete-percentage-adjustment", kwargs={"pk": 1}
        )
        self.create_percentage_adjustment_url = reverse("create-percentage-adjustment")

        self.percentage_adjustment_data = {"percentage_adjustment": "10"}

        self.authenticate_admin()

    def test_successful_deletion(self):
        # Send create percentage adjustment request
        self.client.post(
            self.create_percentage_adjustment_url,
            self.percentage_adjustment_data,
            format="json",
        )

        # Send delete request
        response = self.client.delete(self.delete_percentage_adjustment_url)

        # Get created activity feed
        activity = "The Salary Adjustment Percentage '10%' was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_percentage_adjustment(self):
        # Send delete occurrence request
        response = self.client.delete(self.delete_percentage_adjustment_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create percentage adjustment request
        self.client.post(
            self.create_percentage_adjustment_url,
            self.percentage_adjustment_data,
            format="json",
        )

        # Send delete percentage adjustment request
        for _ in range(13):
            response = self.client.delete(self.delete_percentage_adjustment_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
