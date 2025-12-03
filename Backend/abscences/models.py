from django.db import models
from employees.models import Employee


class Absences(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    absence = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    authority = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Absences"
        verbose_name = "Absences"
        verbose_name_plural = "Absences"

    def __str__(self):
        return f"{self.employee} - {self.absence}"
