from django.db import models
from employees.models import Employee


class EmergencyOrNextOfKin(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    relation = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    emergency_contact = models.CharField(max_length=10, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "EmergencyOrNextOfKin"
        verbose_name = "EmergencyOrNextOfKin"
        verbose_name_plural = "EmergencyOrNextOfKin"

    def __str__(self):
        return f"{self.name}"
