from .base import EmployeeBaseAPITestCase
from django.urls import reverse


class CreateOccurrenceAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_occurrence_url = reverse("create-occurrence")

        self.authenticate_standard_user()

    def test_successfully_create_occurrence(self): ...
