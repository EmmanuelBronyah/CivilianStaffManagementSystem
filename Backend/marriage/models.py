from django.db import models
from employees.models import Employee
from api.models import CustomUser

# TODO: Check Phone Numbers less than 10


class Spouse(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="spouse"
    )
    spouse_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    registration_number = models.CharField(max_length=255, null=True, blank=True)
    marriage_date = models.DateField(null=True, blank=True)
    marriage_place = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_spouses",
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_spouses",
    )

    class Meta:
        db_table = "spouse"
        verbose_name = "spouse"
        verbose_name_plural = "spouse"

    def __str__(self):
        return f"{self.spouse_name}"
