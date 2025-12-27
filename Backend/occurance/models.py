from django.db import models
from employees.models import Employee, Grades
from api.models import CustomUser


class Occurrence(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="occurrences"
    )
    grade = models.ForeignKey(Grades, on_delete=models.PROTECT)
    authority = models.CharField(max_length=10)
    level_step = models.ForeignKey("LevelStep", on_delete=models.PROTECT)
    monthly_salary = models.DecimalField(decimal_places=2, max_digits=15)
    annual_salary = models.DecimalField(decimal_places=2, max_digits=15)
    event = models.ForeignKey("Event", on_delete=models.PROTECT)
    wef_date = models.DateField()
    reason = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_occurrences",
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_occurrences",
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "occurrence"
        verbose_name = "occurrence"
        verbose_name_plural = "occurrences"

    def __str__(self):
        return f"{self.employee} - {self.event}"


class LevelStep(models.Model):
    level_step = models.CharField(max_length=5, unique=True)
    monthly_salary = models.DecimalField(decimal_places=2, max_digits=15)

    class Meta:
        db_table = "levelStep"
        verbose_name = "levelStep"
        verbose_name_plural = "levelStep"

    def __str__(self):
        return f"{self.level_step}"


class Event(models.Model):
    event_name = models.CharField(max_length=255)

    class Meta:
        db_table = "event"
        verbose_name = "event"
        verbose_name_plural = "events"

    def __str__(self):
        return f"{self.event_name}"


class SalaryAdjustmentPercentage(models.Model):
    percentage_adjustment = models.IntegerField()

    class Meta:
        db_table = "salaryAdjustmentPercentage"
        verbose_name = "salaryAdjustmentPercentage"
        verbose_name_plural = "salaryAdjustmentPercentages"

    def __str__(self):
        return f"{self.percentage_adjustment}"


class InvalidOccurrenceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grades, on_delete=models.PROTECT)
    authority = models.CharField(max_length=10)
    level_step = models.ForeignKey("LevelStep", on_delete=models.PROTECT)
    monthly_salary = models.DecimalField(decimal_places=4, max_digits=15)
    annual_salary = models.DecimalField(decimal_places=4, max_digits=15)
    event = models.ForeignKey("Event", on_delete=models.PROTECT)
    wef_date = models.DateField(null=True, blank=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "InvalidOccurrenceRecord"
        verbose_name = "InvalidOccurrenceRecord"
        verbose_name_plural = "InvalidOccurrenceRecords"

    def __str__(self):
        return f"{self.employee.service_id} - {self.event}"
