from django.db import models
from employees.models import Employee


class Spouse(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    spouse_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    registration_number = models.CharField(max_length=255, null=True, blank=True)
    marriage_date = models.DateField(null=True, blank=True)
    marriage_place = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Spouse"
        verbose_name = "Spouse"
        verbose_name_plural = "Spouse"

    def __str__(self):
        return f"{self.spouse_name}"
