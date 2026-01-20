from occurance.tests.base import EmployeeBaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds


class CreateIdentityAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_identity_url = reverse("create-identity")
        self.create_employee_url = reverse("create-employee")

        self.identity_data = {
            "employee": "000993",
            "voters_id": "VVVVVVVVVVVVV",
            "national_id": "NNNNNNNNNNNNN",
            "glico_id": "GGGGGGGGGGGGG",
            "nhis_id": "IIIIIIIIIIIII",
            "tin_number": "TTTTTTTTTTTTT",
        }

        self.authenticate_standard_user()

    def test_successful_identity_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_identity_url, self.identity_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["employee"], "000993")
        self.assertEqual(response.data["voters_id"], "VVVVVVVVVVVVV")
        self.assertIn("added a new Identity", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        invalid_data = {
            "employee": "000993",
            "voters_id": "VVVVVVVVVVVVV",
            "national_id": "NNNNNNNNNNNNN",
            "glico_id": "GGGGGGGGGGGGG",
            "nhis_id": "IIIIIIIIIIIII8**",
            "tin_number": "TTTTTTTTTTTTT",
        }

        # Send create request
        response = self.client.post(
            self.create_identity_url, invalid_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "nhis_id")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "NHIS ID can only contain letters, numbers, spaces and hyphens.",
                )

    def test_all_fields_empty(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        invalid_data = {
            "employee": "000993",
            "voters_id": "",
            "national_id": "",
            "glico_id": "",
            "nhis_id": "",
            "tin_number": "",
        }

        # Send create request
        response = self.client.post(
            self.create_identity_url, invalid_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertEqual(error, "All fields for Identity cannot be empty.")

    def test_unique_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        for _ in range(2):
            response = self.client.post(
                self.create_identity_url, self.identity_data, format="json"
            )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        self.assertTrue(errors.get("voters_id", None))
        self.assertEqual(
            str(errors["voters_id"][0]), "identity with this voters id already exists."
        )
        self.assertIn("added a new Identity", activity_feed)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_identity_url, self.identity_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditIdentityAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_identity_url = reverse("create-identity")
        self.edit_identity_url = reverse("edit-identity", kwargs={"pk": 1})

        self.identity_data = {
            "employee": "000993",
            "voters_id": "VVVVVVVVVVVVV",
            "national_id": "NNNNNNNNNNNNN",
            "glico_id": "GGGGGGGGGGGGG",
            "nhis_id": "IIIIIIIIIIIII",
            "tin_number": "TTTTTTTTTTTTT",
        }

        self.authenticate_standard_user()

    def test_successful_identity_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Identity request
        self.client.post(self.create_identity_url, self.identity_data, format="json")

        edit_data = {"national_id": "AAAAAAAAAAAAA", "glico_id": "CCCCCCCCCCCC"}

        # Send edit Identity request
        response = self.client.patch(self.edit_identity_url, edit_data, format="json")

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["national_id"], "AAAAAAAAAAAAA")
        self.assertEqual(response.data["glico_id"], "CCCCCCCCCCCC")
        self.assertIn("National ID: NNNNNNNNNNNNN → AAAAAAAAAAAAA", activity_feed)
        self.assertIn("GLICO ID: GGGGGGGGGGGGG → CCCCCCCCCCCC", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Identity request
        self.client.post(self.create_identity_url, self.identity_data, format="json")

        edit_data = {"glico_id": "tyui" * 500}

        # Send edit Identity request
        response = self.client.patch(self.edit_identity_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "glico_id")

            for error in field_errors:
                self.assertEqual(
                    error, "Ensure this field has no more than 100 characters."
                )

    def test_edit_all_fields_empty(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_identity_url, self.identity_data, format="json"
        )

        edit_data = {
            "employee": "000993",
            "voters_id": "",
            "national_id": "",
            "glico_id": "",
            "nhis_id": "",
            "tin_number": "",
        }

        # Send edit Identity request
        response = self.client.patch(self.edit_identity_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "non_field_errors")

            for error in field_errors:
                self.assertEqual(error, "All fields for Identity cannot be empty.")

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Identity request
        self.client.post(self.create_identity_url, self.identity_data, format="json")

        edit_data = {"national_id": "CCCCCCCCCCCC"}

        # Send edit Identity request
        for _ in range(13):
            response = self.client.patch(
                self.edit_identity_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveEmployeeIdentityAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_identity_url = reverse("create-identity")
        self.retrieve_employee_identity_url = reverse(
            "list-employee-identity", kwargs={"pk": "000993"}
        )

        self.identity_data = {
            "employee": "000993",
            "voters_id": "VVVVVVVVVVVVV",
            "national_id": "NNNNNNNNNNNNN",
            "glico_id": "GGGGGGGGGGGGG",
            "nhis_id": "IIIIIIIIIIIII",
            "tin_number": "TTTTTTTTTTTTT",
        }

        self.authenticate_standard_user()

    def test_successful_retrieval(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Identity request
        self.client.post(self.create_identity_url, self.identity_data, format="json")

        # Send get employee identity request
        response = self.client.get(self.retrieve_employee_identity_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["voters_id"], "VVVVVVVVVVVVV")
        self.assertEqual(len(response.data), 1)

    def test_non_existing_employee(self):
        # Send create Identity request
        for _ in range(5):
            self.client.post(
                self.create_identity_url, self.identity_data, format="json"
            )

        # Send get employee Identity request
        response = self.client.get(self.retrieve_employee_identity_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Employee matches the given query."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Identity request
        self.client.post(self.create_identity_url, self.identity_data, format="json")

        # Send get employee Identity request
        for _ in range(13):
            response = self.client.get(self.retrieve_employee_identity_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteChildIdentityAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_identity_url = reverse("create-identity")
        self.delete_identity_url = reverse("delete-identity", kwargs={"pk": 1})

        self.identity_data = {
            "employee": "000993",
            "voters_id": "VVVVVVVVVVVVV",
            "national_id": "NNNNNNNNNNNNN",
            "glico_id": "GGGGGGGGGGGGG",
            "nhis_id": "IIIIIIIIIIIII",
            "tin_number": "TTTTTTTTTTTTT",
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Identity request
        self.client.post(self.create_identity_url, self.identity_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_identity_url)

        # Get created activity feed
        activity = "The Identity(Service ID: 000993) was deleted by Standard User"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_identity(self):
        # Send delete Identity request
        response = self.client.delete(self.delete_identity_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Identity request
        self.client.post(self.create_identity_url, self.identity_data, format="json")

        # Send delete Identity request
        for _ in range(13):
            response = self.client.delete(self.delete_identity_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
