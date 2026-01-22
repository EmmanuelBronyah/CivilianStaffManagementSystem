from django.db import models
from employees.models import Employee
from api.models import CustomUser


class PreviousGovernmentService(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="previous_government_service"
    )
    institution = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    position = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_previous_government_service",
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_previous_government_service",
    )

    class Meta:
        db_table = "previous_government_service"
        verbose_name = "previous_government_service"
        verbose_name_plural = "previous_government_service"

    def __str__(self):
        return f"{self.institution}"


class InvalidPreviousGovernmentServiceRecords(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    institution = models.CharField(max_length=255, null=True, blank=True)
    duration = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "invalid_previous_government_service_records"
        verbose_name = "invalid_previous_government_service_records"
        verbose_name_plural = "invalid_previous_government_service_records"

    def __str__(self):
        return f"{self.employee.service_id}"
