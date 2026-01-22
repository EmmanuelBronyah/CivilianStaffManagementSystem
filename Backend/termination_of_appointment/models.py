from django.db import models
from employees.models import Employee
from api.models import CustomUser


class TerminationOfAppointment(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="termination_of_appointment"
    )
    cause = models.ForeignKey("CausesOfTermination", on_delete=models.PROTECT)
    date = models.DateField()
    authority = models.CharField(max_length=10, null=True, blank=True)
    status = models.ForeignKey("TerminationStatus", on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_termination_of_appointment",
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_termination_of_appointment",
    )

    class Meta:
        db_table = "termination_of_appointment"
        verbose_name = "termination_of_appointment"
        verbose_name_plural = "termination_of_appointment"

    def __str__(self):
        return f"{self.employee.service_id} - {self.cause}"


class CausesOfTermination(models.Model):
    termination_cause = models.CharField(max_length=100)

    class Meta:
        db_table = "cause_of_termination"
        verbose_name = "cause_of_termination"
        verbose_name_plural = "cause_of_termination"

    def __str__(self):
        return f"{self.termination_cause}"


class TerminationStatus(models.Model):
    termination_status = models.CharField(max_length=100)

    class Meta:
        db_table = "termination_status"
        verbose_name = "termination_status"
        verbose_name_plural = "termination_status"

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
        db_table = "invalid_termination_of_appointment_records"
        verbose_name = "invalid_termination_of_appointment_records"
        verbose_name_plural = "invalid_termination_of_appointment_records"

    def __str__(self):
        return f"{self.employee.service_id}"
