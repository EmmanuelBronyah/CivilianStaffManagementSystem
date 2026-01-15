from rest_framework import generics, pagination
from . import models
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import serializers
from rest_framework.throttling import UserRateThrottle
from .permissions import IsAdminUserOrStandardUser, RestrictFields, CanEditEmployee
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Count
from datetime import datetime
from django.db.models import F
from django.db.models.functions import ExtractYear
from activity_feeds.models import ActivityFeeds
from . import utils
from flags.services import create_flag


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
    serializer_class = serializers.EmployeeCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser, RestrictFields]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        read_serializer = serializers.EmployeeReadSerializer(self.employee)
        response_data = dict(read_serializer.data)
        response_data["warnings"] = serializer.warnings

        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.employee = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(f"Employee({self.employee}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Employee(Service ID: {self.employee.service_id} — Last Name: {self.employee.last_name} — Other Names: {self.employee.other_names})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Employee(Service ID: {self.employee.service_id} — Last Name: {self.employee.last_name} — Other Names: {self.employee.other_names}) created."
        )


class RetrieveEmployeeAPIView(generics.RetrieveAPIView):
    queryset = models.Employee.objects.select_related(
        "gender",
        "region",
        "religion",
        "marital_status",
        "unit",
        "grade",
        "structure",
        "blood_group",
        "created_by",
        "updated_by",
    )
    lookup_field = "pk"
    serializer_class = serializers.EmployeeReadSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListEmployeesAPIView(generics.ListAPIView):
    queryset = models.Employee.objects.select_related(
        "gender",
        "region",
        "religion",
        "marital_status",
        "unit",
        "grade",
        "structure",
        "blood_group",
        "created_by",
        "updated_by",
    )
    serializer_class = serializers.EmployeeReadSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination


class EditEmployeeAPIView(generics.UpdateAPIView):
    queryset = models.Employee.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.EmployeeUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser, CanEditEmployee]
    throttle_classes = [UserRateThrottle]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        read_serializer = serializers.EmployeeReadSerializer(self.employee)
        response_data = dict(read_serializer.data)
        response_data["warnings"] = serializer.warnings

        return Response(response_data)

    def perform_update(self, serializer):
        previous_employee = self.get_object()
        self.employee = serializer.save(updated_by=self.request.user)
        logger.debug(f"Employee({previous_employee}) updated.")

        changes = utils.employee_record_changes(previous_employee, self.employee)

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Employee(Service ID: {self.employee.service_id} — Last Name: {self.employee.last_name} — Other Names: {self.employee.other_names}): {changes}",
            )
            logger.debug(
                f"Activity feed({self.request.user} updated Employee(Service ID: {self.employee.service_id} — Last Name: {self.employee.last_name} — Other Names: {self.employee.other_names}): {changes}) created."
            )


class DeleteEmployeeAPIView(generics.DestroyAPIView):
    queryset = models.Employee.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.EmployeeReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        service_id = instance.service_id
        instance.delete()
        logger.debug(f"Employee({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"Employee record with Service ID({service_id}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(Employee record with Service ID({service_id}) was deleted by {self.request.user}) created."
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


# * CATEGORY
class CreateCategoryAPIView(generics.CreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        category = serializer.save()
        logger.debug(f"Category({category}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Category({category.category_name})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Category({category.category_name}) created."
        )


class RetrieveCategoryAPIView(generics.RetrieveAPIView):
    queryset = models.Category.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListCategoryAPIView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class EditCategoryAPIView(generics.UpdateAPIView):
    queryset = models.Category.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_category = self.get_object()
        category = serializer.save()
        logger.debug(f"Category({previous_category}) updated.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated Category({previous_category.category_name}): {previous_category.category_name} → {category.category_name}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated Category({previous_category.category_name}): {previous_category.category_name} → {category.category_name}) created."
        )


class DeleteCategoryAPIView(generics.DestroyAPIView):
    queryset = models.Category.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        category = instance.category_name
        instance.delete()
        logger.debug(f"Category({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Category({category}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Category({category}) was deleted by {self.request.user}) created."
        )


# * GRADE
class CreateGradeAPIView(generics.CreateAPIView):
    queryset = models.Grades.objects.all()
    serializer_class = serializers.GradeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = serializers.GradeReadSerializer(self.grade)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.grade = serializer.save()
        logger.debug(f"Grade({self.grade}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Grade({self.grade.grade_name})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Grade({self.grade.grade_name}) created."
        )


class RetrieveGradeAPIView(generics.RetrieveAPIView):
    queryset = models.Grades.objects.select_related("rank", "structure")
    lookup_field = "pk"
    serializer_class = serializers.GradeReadSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListGradesAPIView(generics.ListAPIView):
    queryset = models.Grades.objects.select_related("rank", "structure")
    serializer_class = serializers.GradeReadSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination


class EditGradeAPIView(generics.UpdateAPIView):
    queryset = models.Grades.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.GradeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = serializers.GradeReadSerializer(self.grade)
        return Response(read_serializer.data)

    def perform_update(self, serializer):
        previous_grade = self.get_object()
        self.grade = serializer.save()
        logger.debug(f"Grade({previous_grade}) updated.")

        changes = utils.grade_record_changes(previous_grade, self.grade)

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Grade({previous_grade.grade_name}): {changes}",
            )
            logger.debug(
                f"Activity feed({self.request.user} updated Grade({previous_grade.grade_name}): {changes}) created."
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
        logger.debug(f"Grade({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Grade({grade}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Grade({grade}) was deleted by {self.request.user}) created."
        )


# * UNITS
class CreateUnitAPIView(generics.CreateAPIView):
    queryset = models.Units.objects.all()
    serializer_class = serializers.UnitSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        unit = serializer.save()
        logger.debug(f"Unit({unit}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Unit({unit.unit_name})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Unit({unit.unit_name})) created."
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
        logger.debug(f"Unit({previous_unit}) updated.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated Unit({previous_unit.unit_name}): {previous_unit.unit_name} → {unit.unit_name}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated Unit({previous_unit.unit_name}): {previous_unit.unit_name} → {unit.unit_name}) created."
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
        logger.debug(f"Unit({unit}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Unit({unit}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Unit({unit}) was deleted by {self.request.user}) created."
        )


# * GENDER
class CreateGenderAPIView(generics.CreateAPIView):
    queryset = models.Gender.objects.all()
    serializer_class = serializers.GenderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        gender = serializer.save()
        logger.debug(f"Gender({gender}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Gender({gender.sex})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Gender({gender.sex})) created."
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
        logger.debug(f"Gender({previous_gender}) updated.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated Gender({previous_gender.sex}): {previous_gender.sex} → {gender.sex}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated Gender({previous_gender.sex}): {previous_gender.sex} → {gender.sex}) created."
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
        logger.debug(f"Gender({gender}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Gender({gender}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Gender({gender}) was deleted by {self.request.user}) created."
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
        logger.debug(f"Marital Status({marital_status}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Marital Status({marital_status.marital_status_name})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Marital Status({marital_status.marital_status_name})) created."
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
        logger.debug(f"Marital Status({previous_marital_status}) updated.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated Marital Status({previous_marital_status.marital_status_name}): {previous_marital_status.marital_status_name} → {marital_status.marital_status_name}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated Marital Status({previous_marital_status.marital_status_name}): {previous_marital_status.marital_status_name} → {marital_status.marital_status_name}) created."
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
        logger.debug(f"Marital Status({marital_status}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Marital Status({marital_status}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Marital Status({marital_status}) was deleted by {self.request.user}) created."
        )


# * REGION
class CreateRegionAPIView(generics.CreateAPIView):
    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        region = serializer.save()
        logger.debug(f"Region({region}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Region({region.region_name})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Region({region.region_name})) created."
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
        logger.debug(f"Region({region}) updated.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated Region({previous_region.region_name}): {previous_region.region_name} → {region.region_name}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated Region({previous_region.region_name}): {previous_region.region_name} → {region.region_name}) created."
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
        logger.debug(f"Region({region}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Region({region}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Region({region}) was deleted by {self.request.user}) created."
        )


# * RELIGION
class CreateReligionAPIView(generics.CreateAPIView):
    queryset = models.Religion.objects.all()
    serializer_class = serializers.ReligionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        religion = serializer.save()
        logger.debug(f"Religion({religion}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Religion({religion.religion_name})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Religion({religion.religion_name})) created."
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
        logger.debug(f"Religion({previous_religion}) updated.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated Religion({previous_religion.religion_name}): {previous_religion.religion_name} → {religion.religion_name}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated Religion({previous_religion.religion_name}): {previous_religion.religion_name} → {religion.religion_name}) created."
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
        logger.debug(f"Religion({religion}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Religion({religion}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Religion({religion}) was deleted by {self.request.user}) created."
        )


# * STRUCTURE
class CreateStructureAPIView(generics.CreateAPIView):
    queryset = models.Structure.objects.all()
    serializer_class = serializers.StructureSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        structure = serializer.save()
        logger.debug(f"Structure({structure}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Structure({structure.structure_name})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Structure({structure.structure_name})) created."
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
        logger.debug(f"Structure({previous_structure}) updated.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated Structure({previous_structure.structure_name}): {previous_structure.structure_name} → {structure.structure_name}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated Structure({previous_structure.structure_name}): {previous_structure.structure_name} → {structure.structure_name}) created."
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
        logger.debug(f"Structure({structure}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Structure({structure}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Structure({structure}) was deleted by {self.request.user}) created."
        )


# * BLOOD GROUP
class CreateBloodGroupAPIView(generics.CreateAPIView):
    queryset = models.BloodGroup.objects.all()
    serializer_class = serializers.BloodGroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        blood_group = serializer.save()
        logger.debug(f"Blood Group({blood_group}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Blood Group({blood_group.blood_group_name})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Blood Group({blood_group.blood_group_name})) created."
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
        logger.debug(f"Blood Group({previous_blood_group}) updated.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated Blood Group({previous_blood_group.blood_group_name}): {previous_blood_group.blood_group_name} → {blood_group.blood_group_name}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated Blood Group({previous_blood_group.blood_group_name}): {previous_blood_group.blood_group_name} → {blood_group.blood_group_name}) created."
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
        logger.debug(f"Blood Group({blood_group}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Blood Group({blood_group}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Blood Group({blood_group}) was deleted by {self.request.user}) created."
        )


# * DOCUMENT FILE
class CreateDocumentFileAPIView(generics.CreateAPIView):
    queryset = models.DocumentFile.objects.all()
    serializer_class = serializers.DocumentFileSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        document_file = serializer.save()
        logger.debug(f"Document File({document_file}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Document File({document_file.file_data})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Document File({document_file.file_data})) created."
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
        logger.debug(f"Document File({previous_document_file}) updated.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated Document File({previous_document_file.file_data}): {previous_document_file.file_data} → {document_file.file_data}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated Document File({previous_document_file.file_data}): {previous_document_file.file_data} → {document_file.file_data}) created."
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
        logger.debug(f"Document File({document_file}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Document File({document_file}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Document File({document_file}) was deleted by {self.request.user}) created."
        )


# * UNREGISTERED EMPLOYEES
class CreateUnregisteredEmployeeAPIView(generics.CreateAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    serializer_class = serializers.UnregisteredEmployeesWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        read_serializer = serializers.UnregisteredEmployeeReadSerializer(self.employee)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.employee = serializer.save()
        logger.debug(f"Unregistered Employee({self.employee}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Incomplete Employee Record(ID: {self.employee.id})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Incomplete Employee Record(ID: {self.employee.id})) created."
        )

        # Flag created record
        create_flag(self.employee, self.request.user)


class RetrieveUnregisteredEmployeeAPIView(generics.RetrieveAPIView):
    queryset = models.UnregisteredEmployees.objects.select_related("unit", "grade")
    lookup_field = "pk"
    serializer_class = serializers.UnregisteredEmployeeReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class ListUnregisteredEmployeesAPIView(generics.ListAPIView):
    queryset = models.UnregisteredEmployees.objects.select_related("unit", "grade")
    serializer_class = serializers.UnregisteredEmployeeReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination


class EditUnregisteredEmployeeAPIView(generics.UpdateAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.UnregisteredEmployeesWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        read_serializer = serializers.UnregisteredEmployeeReadSerializer(self.employee)
        return Response(read_serializer.data)

    def perform_update(self, serializer):
        previous_employee = self.get_object()
        self.employee = serializer.save()
        logger.debug(f"Unregistered Employee({previous_employee}) updated.")

        changes = utils.unregistered_employee_record_changes(
            previous_employee, self.employee
        )

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated Incomplete Employee Record(ID: {self.employee.id}): {changes}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated Incomplete Employee Record(ID: {self.employee.id}): {changes}) created."
        )


class DeleteUnregisteredEmployeeAPIView(generics.DestroyAPIView):
    queryset = models.UnregisteredEmployees.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.UnregisteredEmployeesWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        employee_id = instance.id
        instance.delete()
        logger.debug(f"Unregistered Employee({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Incomplete Employee Record(ID: {employee_id}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Incomplete Employee Record(ID: {employee_id}) was deleted by {self.request.user}) created."
        )
