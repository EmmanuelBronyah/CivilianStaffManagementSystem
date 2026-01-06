from django.db import models
from employees.models import Employee
from api.models import CustomUser


class EmergencyOrNextOfKin(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="next_of_kin"
    )
    name = models.CharField(max_length=255)
    relation = models.CharField(max_length=100)
    next_of_kin_email = models.EmailField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    emergency_contact = models.CharField(max_length=10, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_next_of_kin",
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_next_of_kin",
    )

    class Meta:
        db_table = "emergency_or_next_of_kin"
        verbose_name = "emergency_or_next_of_kin"
        verbose_name_plural = "emergency_or_next_of_kin"

    def __str__(self):
        return f"{self.name}"
