from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from employees.tests.base import EmployeeBaseAPITestCase
from django.contrib.contenttypes.models import ContentType
from flags.models import FlagType


class CreateFlagsAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_flag_url = reverse("create-flag")

        self.flag_type = FlagType.objects.create(flag_type="Incomplete Record")

        self.authenticate_admin()

    def test_successful_flag_creation(self):
        create_flag_url = reverse("create-flag")

        employee_model_id = ContentType.objects.get(model="employee").id

        self.flag_data = {
            "content_type": employee_model_id,
            "object_id": "000993",
            "flag_type": self.flag_type.id,
            "field": "date of birth",
            "reason": "Employee data is invalid",
        }

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create flag request
        response = self.client.post(create_flag_url, self.flag_data, format="json")

        # Get Activity feed
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["service_id"], "000993")
        self.assertIn("flagged", activity_feed)
        self.assertIn("Date of birth", activity_feed)
        self.assertIn("Flag Type", activity_feed)
        self.assertIn("Reason", activity_feed)

    def test_omit_required_field(self):
        create_flag_url = reverse("create-flag")

        self.flag_data = {
            "content_type": "",
            "object_id": "000993",
            "flag_type": self.flag_type.id,
            "reason": "Employee data is invalid",
        }

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create flag request
        response = self.client.post(create_flag_url, self.flag_data, format="json")

        # Get Activity feed
        activity_feed = ActivityFeeds.objects.all()

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "content_type")

            for error in field_errors:
                self.assertEqual(error, "This field may not be null.")

        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_invalid_data(self):
        create_flag_url = reverse("create-flag")

        self.flag_data = {
            "content_type": 400,
            "object_id": "000993",
            "flag_type": self.flag_type.id,
            "reason": "Employee data is missing",
        }

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create flag request
        response = self.client.post(create_flag_url, self.flag_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "content_type")

            for error in field_errors:
                self.assertIn("object does not exist", error)

        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_throttling(self):
        create_flag_url = reverse("create-flag")

        employee_model_id = ContentType.objects.get(model="employee").id

        self.flag_data = {
            "content_type": employee_model_id,
            "object_id": "000993",
            "flag_type": self.flag_type.id,
            "reason": "Employee data is missing",
        }

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create flag request
        for _ in range(13):
            response = self.client.post(create_flag_url, self.flag_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveFlagAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_flag_url = reverse("create-flag")
        self.retrieve_flag_url = reverse("retrieve-flag", kwargs={"pk": 1})

        self.flag_type = FlagType.objects.create(flag_type="Incomplete Record")

        self.authenticate_admin()

    def test_retrieve_existing_flag(self):
        create_flag_url = reverse("create-flag")

        employee_model_id = ContentType.objects.get(model="employee").id

        self.flag_data = {
            "content_type": employee_model_id,
            "object_id": "000993",
            "flag_type": self.flag_type.id,
            "field": "date of birth",
            "reason": "Employee data is invalid",
        }

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create flag request
        self.client.post(create_flag_url, self.flag_data, format="json")

        # Send get flag request
        response = self.client.get(self.retrieve_flag_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["object_id"], "000993")

    def test_retrieve_non_existing_flag(self):
        # Send get flag request
        response = self.client.get(self.retrieve_flag_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        create_flag_url = reverse("create-flag")

        employee_model_id = ContentType.objects.get(model="employee").id

        self.flag_data = {
            "content_type": employee_model_id,
            "object_id": "000993",
            "flag_type": self.flag_type.id,
            "field": "date of birth",
            "reason": "Employee data is invalid",
        }

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create flag request
        self.client.post(create_flag_url, self.flag_data, format="json")

        # Send get flag request
        for _ in range(13):
            response = self.client.get(self.retrieve_flag_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditFlagsAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_flag_url = reverse("create-flag")
        self.edit_flag_url = reverse("edit-flag", kwargs={"pk": 1})

        self.flag_type = FlagType.objects.create(flag_type="Incomplete Record")

        self.authenticate_admin()

    def test_successful_flag_edit(self):
        employee_model_id = ContentType.objects.get(model="employee").id

        self.flag_data = {
            "content_type": employee_model_id,
            "object_id": "000993",
            "flag_type": self.flag_type.id,
            "reason": "Employee data is invalid",
        }
        edit_data = {"field": "date of birth", "reason": "Date of birth in the future"}

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create flag request
        self.client.post(self.create_flag_url, self.flag_data, format="json")

        # Send edit flag request
        response = self.client.patch(self.edit_flag_url, edit_data, format="json")

        # Get Activity feed
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("date of birth", response.data["field"])
        self.assertIn("Date of birth in the future", response.data["reason"])
        self.assertIn("Flagged Field: None → Date of birth", activity_feed)
        self.assertIn(
            "Reason: Employee data is invalid → Date of birth in the future",
            activity_feed,
        )

    def test_edit_non_existing_flag(self):
        employee_model_id = ContentType.objects.get(model="employee").id

        self.flag_data = {
            "content_type": employee_model_id,
            "object_id": "000993",
            "flag_type": self.flag_type.id,
            "reason": "Employee data is invalid",
        }
        edit_data = {"field": "date of birth", "reason": "Date of birth in the future"}

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create flag request
        self.client.post(self.create_flag_url, self.flag_data, format="json")

        # Send edit flag request
        edit_flag_url = reverse("edit-flag", kwargs={"pk": 2})
        response = self.client.patch(edit_flag_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 2)

    def test_invalid_data_flag_edit(self):
        employee_model_id = ContentType.objects.get(model="employee").id

        self.flag_data = {
            "content_type": employee_model_id,
            "object_id": "000993",
            "flag_type": self.flag_type.id,
            "reason": "Employee data is invalid",
        }
        edit_data = {"flag_type": 2}

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create flag request
        self.client.post(self.create_flag_url, self.flag_data, format="json")

        # Send edit flag request
        response = self.client.patch(self.edit_flag_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "flag_type")

            for error in field_errors:
                self.assertIn("object does not exist", error)

        self.assertEqual(ActivityFeeds.objects.count(), 2)

    def test_throttling(self):
        employee_model_id = ContentType.objects.get(model="employee").id

        self.flag_data = {
            "content_type": employee_model_id,
            "object_id": "000993",
            "flag_type": self.flag_type.id,
            "reason": "Employee data is invalid",
        }
        edit_data = {"field": "date of birth", "reason": "Date of birth in the future"}

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create flag request
        self.client.post(self.create_flag_url, self.flag_data, format="json")

        # Send edit flag request
        for _ in range(13):
            response = self.client.patch(self.edit_flag_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteFlagAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_flag_url = reverse("create-flag")
        self.delete_flag_url = reverse("delete-flag", kwargs={"pk": 1})

        self.flag_type = FlagType.objects.create(flag_type="Incomplete Record")

        self.authenticate_admin()

    def test_delete_existing_flag(self):
        create_flag_url = reverse("create-flag")

        employee_model_id = ContentType.objects.get(model="employee").id

        self.flag_data = {
            "content_type": employee_model_id,
            "object_id": "000993",
            "flag_type": self.flag_type.id,
            "field": "date of birth",
            "reason": "Employee data is invalid",
        }

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create flag request
        self.client.post(create_flag_url, self.flag_data, format="json")

        # Send get flag request
        response = self.client.delete(self.delete_flag_url)

        # Get delete activity feed
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn("record flag was deleted by", activity_feed)
        self.assertIn("Flag Type", activity_feed)
        self.assertIn("Field", activity_feed)
        self.assertIn("Reason", activity_feed)

    def test_delete_non_existing_flag(self):
        # Send get flag request
        response = self.client.delete(self.delete_flag_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        create_flag_url = reverse("create-flag")

        employee_model_id = ContentType.objects.get(model="employee").id

        self.flag_data = {
            "content_type": employee_model_id,
            "object_id": "000993",
            "flag_type": self.flag_type.id,
            "field": "date of birth",
            "reason": "Employee data is invalid",
        }

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create flag request
        self.client.post(create_flag_url, self.flag_data, format="json")

        # Send get flag request
        for _ in range(13):
            response = self.client.delete(self.delete_flag_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
