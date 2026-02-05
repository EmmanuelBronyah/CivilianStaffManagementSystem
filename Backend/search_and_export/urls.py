from django.urls import path
from . import views

urlpatterns = [
    path(
        "employee/",
        views.ListEmployeeRecordsAPIView.as_view(),
        name="list-employee-search-results",
    ),
    path(
        "employee/export/",
        views.EmployeeExportAPIView.as_view(),
        name="export-employee-search-results",
    ),
    path(
        "employee/export/status",
        views.ExportStatusAPIView.as_view(),
        name="export-status",
    ),
]
