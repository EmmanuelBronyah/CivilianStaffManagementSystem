from occurance.tests.base import BaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds


class CreateMilitaryRankAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_military_rank_url = reverse("create-military-rank")

        self.military_rank_data = {
            "rank": "Captain",
            "branch": "ARMY",
        }

        self.authenticate_admin()

    def test_successful_creation(self):
        # Send create request
        response = self.client.post(
            self.create_military_rank_url, self.military_rank_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["rank"], "Captain")
        self.assertEqual(response.data["branch"], "ARMY")
        self.assertIn("added a new Military Rank", activity_feed)

    def test_invalid_data(self):
        invalid_data = {
            "rank": "Captain" * 200,
            "branch": "NAVY",
        }

        # Send create request
        response = self.client.post(
            self.create_military_rank_url, invalid_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Rank must not have more than 255 characters."
        )

    def test_omit_required_field(self):
        # Omit required field
        self.military_rank_data.update(rank="")

        # Send create request
        response = self.client.post(
            self.create_military_rank_url,
            self.military_rank_data,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Rank cannot be blank or is required.")

    def test_throttling(self):
        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_military_rank_url,
                self.military_rank_data,
                format="json",
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditMilitaryRankAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_military_rank_url = reverse("create-military-rank")
        self.edit_military_rank_url = reverse("edit-military-rank", kwargs={"pk": 1})

        self.military_rank_data = {
            "rank": "Captain",
            "branch": "ARMY",
        }

        self.authenticate_admin()

    def test_successful_edit(self):
        # Send create military rank request
        self.client.post(
            self.create_military_rank_url,
            self.military_rank_data,
            format="json",
        )

        edit_data = {"rank": "Flight Lieutenant", "branch": "AIRFORCE"}

        # Send edit military rank request
        response = self.client.patch(
            self.edit_military_rank_url, edit_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rank"], "Flight Lieutenant")
        self.assertEqual(response.data["branch"], "AIRFORCE")
        self.assertIn("Rank: Captain → Flight Lieutenant", activity_feed)
        self.assertIn("Branch: ARMY → AIRFORCE", activity_feed)

    def test_invalid_data(self):
        # Send create military rank request
        self.client.post(
            self.create_military_rank_url,
            self.military_rank_data,
            format="json",
        )

        edit_data = {"branch": "AIRFPORCE" * 200}

        # Send edit military rank request
        response = self.client.patch(
            self.edit_military_rank_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Branch must not have more than 100 characters."
        )

    def test_omit_required_field(self):
        # Send create military rank request
        self.client.post(
            self.create_military_rank_url,
            self.military_rank_data,
            format="json",
        )

        edit_data = {"rank": ""}

        # Send edit military rank request
        response = self.client.patch(
            self.edit_military_rank_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Rank cannot be blank or is required.")

    def test_throttling(self):
        # Send create military rank request
        self.client.post(
            self.create_military_rank_url,
            self.military_rank_data,
            format="json",
        )

        edit_data = {"rank": "Flight Lieutenant"}

        # Send edit military rank request
        for _ in range(13):
            response = self.client.patch(
                self.edit_military_rank_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteMilitaryRankAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_military_rank_url = reverse("create-military-rank")
        self.delete_military_rank_url = reverse(
            "delete-military-rank", kwargs={"pk": 1}
        )

        self.military_rank_data = {
            "rank": "Captain",
            "branch": "ARMY",
        }

        self.authenticate_admin()

    def test_successful_deletion(self):
        # Send create military rank request
        self.client.post(
            self.create_military_rank_url,
            self.military_rank_data,
            format="json",
        )

        # Send delete request
        response = self.client.delete(self.delete_military_rank_url)

        # Get created activity feed
        activity = "The Military Rank 'Captain' was deleted by Administrator"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_military_rank(self):
        # Send delete military rank request
        response = self.client.delete(self.delete_military_rank_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create military rank request
        self.client.post(
            self.create_military_rank_url,
            self.military_rank_data,
            format="json",
        )

        # Send delete military rank request
        for _ in range(13):
            response = self.client.delete(self.delete_military_rank_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
