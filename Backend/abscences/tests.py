from occurance.tests.base import EmployeeBaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds


class CreateAbsencesAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_absences_url = reverse("create-absences")
        self.create_employee_url = reverse("create-employee")

        self.absences_data = {
            "employee": "000993",
            "absence": "42 DAYS ANNUAL LEAVE",
            "authority": "CEM 20/24",
            "start_date": "2025-08-07",
            "end_date": "2025-09-11",
        }

        absences_data_copy = self.absences_data.copy()
        absences_data_copy["employee"] = "020124"
        absences_data_copy["absence"] = "TERMINAL LEAVE"

        self.absences_data_list = [self.absences_data]
        self.absences_data_list.append(absences_data_copy)

        self.authenticate_standard_user()

    def test_successful_single_absences_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_absences_url, self.absences_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["employee"], "000993")
        self.assertIn("added a new Absences", activity_feed)
        self.assertIn("42 DAYS ANNUAL LEAVE", activity_feed)

    def test_successful_multiple_absences_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")
        self.client.post(
            self.create_employee_url, self.other_employee_data, format="json"
        )

        # Send create request
        response = self.client.post(
            self.create_absences_url, self.absences_data_list, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.all()[2:]
        first_occurrence_feed, second_occurrence_feed = (
            activity_feed[0].activity,
            activity_feed[1].activity,
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("added a new Absences", first_occurrence_feed)
        self.assertIn("42 DAYS ANNUAL LEAVE", first_occurrence_feed)
        self.assertIn("added a new Absences", second_occurrence_feed)
        self.assertIn("TERMINAL LEAVE", second_occurrence_feed)

    def test_single_absences_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        invalid_data = {
            "employee": "000993",
            "absence": "42 DAYS ANNUAL LEAVE" * 200,
            "authority": "CEM 20/24",
            "start_date": "2025-08-07",
            "end_date": "2025-09-11",
        }

        # Send create request
        response = self.client.post(
            self.create_absences_url, invalid_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Absence must not have more than 100 characters."
        )

    def test_multiple_absences_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")
        self.client.post(
            self.create_employee_url, self.other_employee_data, format="json"
        )

        self.absences_data_list[1].update(start_date="edf")

        # Send create request
        response = self.client.post(
            self.create_absences_url, self.absences_data_list, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid format for Start Date.")

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Omit required field
        self.absences_data.update(authority="")

        # Send create request
        response = self.client.post(
            self.create_absences_url, self.absences_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Authority cannot be blank or is required."
        )

    def test_omit_required_field_multiple_absences(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")
        self.client.post(
            self.create_employee_url, self.other_employee_data, format="json"
        )

        self.absences_data_list[1].update(authority="")

        # Send create request
        response = self.client.post(
            self.create_absences_url, self.absences_data_list, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Authority cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_absences_url, self.absences_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditAbsencesAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_absences_url = reverse("create-absences")
        self.edit_absences_url = reverse("edit-absences", kwargs={"pk": 1})

        self.absences_data = {
            "employee": "000993",
            "absence": "42 DAYS ANNUAL LEAVE",
            "authority": "CEM 20/24",
            "start_date": "2025-08-07",
            "end_date": "2025-09-11",
        }

        self.authenticate_standard_user()

    def test_successful_absences_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create absences request
        self.client.post(self.create_absences_url, self.absences_data, format="json")

        edit_data = {"authority": "CEM 13/20", "end_date": "2023-09-09"}

        # Send edit occurrence request
        response = self.client.patch(self.edit_absences_url, edit_data, format="json")

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["authority"], "CEM 13/20")
        self.assertEqual(response.data["end_date"], "2023-09-09")
        self.assertIn("End Date: 2025-09-11 → 2023-09-09", activity_feed)
        self.assertIn("Authority: CEM 20/24 → CEM 13/20", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create absences request
        self.client.post(self.create_absences_url, self.absences_data, format="json")

        edit_data = {"start_date": "tyui"}

        # Send edit occurrence request
        response = self.client.patch(self.edit_absences_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid format for Start Date.")

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create absences request
        self.client.post(self.create_absences_url, self.absences_data, format="json")

        edit_data = {"authority": ""}

        # Send edit occurrence request
        response = self.client.patch(self.edit_absences_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Authority cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create absences request
        self.client.post(self.create_absences_url, self.absences_data, format="json")

        edit_data = {"authority": "CEM 23/24"}

        # Send edit absences request
        for _ in range(13):
            response = self.client.patch(
                self.edit_absences_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveEmployeeAbsencesAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_absences_url = reverse("create-absences")
        self.retrieve_employee_absences_url = reverse(
            "list-employee-absences", kwargs={"pk": "000993"}
        )

        self.absences_data = {
            "employee": "000993",
            "absence": "42 DAYS ANNUAL LEAVE",
            "authority": "CEM 20/24",
            "start_date": "2025-08-07",
            "end_date": "2025-09-11",
        }

        self.authenticate_standard_user()

    def test_successful_absences_retrieval(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create absences request
        for _ in range(5):
            self.client.post(
                self.create_absences_url, self.absences_data, format="json"
            )

        # Send get employee occurrences request
        response = self.client.get(self.retrieve_employee_absences_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_non_existing_employee(self):
        # Send create occurrence request
        for _ in range(5):
            self.client.post(
                self.create_absences_url, self.absences_data, format="json"
            )

        # Send get employee absences request
        response = self.client.get(self.retrieve_employee_absences_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Employee matches the given query."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create absences request
        self.client.post(self.create_absences_url, self.absences_data, format="json")

        # Send get employee absences request
        for _ in range(13):
            response = self.client.get(self.retrieve_employee_absences_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteAbsencesAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_absences_url = reverse("create-absences")
        self.delete_absences_url = reverse("delete-absences", kwargs={"pk": 1})

        self.absences_data = {
            "employee": "000993",
            "absence": "42 DAYS ANNUAL LEAVE",
            "authority": "CEM 20/24",
            "start_date": "2025-08-07",
            "end_date": "2025-09-11",
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create absences request
        self.client.post(self.create_absences_url, self.absences_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_absences_url)

        # Get created activity feed
        activity = "The Absences '42 DAYS ANNUAL LEAVE' was deleted by Standard User"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_absences(self):
        # Send delete occurrence request
        response = self.client.delete(self.delete_absences_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create absences request
        self.client.post(self.create_absences_url, self.absences_data, format="json")

        # Send delete absences request
        for _ in range(13):
            response = self.client.delete(self.delete_absences_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
