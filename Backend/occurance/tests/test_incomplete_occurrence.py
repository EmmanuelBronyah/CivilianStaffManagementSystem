from django.urls import reverse
from ..models import IncompleteOccurrence
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from occurance.tests.base import EmployeeBaseAPITestCase
from flags.models import FlagType


class CreateIncompleteOccurrenceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_incomplete_occurrence_url = reverse("create-incomplete-occurrence")
        self.create_employee_url = reverse("create-employee")

        FlagType.objects.create(flag_type="Incomplete Record")

        self.incomplete_occurrence = {
            "employee": "000993",
            "service_id": "",
            "grade": self.grade.id,
            "authority": "CEM 20/24",
            "level_step": self.level_step.id,
            "event": self.event.id,
            "wef_date": None,
            "reason": "10% Salary Adjustment",
            "percentage_adjustment": 10,
        }

        self.authenticate_standard_user()

    def test_successful_occurrence_record_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_incomplete_occurrence_url,
            self.incomplete_occurrence,
            format="json",
        )

        # Get last activity
        activity_feed = ActivityFeeds.objects.all()[1].activity
        last_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["service_id"], "")
        self.assertTrue(IncompleteOccurrence.objects.filter(id=1).exists())
        self.assertIn("added a new Incomplete Occurrence", activity_feed)
        self.assertIn("Incomplete occurrence was flagged", last_feed)

    def test_create_occurrence_record_with_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        occurrence_record = self.incomplete_occurrence.copy()
        occurrence_record["wef_date"] = "2027-09-07"

        # Send create request
        response = self.client.post(
            self.create_incomplete_occurrence_url,
            occurrence_record,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "wef_date")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Wef Date cannot be a future date.",
                )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        for _ in range(13):
            response = self.client.post(
                self.create_incomplete_occurrence_url,
                self.incomplete_occurrence,
                format="json",
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveIncompleteOccurrenceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_incomplete_occurrence_url = reverse("create-incomplete-occurrence")
        self.retrieve_incomplete_occurrence_url = reverse(
            "retrieve-incomplete-occurrence", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")

        self.incomplete_occurrence = {
            "employee": "000993",
            "service_id": "",
            "grade": self.grade.id,
            "authority": "CEM 20/24",
            "level_step": self.level_step.id,
            "event": self.event.id,
            "wef_date": None,
            "reason": "10% Salary Adjustment",
            "percentage_adjustment": 10,
        }

        self.authenticate_standard_user()

    def test_get_existing_occurrence_record(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_occurrence_url,
            self.incomplete_occurrence,
            format="json",
        )

        # Send get request
        response = self.client.get(
            self.retrieve_incomplete_occurrence_url, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn("service_id", response.data)

    def test_get_non_existing_occurrence_record(self):
        # Send get request
        response = self.client.get(
            self.retrieve_incomplete_occurrence_url, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_occurrence_url,
            self.incomplete_occurrence,
            format="json",
        )

        # Send get requests
        for _ in range(13):
            response = self.client.get(
                self.retrieve_incomplete_occurrence_url, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditIncompleteOccurrenceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_incomplete_occurrence_url = reverse("create-incomplete-occurrence")
        self.edit_incomplete_occurrence_url = reverse(
            "edit-incomplete-occurrence", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")

        self.incomplete_occurrence = {
            "employee": "000993",
            "service_id": "",
            "grade": self.grade.id,
            "authority": "CEM 20/24",
            "level_step": self.level_step.id,
            "event": self.event.id,
            "wef_date": None,
            "reason": "10% Salary Adjustment",
            "percentage_adjustment": 10,
        }

        self.authenticate_standard_user()

    def test_edit_occurrence_record(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        create_response = self.client.post(
            self.create_incomplete_occurrence_url,
            self.incomplete_occurrence,
            format="json",
        )

        # Send patch/edit request
        edit_data = {
            "wef_date": "2023-09-06",
            "authority": "CEM 09/23",
        }
        edit_response = self.client.patch(
            self.edit_incomplete_occurrence_url, edit_data, format="json"
        )

        # Get created activity feed
        activity_feed = ActivityFeeds.objects.all()[3].activity

        # Assertions
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(edit_response.status_code, status.HTTP_200_OK)
        self.assertTrue(IncompleteOccurrence.objects.filter(id=1).exists())
        self.assertIn("updated Incomplete Occurrence", activity_feed)

    def test_invalid_data_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_occurrence_url,
            self.incomplete_occurrence,
            format="json",
        )

        # Send patch/edit request with a blank required field
        edit_data = {
            "service_id": "tyu88*",
        }
        edit_response = self.client.patch(
            self.edit_incomplete_occurrence_url, edit_data, format="json"
        )

        # Get last activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = edit_response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "service_id")

            for error in field_errors:
                self.assertIn(error, "Service ID can only contain numbers.")

        self.assertNotIn("updated employee", activity_feed)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_occurrence_url,
            self.incomplete_occurrence,
            format="json",
        )

        edit_data = {
            "service_id": "012763",
        }

        # Send patch/edit request
        for _ in range(13):
            response = self.client.patch(
                self.edit_incomplete_occurrence_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteIncompleteOccurrenceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_incomplete_occurrence_url = reverse("create-incomplete-occurrence")
        self.delete_incomplete_occurrence_url = reverse(
            "delete-incomplete-occurrence", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")

        self.incomplete_occurrence = {
            "employee": "000993",
            "service_id": "",
            "grade": self.grade.id,
            "authority": "CEM 20/24",
            "level_step": self.level_step.id,
            "event": self.event.id,
            "wef_date": None,
            "reason": "10% Salary Adjustment",
            "percentage_adjustment": 10,
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_occurrence_url,
            self.incomplete_occurrence,
            format="json",
        )

        # Send delete request
        response = self.client.delete(self.delete_incomplete_occurrence_url)

        # Get created activity feed
        activity_feed = ActivityFeeds.objects.all()[3].activity
        last_activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            "The Incomplete Occurrence(ID: 1 — Authority: CEM 20/24 — Event: Salary Adjustment) was deleted by Standard User",
            activity_feed,
        )
        self.assertIn(
            "Incomplete occurrence flag was deleted by Standard User.",
            last_activity_feed,
        )

    def test_delete_non_existing_employee(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_incomplete_occurrence_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_occurrence_url,
            self.incomplete_occurrence,
            format="json",
        )

        # Send delete requests
        for _ in range(13):
            response = self.client.delete(self.delete_incomplete_occurrence_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
