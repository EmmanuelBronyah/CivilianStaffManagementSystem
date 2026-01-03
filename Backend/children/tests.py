from occurance.tests.base import EmployeeBaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds


class CreateChildRecordAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_child_record_url = reverse("create-child")
        self.create_employee_url = reverse("create-employee")

        self.child_record_data = {
            "employee": "000993",
            "child_name": "Ama",
            "authority": "CEM 20/24",
            "dob": "2025-08-07",
            "other_parent": "John Doe",
            "gender": self.gender.id,
        }

        self.authenticate_standard_user()

    def test_successful_child_record_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_child_record_url, self.child_record_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["employee"], "000993")
        self.assertEqual(response.data["child_name"], "Ama")
        self.assertIn("added a new Child Record", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        invalid_data = {
            "employee": "000993",
            "child_name": "Ama",
            "authority": "CEM 20/24",
            "dob": "2025-08-07",
            "other_parent": "John Doe" * 300,
            "gender": self.gender.id,
        }

        # Send create request
        response = self.client.post(
            self.create_child_record_url, invalid_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "Other Parent must not have more than 255 characters.",
        )

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Omit required field
        self.child_record_data.update(authority="")

        # Send create request
        response = self.client.post(
            self.create_child_record_url, self.child_record_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Authority cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_child_record_url, self.child_record_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditChildRecordAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_child_record_url = reverse("create-child")
        self.edit_child_record_url = reverse("edit-child", kwargs={"pk": 1})

        self.child_record_data = {
            "employee": "000993",
            "child_name": "Ama",
            "authority": "CEM 20/24",
            "dob": "2025-08-07",
            "other_parent": "John Doe",
            "gender": self.gender.id,
        }

        self.authenticate_standard_user()

    def test_successful_child_record_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create child record request
        self.client.post(
            self.create_child_record_url, self.child_record_data, format="json"
        )

        edit_data = {"authority": "CEM 13/20", "dob": "2023-09-09"}

        # Send edit child record request
        response = self.client.patch(
            self.edit_child_record_url, edit_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["authority"], "CEM 13/20")
        self.assertEqual(response.data["dob"], "2023-09-09")
        self.assertIn("Date of Birth: 2025-08-07 → 2023-09-09", activity_feed)
        self.assertIn("Authority: CEM 20/24 → CEM 13/20", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create child record request
        self.client.post(
            self.create_child_record_url, self.child_record_data, format="json"
        )

        edit_data = {"dob": "tyui"}

        # Send edit child record request
        response = self.client.patch(
            self.edit_child_record_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid format for Date of Birth.")

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create child record request
        self.client.post(
            self.create_child_record_url, self.child_record_data, format="json"
        )

        edit_data = {"authority": ""}

        # Send edit child record request
        response = self.client.patch(
            self.edit_child_record_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Authority cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create child record request
        self.client.post(
            self.create_child_record_url, self.child_record_data, format="json"
        )

        edit_data = {"authority": "CEM 23/24"}

        # Send edit child record request
        for _ in range(13):
            response = self.client.patch(
                self.edit_child_record_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveEmployeeChildrenAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_child_record_url = reverse("create-child")
        self.retrieve_employee_children_url = reverse(
            "list-employee-children", kwargs={"pk": "000993"}
        )

        self.child_record_data = {
            "employee": "000993",
            "child_name": "Ama",
            "authority": "CEM 20/24",
            "dob": "2025-08-07",
            "other_parent": "John Doe",
            "gender": self.gender.id,
        }

        self.authenticate_standard_user()

    def test_successful_retrieval(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create child record request
        for _ in range(5):
            self.client.post(
                self.create_child_record_url, self.child_record_data, format="json"
            )

        # Send get employee children request
        response = self.client.get(self.retrieve_employee_children_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_non_existing_employee(self):
        # Send create child record request
        for _ in range(5):
            self.client.post(
                self.create_child_record_url, self.child_record_data, format="json"
            )

        # Send get employee child record request
        response = self.client.get(self.retrieve_employee_children_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Employee matches the given query."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create child record request
        self.client.post(
            self.create_child_record_url, self.child_record_data, format="json"
        )

        # Send get employee child record request
        for _ in range(13):
            response = self.client.get(self.retrieve_employee_children_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteChildRecordAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_child_record_url = reverse("create-child")
        self.delete_child_record_url = reverse("delete-child", kwargs={"pk": 1})

        self.child_record_data = {
            "employee": "000993",
            "child_name": "Ama",
            "authority": "CEM 20/24",
            "dob": "2025-08-07",
            "other_parent": "John Doe",
            "gender": self.gender.id,
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create child record request
        self.client.post(
            self.create_child_record_url, self.child_record_data, format="json"
        )

        # Send delete request
        response = self.client.delete(self.delete_child_record_url)

        # Get created activity feed
        activity = "The Child Record 'Ama — 2025-08-07' was deleted by Standard User"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_child_record(self):
        # Send delete child record request
        response = self.client.delete(self.delete_child_record_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create child record request
        self.client.post(
            self.create_child_record_url, self.child_record_data, format="json"
        )

        # Send delete child record request
        for _ in range(13):
            response = self.client.delete(self.delete_child_record_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
