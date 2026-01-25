from django.urls import reverse
from ..models import IncompleteServiceWithForcesRecords
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from occurance.tests.base import EmployeeBaseAPITestCase
from flags.models import FlagType


class CreateIncompleteServiceWithForcesRecordsAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_incomplete_service_with_forces_url = reverse(
            "create-incomplete-service-with-forces"
        )
        self.create_employee_url = reverse("create-employee")
        FlagType.objects.create(flag_type="Incomplete Record")

        self.service_record = {
            "employee": "000993",
            "service_date": "2022-09-09",
            "last_unit": self.unit.id,
            "service_id": "000993",
            "military_rank": None,
        }

        self.authenticate_standard_user()

    def test_successful_service_with_forces_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_incomplete_service_with_forces_url,
            self.service_record,
            format="json",
        )

        # Get last activity
        activity_feed = ActivityFeeds.objects.all()[1].activity
        last_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["service_id"], "000993")
        self.assertTrue(
            IncompleteServiceWithForcesRecords.objects.filter(id=1).exists()
        )
        self.assertIn("added a new Incomplete Service With Forces", activity_feed)
        self.assertIn("Incomplete service with forces records was flagged", last_feed)

    def test_create_service_with_forces_with_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        service_record = self.service_record.copy()
        service_record["service_date"] = "2027-09-07"

        # Send create request
        response = self.client.post(
            self.create_incomplete_service_with_forces_url,
            service_record,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "service_date")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Service Date cannot be the present date or a future date.",
                )

    def test_all_fields_none(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        service_record = self.service_record.copy()
        service_record = {key: None for key, _ in service_record.items()}

        # Send create request
        response = self.client.post(
            self.create_incomplete_service_with_forces_url,
            service_record,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error,
                    "All fields for Incomplete Service With Forces cannot be empty.",
                )

    def test_only_service_id_has_value(self):
        service_record = self.service_record.copy()
        service_record = {
            key: "000993" if key == "service_id" else None
            for key, value in service_record.items()
        }

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_incomplete_service_with_forces_url,
            service_record,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Cannot save Incomplete Service With Forces with Service Date or Service ID as the only non-empty fields.",
                )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        for _ in range(13):
            response = self.client.post(
                self.create_incomplete_service_with_forces_url,
                self.service_record,
                format="json",
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveIncompleteServiceWithForcesRecordsAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_incomplete_service_with_forces_url = reverse(
            "create-incomplete-service-with-forces"
        )
        self.retrieve_service_with_forces_record_url = reverse(
            "retrieve-incomplete-service-with-forces", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")

        self.service_record = {
            "employee": "000993",
            "service_date": "2022-09-09",
            "last_unit": self.unit.id,
            "service_id": "000993",
            "military_rank": None,
        }

        self.authenticate_standard_user()

    def test_get_existing_service_record(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_service_with_forces_url,
            self.service_record,
            format="json",
        )

        # Send get request
        response = self.client.get(
            self.retrieve_service_with_forces_record_url, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn("service_id", response.data)

    def test_get_non_existing_service_record(self):
        # Send get request
        response = self.client.get(
            self.retrieve_service_with_forces_record_url, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_service_with_forces_url,
            self.service_record,
            format="json",
        )

        # Send get requests
        for _ in range(13):
            response = self.client.get(
                self.retrieve_service_with_forces_record_url, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditIncompleteServiceWithForcesRecordsAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_incomplete_service_with_forces_url = reverse(
            "create-incomplete-service-with-forces"
        )
        self.edit_service_with_forces_record_url = reverse(
            "edit-incomplete-service-with-forces", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")

        self.service_record = {
            "employee": "000993",
            "service_date": "2022-09-09",
            "last_unit": self.unit.id,
            "service_id": "000993",
            "military_rank": None,
        }

        self.authenticate_standard_user()

    def test_edit_service_record(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        create_response = self.client.post(
            self.create_incomplete_service_with_forces_url,
            self.service_record,
            format="json",
        )

        # Send patch/edit request
        edit_data = {
            "employee": "000993",
            "service_date": "2023-09-06",
            "service_id": "000993",
            "last_unit": self.unit.id,
            "military_rank": None,
        }
        edit_response = self.client.patch(
            self.edit_service_with_forces_record_url, edit_data, format="json"
        )

        # Get created activity feed
        activity_feed = ActivityFeeds.objects.all()[3].activity

        # Assertions
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(edit_response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            IncompleteServiceWithForcesRecords.objects.filter(id=1).exists()
        )
        self.assertIn("updated Incomplete Service With Forces", activity_feed)

    def test_all_fields_none(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_incomplete_service_with_forces_url,
            self.service_record,
            format="json",
        )

        # Send patch/edit request
        edit_data = self.service_record.copy()
        edit_data = {key: None for key, _ in edit_data.items()}
        edit_response = self.client.patch(
            self.edit_service_with_forces_record_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = edit_response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error,
                    "All fields for Incomplete Service With Forces cannot be empty.",
                )

    def test_invalid_data_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_service_with_forces_url,
            self.service_record,
            format="json",
        )

        # Send patch/edit request with a blank required field
        edit_data = {
            "service_id": "tyu88*",
        }
        edit_response = self.client.patch(
            self.edit_service_with_forces_record_url, edit_data, format="json"
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

    def test_only_service_id_has_value(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_incomplete_service_with_forces_url,
            self.service_record,
            format="json",
        )

        # Send edit request
        edit_data = self.service_record.copy()
        edit_data = {
            key: "000993" if key == "service_id" else None
            for key, value in edit_data.items()
        }
        edit_response = self.client.patch(
            self.edit_service_with_forces_record_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = edit_response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Cannot save Incomplete Service With Forces with Service Date or Service ID as the only non-empty fields.",
                )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_service_with_forces_url,
            self.service_record,
            format="json",
        )

        edit_data = {
            "service_id": "012763",
        }

        # Send patch/edit request
        for _ in range(13):
            response = self.client.patch(
                self.edit_service_with_forces_record_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteIncompleteServiceWithForcesRecordsAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_incomplete_service_with_forces_url = reverse(
            "create-incomplete-service-with-forces"
        )
        self.delete_service_with_forces_record_url = reverse(
            "delete-incomplete-service-with-forces", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")

        self.service_record = {
            "employee": "000993",
            "service_date": "2022-09-09",
            "last_unit": self.unit.id,
            "service_id": "000993",
            "military_rank": None,
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_service_with_forces_url,
            self.service_record,
            format="json",
        )

        # Send delete request
        response = self.client.delete(self.delete_service_with_forces_record_url)

        # Get created activity feed
        activity_feed = ActivityFeeds.objects.all()[3].activity
        last_activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            "The Incomplete Service With Forces(ID: 1) was deleted by Standard User",
            activity_feed,
        )
        self.assertIn(
            "Incomplete service with forces records flag was deleted by Standard User.",
            last_activity_feed,
        )

    def test_delete_non_existing_employee(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_service_with_forces_record_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(
            self.create_incomplete_service_with_forces_url,
            self.service_record,
            format="json",
        )

        # Send delete requests
        for _ in range(13):
            response = self.client.delete(self.delete_service_with_forces_record_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
