from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateCourseAPIView.as_view(), name="create-course"),
    path(
        "<str:pk>/detail/",
        views.RetrieveCourseAPIView.as_view(),
        name="retrieve-course",
    ),
    path(
        "<str:pk>/employee/",
        views.ListEmployeeCoursesAPIView.as_view(),
        name="list-employee-courses",
    ),
    path("<str:pk>/edit/", views.EditCourseAPIView.as_view(), name="edit-course"),
    path(
        "<str:pk>/delete/",
        views.DeleteCourseAPIView.as_view(),
        name="delete-course",
    ),
    # incomplete course record
    path(
        "incomplete-course-record/create/",
        views.CreateIncompleteCourseRecordsAPIView.as_view(),
        name="create-incomplete-course-record",
    ),
    path(
        "incomplete-course-record/<str:pk>/detail/",
        views.RetrieveIncompleteCourseRecordsAPIView.as_view(),
        name="retrieve-incomplete-course-record",
    ),
    path(
        "incomplete-course-record/<str:pk>/employee/",
        views.ListEmployeeIncompleteCourseRecordsAPIView.as_view(),
        name="list-employee-incomplete-course-record",
    ),
    path(
        "incomplete-course-record/",
        views.ListIncompleteCourseRecordsAPIView.as_view(),
        name="list-incomplete-course-record",
    ),
    path(
        "incomplete-course-record/<str:pk>/edit/",
        views.EditIncompleteCourseRecordsAPIView.as_view(),
        name="edit-incomplete-course-record",
    ),
    path(
        "incomplete-course-record/<str:pk>/delete/",
        views.DeleteIncompleteCourseRecordsAPIView.as_view(),
        name="delete-incomplete-course-record",
    ),
]
