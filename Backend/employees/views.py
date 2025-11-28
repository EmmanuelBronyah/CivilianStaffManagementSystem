from rest_framework import generics, pagination
from . import models
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import serializers
from rest_framework.throttling import UserRateThrottle
from .permissions import IsAdminUserOrStandardUser
import logging
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Count
from datetime import datetime
from django.db.models import F
from django.db.models.functions import ExtractYear

logger = logging.getLogger(__name__)


# * PAGINATION
class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 500
    page_size_query_param = "page_size"
    max_page_size = 1000


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 200


# * EMPLOYEES
class CreateEmployeeAPIView(generics.CreateAPIView):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    permission_classes = [IsAuthenticated & IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class RetrieveEmployeeAPIView(generics.RetrieveAPIView):
    queryset = models.Employee.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.EmployeeSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListEmployeesAPIView(generics.ListAPIView):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination


class EditEmployeeAPIView(generics.UpdateAPIView):
    queryset = models.Employee.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.EmployeeSerializer
    permission_classes = [IsAuthenticated & IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class DeleteEmployeeAPIView(generics.DestroyAPIView):
    queryset = models.Employee.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.EmployeeSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class TotalNumberOfEmployeesAPIView(APIView):

    def get(self, request):
        total = models.Employee.objects.count()
        return Response({"results": total})


class ForecastedRetireesAPIView(APIView):

    def get(self, request):
        current_year = datetime.now().year
        number_of_years = 11

        # Computes and associates retirement year to each employee
        employees_and_retirement_year = models.Employee.objects.annotate(
            retirement_year=ExtractYear(F("dob")) + 60
        )

        results = []

        for offset in range(number_of_years):

            year = current_year + offset

            retirees_queryset = employees_and_retirement_year.filter(
                retirement_year=year
            )

            employees = list(retirees_queryset.values("service_id"))

            results.append(
                {
                    "year": year,
                    "count": retirees_queryset.count(),
                    "employees": [employee["service_id"] for employee in employees],
                }
            )

        return Response({"results": results}, status=status.HTTP_200_OK)


# * GRADE
class CreateGradeAPIView(generics.CreateAPIView):
    queryset = models.Grades.objects.all()
    serializer_class = serializers.GradeSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class RetrieveGradeAPIView(generics.RetrieveAPIView):
    queryset = models.Grades.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.GradeSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListGradesAPIView(generics.ListAPIView):
    queryset = models.Grades.objects.all()
    serializer_class = serializers.GradeSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination


class EditGradeAPIView(generics.UpdateAPIView):
    queryset = models.Grades.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.GradeSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class DeleteGradeAPIView(generics.DestroyAPIView):
    queryset = models.Grades.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.GradeSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


# * UNITS
class CreateUnitAPIView(generics.CreateAPIView):
    queryset = models.Units.objects.all()
    serializer_class = serializers.UnitSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class RetrieveUnitAPIView(generics.RetrieveAPIView):
    queryset = models.Units.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.UnitSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListUnitsAPIView(generics.ListAPIView):
    queryset = models.Units.objects.all()
    serializer_class = serializers.UnitSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    pagination_class = StandardResultsSetPagination


class TotalEmployeesPerUnitAPIView(APIView):

    def get(self, request, *args, **kwargs):
        units = models.Units.objects.annotate(total_employees=Count("employee"))
        results = [{unit.unit_name: unit.total_employees} for unit in units]

        return Response({"results": results}, status=status.HTTP_200_OK)


class EditUnitAPIView(generics.UpdateAPIView):
    queryset = models.Units.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.UnitSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class DeleteUnitAPIView(generics.DestroyAPIView):
    queryset = models.Units.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.UnitSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


# * GENDER
class CreateGenderAPIView(generics.CreateAPIView):
    queryset = models.Gender.objects.all()
    serializer_class = serializers.GenderSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class RetrieveGenderAPIView(generics.RetrieveAPIView):
    queryset = models.Gender.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.GenderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListGendersAPIView(generics.ListAPIView):
    queryset = models.Gender.objects.all()
    serializer_class = serializers.GenderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class EditGenderAPIView(generics.UpdateAPIView):
    queryset = models.Gender.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.GenderSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class DeleteGenderAPIView(generics.DestroyAPIView):
    queryset = models.Gender.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.GenderSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class TotalMaleAndFemaleAPIView(APIView):

    def get(self, request, *args, **kwargs):
        genders = models.Gender.objects.annotate(total_employees=Count("employee"))
        results = [{gender.sex: gender.total_employees} for gender in genders]

        return Response({"results": results}, status=status.HTTP_200_OK)


# * MARITAL STATUS
class CreateMaritalStatusAPIView(generics.CreateAPIView):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.MaritalStatusSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class RetrieveMaritalStatusAPIView(generics.RetrieveAPIView):
    queryset = models.MaritalStatus.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.MaritalStatusSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListMaritalStatusAPIView(generics.ListAPIView):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.MaritalStatusSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class EditMaritalStatusAPIView(generics.UpdateAPIView):
    queryset = models.MaritalStatus.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.MaritalStatusSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class DeleteMaritalStatusAPIView(generics.DestroyAPIView):
    queryset = models.MaritalStatus.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.MaritalStatusSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


# * REGION
class CreateRegionAPIView(generics.CreateAPIView):
    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class RetrieveRegionAPIView(generics.RetrieveAPIView):
    queryset = models.Region.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.RegionSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListRegionsAPIView(generics.ListAPIView):
    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class EditRegionAPIView(generics.UpdateAPIView):
    queryset = models.Region.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.RegionSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class DeleteRegionAPIView(generics.DestroyAPIView):
    queryset = models.Region.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.RegionSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


# * RELIGION
class CreateReligionAPIView(generics.CreateAPIView):
    queryset = models.Religion.objects.all()
    serializer_class = serializers.ReligionSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class RetrieveReligionAPIView(generics.RetrieveAPIView):
    queryset = models.Religion.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.ReligionSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListReligionsAPIView(generics.ListAPIView):
    queryset = models.Religion.objects.all()
    serializer_class = serializers.ReligionSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class EditReligionAPIView(generics.UpdateAPIView):
    queryset = models.Religion.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.ReligionSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class DeleteReligionAPIView(generics.DestroyAPIView):
    queryset = models.Religion.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.ReligionSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


# * STRUCTURE
class CreateStructureAPIView(generics.CreateAPIView):
    queryset = models.Structure.objects.all()
    serializer_class = serializers.StructureSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class RetrieveStructureAPIView(generics.RetrieveAPIView):
    queryset = models.Structure.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.StructureSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListStructuresAPIView(generics.ListAPIView):
    queryset = models.Structure.objects.all()
    serializer_class = serializers.StructureSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class EditStructureAPIView(generics.UpdateAPIView):
    queryset = models.Structure.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.StructureSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class DeleteStructureAPIView(generics.DestroyAPIView):
    queryset = models.Structure.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.StructureSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


# * BLOOD GROUP
class CreateBloodGroupAPIView(generics.CreateAPIView):
    queryset = models.BloodGroup.objects.all()
    serializer_class = serializers.BloodGroupSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class RetrieveBloodGroupAPIView(generics.RetrieveAPIView):
    queryset = models.BloodGroup.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.BloodGroupSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListBloodGroupsAPIView(generics.ListAPIView):
    queryset = models.BloodGroup.objects.all()
    serializer_class = serializers.BloodGroupSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class EditBloodGroupAPIView(generics.UpdateAPIView):
    queryset = models.BloodGroup.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.BloodGroupSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


class DeleteBloodGroupAPIView(generics.DestroyAPIView):
    queryset = models.BloodGroup.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.BloodGroupSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_classes = [UserRateThrottle]


# * DOCUMENT FILE
class CreateDocumentFileAPIView(generics.CreateAPIView):
    queryset = models.DocumentFile.objects.all()
    serializer_class = serializers.DocumentFileSerializer
    permission_classes = [IsAuthenticated & IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class RetrieveDocumentFileAPIView(generics.RetrieveAPIView):
    queryset = models.DocumentFile.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.DocumentFileSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListDocumentFileAPIView(generics.ListAPIView):
    queryset = models.DocumentFile.objects.all()
    serializer_class = serializers.DocumentFileSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class EditDocumentFileAPIView(generics.UpdateAPIView):
    queryset = models.DocumentFile.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.DocumentFileSerializer
    permission_classes = [IsAuthenticated & IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class DeleteDocumentFileAPIView(generics.DestroyAPIView):
    queryset = models.DocumentFile.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.DocumentFileSerializer
    permission_classes = [IsAuthenticated & IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


# * UNREGISTERED EMPLOYEES
class CreateUnregisteredEmployeeAPIView(generics.CreateAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    serializer_class = serializers.UnregisteredEmployeesSerializer
    permission_classes = [IsAuthenticated & IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class RetrieveUnregisteredEmployeeAPIView(generics.RetrieveAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.UnregisteredEmployeesSerializer
    permission_classes = [IsAuthenticated & IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class ListUnregisteredEmployeesAPIView(generics.ListAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    serializer_class = serializers.UnregisteredEmployeesSerializer
    permission_classes = [IsAuthenticated & IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination


class EditUnregisteredEmployeeAPIView(generics.UpdateAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.UnregisteredEmployeesSerializer
    permission_classes = [IsAuthenticated & IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class DeleteUnregisteredEmployeeAPIView(generics.DestroyAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.UnregisteredEmployeesSerializer
    permission_classes = [IsAuthenticated & IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]
