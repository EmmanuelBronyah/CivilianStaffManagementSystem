from occurance.tests.base import EmployeeBaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds


class CreatePreviousGovernmentServiceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_previous_government_service_url = reverse(
            "create-previous-government-service"
        )
        self.create_employee_url = reverse("create-employee")

        self.previous_government_service_data = {
            "employee": "000993",
            "institution": "GAF",
            "start_date": "2025-09-05",
            "end_date": "2025-09-06",
            "position": "SEO",
        }

        self.authenticate_standard_user()

    def test_successful_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_previous_government_service_url,
            self.previous_government_service_data,
            format="json",
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["employee"], "000993")
        self.assertEqual(response.data["institution"], "GAF")
        self.assertIn("added a new Previous Government Service", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        invalid_data = {
            "employee": "000993",
            "institution": "GAF",
            "start_date": "2025-20-05",
            "end_date": "2025-09-06",
            "position": "SEO",
        }

        # Send create request
        response = self.client.post(
            self.create_previous_government_service_url, invalid_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid format for Start Date.")

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Omit required field
        self.previous_government_service_data.update(position="")

        # Send create request
        response = self.client.post(
            self.create_previous_government_service_url,
            self.previous_government_service_data,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Position cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_previous_government_service_url,
                self.previous_government_service_data,
                format="json",
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditPreviousGovernmentServiceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_previous_government_service_url = reverse(
            "create-previous-government-service"
        )
        self.edit_previous_government_service_url = reverse(
            "edit-previous-government-service", kwargs={"pk": 1}
        )

        self.previous_government_service_data = {
            "employee": "000993",
            "institution": "GAF",
            "start_date": "2025-09-05",
            "end_date": "2025-09-06",
            "position": "SEO",
        }

        self.authenticate_standard_user()

    def test_successful_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create previous government service request
        self.client.post(
            self.create_previous_government_service_url,
            self.previous_government_service_data,
            format="json",
        )

        edit_data = {"position": "CTO", "institution": "META"}

        # Send edit previous government service request
        response = self.client.patch(
            self.edit_previous_government_service_url, edit_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["position"], "CTO")
        self.assertEqual(response.data["institution"], "META")
        self.assertIn("Position: SEO → CTO", activity_feed)
        self.assertIn("Institution: GAF → META", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create previous government service request
        self.client.post(
            self.create_previous_government_service_url,
            self.previous_government_service_data,
            format="json",
        )

        edit_data = {"end_date": "tyui"}

        # Send edit previous government service request
        response = self.client.patch(
            self.edit_previous_government_service_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid format for End Date.")

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create previous government service request
        self.client.post(
            self.create_previous_government_service_url,
            self.previous_government_service_data,
            format="json",
        )

        edit_data = {"position": ""}

        # Send edit previous government service request
        response = self.client.patch(
            self.edit_previous_government_service_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Position cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create previous government service request
        self.client.post(
            self.create_previous_government_service_url,
            self.previous_government_service_data,
            format="json",
        )

        edit_data = {"position": "CTO"}

        # Send edit previous government service request
        for _ in range(13):
            response = self.client.patch(
                self.edit_previous_government_service_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveEmployeePreviousGovernmentServiceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_previous_government_service_url = reverse(
            "create-previous-government-service"
        )
        self.retrieve_employee_previous_government_service_url = reverse(
            "list-employee-previous-government-service", kwargs={"pk": "000993"}
        )

        self.previous_government_service_data = {
            "employee": "000993",
            "institution": "GAF",
            "start_date": "2025-09-05",
            "end_date": "2025-09-06",
            "position": "SEO",
        }

        self.authenticate_standard_user()

    def test_successful_retrieval(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create previous government service request
        for _ in range(5):
            self.client.post(
                self.create_previous_government_service_url,
                self.previous_government_service_data,
                format="json",
            )

        # Send get employee children request
        response = self.client.get(
            self.retrieve_employee_previous_government_service_url
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_non_existing_employee(self):
        # Send create previous government service request
        for _ in range(5):
            self.client.post(
                self.create_previous_government_service_url,
                self.previous_government_service_data,
                format="json",
            )

        # Send get employee previous government service request
        response = self.client.get(
            self.retrieve_employee_previous_government_service_url
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Employee matches the given query."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create previous government service request
        self.client.post(
            self.create_previous_government_service_url,
            self.previous_government_service_data,
            format="json",
        )

        # Send get employee previous government service request
        for _ in range(13):
            response = self.client.get(
                self.retrieve_employee_previous_government_service_url
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeletePreviousGovernmentServiceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_previous_government_service_url = reverse(
            "create-previous-government-service"
        )
        self.delete_previous_government_service_url = reverse(
            "delete-previous-government-service", kwargs={"pk": 1}
        )

        self.previous_government_service_data = {
            "employee": "000993",
            "institution": "GAF",
            "start_date": "2025-09-05",
            "end_date": "2025-09-06",
            "position": "SEO",
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create previous government service request
        self.client.post(
            self.create_previous_government_service_url,
            self.previous_government_service_data,
            format="json",
        )

        # Send delete request
        response = self.client.delete(self.delete_previous_government_service_url)

        # Get created activity feed
        activity = (
            "The Previous Government Service 'GAF — SEO' was deleted by Standard User"
        )
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_previous_government_service(self):
        # Send delete previous government service request
        response = self.client.delete(self.delete_previous_government_service_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create previous government service request
        self.client.post(
            self.create_previous_government_service_url,
            self.previous_government_service_data,
            format="json",
        )

        # Send delete previous government service request
        for _ in range(13):
            response = self.client.delete(self.delete_previous_government_service_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
