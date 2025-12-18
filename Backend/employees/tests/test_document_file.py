from django.urls import reverse
from employees import models
from rest_framework import status
from activity_feeds.models import ActivityFeeds
from .base import EmployeeBaseAPITestCase, BaseAPITestCase
from django.core.files.uploadedfile import SimpleUploadedFile


class CreateDocumentFileAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_document_file_url = reverse("create-file")

        self.authenticate_admin()

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Get employee & file data
        self.employee = models.Employee.objects.get(service_id="000993")
        self.file_data = SimpleUploadedFile(
            "example.txt", b"Test Create Employee", "application/octet-stream"
        )

        self.document_file_data = {
            "employee": self.employee,
            "file_data": self.file_data,
        }

    def test_successful_document_file_creation(self):
        # Send create document request
        response = self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )  # Document -> <DocumentFile: documents/example_7qNM22y.txt>

        # Get created activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            models.DocumentFile.objects.filter(
                file_data__startswith="documents/example"
            ).exists()
        )
        self.assertIn("added a new document file", activity_feed)
        self.assertIn("documents/example", activity_feed)

    def test_empty_document_file(self):
        document_file_data_copy = self.document_file_data.copy()
        document_file_data_copy["file_data"] = ""

        # Send create request
        response = self.client.post(
            self.create_document_file_url, document_file_data_copy, format="multipart"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "A valid file must be uploaded.")
        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_throttling(self):
        # Send create requests
        response = self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )
        response = self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )
        response = self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )
        response = self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )
        response = self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )
        response = self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )
        response = self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )
        response = self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )
        response = self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveDocumentFileAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_document_file_url = reverse("create-file")
        self.retrieve_document_file_url = reverse("retrieve-file", kwargs={"pk": 1})

        self.authenticate_admin()

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Get employee & file data
        self.employee = models.Employee.objects.get(service_id="000993")
        self.file_data = SimpleUploadedFile(
            "example.txt", b"Test Create Employee", "application/octet-stream"
        )

        self.document_file_data = {
            "employee": self.employee,
            "file_data": self.file_data,
        }

    def test_retrieve_existing_document_file(self):
        # Send create request
        self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )

        # Send get request
        response = self.client.get(self.retrieve_document_file_url)
        print(response.data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("documents/example", response.data["file_data"])

    def test_retrieve_non_existing_document_file(self):
        # Send get request
        response = self.client.get(self.retrieve_document_file_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_throttling(self):
        # Send create request
        self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )

        # Send get requests
        response = self.client.get(self.retrieve_document_file_url)
        response = self.client.get(self.retrieve_document_file_url)
        response = self.client.get(self.retrieve_document_file_url)
        response = self.client.get(self.retrieve_document_file_url)
        response = self.client.get(self.retrieve_document_file_url)
        response = self.client.get(self.retrieve_document_file_url)
        response = self.client.get(self.retrieve_document_file_url)
        response = self.client.get(self.retrieve_document_file_url)
        response = self.client.get(self.retrieve_document_file_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditDocumentFileAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_document_file_url = reverse("create-file")
        self.edit_document_file_url = reverse("edit-file", kwargs={"pk": 1})

        self.authenticate_admin()

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Get employee & file data
        self.employee = models.Employee.objects.get(service_id="000993")
        self.file_data = SimpleUploadedFile(
            "example.txt", b"Test Create Employee", "application/octet-stream"
        )

        self.document_file_data = {
            "employee": self.employee,
            "file_data": self.file_data,
        }

    def test_edit_existing_document_file(self):
        new_file = SimpleUploadedFile(
            "test.pdf", b"Test Edit Document", "application/octet-stream"
        )
        edit_data = {"file_data": new_file}

        # Send create document request
        self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )

        # Send edit document request
        response = self.client.patch(
            self.edit_document_file_url, edit_data, format="multipart"
        )

        # Get created activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            models.DocumentFile.objects.filter(
                file_data__startswith="documents/test"
            ).exists()
        )
        self.assertIn("updated document file", activity_feed)
        self.assertIn("documents/example", activity_feed)
        self.assertIn("documents/test", activity_feed)

    def test_edit_non_existing_document_file(self):
        new_file = SimpleUploadedFile(
            "test.pdf", b"Test Edit Document", "application/octet-stream"
        )
        edit_data = {"file_data": new_file}

        # Send edit request
        response = self.client.patch(
            self.edit_document_file_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_edit_document_file_as_empty(self):
        edit_data = {"file_data": ""}

        # Send create request
        self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )

        # Send edit request
        response = self.client.patch(
            self.edit_document_file_url, edit_data, format="multipart"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "A valid file must be uploaded.")
        self.assertEqual(ActivityFeeds.objects.count(), 2)

    def test_throttling(self):
        new_file = SimpleUploadedFile(
            "test.pdf", b"Test Edit Document", "application/octet-stream"
        )
        edit_data = {"file_data": new_file}

        # Send create request
        self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )

        # Send edit requests
        response = self.client.patch(
            self.edit_document_file_url, edit_data, format="multipart"
        )
        response = self.client.patch(
            self.edit_document_file_url, edit_data, format="multipart"
        )
        response = self.client.patch(
            self.edit_document_file_url, edit_data, format="multipart"
        )
        response = self.client.patch(
            self.edit_document_file_url, edit_data, format="multipart"
        )
        response = self.client.patch(
            self.edit_document_file_url, edit_data, format="multipart"
        )
        response = self.client.patch(
            self.edit_document_file_url, edit_data, format="multipart"
        )
        response = self.client.patch(
            self.edit_document_file_url, edit_data, format="multipart"
        )
        response = self.client.patch(
            self.edit_document_file_url, edit_data, format="multipart"
        )
        response = self.client.patch(
            self.edit_document_file_url, edit_data, format="multipart"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteDocumentFileAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_document_file_url = reverse("create-file")
        self.delete_document_file_url = reverse("delete-file", kwargs={"pk": 1})

        self.authenticate_admin()

        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Get employee & file data
        self.employee = models.Employee.objects.get(service_id="000993")
        self.file_data = SimpleUploadedFile(
            "example.txt", b"Test Create Employee", "application/octet-stream"
        )

        self.document_file_data = {
            "employee": self.employee,
            "file_data": self.file_data,
        }

    def test_delete_existing_document_file(self):
        # Send create request
        self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )

        # Send delete request
        response = self.client.delete(self.delete_document_file_url)

        # Get created activity feed
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn("documents/example", activity_feed)
        self.assertIn("deleted by", activity_feed)

    def test_delete_non_existing_document_file(self):
        # Send delete request
        response = self.client.delete(self.delete_document_file_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 1)

    def test_throttling(self):
        # Send create request
        self.client.post(
            self.create_document_file_url, self.document_file_data, format="multipart"
        )

        # Send delete requests
        response = self.client.delete(self.delete_document_file_url)
        response = self.client.delete(self.delete_document_file_url)
        response = self.client.delete(self.delete_document_file_url)
        response = self.client.delete(self.delete_document_file_url)
        response = self.client.delete(self.delete_document_file_url)
        response = self.client.delete(self.delete_document_file_url)
        response = self.client.delete(self.delete_document_file_url)
        response = self.client.delete(self.delete_document_file_url)
        response = self.client.delete(self.delete_document_file_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
