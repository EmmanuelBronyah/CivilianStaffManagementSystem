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
]
