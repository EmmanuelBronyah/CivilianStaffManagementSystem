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
from activity_feeds.models import ActivityFeeds
from . import utils

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
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        employee = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new employee: {employee.service_id} — {employee.last_name} {employee.other_names}",
        )


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
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_employee = self.get_object()
        employee = serializer.save()

        changes = utils.get_records_changed(previous_employee, employee)

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated employee '{previous_employee.service_id}': {changes}",
        )


class DeleteEmployeeAPIView(generics.DestroyAPIView):
    queryset = models.Employee.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        service_id = instance.service_id
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"Employee record with Service ID '{service_id}' was deleted by {self.request.user}",
        )


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        grade = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new grade: '{grade.grade_name}'",
        )


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_grade = self.get_object()
        grade = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated grade '{previous_grade.grade_name}': {previous_grade.grade_name} → {grade.grade_name}",
        )


class DeleteGradeAPIView(generics.DestroyAPIView):
    queryset = models.Grades.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.GradeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        grade = instance.grade_name
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The grade '{grade}' was deleted by {self.request.user}",
        )


# * UNITS
class CreateUnitAPIView(generics.CreateAPIView):
    queryset = models.Units.objects.all()
    serializer_class = serializers.UnitSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        unit = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new unit: '{unit.unit_name}'",
        )


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_unit = self.get_object()
        unit = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated unit '{previous_unit.unit_name}': {previous_unit.unit_name} → {unit.unit_name}",
        )


class DeleteUnitAPIView(generics.DestroyAPIView):
    queryset = models.Units.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.UnitSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        unit = instance.unit_name
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The unit '{unit}' was deleted by {self.request.user}",
        )


# * GENDER
class CreateGenderAPIView(generics.CreateAPIView):
    queryset = models.Gender.objects.all()
    serializer_class = serializers.GenderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        gender = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new gender: '{gender.sex}'",
        )


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_gender = self.get_object()
        gender = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated gender '{previous_gender.sex}': {previous_gender.sex} → {gender.sex}",
        )


class DeleteGenderAPIView(generics.DestroyAPIView):
    queryset = models.Gender.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.GenderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        gender = instance.sex
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The gender '{gender}' was deleted by {self.request.user}",
        )


class TotalMaleAndFemaleAPIView(APIView):

    def get(self, request, *args, **kwargs):
        genders = models.Gender.objects.annotate(total_employees=Count("employee"))
        results = [{gender.sex: gender.total_employees} for gender in genders]

        return Response({"results": results}, status=status.HTTP_200_OK)


# * MARITAL STATUS
class CreateMaritalStatusAPIView(generics.CreateAPIView):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.MaritalStatusSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        marital_status = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new marital status: '{marital_status.marital_status_name}'",
        )


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_marital_status = self.get_object()
        marital_status = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated marital status '{previous_marital_status.marital_status_name}': {previous_marital_status.marital_status_name} → {marital_status.marital_status_name}",
        )


class DeleteMaritalStatusAPIView(generics.DestroyAPIView):
    queryset = models.MaritalStatus.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.MaritalStatusSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        marital_status = instance.marital_status_name
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The marital status '{marital_status}' was deleted by {self.request.user}",
        )


# * REGION
class CreateRegionAPIView(generics.CreateAPIView):
    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        region = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new region: '{region.region_name}'",
        )


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_region = self.get_object()
        region = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated region '{previous_region.region_name}': {previous_region.region_name} → {region.region_name}",
        )


class DeleteRegionAPIView(generics.DestroyAPIView):
    queryset = models.Region.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.RegionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        region = instance.region_name
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The region '{region}' was deleted by {self.request.user}",
        )


# * RELIGION
class CreateReligionAPIView(generics.CreateAPIView):
    queryset = models.Religion.objects.all()
    serializer_class = serializers.ReligionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        religion = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new religion: '{religion.religion_name}'",
        )


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_religion = self.get_object()
        religion = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated religion '{previous_religion.religion_name}': {previous_religion.religion_name} → {religion.religion_name}",
        )


class DeleteReligionAPIView(generics.DestroyAPIView):
    queryset = models.Religion.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.ReligionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        religion = instance.religion_name
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The religion '{religion}' was deleted by {self.request.user}",
        )


# * STRUCTURE
class CreateStructureAPIView(generics.CreateAPIView):
    queryset = models.Structure.objects.all()
    serializer_class = serializers.StructureSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        structure = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new structure: '{structure.structure_name}'",
        )


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_structure = self.get_object()
        structure = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated structure '{previous_structure.structure_name}': {previous_structure.structure_name} → {structure.structure_name}",
        )


class DeleteStructureAPIView(generics.DestroyAPIView):
    queryset = models.Structure.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.StructureSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        structure = instance.structure_name
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The structure '{structure}' was deleted by {self.request.user}",
        )


# * BLOOD GROUP
class CreateBloodGroupAPIView(generics.CreateAPIView):
    queryset = models.BloodGroup.objects.all()
    serializer_class = serializers.BloodGroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        blood_group = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new blood group: '{blood_group.blood_group_name}'",
        )


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_blood_group = self.get_object()
        blood_group = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated blood group '{previous_blood_group.blood_group_name}': {previous_blood_group.blood_group_name} → {blood_group.blood_group_name}",
        )


class DeleteBloodGroupAPIView(generics.DestroyAPIView):
    queryset = models.BloodGroup.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.BloodGroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        blood_group = instance.blood_group_name
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The blood group '{blood_group}' was deleted by {self.request.user}",
        )


# * DOCUMENT FILE
class CreateDocumentFileAPIView(generics.CreateAPIView):
    queryset = models.DocumentFile.objects.all()
    serializer_class = serializers.DocumentFileSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        document_file = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new document file: '{document_file.file_data}'",
        )


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
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_document_file = self.get_object()
        document_file = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated document file '{previous_document_file.file_data}': {previous_document_file.file_data} → {document_file.file_data}",
        )


class DeleteDocumentFileAPIView(generics.DestroyAPIView):
    queryset = models.DocumentFile.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.DocumentFileSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        document_file = instance.file_data
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The document file '{document_file}' was deleted by {self.request.user}",
        )


# * UNREGISTERED EMPLOYEES
class CreateUnregisteredEmployeeAPIView(generics.CreateAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    serializer_class = serializers.UnregisteredEmployeesSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        employee = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new incomplete employee record: 'Service id: {employee.service_id or 'None'}' — 'Last name: {employee.last_name or 'None'}' — 'Other names: {employee.other_names or 'None'}' — 'Unit: {employee.unit.unit_name if employee.unit else 'None'}' — 'Grade: {employee.grade.grade_name if employee.grade else 'None'}' — 'Social Security: {employee.social_security or 'None'}'",
        )


class RetrieveUnregisteredEmployeeAPIView(generics.RetrieveAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.UnregisteredEmployeesSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class ListUnregisteredEmployeesAPIView(generics.ListAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    serializer_class = serializers.UnregisteredEmployeesSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination


class EditUnregisteredEmployeeAPIView(generics.UpdateAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.UnregisteredEmployeesSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_employee = self.get_object()
        employee = serializer.save()

        changes = utils.get_records_changed(previous_employee, employee)

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated incomplete employee record with ID '{employee.id}': {changes}",
        )


class DeleteUnregisteredEmployeeAPIView(generics.DestroyAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.UnregisteredEmployeesSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        employee_id = instance.id
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The incomplete employee record with ID '{employee_id}' was deleted by {self.request.user}",
        )
