from django.db import models
from employees.models import Employee
from api.models import CustomUser


class Courses(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="courses"
    )
    course_type = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    date_commenced = models.DateField()
    date_ended = models.DateField()
    qualification = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    authority = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_courses",
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_courses",
    )

    class Meta:
        db_table = "courses"
        verbose_name = "course"
        verbose_name_plural = "courses"

    def __str__(self):
        return f"{self.course_type}"


class InvalidCourseRecords(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    course_type = models.CharField(max_length=255, null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    date_commenced = models.DateField(null=True, blank=True)
    date_ended = models.DateField(null=True, blank=True)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    result = models.CharField(max_length=255, null=True, blank=True)
    authority = models.CharField(max_length=10, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "InvalidCourseRecords"
        verbose_name = "InvalidCourseRecords"
        verbose_name_plural = "InvalidCourseRecords"

    def __str__(self):
        return f"{self.employee.service_id}"
