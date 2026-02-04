from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


class Employee(models.Model):
    service_id = models.CharField(primary_key=True, max_length=7)
    last_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255)
    gender = models.ForeignKey("Gender", on_delete=models.PROTECT)
    age = models.CharField(max_length=3, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    hometown = models.CharField(max_length=255, null=True, blank=True)
    region = models.ForeignKey(
        "Region", on_delete=models.PROTECT, null=True, blank=True
    )
    religion = models.ForeignKey(
        "Religion", on_delete=models.PROTECT, null=True, blank=True
    )
    nationality = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    marital_status = models.ForeignKey(
        "MaritalStatus", on_delete=models.PROTECT, null=True, blank=True
    )
    unit = models.ForeignKey("Units", on_delete=models.PROTECT)
    grade = models.ForeignKey("Grades", on_delete=models.PROTECT)
    station = models.CharField(max_length=100)
    structure = models.ForeignKey("Structure", on_delete=models.PROTECT)
    blood_group = models.ForeignKey(
        "BloodGroup", on_delete=models.PROTECT, null=True, blank=True
    )
    disable = models.BooleanField(null=True, blank=True)
    social_security = models.CharField(max_length=13)
    category = models.CharField(max_length=25)
    appointment_date = models.DateField()
    confirmation_date = models.DateField(null=True, blank=True)
    probation = models.CharField(null=True, blank=True)
    entry_qualification = models.CharField(max_length=255, null=True, blank=True)

    created_by = models.ForeignKey(
        "api.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_employees",
    )
    updated_by = models.ForeignKey(
        "api.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_employees",
    )

    search_vector = SearchVectorField(null=True)

    class Meta:
        db_table = "employee"
        verbose_name = "employee"

        indexes = [GinIndex(fields=["search_vector"])]

    def __str__(self):
        return f"{self.service_id}"


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        db_table = "category"
        verbose_name = "category"

    def __str__(self):
        return self.category_name


class Grades(models.Model):
    grade_name = models.CharField(max_length=255)
    rank = models.ForeignKey(Category, on_delete=models.PROTECT)
    structure = models.ForeignKey("Structure", on_delete=models.PROTECT)

    class Meta:
        db_table = "grades"
        verbose_name = "grade"

    def __str__(self):
        return f"{self.grade_name}"


class Units(models.Model):
    unit_name = models.CharField(max_length=100)
    city = models.CharField(max_length=25)

    class Meta:
        db_table = "units"
        verbose_name = "unit"

    def __str__(self):
        return f"{self.unit_name}"


class Gender(models.Model):
    sex = models.CharField(max_length=50)

    class Meta:
        db_table = "gender"
        verbose_name = "gender"

    def __str__(self):
        return f"{self.sex}"


class MaritalStatus(models.Model):
    marital_status_name = models.CharField(max_length=50)

    class Meta:
        db_table = "marital_status"
        verbose_name = "marital_status"

    def __str__(self):
        return f"{self.marital_status_name}"


class Region(models.Model):
    region_name = models.CharField(max_length=100)

    class Meta:
        db_table = "region"
        verbose_name = "region"

    def __str__(self):
        return f"{self.region_name}"


class Religion(models.Model):
    religion_name = models.CharField(max_length=100)

    class Meta:
        db_table = "religion"
        verbose_name = "religion"

    def __str__(self):
        return f"{self.religion_name}"


class Structure(models.Model):
    structure_name = models.CharField(max_length=50)

    class Meta:
        db_table = "structure"
        verbose_name = "structure"

    def __str__(self):
        return f"{self.structure_name}"


class BloodGroup(models.Model):
    blood_group_name = models.CharField(max_length=3)

    class Meta:
        db_table = "blood_group"
        verbose_name = "blood_group"

    def __str__(self):
        return f"{self.blood_group_name}"


class DocumentFile(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="files"
    )
    file_data = models.FileField(upload_to="documents/", null=False, blank=False)

    class Meta:
        db_table = "document_file"
        verbose_name = "document_file"

    def __str__(self):
        return f"{self.file_data.name}"


class UnregisteredEmployees(models.Model):
    service_id = models.CharField(max_length=7, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    other_names = models.CharField(max_length=255, null=True, blank=True)
    unit = models.ForeignKey(Units, on_delete=models.PROTECT, null=True, blank=True)
    grade = models.ForeignKey(Grades, on_delete=models.PROTECT, null=True, blank=True)
    social_security = models.CharField(max_length=13, null=True, blank=True)
    created_by = models.ForeignKey(
        "api.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_unregistered_employees",
    )
    updated_by = models.ForeignKey(
        "api.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_unregistered_employees",
    )

    class Meta:
        db_table = "unregistered_employees"
        verbose_name = "unregistered_employees"

    def __str__(self):
        return f"{self.service_id} - {self.id}"
