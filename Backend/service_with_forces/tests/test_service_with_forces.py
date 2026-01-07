from occurance.tests.base import EmployeeBaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from service_with_forces.models import MilitaryRanks


class CreateServiceWithForcesAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_service_with_forces_url = reverse("create-service-with-forces")
        self.create_employee_url = reverse("create-employee")

        self.military_rank = MilitaryRanks.objects.create(rank="Captain", branch="ARMY")

        self.service_with_forces_data = {
            "employee": "000993",
            "service_date": "2022-09-09",
            "last_unit": self.unit.id,
            "service_number": "000993",
            "military_rank": self.military_rank.id,
        }

        self.authenticate_standard_user()

    def test_successful_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_service_with_forces_url,
            self.service_with_forces_data,
            format="json",
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["employee"], "000993")
        self.assertEqual(response.data["service_date"], "2022-09-09")
        self.assertIn("added a new Service With Forces", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        invalid_data = {
            "employee": "000993",
            "service_date": "2022-20-09",
            "last_unit": self.unit.id,
            "service_number": "000993",
            "military_rank": self.military_rank.id,
        }

        # Send create request
        response = self.client.post(
            self.create_service_with_forces_url, invalid_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid format for Service Date.")

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Omit required field
        self.service_with_forces_data.update(service_number="")

        # Send create request
        response = self.client.post(
            self.create_service_with_forces_url,
            self.service_with_forces_data,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Service Number cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_service_with_forces_url,
                self.service_with_forces_data,
                format="json",
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditServiceWithForcesAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_service_with_forces_url = reverse("create-service-with-forces")
        self.edit_service_with_forces_url = reverse(
            "edit-service-with-forces", kwargs={"pk": 1}
        )

        self.military_rank = MilitaryRanks.objects.create(rank="Captain", branch="ARMY")

        self.service_with_forces_data = {
            "employee": "000993",
            "service_date": "2022-09-09",
            "last_unit": self.unit.id,
            "service_number": "000993",
            "military_rank": self.military_rank.id,
        }

        self.authenticate_standard_user()

    def test_successful_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create service with forces request
        self.client.post(
            self.create_service_with_forces_url,
            self.service_with_forces_data,
            format="json",
        )

        edit_data = {"service_date": "2023-09-03"}

        # Send edit service with forces request
        response = self.client.patch(
            self.edit_service_with_forces_url, edit_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["service_date"], "2023-09-03")
        self.assertIn("Service Date: 2022-09-09 → 2023-09-03", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create service with forces request
        self.client.post(
            self.create_service_with_forces_url,
            self.service_with_forces_data,
            format="json",
        )

        edit_data = {"service_date": "tyui"}

        # Send edit service with forces request
        response = self.client.patch(
            self.edit_service_with_forces_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid format for Service Date.")

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create service with forces request
        self.client.post(
            self.create_service_with_forces_url,
            self.service_with_forces_data,
            format="json",
        )

        edit_data = {"military_rank": ""}

        # Send edit service with forces request
        response = self.client.patch(
            self.edit_service_with_forces_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Military Rank cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create service with forces request
        self.client.post(
            self.create_service_with_forces_url,
            self.service_with_forces_data,
            format="json",
        )

        edit_data = {"service_date": "2023-09-03"}

        # Send edit service with forces request
        for _ in range(13):
            response = self.client.patch(
                self.edit_service_with_forces_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveEmployeeServiceWithForcesAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_service_with_forces_url = reverse("create-service-with-forces")
        self.retrieve_service_with_forces_url = reverse(
            "list-employee-service-with-forces", kwargs={"pk": "000993"}
        )

        self.military_rank = MilitaryRanks.objects.create(rank="Captain", branch="ARMY")

        self.service_with_forces_data = {
            "employee": "000993",
            "service_date": "2022-09-09",
            "last_unit": self.unit.id,
            "service_number": "000993",
            "military_rank": self.military_rank.id,
        }

        self.authenticate_standard_user()

    def test_successful_retrieval(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create service with forces request
        for _ in range(5):
            self.client.post(
                self.create_service_with_forces_url,
                self.service_with_forces_data,
                format="json",
            )

        # Send get service with forces request
        response = self.client.get(self.retrieve_service_with_forces_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_non_existing_employee(self):
        # Send create service with forces request
        for _ in range(5):
            self.client.post(
                self.create_service_with_forces_url,
                self.service_with_forces_data,
                format="json",
            )

        # Send get service with forces request
        response = self.client.get(self.retrieve_service_with_forces_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Employee matches the given query."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create service with forces request
        self.client.post(
            self.create_service_with_forces_url,
            self.service_with_forces_data,
            format="json",
        )

        # Send get service with forces request
        for _ in range(13):
            response = self.client.get(self.retrieve_service_with_forces_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteServiceWithForcesAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_service_with_forces_url = reverse("create-service-with-forces")
        self.delete_service_with_forces_url = reverse(
            "delete-service-with-forces", kwargs={"pk": 1}
        )

        self.military_rank = MilitaryRanks.objects.create(rank="Captain", branch="ARMY")

        self.service_with_forces_data = {
            "employee": "000993",
            "service_date": "2022-09-09",
            "last_unit": self.unit.id,
            "service_number": "000993",
            "military_rank": self.military_rank.id,
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create service with forces request
        self.client.post(
            self.create_service_with_forces_url,
            self.service_with_forces_data,
            format="json",
        )

        # Send delete request
        response = self.client.delete(self.delete_service_with_forces_url)

        # Get created activity feed
        activity = "The Service With Forces '2022-09-09 — 4 Bn - ' was deleted by Standard User"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_service_with_forces(self):
        # Send delete service with forces request
        response = self.client.delete(self.delete_service_with_forces_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create service with forces request
        self.client.post(
            self.create_service_with_forces_url,
            self.service_with_forces_data,
            format="json",
        )

        # Send delete service with forces request
        for _ in range(13):
            response = self.client.delete(self.delete_service_with_forces_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
