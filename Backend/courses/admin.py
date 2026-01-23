from django.contrib import admin
from .models import Courses, IncompleteCourseRecords


admin.site.register(Courses)
admin.site.register(IncompleteCourseRecords)
