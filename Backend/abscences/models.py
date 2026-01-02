from django.db import models
from employees.models import Employee
from api.models import CustomUser


class Absences(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="absences"
    )
    absence = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    authority = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_absences",
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_absences",
    )

    class Meta:
        db_table = "absences"
        verbose_name = "absences"
        verbose_name_plural = "absences"

    def __str__(self):
        return f"{self.employee} - {self.absence}"
