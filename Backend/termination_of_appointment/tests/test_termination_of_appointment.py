from occurance.tests.base import EmployeeBaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from ..models import CausesOfTermination, TerminationStatus


class CreateTerminationOfAppointmentAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_termination_of_appointment_url = reverse(
            "create-termination-of-appointment"
        )
        self.create_employee_url = reverse("create-employee")

        self.termination_cause = CausesOfTermination.objects.create(
            termination_cause="Death"
        )
        self.termination_status = TerminationStatus.objects.create(
            termination_status="Awol"
        )

        self.termination_of_appointment_data = {
            "employee": "000993",
            "date": "2022-09-09",
            "cause": self.termination_cause.id,
            "authority": "CEM 20/24",
            "status": self.termination_status.id,
        }

        self.authenticate_standard_user()

    def test_successful_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_termination_of_appointment_url,
            self.termination_of_appointment_data,
            format="json",
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["employee"], "000993")
        self.assertEqual(response.data["date"], "2022-09-09")
        self.assertIn("added a new Termination Of Appointment", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        invalid_data = {
            "employee": "000993",
            "date": "2022-099-09",
            "cause": self.termination_cause.id,
            "status": self.termination_status.id,
        }

        # Send create request
        response = self.client.post(
            self.create_termination_of_appointment_url, invalid_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "date")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
                )

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Omit required field
        self.termination_of_appointment_data.update(date="")

        # Send create request
        response = self.client.post(
            self.create_termination_of_appointment_url,
            self.termination_of_appointment_data,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "date")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
                )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_termination_of_appointment_url,
                self.termination_of_appointment_data,
                format="json",
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditTerminationStatusAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_termination_of_appointment_url = reverse(
            "create-termination-of-appointment"
        )
        self.edit_termination_of_appointment_url = reverse(
            "edit-termination-of-appointment", kwargs={"pk": 1}
        )

        self.termination_cause = CausesOfTermination.objects.create(
            termination_cause="Death"
        )
        self.termination_cause_edit = CausesOfTermination.objects.create(
            termination_cause="Awol"
        )
        self.termination_status = TerminationStatus.objects.create(
            termination_status="Awol"
        )

        self.termination_of_appointment_data = {
            "employee": "000993",
            "date": "2022-09-09",
            "cause": self.termination_cause.id,
            "authority": "CEM 20/24",
            "status": self.termination_status.id,
        }

        self.authenticate_standard_user()

    def test_successful_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Termination Of Appointment request
        self.client.post(
            self.create_termination_of_appointment_url,
            self.termination_of_appointment_data,
            format="json",
        )

        edit_data = {"cause": self.termination_cause_edit.id}

        # Send edit Termination Of Appointment request
        response = self.client.patch(
            self.edit_termination_of_appointment_url, edit_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["cause_display"], "Awol")
        self.assertIn("Cause: Death → Awol", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Termination Of Appointment request
        self.client.post(
            self.create_termination_of_appointment_url,
            self.termination_of_appointment_data,
            format="json",
        )

        edit_data = {"date": "tyui"}

        # Send edit Termination Of Appointment request
        response = self.client.patch(
            self.edit_termination_of_appointment_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "date")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
                )

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Termination Of Appointment request
        self.client.post(
            self.create_termination_of_appointment_url,
            self.termination_of_appointment_data,
            format="json",
        )

        edit_data = {"cause": ""}

        # Send edit Termination Of Appointment request
        response = self.client.patch(
            self.edit_termination_of_appointment_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "cause")

            for error in field_errors:
                self.assertEqual(error, "This field may not be null.")

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Termination Of Appointment request
        self.client.post(
            self.create_termination_of_appointment_url,
            self.termination_of_appointment_data,
            format="json",
        )

        edit_data = {"date": "2023-09-03"}

        # Send edit Termination Of Appointment request
        for _ in range(13):
            response = self.client.patch(
                self.edit_termination_of_appointment_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveEmployeeTerminationStatusAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_termination_of_appointment_url = reverse(
            "create-termination-of-appointment"
        )
        self.retrieve_termination_of_appointment_url = reverse(
            "list-employee-termination-of-appointment", kwargs={"pk": "000993"}
        )

        self.termination_cause = CausesOfTermination.objects.create(
            termination_cause="Death"
        )
        self.termination_status = TerminationStatus.objects.create(
            termination_status="Awol"
        )

        self.termination_of_appointment_data = {
            "employee": "000993",
            "date": "2022-09-09",
            "cause": self.termination_cause.id,
            "authority": "CEM 20/24",
            "status": self.termination_status.id,
        }

        self.authenticate_standard_user()

    def test_successful_retrieval(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Termination Of Appointment request
        for _ in range(5):
            self.client.post(
                self.create_termination_of_appointment_url,
                self.termination_of_appointment_data,
                format="json",
            )

        # Send get Termination Of Appointment request
        response = self.client.get(self.retrieve_termination_of_appointment_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_non_existing_employee(self):
        # Send create Termination Of Appointment request
        for _ in range(5):
            self.client.post(
                self.create_termination_of_appointment_url,
                self.termination_of_appointment_data,
                format="json",
            )

        # Send get Termination Of Appointment request
        response = self.client.get(self.retrieve_termination_of_appointment_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Employee matches the given query."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Termination Of Appointment request
        self.client.post(
            self.create_termination_of_appointment_url,
            self.termination_of_appointment_data,
            format="json",
        )

        # Send get Termination Of Appointment request
        for _ in range(13):
            response = self.client.get(self.retrieve_termination_of_appointment_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteTerminationStatusAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_termination_of_appointment_url = reverse(
            "create-termination-of-appointment"
        )
        self.delete_termination_of_appointment_url = reverse(
            "delete-termination-of-appointment", kwargs={"pk": 1}
        )

        self.termination_cause = CausesOfTermination.objects.create(
            termination_cause="Death"
        )
        self.termination_status = TerminationStatus.objects.create(
            termination_status="Awol"
        )

        self.termination_of_appointment_data = {
            "employee": "000993",
            "date": "2022-09-09",
            "cause": self.termination_cause.id,
            "authority": "CEM 20/24",
            "status": self.termination_status.id,
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Termination Of Appointment request
        self.client.post(
            self.create_termination_of_appointment_url,
            self.termination_of_appointment_data,
            format="json",
        )

        # Send delete request
        response = self.client.delete(self.delete_termination_of_appointment_url)

        # Get created activity feed
        activity = "The Termination Of Appointment(Service ID: 000993 — Status: Death) was deleted by Standard User"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_termination_of_appointment(self):
        # Send delete Termination Of Appointment request
        response = self.client.delete(self.delete_termination_of_appointment_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create Termination Of Appointment request
        self.client.post(
            self.create_termination_of_appointment_url,
            self.termination_of_appointment_data,
            format="json",
        )

        # Send delete Termination Of Appointment request
        for _ in range(13):
            response = self.client.delete(self.delete_termination_of_appointment_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
