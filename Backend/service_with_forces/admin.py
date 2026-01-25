from django.contrib import admin
from .models import ServiceWithForces, MilitaryRanks, IncompleteServiceWithForcesRecords


admin.site.register(ServiceWithForces)
admin.site.register(MilitaryRanks)
admin.site.register(IncompleteServiceWithForcesRecords)
