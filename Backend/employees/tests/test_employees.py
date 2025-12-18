from rest_framework.test import APITestCase
from api.models import CustomUser, Divisions
from django.urls import reverse
from django.contrib.auth.models import Group
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import EmployeeBaseAPITestCase


class CreateEmployeeAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")

        self.authenticate_admin()

    def test_successful_employee_creation(self):
        # Send create request
        response = self.client.post(
            self.create_employee_url, self.employee_data, format="json"
        )

        # Get last activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.Employee.objects.filter(service_id="000993").exists())
        self.assertNotEqual(response.data["service_id"], "")
        self.assertIn("added a new employee", activity_feed)
        self.assertIn("000993 — Kana Steve", activity_feed)

    def test_create_existing_employee(self):
        # Send two create requests
        self.client.post(self.create_employee_url, self.employee_data, format="json")
        response = self.client.post(
            self.create_employee_url, self.employee_data, format="json"
        )

        # Get activity
        activity_feed = ActivityFeeds.objects.all().first().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())
        self.assertEqual(response.data["error"], "Service ID already exists.")
        self.assertEqual(ActivityFeeds.objects.count(), 1)
        self.assertIn("added a new employee", activity_feed)
        self.assertIn("000993 — Kana Steve", activity_feed)

    def test_create_employee_with_invalid_data(self):
        employee_data = self.employee_data.copy()
        employee_data["service_id"] = "013782198"

        # Send create request
        response = self.client.post(
            self.create_employee_url, employee_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())
        self.assertEqual(
            response.data["error"], "Service ID must not have more than 7 characters."
        )
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_create_employee_without_required_field(self):
        # Omit service_if field
        employee_data = self.employee_data.copy()
        employee_data.pop("service_id")

        # Send create request
        response = self.client.post(
            self.create_employee_url, employee_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())
        self.assertEqual(
            response.data["error"], "Service ID cannot be blank or is required."
        )
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create requests & Change service number to avoid Service ID already exists error
        employee_data_copy = self.employee_data.copy()
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )

        employee_data_copy["service_id"] = "011111"
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )

        employee_data_copy["service_id"] = "022222"
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )

        employee_data_copy["service_id"] = "022221"
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )

        employee_data_copy["service_id"] = "011118"
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )

        employee_data_copy["service_id"] = "011112"
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )

        employee_data_copy["service_id"] = "011126"
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )

        employee_data_copy["service_id"] = "011762"
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )

        employee_data_copy["service_id"] = "017299"
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )

        employee_data_copy["service_id"] = "020009"
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveEmployeeAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.retrieve_employee_url = reverse(
            "retrieve-employee", kwargs={"pk": "000993"}
        )

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
        response = self.client.get(self.retrieve_employee_url, format="json")
        response = self.client.get(self.retrieve_employee_url, format="json")
        response = self.client.get(self.retrieve_employee_url, format="json")
        response = self.client.get(self.retrieve_employee_url, format="json")
        response = self.client.get(self.retrieve_employee_url, format="json")
        response = self.client.get(self.retrieve_employee_url, format="json")
        response = self.client.get(self.retrieve_employee_url, format="json")
        response = self.client.get(self.retrieve_employee_url, format="json")
        response = self.client.get(self.retrieve_employee_url, format="json")
        response = self.client.get(self.retrieve_employee_url, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditEmployeeAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.edit_employee_url = reverse("edit-employee", kwargs={"pk": "000993"})

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
        activity = "Administrator updated employee '000993': Service id: 000993 → 012173, Other names: Steve → Gloria"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(edit_response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.Employee.objects.filter(service_id="012173").exists())
        self.assertEqual(activity_feed, activity)

    def test_edit_required_field_as_empty(self):
        # Send create request
        create_response = self.client.post(
            self.create_employee_url, self.employee_data, format="json"
        )

        # Send patch/edit request with a blank required field
        edit_data = {
            "service_id": "",
            "other_names": "Gloria",
        }
        edit_response = self.client.patch(
            self.edit_employee_url, edit_data, format="json"
        )

        # Get last activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", edit_response.json())
        self.assertEqual(
            edit_response.data["error"], "Service ID cannot be blank or is required."
        )
        self.assertNotIn("updated employee", activity_feed)

    def test_invalid_data_edit(self):
        # Send create request
        create_response = self.client.post(
            self.create_employee_url, self.employee_data, format="json"
        )

        # Send patch/edit request with a blank required field
        edit_data = {
            "appointment_date": "2nd December, 2025",
        }
        edit_response = self.client.patch(
            self.edit_employee_url, edit_data, format="json"
        )

        # Get last activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", edit_response.json())
        self.assertEqual(
            edit_response.data["error"], "Invalid format for Appointment date."
        )
        self.assertNotIn("updated employee", activity_feed)

    def test_throttling(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        edit_data = {
            "service_id": "012763",
        }

        # Send patch/edit request
        response = self.client.patch(self.edit_employee_url, edit_data, format="json")
        response = self.client.patch(self.edit_employee_url, edit_data, format="json")
        response = self.client.patch(self.edit_employee_url, edit_data, format="json")
        response = self.client.patch(self.edit_employee_url, edit_data, format="json")
        response = self.client.patch(self.edit_employee_url, edit_data, format="json")
        response = self.client.patch(self.edit_employee_url, edit_data, format="json")
        response = self.client.patch(self.edit_employee_url, edit_data, format="json")
        response = self.client.patch(self.edit_employee_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteEmployeeAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.delete_employee_url = reverse("delete-employee", kwargs={"pk": "000993"})

        self.authenticate_admin()

    def test_successful_deletion(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_employee_url)

        # Get created activity feed
        activity = (
            "Employee record with Service ID '000993' was deleted by Administrator"
        )
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

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
        response = self.client.delete(self.delete_employee_url)
        response = self.client.delete(self.delete_employee_url)
        response = self.client.delete(self.delete_employee_url)
        response = self.client.delete(self.delete_employee_url)
        response = self.client.delete(self.delete_employee_url)
        response = self.client.delete(self.delete_employee_url)
        response = self.client.delete(self.delete_employee_url)
        response = self.client.delete(self.delete_employee_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class TotalNumberOfEmployeesAPITest(APITestCase):

    def setUp(self):
        self.total_employees_url = reverse("employee-total-number")

    def test_total_number_of_employees(self):
        # Send get request
        response = self.client.get(self.total_employees_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)


class ForecastedRetireesAPITest(APITestCase):

    def setUp(self):
        self.retirees_url = reverse("employee-pension")

    def test_forecasted_retirees(self):
        # Send get request
        response = self.client.get(self.retirees_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
