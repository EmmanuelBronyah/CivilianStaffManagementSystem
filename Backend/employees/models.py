from django.db import models

# TODO: Check against saving an Unregistered Employee model instance with all it's values set to Null


class Employee(models.Model):
    service_id = models.CharField(primary_key=True, max_length=7)
    lastname = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255)
    gender = models.ForeignKey("Gender", on_delete=models.PROTECT)
    dob = models.DateField()
    hometown = models.CharField(max_length=255, null=True, blank=True)
    region = models.ForeignKey(
        "Region", on_delete=models.PROTECT, null=True, blank=True
    )
    religion = models.ForeignKey(
        "Religion", on_delete=models.PROTECT, null=True, blank=True
    )
    nationality = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
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
    category = models.CharField(max_length=25, null=True, blank=True)
    appointment_date = models.DateField()
    confirmation_date = models.DateField(null=True, blank=True)
    probation = models.CharField(null=True, blank=True)
    entry_qualification = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "Employee"
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f"{self.service_id}"


class Grades(models.Model):
    grade_name = models.CharField(max_length=255)

    class Meta:
        db_table = "Grades"
        verbose_name = "Grade"
        verbose_name_plural = "Grades"

    def __str__(self):
        return f"{self.grade_name}"


class Units(models.Model):
    unit_name = models.CharField(max_length=100)
    city = models.CharField(max_length=25)

    class Meta:
        db_table = "Units"
        verbose_name = "Unit"
        verbose_name_plural = "Units"

    def __str__(self):
        return f"{self.unit} - {self.city}"


class Gender(models.Model):
    sex = models.CharField(max_length=50)

    class Meta:
        db_table = "Gender"
        verbose_name = "Gender"
        verbose_name_plural = "Genders"

    def __str__(self):
        return f"{self.sex}"


class MaritalStatus(models.Model):
    marital_status_name = models.CharField(max_length=50)

    class Meta:
        db_table = "MaritalStatus"
        verbose_name = "MaritalStatus"
        verbose_name_plural = "MaritalStatuses"

    def __str__(self):
        return f"{self.marital_status_name}"


class Region(models.Model):
    region_name = models.CharField(max_length=100)

    class Meta:
        db_table = "Region"
        verbose_name = "Region"
        verbose_name_plural = "Regions"

    def __str__(self):
        return f"{self.region_name}"


class Religion(models.Model):
    religion_name = models.CharField(max_length=100)

    class Meta:
        db_table = "Religion"
        verbose_name = "Religion"
        verbose_name_plural = "Religions"

    def __str__(self):
        return f"{self.religion_name}"


class Structure(models.Model):
    structure_name = models.CharField(max_length=50)

    class Meta:
        db_table = "Structure"
        verbose_name = "Structure"
        verbose_name_plural = "Structures"

    def __str__(self):
        return f"{self.structure_name}"


class BloodGroup(models.Model):
    blood_group_name = models.CharField(max_length=3)

    class Meta:
        db_table = "BloodGroup"
        verbose_name = "BloodGroup"
        verbose_name_plural = "BloodGroups"

    def __str__(self):
        return f"{self.blood_group_name}"


class DocumentFile(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="files"
    )
    file_data = models.FileField(upload_to="documents/", null=False, blank=False)

    class Meta:
        db_table = "DocumentFile"
        verbose_name = "DocumentFile"
        verbose_name_plural = "DocumentFiles"

    def __str__(self):
        return f"{self.file_data.name}"


class UnregisteredEmployees(models.Model):
    service_id = models.CharField(max_length=7, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    other_names = models.CharField(max_length=255, null=True, blank=True)
    unit = models.ForeignKey(Units, on_delete=models.PROTECT, null=True, blank=True)
    grade = models.ForeignKey(Grades, on_delete=models.PROTECT, null=True, blank=True)
    social_security = models.CharField(max_length=13, null=True, blank=True)

    class Meta:
        db_table = "UnregisteredEmployees"
        verbose_name = "UnregisteredEmployees"
        verbose_name_plural = "UnregisteredEmployees"

    def __str__(self):
        return f"{self.service_id} - {self.lastname, self.other_names}"
