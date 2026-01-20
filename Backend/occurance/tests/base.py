from rest_framework.test import APITestCase
from api.models import CustomUser, Divisions
from django.contrib.auth.models import Group
from employees import models
from occurance.models import LevelStep, Event


class BaseAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.division = Divisions.objects.create(division_name="DCE-IT")

        cls.structure = models.Structure.objects.create(structure_name="Non-medical")
        cls.rank = models.Category.objects.create(category_name="Junior")

        cls.grade = models.Grades.objects.create(
            grade_name="Programmer", rank=cls.rank, structure=cls.structure
        )

        cls.admin_group = Group.objects.create(name="ADMINISTRATOR")

        cls.admin = CustomUser.objects.create_user(
            fullname="Administrator",
            username="Admin",
            password="lovesogreat",
            email="admin@email.com",
            role="ADMINISTRATOR",
            grade=cls.grade,
            division=cls.division,
        )

        cls.admin.is_staff = True
        cls.admin.is_superuser = True
        cls.admin.groups.add(cls.admin_group)

    def authenticate_admin(self):
        self.client.force_authenticate(user=self.admin)


class EmployeeBaseAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.gender = models.Gender.objects.create(sex="Male")
        cls.region = models.Region.objects.create(region_name="ACCRA")
        cls.religion = models.Religion.objects.create(religion_name="Christianity")
        cls.marital_status = models.MaritalStatus.objects.create(
            marital_status_name="Married"
        )
        cls.unit = models.Units.objects.create(unit_name="4 Bn")
        cls.blood_group = models.BloodGroup.objects.create(blood_group_name="O+")
        cls.division = Divisions.objects.create(division_name="DCE-IT")

        cls.structure = models.Structure.objects.create(structure_name="Non-medical")
        cls.rank = models.Category.objects.create(category_name="Junior")

        cls.grade = models.Grades.objects.create(
            grade_name="Programmer", rank=cls.rank, structure=cls.structure
        )

        cls.level_step = LevelStep.objects.create(
            level_step="25H01", monthly_salary="12971.8400"
        )
        cls.event = Event.objects.create(event_name="Salary Adjustment")

        cls.standard_user_group = Group.objects.create(name="STANDARD USER")

        cls.standard_user = CustomUser.objects.create_user(
            fullname="Standard User",
            username="user",
            password="lovesogreat",
            email="standarduser@email.com",
            role="STANDARD USER",
            grade=cls.grade,
            division=cls.division,
        )

        cls.standard_user.is_staff = False
        cls.standard_user.is_superuser = False
        cls.standard_user.groups.add(cls.standard_user_group)

        cls.employee_data = {
            "service_id": "000993",
            "last_name": "Kana",
            "other_names": "Steve",
            "gender": cls.gender.id,
            "hometown": "Ajumako",
            "region": cls.region.id,
            "religion": cls.religion.id,
            "nationality": "Ghanaian",
            "address": "P.o.box 2367",
            "marital_status": cls.marital_status.id,
            "unit": cls.unit.id,
            "grade": cls.grade.id,
            "blood_group": cls.blood_group.id,
            "disable": False,
            "social_security": "C019000819236",
            "appointment_date": "2025-11-25",
            "confirmation_date": None,
            "entry_qualification": "",
        }

        employee_data_copy = cls.employee_data.copy()
        employee_data_copy["service_id"] = "020124"

        cls.other_employee_data = employee_data_copy

    def authenticate_standard_user(self):
        self.client.force_authenticate(user=self.standard_user)
