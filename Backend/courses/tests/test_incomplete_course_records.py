from django.urls import reverse
from ..models import InCompleteChildRecords
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from employees.tests.base import EmployeeBaseAPITestCase
from flags.models import FlagType


class CreateInCompleteChildRecordAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_child_record_url = reverse("create-incomplete-child-record")
        self.create_employee_url = reverse("create-employee")
        FlagType.objects.create(flag_type="Incomplete Record")

        self.child_record = {
            "employee": "000993",
            "child_name": "Emmanuel",
            "service_id": "",
            "dob": None,
            "gender": 1,
            "other_parent": "",
            "authority": "",
        }

        self.authenticate_admin()

    def test_successful_child_record_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_child_record_url, self.child_record, format="json"
        )

        # Get last activity
        activity_feed = ActivityFeeds.objects.all()[1].activity
        last_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["child_name"], "Emmanuel")
        self.assertTrue(InCompleteChildRecords.objects.filter(id=1).exists())
        self.assertIn("added a new Incomplete Child Record", activity_feed)
        self.assertIn("Incomplete child records was flagged", last_feed)

    def test_create_child_record_with_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        child_record = self.child_record.copy()
        child_record["dob"] = "2002-09-009"

        # Send create request
        response = self.client.post(
            self.create_child_record_url, child_record, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "dob")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
                )

    def test_all_fields_none(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        child_record = self.child_record.copy()
        child_record = {key: None for key, _ in child_record.items()}

        # Send create request
        response = self.client.post(
            self.create_child_record_url, child_record, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error, "All fields for Incomplete Child Record cannot be empty."
                )

    def test_only_authority_has_value(self):
        child_record = self.child_record.copy()
        child_record = {
            key: "CEM 23/24" if key == "authority" else None
            for key, value in child_record.items()
        }

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_child_record_url, child_record, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Cannot save Unregistered Employee with Gender or Authority as the only non-empty field.",
                )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        for _ in range(13):
            response = self.client.post(
                self.create_child_record_url, self.child_record, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveInCompleteChildRecordAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_child_record_url = reverse("create-incomplete-child-record")
        self.retrieve_child_record_url = reverse(
            "retrieve-incomplete-child-record", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")

        self.child_record = {
            "employee": "000993",
            "child_name": "Emmanuel",
            "service_id": "",
            "dob": None,
            "gender": 1,
            "other_parent": "",
            "authority": "",
        }

        self.authenticate_admin()

    def test_get_existing_child_record(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(self.create_child_record_url, self.child_record, format="json")

        # Send get request
        response = self.client.get(self.retrieve_child_record_url, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn("service_id", response.data)

    def test_get_non_existing_child_record(self):
        # Send get request
        response = self.client.get(self.retrieve_child_record_url, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(self.create_child_record_url, self.child_record, format="json")

        # Send get requests
        for _ in range(13):
            response = self.client.get(self.retrieve_child_record_url, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditInCompleteChildRecordAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_child_record_url = reverse("create-incomplete-child-record")
        self.edit_child_record_url = reverse(
            "edit-incomplete-child-record", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")

        self.child_record = {
            "employee": "000993",
            "child_name": "Emmanuel",
            "service_id": "",
            "dob": None,
            "gender": 1,
            "other_parent": "",
            "authority": "",
        }

        self.authenticate_admin()

    def test_edit_child_record(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        create_response = self.client.post(
            self.create_child_record_url, self.child_record, format="json"
        )

        # Send patch/edit request
        edit_data = {
            "service_id": "012173",
            "other_parent": "Gloria",
        }
        edit_response = self.client.patch(
            self.edit_child_record_url, edit_data, format="json"
        )

        # Get created activity feed
        activity_feed = ActivityFeeds.objects.all()[3].activity

        # Assertions
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(edit_response.status_code, status.HTTP_200_OK)
        self.assertTrue(InCompleteChildRecords.objects.filter(id=1).exists())
        self.assertIn("updated Incomplete Child Record", activity_feed)

    def test_all_fields_none(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_child_record_url, self.child_record, format="json"
        )

        # Send patch/edit request
        edit_data = self.child_record.copy()
        edit_data = {key: None for key, _ in edit_data.items()}
        edit_response = self.client.patch(
            self.edit_child_record_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = edit_response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error, "All fields for Incomplete Child Record cannot be empty."
                )

    def test_invalid_data_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(self.create_child_record_url, self.child_record, format="json")

        # Send patch/edit request with a blank required field
        edit_data = {
            "service_id": "tyu88",
        }
        edit_response = self.client.patch(
            self.edit_child_record_url, edit_data, format="json"
        )

        # Get last activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = edit_response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "service_id")

            for error in field_errors:
                self.assertIn(error, "Field can only contain numbers.")

        self.assertNotIn("updated employee", activity_feed)

    def test_only_authority_has_value(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_child_record_url, self.child_record, format="json"
        )

        # Send edit request
        edit_data = self.child_record.copy()
        edit_data = {
            key: "CEM 23/24" if key == "authority" else None
            for key, value in edit_data.items()
        }
        edit_response = self.client.patch(
            self.edit_child_record_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = edit_response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Cannot save Unregistered Employee with Gender or Authority as the only non-empty field.",
                )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(self.create_child_record_url, self.child_record, format="json")

        edit_data = {
            "service_id": "012763",
        }

        # Send patch/edit request
        for _ in range(13):
            response = self.client.patch(
                self.edit_child_record_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteInCompleteChildRecordAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_child_record_url = reverse("create-incomplete-child-record")
        self.delete_child_record_url = reverse(
            "delete-incomplete-child-record", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")

        self.child_record = {
            "employee": "000993",
            "child_name": "Emmanuel",
            "service_id": "",
            "dob": None,
            "gender": 1,
            "other_parent": "",
            "authority": "",
        }

        self.authenticate_admin()

    def test_successful_deletion(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(self.create_child_record_url, self.child_record, format="json")

        # Send delete request
        response = self.client.delete(self.delete_child_record_url)

        # Get created activity feed
        activity_feed = ActivityFeeds.objects.all()[3].activity
        last_activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            "The Incomplete Child Record(ID: 1) was deleted by Administrator",
            activity_feed,
        )
        self.assertIn(
            "Incomplete child records flag was deleted by Administrator.",
            last_activity_feed,
        )

    def test_delete_non_existing_employee(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_child_record_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        self.client.post(self.create_child_record_url, self.child_record, format="json")

        # Send delete requests
        for _ in range(13):
            response = self.client.delete(self.delete_child_record_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
