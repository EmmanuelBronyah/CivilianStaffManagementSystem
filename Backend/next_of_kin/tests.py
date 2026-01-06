from occurance.tests.base import EmployeeBaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds


class CreateNextOfKinAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_next_of_kin_url = reverse("create-next-of-kin")
        self.create_employee_url = reverse("create-employee")

        self.next_of_kin_data = {
            "employee": "000993",
            "name": "Ama",
            "phone_number": "0554981873",
            "address": "caper st",
            "emergency_contact": "0202367489",
            "relation": "Sister",
            "next_of_kin_email": "email@gmail.com",
        }

        self.authenticate_standard_user()

    def test_successful_next_of_kin_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_next_of_kin_url, self.next_of_kin_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["employee"], "000993")
        self.assertEqual(response.data["name"], "Ama")
        self.assertIn("added a new Next Of Kin", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        invalid_data = {
            "employee": "000993",
            "name": "Ama",
            "phone_number": "055498187378",
            "address": "caper st",
            "emergency_contact": "0202367489",
            "relation": "Sister",
            "next_of_kin_email": "email@gmail.com",
        }

        # Send create request
        response = self.client.post(
            self.create_next_of_kin_url, invalid_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "Phone Number must not have more than 10 characters.",
        )

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Omit required field
        self.next_of_kin_data.update(relation="")

        # Send create request
        response = self.client.post(
            self.create_next_of_kin_url, self.next_of_kin_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Relation cannot be blank or is required."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_next_of_kin_url, self.next_of_kin_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditNextOfKinAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_next_of_kin_url = reverse("create-next-of-kin")
        self.edit_next_of_kin_url = reverse("edit-next-of-kin", kwargs={"pk": 1})

        self.next_of_kin_data = {
            "employee": "000993",
            "name": "Ama",
            "phone_number": "0554981873",
            "address": "caper st",
            "emergency_contact": "0202367489",
            "relation": "Sister",
            "next_of_kin_email": "email@gmail.com",
        }

        self.authenticate_standard_user()

    def test_successful_next_of_kin_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create next of kin request
        self.client.post(
            self.create_next_of_kin_url, self.next_of_kin_data, format="json"
        )

        edit_data = {"phone_number": "0202491783", "address": "tontre st"}

        # Send edit next of kin request
        response = self.client.patch(
            self.edit_next_of_kin_url, edit_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], "0202491783")
        self.assertEqual(response.data["address"], "tontre st")
        self.assertIn("Address: caper st → tontre st", activity_feed)
        self.assertIn("Phone Number: 0554981873 → 0202491783", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create next of kin request
        self.client.post(
            self.create_next_of_kin_url, self.next_of_kin_data, format="json"
        )

        edit_data = {"phone_number": "tyui" * 30}

        # Send edit next of kin request
        response = self.client.patch(
            self.edit_next_of_kin_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "Phone Number must not have more than 10 characters.",
        )

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create next of kin request
        self.client.post(
            self.create_next_of_kin_url, self.next_of_kin_data, format="json"
        )

        edit_data = {"name": ""}

        # Send edit next of kin request
        response = self.client.patch(
            self.edit_next_of_kin_url, edit_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Name cannot be blank or is required.")

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create next of kin request
        self.client.post(
            self.create_next_of_kin_url, self.next_of_kin_data, format="json"
        )

        edit_data = {"phone_number": "020237482"}

        # Send edit next of kin request
        for _ in range(13):
            response = self.client.patch(
                self.edit_next_of_kin_url, edit_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveEmployeeNextOfKinAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_next_of_kin_url = reverse("create-next-of-kin")
        self.retrieve_employee_next_of_kin_url = reverse(
            "list-employee-next-of-kin", kwargs={"pk": "000993"}
        )

        self.next_of_kin_data = {
            "employee": "000993",
            "name": "Ama",
            "phone_number": "0554981873",
            "address": "caper st",
            "emergency_contact": "0202367489",
            "relation": "Sister",
            "next_of_kin_email": "email@gmail.com",
        }

        self.authenticate_standard_user()

    def test_successful_retrieval(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create next of kin request
        for _ in range(5):
            self.client.post(
                self.create_next_of_kin_url, self.next_of_kin_data, format="json"
            )

        # Send get employee children request
        response = self.client.get(self.retrieve_employee_next_of_kin_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_non_existing_employee(self):
        # Send create next of kin request
        for _ in range(5):
            self.client.post(
                self.create_next_of_kin_url, self.next_of_kin_data, format="json"
            )

        # Send get employee next of kin request
        response = self.client.get(self.retrieve_employee_next_of_kin_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Employee matches the given query."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create next of kin request
        self.client.post(
            self.create_next_of_kin_url, self.next_of_kin_data, format="json"
        )

        # Send get employee next of kin request
        for _ in range(13):
            response = self.client.get(self.retrieve_employee_next_of_kin_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteNextOfKinAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_next_of_kin_url = reverse("create-next-of-kin")
        self.delete_next_of_kin_url = reverse("delete-next-of-kin", kwargs={"pk": 1})

        self.next_of_kin_data = {
            "employee": "000993",
            "name": "Ama",
            "phone_number": "0554981873",
            "address": "caper st",
            "emergency_contact": "0202367489",
            "relation": "Sister",
            "next_of_kin_email": "email@gmail.com",
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create next of kin request
        self.client.post(
            self.create_next_of_kin_url, self.next_of_kin_data, format="json"
        )

        # Send delete request
        response = self.client.delete(self.delete_next_of_kin_url)

        # Get created activity feed
        activity = "The Next Of Kin 'Ama — Sister' was deleted by Standard User"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_next_of_kin(self):
        # Send delete next of kin request
        response = self.client.delete(self.delete_next_of_kin_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create next of kin request
        self.client.post(
            self.create_next_of_kin_url, self.next_of_kin_data, format="json"
        )

        # Send delete next of kin request
        for _ in range(13):
            response = self.client.delete(self.delete_next_of_kin_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
