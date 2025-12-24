from rest_framework.test import APITestCase
from api.models import CustomUser, Divisions
from django.contrib.auth.models import Group
from employees import models


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
        cls.structure = models.Structure.objects.create(structure_name="Non-medical")

        cls.division = Divisions.objects.create(division_name="DCE-IT")
        cls.grade = models.Grades.objects.create(grade_name="Programmer")

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
            "dob": "2000-04-05",
            "hometown": "Ajumako",
            "region": cls.region.id,
            "religion": cls.religion.id,
            "nationality": "Ghanaian",
            "address": "P.o.box 2367",
            "marital_status": cls.marital_status.id,
            "unit": cls.unit.id,
            "grade": cls.grade.id,
            "station": "ACCRA",
            "structure": cls.structure.id,
            "blood_group": cls.blood_group.id,
            "disable": False,
            "social_security": "C019000819236",
            "category": None,
            "appointment_date": "2025-11-25",
            "confirmation_date": None,
            "probation": "",
            "entry_qualification": "",
        }

    def authenticate_standard_user(self):
        self.client.force_authenticate(user=self.standard_user)
