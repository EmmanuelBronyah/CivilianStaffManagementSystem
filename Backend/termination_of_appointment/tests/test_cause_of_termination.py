from occurance.tests.base import BaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds


class CreateCauseOfTerminationAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_cause_url = reverse("create-cause-of-termination")

        self.cause_data = {"termination_cause": "Death"}

        self.authenticate_admin()

    def test_successful_creation(self):
        # Send create request
        response = self.client.post(
            self.create_cause_url, self.cause_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["termination_cause"], "Death")
        self.assertIn("added a new Causes Of Termination", activity_feed)

    def test_invalid_data(self):
        invalid_data = {
            "termination_cause": "Death1",
        }

        # Send create request
        response = self.client.post(self.create_cause_url, invalid_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "termination_cause")

            for error in field_errors:
                self.assertEqual(error, "Cause can only contain letters and spaces.")

    def test_omit_required_field(self):
        # Omit required field
        self.cause_data.update(termination_cause="")

        # Send create request
        response = self.client.post(
            self.create_cause_url,
            self.cause_data,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "termination_cause")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

    def test_throttling(self):
        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_cause_url,
                self.cause_data,
                format="json",
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditCauseOfTerminationAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_cause_url = reverse("create-cause-of-termination")
        self.edit_cause_url = reverse("edit-cause-of-termination", kwargs={"pk": 1})

        self.cause_data = {"termination_cause": "Death"}

        self.authenticate_admin()

    def test_successful_edit(self):
        # Send create Cause Of Termination request
        self.client.post(
            self.create_cause_url,
            self.cause_data,
            format="json",
        )

        edit_data = {"termination_cause": "Retired"}

        # Send edit Cause Of Termination request
        response = self.client.patch(self.edit_cause_url, edit_data, format="json")

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["termination_cause"], "Retired")
        self.assertIn("Cause: Death → Retired", activity_feed)

    def test_invalid_data(self):
        # Send create Cause Of Termination request
        self.client.post(
            self.create_cause_url,
            self.cause_data,
            format="json",
        )

        edit_data = {"termination_cause": "Retired%"}

        # Send edit Cause Of Termination request
        response = self.client.patch(self.edit_cause_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "termination_cause")

            for error in field_errors:
                self.assertEqual(error, "Cause can only contain letters and spaces.")

    def test_omit_required_field(self):
        # Send create Cause Of Termination request
        self.client.post(
            self.create_cause_url,
            self.cause_data,
            format="json",
        )

        edit_data = {"termination_cause": ""}

        # Send edit Cause Of Termination request
        response = self.client.patch(self.edit_cause_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "termination_cause")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

    def test_throttling(self):
        # Send create Cause Of Termination request
        self.client.post(
            self.create_cause_url,
            self.cause_data,
            format="json",
        )

        edit_data = {"termination_cause": "Retired"}

        # Send edit Cause Of Termination request
        for _ in range(13):
            response = self.client.patch(self.edit_cause_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteCauseOfTerminationAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_cause_url = reverse("create-cause-of-termination")
        self.delete_cause_url = reverse("delete-cause-of-termination", kwargs={"pk": 1})

        self.cause_data = {"termination_cause": "Death"}

        self.authenticate_admin()

    def test_successful_deletion(self):
        # Send create Cause Of Termination request
        self.client.post(
            self.create_cause_url,
            self.cause_data,
            format="json",
        )

        # Send delete request
        response = self.client.delete(self.delete_cause_url)

        # Get created activity feed
        activity = "The Causes Of Termination(Death) was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_cause(self):
        # Send delete Cause Of Termination request
        response = self.client.delete(self.delete_cause_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create Cause Of Termination request
        self.client.post(
            self.create_cause_url,
            self.cause_data,
            format="json",
        )

        # Send delete Cause Of Termination request
        for _ in range(13):
            response = self.client.delete(self.delete_cause_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
