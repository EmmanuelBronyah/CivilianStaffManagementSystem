from django.db import models
from employees.models import Employee, Units
from api.models import CustomUser


class ServiceWithForces(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="service_with_forces"
    )
    service_date = models.DateField()
    last_unit = models.ForeignKey(Units, on_delete=models.CASCADE)
    service_number = models.CharField(max_length=7)
    military_rank = models.ForeignKey("MilitaryRanks", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_service_with_forces",
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_service_with_forces",
    )

    class Meta:
        db_table = "service_with_forces"
        verbose_name = "service_with_forces"
        verbose_name_plural = "service_with_forces"

    def __str__(self):
        return f"{self.last_unit}"


class MilitaryRanks(models.Model):
    rank = models.CharField(max_length=255)
    branch = models.CharField(max_length=100)

    class Meta:
        db_table = "military_ranks"
        verbose_name = "military_ranks"
        verbose_name_plural = "military_ranks"

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
