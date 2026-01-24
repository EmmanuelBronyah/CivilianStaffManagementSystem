from django.contrib import admin
from .models import (
    PreviousGovernmentService,
    IncompletePreviousGovernmentServiceRecords,
)


admin.site.register(PreviousGovernmentService)
admin.site.register(IncompletePreviousGovernmentServiceRecords)
