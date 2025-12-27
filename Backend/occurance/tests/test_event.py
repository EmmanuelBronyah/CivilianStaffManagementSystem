from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import BaseAPITestCase


class CreateEventAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_event_url = reverse("create-event")

        self.authenticate_admin()

    def test_successful_event_creation(self):
        self.event_data = {"event_name": "Dead"}
        # Send create request
        response = self.client.post(
            self.create_event_url, self.event_data, format="json"
        )

        # Get activity
        activity_feed = ActivityFeeds.objects.first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("added a new Event", activity_feed)
        self.assertIn("Dead", activity_feed)

    def test_omit_required_field(self):
        self.event_data = {"event_name": ""}
        # Send create request
        response = self.client.post(
            self.create_event_url, self.event_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "Event cannot be blank or is required."
        )

    def test_invalid_data(self):
        self.event_data = {"event_name": "t" * 300}
        # Send create request
        response = self.client.post(
            self.create_event_url, self.event_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "Event must not have more than 255 characters."
        )

    def test_throttling(self):
        self.event_data = {"event_name": "Dead"}
        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_event_url, self.event_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditEventAPITest(BaseAPITestCase):

    def setUp(self):
        self.edit_event_url = reverse("edit-event", kwargs={"pk": 1})
        self.create_event_url = reverse("create-event")

        self.event_data = {"event_name": "Dead"}

        self.authenticate_admin()

    def test_successful_event_edit(self):
        edit_data = {"event_name": "Alive"}
        # Send create event request
        self.client.post(self.create_event_url, self.event_data, format="json")

        # Send edit event request
        response = self.client.patch(self.edit_event_url, edit_data, format="json")

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Event: Dead → Alive", activity_feed)

    def test_omit_required_field(self):
        edit_data = {"event_name": ""}
        # Send create event request
        self.client.post(self.create_event_url, self.event_data, format="json")

        # Send edit event request
        response = self.client.patch(self.edit_event_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("Event cannot be blank or is required", response.data["error"])

    def test_invalid_data(self):
        edit_data = {"event_name": "t" * 300}
        # Send create event request
        self.client.post(self.create_event_url, self.event_data, format="json")

        # Send edit event request
        response = self.client.patch(self.edit_event_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "Event must not have more than 255 characters."
        )

    def test_throttling(self):
        edit_data = {"event_name": "Dead"}
        # Send create Event request
        self.client.post(self.create_event_url, self.event_data, format="json")

        # Send edit event request
        for _ in range(13):
            response = self.client.patch(self.edit_event_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveEventAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_event_url = reverse("create-event")
        self.retrieve_event_url = reverse("retrieve-event", kwargs={"pk": 1})

        self.event_data = {"event_name": "Dead"}

        self.authenticate_admin()

    def test_retrieve_existing_event(self):
        self.client.post(self.create_event_url, self.event_data, format="json")

        # Send edit event request
        response = self.client.get(self.retrieve_event_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)

    def test_retrieve_non_existing_event(self):
        # Send edit event request
        response = self.client.get(self.retrieve_event_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        self.client.post(self.create_event_url, self.event_data, format="json")

        # Send edit event request
        for _ in range(13):
            response = self.client.get(self.retrieve_event_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteEventAPITest(BaseAPITestCase):

    def setUp(self):
        self.delete_event_url = reverse("delete-event", kwargs={"pk": 1})
        self.create_event_url = reverse("create-event")

        self.event_data = {"event_name": "Dead"}

        self.authenticate_admin()

    def test_successful_deletion(self):
        # Send create event request
        self.client.post(self.create_event_url, self.event_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_event_url)

        # Get created activity feed
        activity = "The Event 'Dead' was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_event(self):
        # Send delete event request
        response = self.client.delete(self.delete_event_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create event request
        self.client.post(self.create_event_url, self.event_data, format="json")

        # Send delete event request
        for _ in range(13):
            response = self.client.delete(self.delete_event_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
