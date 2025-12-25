from .base import EmployeeBaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds


class CreateOccurrenceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_occurrence_url = reverse("create-occurrence")
        self.create_employee_url = reverse("create-employee")

        self.occurrence_data = {
            "employee": "000993",
            "grade": self.grade.id,
            "authority": "CEM 20/24",
            "level_step": self.level_step.id,
            "monthly_salary": "12971.8400",
            "annual_salary": "155662.08",
            "event": self.event.id,
            "wef_date": "2024-09-23",
            "reason": "23% Salary Adjustment",
        }

        occurrence_data_copy = self.occurrence_data.copy()
        occurrence_data_copy["employee"] = "020124"

        self.occurrence_data_list = [self.occurrence_data]
        self.occurrence_data_list.append(occurrence_data_copy)

        self.authenticate_standard_user()

    def test_successful_single_occurrence_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_occurrence_url, self.occurrence_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["employee"], "000993")
        self.assertIn("added a new occurrence", activity_feed)
        self.assertIn("000993", activity_feed)

    def test_successful_multiple_occurrence_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")
        self.client.post(
            self.create_employee_url, self.other_employee_data, format="json"
        )

        # Send create request
        response = self.client.post(
            self.create_occurrence_url, self.occurrence_data_list, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.all()[2:]
        first_occurrence_feed, second_occurrence_feed = (
            activity_feed[0].activity,
            activity_feed[1].activity,
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data[0]["employee"],
            "000993",
        )
        self.assertEqual(
            response.data[1]["employee"],
            "020124",
        )
        self.assertIn("added a new occurrence", first_occurrence_feed)
        self.assertIn("000993 — CEM 20/24 — Salary Adjustment", first_occurrence_feed)
        self.assertIn("added a new occurrence", second_occurrence_feed)
        self.assertIn("020124 — CEM 20/24 — Salary Adjustment", second_occurrence_feed)

    def test_single_occurrence_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        invalid_data = {
            "employee": "000993",
            "grade": self.grade.id,
            "authority": "CEM 20/24",
            "level_step": self.level_step.id,
            "monthly_salary": "yu",
            "annual_salary": "155662.08",
            "event": self.event.id,
            "wef_date": "2024-09-23",
            "reason": "23% Salary Adjustment",
        }

        # Send create request
        response = self.client.post(
            self.create_occurrence_url, invalid_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid format for Monthly Salary.")

    def test_multiple_occurrence_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")
        self.client.post(
            self.create_employee_url, self.other_employee_data, format="json"
        )

        self.occurrence_data_list[1].update(monthly_salary="edf")

        # Send create request
        response = self.client.post(
            self.create_occurrence_url, self.occurrence_data_list, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid format for Monthly Salary.")

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Omit required field
        self.occurrence_data.update(grade="")

        # Send create request
        response = self.client.post(
            self.create_occurrence_url, self.occurrence_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Grade cannot be blank or is required."
        )

    def test_omit_required_field_multiple_occurrence(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")
        self.client.post(
            self.create_employee_url, self.other_employee_data, format="json"
        )

        self.occurrence_data_list[1].update(grade="")

        # Send create request
        response = self.client.post(
            self.create_occurrence_url, self.occurrence_data_list, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Grade cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_occurrence_url, self.occurrence_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditOccurrenceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_occurrence_url = reverse("create-occurrence")
        self.edit_occurrence_url = reverse("edit-occurrence", kwargs={"pk": 1})

        self.occurrence_data = {
            "employee": "000993",
            "grade": self.grade.id,
            "authority": "CEM 20/24",
            "level_step": self.level_step.id,
            "monthly_salary": 12971.84,
            "annual_salary": 155662.08,
            "event": self.event.id,
            "wef_date": "2024-09-23",
            "reason": "23% Salary Adjustment",
        }

        self.authenticate_standard_user()

    def test_successful_occurrence_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create occurrence request
        self.client.post(
            self.create_occurrence_url, self.occurrence_data, format="json"
        )

        edit_data = {"authority": "CEM 13/20", "monthly_salary": 2997.56}

        # Send edit occurrence request
        response = self.client.patch(self.edit_occurrence_url, edit_data, format="json")

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["authority"], "CEM 13/20")
        self.assertEqual(response.data["monthly_salary"], "2997.56")
        self.assertIn("Monthly Salary: 12971.84 → 2997.56", activity_feed)
        self.assertIn("Authority: CEM 20/24 → CEM 13/20", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create occurrence request
        self.client.post(
            self.create_occurrence_url, self.occurrence_data, format="json"
        )

        edit_data = {"annual_salary": "tyui"}

        # Send edit occurrence request
        response = self.client.patch(self.edit_occurrence_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid format for Annual Salary.")

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create occurrence request
        self.client.post(
            self.create_occurrence_url, self.occurrence_data, format="json"
        )

        edit_data = {"authority": ""}

        # Send edit occurrence request
        response = self.client.patch(self.edit_occurrence_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Authority cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create occurrence request
        self.client.post(
            self.create_occurrence_url, self.occurrence_data, format="json"
        )

        edit_data = {"authority": "CEM 23/24"}

        # Send edit occurrence request
        for _ in range(13):
            response = self.client.patch(
                self.edit_occurrence_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveEmployeeOccurrenceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_occurrence_url = reverse("create-occurrence")
        self.retrieve_employee_occurrences_url = reverse(
            "list-employee-occurrence", kwargs={"pk": "000993"}
        )

        self.occurrence_data = {
            "employee": "000993",
            "grade": self.grade.id,
            "authority": "CEM 20/24",
            "level_step": self.level_step.id,
            "monthly_salary": 12971.84,
            "annual_salary": 155662.08,
            "event": self.event.id,
            "wef_date": "2024-09-23",
            "reason": "23% Salary Adjustment",
        }

        self.authenticate_standard_user()

    def test_successful_occurrence_retrieval(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create occurrence request
        for _ in range(5):
            self.client.post(
                self.create_occurrence_url, self.occurrence_data, format="json"
            )

        # Send get employee occurrences request
        response = self.client.get(self.retrieve_employee_occurrences_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_non_existing_employee(self):
        # Send create occurrence request
        for _ in range(5):
            self.client.post(
                self.create_occurrence_url, self.occurrence_data, format="json"
            )

        # Send get employee occurrences request
        response = self.client.get(self.retrieve_employee_occurrences_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Employee matches the given query."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create occurrence request
        self.client.post(
            self.create_occurrence_url, self.occurrence_data, format="json"
        )

        # Send get employee occurrences request
        for _ in range(13):
            response = self.client.get(self.retrieve_employee_occurrences_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteOccurrenceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_occurrence_url = reverse("create-occurrence")
        self.delete_occurrence_url = reverse("delete-occurrence", kwargs={"pk": 1})

        self.occurrence_data = {
            "employee": "000993",
            "grade": self.grade.id,
            "authority": "CEM 20/24",
            "level_step": self.level_step.id,
            "monthly_salary": 12971.84,
            "annual_salary": 155662.08,
            "event": self.event.id,
            "wef_date": "2024-09-23",
            "reason": "23% Salary Adjustment",
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create occurrence request
        self.client.post(
            self.create_occurrence_url, self.occurrence_data, format="json"
        )

        # Send delete request
        response = self.client.delete(self.delete_occurrence_url)

        # Get created activity feed
        activity = "The occurrence '000993 — CEM 20/24 — Salary Adjustment' was deleted by Standard User"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_occurrence(self):
        # Send delete occurrence request
        response = self.client.delete(self.delete_occurrence_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create occurrence request
        self.client.post(
            self.create_occurrence_url, self.occurrence_data, format="json"
        )

        # Send delete occurrence request
        for _ in range(13):
            response = self.client.delete(self.delete_occurrence_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
