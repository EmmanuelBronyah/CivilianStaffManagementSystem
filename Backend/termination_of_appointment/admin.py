from django.contrib import admin
from termination_of_appointment import models

admin.site.register(models.TerminationOfAppointment)
admin.site.register(models.CausesOfTermination)
admin.site.register(models.TerminationStatus)
admin.site.register(models.InvalidTerminationOfAppointmentRecords)
