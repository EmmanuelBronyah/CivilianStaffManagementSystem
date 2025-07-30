from django.db import models
from employees.models import Employee, Gender


class Children(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    child_name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    other_parent = models.CharField(max_length=255)
    authority = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Children"
        verbose_name = "Children"
        verbose_name_plural = "Children"

    def __str__(self):
        return f"{self.child_name}"


class InvalidChildRecords(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    child_name = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, null=True, blank=True)
    other_parent = models.CharField(max_length=255, null=True, blank=True)
    authority = models.CharField(max_length=10, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "InvalidChildRecords"
        verbose_name = "InvalidChildRecords"
        verbose_name_plural = "InvalidChildRecords"

    def __str__(self):
        return f"{self.employee.service_id}"
