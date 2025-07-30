from django.db import models
from employees.models import Employee, Units


class ServiceWithForces(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    service_date = models.DateField()
    last_unit = models.ForeignKey(Units, on_delete=models.CASCADE)
    service_number = models.CharField(max_length=7)
    military_rank = models.ForeignKey("MilitaryRanks", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ServiceWithForces"
        verbose_name = "ServiceWithForces"
        verbose_name_plural = "ServiceWithForces"

    def __str__(self):
        return f"{self.last_unit}"


class MilitaryRanks(models.Model):
    rank = models.CharField(max_length=255)
    branch = models.CharField(max_length=100)

    class Meta:
        db_table = "MilitaryRanks"
        verbose_name = "MilitaryRank"
        verbose_name_plural = "MilitaryRanks"

    def __str__(self):
        return f"{self.rank}"


class InvalidServiceWithForcesRecords(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    service_date = models.DateField(null=True, blank=True)
    last_unit = models.ForeignKey(
        Units, on_delete=models.CASCADE, null=True, blank=True
    )
    service_number = models.CharField(max_length=7, null=True, blank=True)
    military_rank = models.ForeignKey(
        MilitaryRanks, on_delete=models.CASCADE, null=True, blank=True
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "InvalidServiceWithForcesRecords"
        verbose_name = "InvalidServiceWithForcesRecords"
        verbose_name_plural = "InvalidServiceWithForcesRecords"

    def __str__(self):
        return f"{self.employee.service_id}"
