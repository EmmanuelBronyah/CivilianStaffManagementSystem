from django.db import models
from employees.models import Employee, Grades


class Occurrence(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grades, on_delete=models.PROTECT)
    authority = models.CharField(max_length=10)
    level_step = models.ForeignKey("LevelStep", on_delete=models.PROTECT)
    monthly_salary = models.DecimalField(decimal_places=4, max_digits=15)
    annual_salary = models.DecimalField(decimal_places=4, max_digits=15)
    event = models.ForeignKey("Event", on_delete=models.PROTECT)
    wef_date = models.DateField()
    reason = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Occurrence"
        verbose_name = "Occurrence"
        verbose_name_plural = "Occurrences"

    def __str__(self):
        return f"{self.employee} - {self.event}"


class LevelStep(models.Model):
    level_step = models.CharField(max_length=5, unique=True)
    monthly_salary = models.DecimalField(decimal_places=4, max_digits=15)

    class Meta:
        db_table = "LevelStep"
        verbose_name = "LevelStep"
        verbose_name_plural = "LevelStep"

    def __str__(self):
        return f"{self.level_step}"


class Event(models.Model):
    event = models.CharField(max_length=255)

    class Meta:
        db_table = "Event"
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return f"{self.event}"


class SalaryPercentageAdjustment(models.Model):
    percentage_adjustment = models.CharField()
    formula = models.CharField()


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
