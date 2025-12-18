from rest_framework.test import APITestCase
import socket
from unittest.mock import patch
from django.urls import reverse
from api.models import CustomUser, Divisions
from employees import models
from django.contrib.auth.models import Group
import ssl
import requests
import smtplib
import redis
from rest_framework.exceptions import ValidationError
from Backend.utils import handle_validation_error, handle_field_validation_error


class CustomExceptionHandlerAPITest(APITestCase):

    def setUp(self):
        grade = models.Grades.objects.create(grade_name="Programmer")
        gender = models.Gender.objects.create(sex="Male")
        region = models.Region.objects.create(region_name="Greater Accra Region")
        religion = models.Religion.objects.create(religion_name="Christianity")
        marital_status = models.MaritalStatus.objects.create(
            marital_status_name="Married"
        )
        unit = models.Units.objects.create(unit_name="4 BN")
        structure = models.Structure.objects.create(structure_name="Non-Medical")
        blood_group = models.BloodGroup.objects.create(blood_group_name="A+")

        division = Divisions.objects.create(division_name="DCE-IT")
        admin_group = Group.objects.create(name="ADMINISTRATOR")

        self.employee_data = {
            "service_id": "000993",
            "last_name": "Kana",
            "other_names": "Steve",
            "gender": gender.id,
            "dob": "2000-04-05",
            "hometown": "Ajumako",
            "region": region.id,
            "religion": religion.id,
            "nationality": "Ghanaian",
            "address": "P.o.box 2367",
            "marital_status": marital_status.id,
            "unit": unit.id,
            "grade": grade.id,
            "station": "ACCRA",
            "structure": structure.id,
            "blood_group": blood_group.id,
            "disable": False,
            "social_security": "C019000819236",
            "category": None,
            "appointment_date": "2025-11-25",
            "confirmation_date": None,
            "probation": "",
            "entry_qualification": "",
        }

        self.employee_patch_data = {
            "last_name": "Oyo",
            "other_names": "Isaac",
        }

        self.user_data = {"username": "Admin", "password": "lovesogreat"}

        admin = CustomUser.objects.create_user(
            fullname="Administrator",
            username="Admin",
            password="lovesogreat",
            email="admin@email.com",
            role="ADMINISTRATOR",
            grade=grade.id,
            division=division.id,
        )
        admin.is_staff, admin.is_superuser = True, True
        admin.groups.add(admin_group)

        self.client.force_authenticate(user=admin)

    @patch(
        "employees.views.CreateEmployeeAPIView.perform_create",
        side_effect=socket.gaierror("Simulated Internet Failure"),
    )
    def test_dns_error_handling(self, mock_get):
        create_employee_url = reverse("create-employee")

        # Send create request
        response = self.client.post(
            create_employee_url, data=self.employee_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, 503)

    @patch(
        "employees.views.ListEmployeesAPIView.list",
        side_effect=ConnectionRefusedError("Simulated Internet Failure"),
    )
    def test_socket_connection_error_handling(self, mock_get):
        list_employees_url = reverse("list-all-employees")

        # Send get request
        response = self.client.get(list_employees_url, format="json")

        # Assertions
        self.assertEqual(response.status_code, 503)

    @patch(
        "employees.views.CreateGradeAPIView.perform_create",
        side_effect=ssl.SSLError("Simulated Internet Failure"),
    )
    def test_ssl_error_handling(self, mock_get):
        create_grade_url = reverse("create-grade")

        # Send create request
        response = self.client.post(
            create_grade_url,
            data={"grade_name": "Senior Executive Officer"},
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, 503)

    @patch(
        "employees.views.EditEmployeeAPIView.perform_update",
        side_effect=requests.exceptions.RequestException("Simulated Internet Failure"),
    )
    def test_http_request_error_handling(self, mock_get):
        create_employee_url = reverse("create-employee")
        update_employee_url = reverse("edit-employee", kwargs={"pk": "000993"})

        # Send create request
        self.client.post(create_employee_url, data=self.employee_data, format="json")

        # Send update request
        response = self.client.patch(
            update_employee_url, data=self.employee_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, 503)

    @patch(
        "api.views.EmailDevice.generate_challenge",
        side_effect=smtplib.SMTPException("Simulated Internet Failure"),
    )
    def test_email_errors_handling(self, mock_get):
        login_url = reverse("user-login")

        # Send login request
        response = self.client.post(login_url, data=self.user_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, 503)

    @patch(
        "api.views.cache.set",
        side_effect=redis.exceptions.ConnectionError("Simulated Internet Failure"),
    )
    def test_redis_errors_handling(self, mock_get):
        login_url = reverse("user-login")

        # Send login request
        response = self.client.post(login_url, data=self.user_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, 503)

    @patch(
        "employees.views.CreateEmployeeAPIView.perform_create",
        side_effect=ValidationError("Simulate Validation Error"),
    )
    def test_validation_errors_handling(self, mock_get):
        create_employee_url = reverse("create-employee")

        # Send create request
        response = self.client.post(
            create_employee_url, data=self.employee_data, format="json"
        )

        # Assertions
        self.assertIn("error", response.json())
        self.assertEqual(response.status_code, 400)


class ValidationFunctionsAPITest(APITestCase):

    def setUp(self):
        grade = models.Grades.objects.create(grade_name="Programmer")
        division = Divisions.objects.create(division_name="DCE-IT")

        admin_group = Group.objects.create(name="ADMINISTRATOR")

        self.create_division_url = reverse("create-division")

        admin = CustomUser.objects.create_user(
            fullname="Administrator",
            username="Admin",
            password="lovesogreat",
            email="admin@email.com",
            role="ADMINISTRATOR",
            grade=grade.id,
            division=division.id,
        )
        admin.is_staff, admin.is_superuser = True, True
        admin.groups.add(admin_group)

        self.user_data = {"username": "Admin", "password": "lovesogreat"}

        self.client.force_authenticate(user=admin)

    @patch("Backend.utils.handle_validation_error", wraps=handle_validation_error)
    def test_handle_validation_error(self, mock_builder):
        # Send create request
        response = self.client.post(
            self.create_division_url, {"division_name": "DCE-IT"}, format="json"
        )

        mock_builder.assert_called_once()

        # Assertions
        self.assertIsInstance(response.data["error"], str)
        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(response.data["error"], "")

    @patch(
        "Backend.utils.handle_field_validation_error",
        wraps=handle_field_validation_error,
    )
    def test_handle_field_validation_error(self, mock_builder):
        # Send create request
        response = self.client.post(
            self.create_division_url, {"division_name": "DCE-IT"}, format="json"
        )

        mock_builder.assert_called_once()

        # Assertions
        self.assertIsInstance(response.data["error"], str)
        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(response.data["error"], "")
