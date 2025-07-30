from django.db import models
from employees.models import Employee


class Identity(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    voters_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    national_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    glico_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    nhis_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    tin_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    class Meta:
        db_table = "Identity"
        verbose_name = "Identity"
        verbose_name_plural = "Identities"

    def __str__(self):
        return f"{self.employee} - {self.voters_id}"
