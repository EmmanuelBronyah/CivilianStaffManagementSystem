from django.contrib import admin
from occurance import models


admin.site.register(models.Occurrence)
admin.site.register(models.LevelStep)
admin.site.register(models.Event)
admin.site.register(models.SalaryAdjustmentPercentage)
admin.site.register(models.IncompleteOccurrence)
