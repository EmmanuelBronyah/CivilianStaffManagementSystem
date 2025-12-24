from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateOccurrenceAPIView.as_view(), name="create-occurrence"),
]
