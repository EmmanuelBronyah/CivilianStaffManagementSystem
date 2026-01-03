from django.db import models
from employees.models import Employee, Gender
from api.models import CustomUser


class Children(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="children"
    )
    child_name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    other_parent = models.CharField(max_length=255)
    authority = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_children_records",
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_children_records",
    )

    class Meta:
        db_table = "children"
        verbose_name = "children"
        verbose_name_plural = "children"

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
        db_table = "invalidChildRecords"
        verbose_name = "invalidChildRecords"
        verbose_name_plural = "invalidChildRecords"

    def __str__(self):
        return f"{self.employee.service_id}"
