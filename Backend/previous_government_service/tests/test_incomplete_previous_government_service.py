from django.urls import reverse
from ..models import IncompletePreviousGovernmentServiceRecords
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from occurance.tests.base import EmployeeBaseAPITestCase
from flags.models import FlagType


class CreateIncompletePreviousGovernmentServiceRecordsAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_incomplete_government_service_url = reverse(
            "create-incomplete-previous-government-service"
        )
        self.create_employee_url = reverse("create-employee")
        FlagType.objects.create(flag_type="Incomplete Record")

        self.service_record = {
            "employee": "000993",
            "service_id": "",
            "institution": "GAF",
            "duration": "5 years",
            "position": "SEO",
        }

        self.authenticate_standard_user()

    def test_successful_service_record_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_incomplete_government_service_url,
            self.service_record,
            format="json",
        )

        # Get last activity
        activity_feed = ActivityFeeds.objects.all()[1].activity
        last_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["institution"], "GAF")
        self.assertTrue(
            IncompletePreviousGovernmentServiceRecords.objects.filter(id=1).exists()
        )
        self.assertIn(
            "added a new Incomplete Previous Government Service", activity_feed
        )
        self.assertIn(
            "Incomplete previous government service records was flagged", last_feed
        )

    def test_create_service_record_with_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        service_record = self.service_record.copy()
        service_record["position"] = "HR1"

        # Send create request
        response = self.client.post(
            self.create_incomplete_government_service_url, service_record, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "position")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Position can only contain letters, spaces, hyphens, commas, and periods.",
                )

    def test_all_fields_none(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        service_record = self.service_record.copy()
        service_record = {key: None for key, _ in service_record.items()}

        # Send create request
        response = self.client.post(
            self.create_incomplete_government_service_url, service_record, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error,
                    "All fields for Incomplete Previous Government Service cannot be empty.",
                )

    def test_only_duration_has_value(self):
        service_record = self.service_record.copy()
        service_record = {
            key: "5years" if key == "duration" else None
            for key, value in service_record.items()
        }

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_incomplete_government_service_url, service_record, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Cannot save Incomplete Previous Government Service with Duration or Service ID as the only non-empty fields.",
                )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        for _ in range(13):
            response = self.client.post(
                self.create_incomplete_government_service_url,
                self.service_record,
                format="json",
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveIncompletePreviousGovernmentServiceRecordsAPITest(
    EmployeeBaseAPITestCase
):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_incomplete_government_service_url = reverse(
            "create-incomplete-previous-government-service"
        )
        self.retrieve_service_record_url = reverse(
            "retrieve-incomplete-previous-government-service", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")

        self.service_record = {
            "employee": "000993",
            "service_id": "",
            "institution": "GAF",
            "duration": "5 years",
            "position": "SEO",
        }

        self.authenticate_standard_user()

    def test_get_existing_service_record(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_government_service_url,
            self.service_record,
            format="json",
        )

        # Send get request
        response = self.client.get(self.retrieve_service_record_url, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn("service_id", response.data)

    def test_get_non_existing_service_record(self):
        # Send get request
        response = self.client.get(self.retrieve_service_record_url, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_government_service_url,
            self.service_record,
            format="json",
        )

        # Send get requests
        for _ in range(13):
            response = self.client.get(self.retrieve_service_record_url, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditIncompletePreviousGovernmentServiceRecordsAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_incomplete_government_service_url = reverse(
            "create-incomplete-previous-government-service"
        )
        self.edit_service_record_url = reverse(
            "edit-incomplete-previous-government-service", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")

        self.service_record = {
            "employee": "000993",
            "service_id": "",
            "institution": "GAF",
            "duration": "5 years",
            "position": "SEO",
        }

        self.authenticate_standard_user()

    def test_edit_service_record(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        create_response = self.client.post(
            self.create_incomplete_government_service_url,
            self.service_record,
            format="json",
        )

        # Send patch/edit request
        edit_data = {
            "position": "nurse",
            "institution": "GAF",
        }
        edit_response = self.client.patch(
            self.edit_service_record_url, edit_data, format="json"
        )

        # Get created activity feed
        activity_feed = ActivityFeeds.objects.all()[3].activity

        # Assertions
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(edit_response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            IncompletePreviousGovernmentServiceRecords.objects.filter(id=1).exists()
        )
        self.assertIn("updated Incomplete Previous Government Service", activity_feed)

    def test_all_fields_none(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_incomplete_government_service_url,
            self.service_record,
            format="json",
        )

        # Send patch/edit request
        edit_data = self.service_record.copy()
        edit_data = {key: None for key, _ in edit_data.items()}
        edit_response = self.client.patch(
            self.edit_service_record_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = edit_response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error,
                    "All fields for Incomplete Previous Government Service cannot be empty.",
                )

    def test_invalid_data_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_government_service_url,
            self.service_record,
            format="json",
        )

        # Send patch/edit request with a blank required field
        edit_data = {
            "institution": "tyu88*",
        }
        edit_response = self.client.patch(
            self.edit_service_record_url, edit_data, format="json"
        )

        # Get last activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = edit_response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "institution")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Institution can only contain letters, spaces, hyphens, commas, and periods.",
                )

        self.assertNotIn("updated employee", activity_feed)

    def test_only_duration_has_value(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_incomplete_government_service_url,
            self.service_record,
            format="json",
        )

        # Send edit request
        edit_data = self.service_record.copy()
        edit_data = {
            key: "5years" if key == "duration" else None
            for key, value in edit_data.items()
        }
        edit_response = self.client.patch(
            self.edit_service_record_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = edit_response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Cannot save Incomplete Previous Government Service with Duration or Service ID as the only non-empty fields.",
                )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_government_service_url,
            self.service_record,
            format="json",
        )

        edit_data = {
            "service_id": "012763",
        }

        # Send patch/edit request
        for _ in range(13):
            response = self.client.patch(
                self.edit_service_record_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteIncompletePreviousGovernmentServiceRecordsAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_incomplete_government_service_url = reverse(
            "create-incomplete-previous-government-service"
        )
        self.delete_service_record_url = reverse(
            "delete-incomplete-previous-government-service", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")

        self.service_record = {
            "employee": "000993",
            "service_id": "",
            "institution": "GAF",
            "duration": "5 years",
            "position": "SEO",
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_government_service_url,
            self.service_record,
            format="json",
        )

        # Send delete request
        response = self.client.delete(self.delete_service_record_url)

        # Get created activity feed
        activity_feed = ActivityFeeds.objects.all()[3].activity
        last_activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            "The Incomplete Previous Government Service(ID: 1) was deleted by Standard User",
            activity_feed,
        )
        self.assertIn(
            "Incomplete previous government service records flag was deleted by Standard User.",
            last_activity_feed,
        )

    def test_delete_non_existing_employee(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_service_record_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_government_service_url,
            self.service_record,
            format="json",
        )

        # Send delete requests
        for _ in range(13):
            response = self.client.delete(self.delete_service_record_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
