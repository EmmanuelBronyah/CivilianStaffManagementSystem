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


class InCompleteChildRecords(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="incomplete_child_records",
    )
    service_id = models.CharField(max_length=7, null=True, blank=True)
    child_name = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, null=True, blank=True)
    other_parent = models.CharField(max_length=255, null=True, blank=True)
    authority = models.CharField(max_length=10, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "api.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_incomplete_child_records",
    )
    updated_by = models.ForeignKey(
        "api.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_incomplete_child_records",
    )

    class Meta:
        db_table = "incomplete_child_records"
        verbose_name = "incomplete_child_records"
        verbose_name_plural = "incomplete_child_records"

    def __str__(self):
        return f"{self.id}"
