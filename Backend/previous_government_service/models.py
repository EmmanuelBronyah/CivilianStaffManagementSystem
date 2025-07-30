from django.db import models
from employees.models import Employee


class PreviousGovernmentService(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "PreviousGovernmentService"
        verbose_name = "PreviousGovernmentService"
        verbose_name_plural = "PreviousGovernmentService"

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
        db_table = "InvalidPreviousGovernmentServiceRecords"
        verbose_name = "InvalidPreviousGovernmentServiceRecords"
        verbose_name_plural = "InvalidPreviousGovernmentServiceRecords"

    def __str__(self):
        return f"{self.employee.service_id}"
