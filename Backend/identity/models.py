from django.db import models
from employees.models import Employee
from api.models import CustomUser

# TODO: Validate when saving an instance with all fields NULL


class Identity(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="identity"
    )
    voters_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    national_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    glico_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    nhis_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    tin_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_identity_records",
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="updated_identity_records",
    )

    class Meta:
        db_table = "identity"
        verbose_name = "identity"
        verbose_name_plural = "identities"

    def __str__(self):
        return f"{self.employee} - {self.voters_id}"
