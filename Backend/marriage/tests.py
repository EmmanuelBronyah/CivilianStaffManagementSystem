from occurance.tests.base import EmployeeBaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds


class CreateMarriageAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_marriage_url = reverse("create-spouse")
        self.create_employee_url = reverse("create-employee")

        self.marriage_data = {
            "employee": "000993",
            "spouse_name": "Ama",
            "phone_number": "0554981873",
            "address": "caper st",
            "registration_number": "po902w1",
            "marriage_date": "2025-09-19",
            "marriage_place": "Accra",
        }

        self.authenticate_standard_user()

    def test_successful_marriage_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_marriage_url, self.marriage_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["employee"], "000993")
        self.assertEqual(response.data["spouse_name"], "Ama")
        self.assertIn("added a new Spouse", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        invalid_data = {
            "employee": "000993",
            "spouse_name": "Ama",
            "phone_number": "0554981873",
            "address": "caper st",
            "registration_number": "po902w1" * 300,
            "marriage_date": "2025-09-19",
            "marriage_place": "Accra",
        }

        # Send create request
        response = self.client.post(
            self.create_marriage_url, invalid_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "registration_number")

            for error in field_errors:
                self.assertEqual(
                    error, "Ensure this field has no more than 255 characters."
                )

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Omit required field
        self.marriage_data.update(spouse_name="")

        # Send create request
        response = self.client.post(
            self.create_marriage_url, self.marriage_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "spouse_name")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_marriage_url, self.marriage_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditMarriageAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_marriage_url = reverse("create-spouse")
        self.edit_marriage_url = reverse("edit-spouse", kwargs={"pk": 1})

        self.marriage_data = {
            "employee": "000993",
            "spouse_name": "Ama",
            "phone_number": "0554981873",
            "address": "caper st",
            "registration_number": "po902w1",
            "marriage_date": "2025-09-19",
            "marriage_place": "Accra",
        }

        self.authenticate_standard_user()

    def test_successful_marriage_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Marriage request
        self.client.post(self.create_marriage_url, self.marriage_data, format="json")

        edit_data = {"phone_number": "0202491783", "address": "tontre st"}

        # Send edit Marriage request
        response = self.client.patch(self.edit_marriage_url, edit_data, format="json")

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], "0202491783")
        self.assertEqual(response.data["address"], "tontre st")
        self.assertIn("Address: caper st → tontre st", activity_feed)
        self.assertIn("Phone Number: 0554981873 → 0202491783", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Marriage request
        self.client.post(self.create_marriage_url, self.marriage_data, format="json")

        edit_data = {"phone_number": "tyui"}

        # Send edit Marriage request
        response = self.client.patch(self.edit_marriage_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "phone_number")

            for error in field_errors:
                self.assertEqual(error, "Phone Number can only contain numbers.")

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Marriage request
        self.client.post(self.create_marriage_url, self.marriage_data, format="json")

        edit_data = {"spouse_name": ""}

        # Send edit Marriage request
        response = self.client.patch(self.edit_marriage_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "spouse_name")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Marriage request
        self.client.post(self.create_marriage_url, self.marriage_data, format="json")

        edit_data = {"phone_number": "020237482"}

        # Send edit Marriage request
        for _ in range(13):
            response = self.client.patch(
                self.edit_marriage_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveEmployeeMarriageAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_marriage_url = reverse("create-spouse")
        self.retrieve_employee_marriage_url = reverse(
            "list-employee-spouse", kwargs={"pk": "000993"}
        )

        self.marriage_data = {
            "employee": "000993",
            "spouse_name": "Ama",
            "phone_number": "0554981873",
            "address": "caper st",
            "registration_number": "po902w1",
            "marriage_date": "2025-09-19",
            "marriage_place": "Accra",
        }

        self.authenticate_standard_user()

    def test_successful_retrieval(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Marriage request
        for _ in range(5):
            self.client.post(
                self.create_marriage_url, self.marriage_data, format="json"
            )

        # Send get employee children request
        response = self.client.get(self.retrieve_employee_marriage_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_non_existing_employee(self):
        # Send create Marriage request
        for _ in range(5):
            self.client.post(
                self.create_marriage_url, self.marriage_data, format="json"
            )

        # Send get employee Marriage request
        response = self.client.get(self.retrieve_employee_marriage_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Employee matches the given query."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Marriage request
        self.client.post(self.create_marriage_url, self.marriage_data, format="json")

        # Send get employee Marriage request
        for _ in range(13):
            response = self.client.get(self.retrieve_employee_marriage_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteMarriageAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_marriage_url = reverse("create-spouse")
        self.delete_marriage_url = reverse("delete-spouse", kwargs={"pk": 1})

        self.marriage_data = {
            "employee": "000993",
            "spouse_name": "Ama",
            "phone_number": "0554981873",
            "address": "caper st",
            "registration_number": "po902w1",
            "marriage_date": "2025-09-19",
            "marriage_place": "Accra",
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Marriage request
        self.client.post(self.create_marriage_url, self.marriage_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_marriage_url)

        # Get created activity feed
        activity = "The Spouse(Ama) was deleted by Standard User"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_marriage(self):
        # Send delete Marriage request
        response = self.client.delete(self.delete_marriage_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Marriage request
        self.client.post(self.create_marriage_url, self.marriage_data, format="json")

        # Send delete Marriage request
        for _ in range(13):
            response = self.client.delete(self.delete_marriage_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
