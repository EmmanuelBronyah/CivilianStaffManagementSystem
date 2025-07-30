from django.db import models
from employees.models import Employee


class TerminationOfAppointment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cause = models.ForeignKey("CausesOfTermination", on_delete=models.PROTECT)
    date = models.DateField()
    authority = models.CharField(max_length=10, null=True, blank=True)
    status = models.ForeignKey("TerminationStatus", on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "TerminationOfAppointment"
        verbose_name = "TerminationOfAppointment"
        verbose_name_plural = "TerminationOfAppointment"

    def __str__(self):
        return f"{self.employee.service_id} - {self.cause}"


class CausesOfTermination(models.Model):
    cause = models.CharField(max_length=255)

    class Meta:
        db_table = "CausesOfTermination"
        verbose_name = "CausesOfTermination"
        verbose_name_plural = "CausesOfTermination"

    def __str__(self):
        return f"{self.cause}"


class TerminationStatus(models.Model):
    termination_status = models.CharField(max_length=255)

    class Meta:
        db_table = "TerminationStatus"
        verbose_name = "TerminationStatus"
        verbose_name_plural = "TerminationStatus"

    def __str__(self):
        return f"{self.termination_status}"


class InvalidTerminationOfAppointmentRecords(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cause = models.ForeignKey(
        CausesOfTermination, on_delete=models.PROTECT, null=True, blank=True
    )
    date = models.DateField(null=True, blank=True)
    authority = models.CharField(max_length=10, null=True, blank=True)
    status = models.ForeignKey(
        TerminationStatus, on_delete=models.PROTECT, null=True, blank=True
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "InvalidTerminationOfAppointmentRecords"
        verbose_name = "InvalidTerminationOfAppointmentRecords"
        verbose_name_plural = "InvalidTerminationOfAppointmentRecords"

    def __str__(self):
        return f"{self.employee.service_id}"
