from rest_framework.test import APITestCase
from api.models import CustomUser, Divisions
from django.urls import reverse
from django.contrib.auth.models import Group
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import EmployeeBaseAPITestCase, BaseAPITestCase


class CreateUnregisteredEmployeeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-unregistered-employee")
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

    def test_successful_employee_creation(self):
        # Send create request
        response = self.client.post(
            self.create_employee_url, self.employee_data, format="json"
        )

        # Get last activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.UnregisteredEmployees.objects.filter(id=1).exists())
        self.assertNotEqual(response.data["service_id"], "")
        self.assertIn("added a new incomplete employee record", activity_feed)

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

    def test_throttling(self):
        # Send create requests & Change service number to avoid Service ID already exists error
        employee_data_copy = self.employee_data.copy()
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )
        response = self.client.post(
            self.create_employee_url, employee_data_copy, format="json"
        )
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


class EditUnregisteredEmployeeAPITest(BaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-unregistered-employee")
        self.edit_employee_url = reverse("edit-unregistered-employee", kwargs={"pk": 1})

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
        self.assertIn("updated incomplete employee record with ID '1'", activity_feed)

    def test_invalid_data_edit(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send patch/edit request with a blank required field
        edit_data = {
            "service_id": "2nd December, 2025",
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
            edit_response.data["error"],
            "Service ID must not have more than 7 characters.",
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


class DeleteUnregisteredEmployeeAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-unregistered-employee")
        self.delete_employee_url = reverse(
            "delete-unregistered-employee", kwargs={"pk": 1}
        )

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
        activity = (
            "The incomplete employee record with ID '1' was deleted by Administrator"
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
