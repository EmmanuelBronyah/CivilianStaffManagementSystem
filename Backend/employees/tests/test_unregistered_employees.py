from django.urls import reverse
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import EmployeeBaseAPITestCase, BaseAPITestCase
from flags.models import FlagType


class CreateUnregisteredEmployeeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-unregistered-employee")
        unit = models.Units.objects.create(unit_name="4 BN", city="KUMASI")
        FlagType.objects.create(flag_type="Incomplete Record")

        self.employee_data = {
            "service_id": "001267",
            "last_name": "",
            "other_names": "Angie",
            "unit": unit.id,
            "grade": self.grade.id,
            "social_security": None,
        }

        self.authenticate_admin()

    def test_successful_employee_creation(self):
        # Send create request
        response = self.client.post(
            self.create_employee_url, self.employee_data, format="json"
        )

        # Get last activity
        activity_feed = ActivityFeeds.objects.all()[0].activity
        last_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["service_id"], "001267")
        self.assertTrue(models.UnregisteredEmployees.objects.filter(id=1).exists())
        self.assertIn("added a new Incomplete Employee Record", activity_feed)
        self.assertIn("Unregistered employees Record was flagged", last_feed)

    def test_create_employee_with_invalid_data(self):
        employee_data = self.employee_data.copy()
        employee_data["service_id"] = "013782198"

        # Send create request
        response = self.client.post(
            self.create_employee_url, employee_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "service_id")

            for error in field_errors:
                self.assertIn(error, "Ensure this field has no more than 7 characters.")

        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_all_fields_none(self):
        employee_data = self.employee_data.copy()
        employee_data = {key: "" for key, _ in employee_data.items()}

        # Send create request
        response = self.client.post(
            self.create_employee_url, employee_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error, "All fields for Unregistered Employee cannot be empty."
                )

        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_only_grade_has_value(self):
        employee_data = self.employee_data.copy()
        employee_data = {
            key: value if key == "grade" else "" for key, value in employee_data.items()
        }

        # Send create request
        response = self.client.post(
            self.create_employee_url, employee_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Cannot save Unregistered Employee with Grade or Unit as the only non-empty field.",
                )

        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create requests & Change service number to avoid Service ID already exists error
        employee_data_copy = self.employee_data.copy()

        for _ in range(13):
            response = self.client.post(
                self.create_employee_url, employee_data_copy, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveUnregisteredEmployeeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-unregistered-employee")
        self.retrieve_employee_url = reverse(
            "retrieve-unregistered-employee", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")
        unit = models.Units.objects.create(unit_name="4 BN", city="KUMASI")

        self.employee_data = {
            "service_id": "001267",
            "last_name": "",
            "other_names": "Angie",
            "unit": unit.id,
            "grade": self.grade.id,
            "social_security": "",
        }

        self.authenticate_admin()

    def test_get_existing_employee(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send get request
        response = self.client.get(self.retrieve_employee_url, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn("service_id", response.data)

    def test_get_non_existing_employee(self):
        # Send get request
        response = self.client.get(self.retrieve_employee_url, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send get requests
        for _ in range(13):
            response = self.client.get(self.retrieve_employee_url, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditUnregisteredEmployeeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-unregistered-employee")
        self.edit_employee_url = reverse("edit-unregistered-employee", kwargs={"pk": 1})
        FlagType.objects.create(flag_type="Incomplete Record")
        unit = models.Units.objects.create(unit_name="4 BN", city="KUMASI")

        self.employee_data = {
            "service_id": "001267",
            "last_name": "",
            "other_names": "Angie",
            "unit": unit.id,
            "grade": self.grade.id,
            "social_security": "",
        }

        self.authenticate_admin()

    def test_edit_employee_data(self):
        # Send create request
        create_response = self.client.post(
            self.create_employee_url, self.employee_data, format="json"
        )

        # Send patch/edit request
        edit_data = {
            "service_id": "012173",
            "other_names": "Gloria",
        }
        edit_response = self.client.patch(
            self.edit_employee_url, edit_data, format="json"
        )

        # Get created activity feed
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(edit_response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.UnregisteredEmployees.objects.filter(id=1).exists())
        self.assertIn("updated Incomplete Employee Record", activity_feed)

    def test_all_fields_none(self):
        # Send create request
        response = self.client.post(
            self.create_employee_url, self.employee_data, format="json"
        )

        # Send patch/edit request
        edit_data = self.employee_data.copy()
        edit_data = {key: "" for key, _ in edit_data.items()}
        edit_response = self.client.patch(
            self.edit_employee_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = edit_response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error, "All fields for Unregistered Employee cannot be empty."
                )

    def test_invalid_data_edit(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send patch/edit request with a blank required field
        edit_data = {
            "service_id": "tyu88",
        }
        edit_response = self.client.patch(
            self.edit_employee_url, edit_data, format="json"
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

    def test_only_grade_has_value(self):
        # Send create request
        response = self.client.post(
            self.create_employee_url, self.employee_data, format="json"
        )

        # Send edit request
        edit_data = self.employee_data.copy()
        edit_data = {
            key: value if key == "grade" else "" for key, value in edit_data.items()
        }
        edit_response = self.client.patch(
            self.edit_employee_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = edit_response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertIn(
                    error,
                    "Cannot save Unregistered Employee with Grade or Unit as the only non-empty field.",
                )

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        edit_data = {
            "service_id": "012763",
        }

        # Send patch/edit request
        for _ in range(13):
            response = self.client.patch(
                self.edit_employee_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteUnregisteredEmployeeAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-unregistered-employee")
        self.delete_employee_url = reverse(
            "delete-unregistered-employee", kwargs={"pk": 1}
        )
        FlagType.objects.create(flag_type="Incomplete Record")
        unit = models.Units.objects.create(unit_name="4 BN", city="KUMASI")

        self.employee_data = {
            "service_id": "001267",
            "last_name": "",
            "other_names": "Angie",
            "unit": unit.id,
            "grade": self.grade.id,
            "social_security": "",
        }

        self.authenticate_admin()

    def test_successful_deletion(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_employee_url)

        # Get created activity feed
        activity_feed = ActivityFeeds.objects.all()[2].activity
        last_activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            "The Incomplete Employee Record(ID: 1) was deleted by Administrator",
            activity_feed,
        )
        self.assertIn(
            "Unregistered employees record flag was deleted by Administrator.",
            last_activity_feed,
        )

    def test_delete_non_existing_employee(self):
        # Send delete request
        response = self.client.delete(self.delete_employee_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send delete requests
        for _ in range(13):
            response = self.client.delete(self.delete_employee_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
