from occurance.tests.base import EmployeeBaseAPITestCase
from django.urls import reverse
from rest_framework import status
from activity_feeds.models import ActivityFeeds


class CreateCourseAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_course_url = reverse("create-course")
        self.create_employee_url = reverse("create-employee")

        self.course_data = {
            "employee": "000993",
            "course_type": "HEALTH PROFICIENCY",
            "authority": "CEM 20/24",
            "place": "KNUST",
            "date_commenced": "2024-09-07",
            "date_ended": "2025-09-07",
            "qualification": "HEALTH PROFICIENCY",
            "result": "SECOND CLASS UPPER DIVISION",
        }

        course_data_copy = self.course_data.copy()
        course_data_copy["employee"] = "020124"

        self.course_data_list = [self.course_data]
        self.course_data_list.append(course_data_copy)

        self.authenticate_standard_user()

    def test_successful_single_course_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        response = self.client.post(
            self.create_course_url, self.course_data, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["employee"], "000993")
        self.assertIn("added a new Course", activity_feed)
        self.assertIn("HEALTH PROFICIENCY", activity_feed)

    def test_successful_multiple_course_creation(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")
        self.client.post(
            self.create_employee_url, self.other_employee_data, format="json"
        )

        # Send create request
        response = self.client.post(
            self.create_course_url, self.course_data_list, format="json"
        )

        # Get Activity
        activity_feed = ActivityFeeds.objects.all()[2:]
        first_course_feed, second_course_feed = (
            activity_feed[0].activity,
            activity_feed[1].activity,
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data[0]["employee"],
            "000993",
        )
        self.assertEqual(
            response.data[1]["employee"],
            "020124",
        )
        self.assertIn("added a new Course", first_course_feed)
        self.assertIn("HEALTH PROFICIENCY", first_course_feed)
        self.assertIn("added a new Course", second_course_feed)
        self.assertIn("HEALTH PROFICIENCY", second_course_feed)

    def test_single_course_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        invalid_data = {
            "employee": "000993",
            "course_type": "HEALTH PROFICIENCY*",
            "authority": "CEM 20/24",
            "place": "KNUST",
            "date_commenced": "2022-09-07",
            "date_ended": "2024-09-07",
            "qualification": "HEALTH PROFICIENCY",
            "result": "SECOND CLASS UPPER DIVISION",
        }

        # Send create request
        response = self.client.post(self.create_course_url, invalid_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "course_type")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Course Type can only contain letters, numbers, spaces, hyphens, commas, and periods.",
                )

    def test_multiple_course_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")
        self.client.post(
            self.create_employee_url, self.other_employee_data, format="json"
        )

        self.course_data_list[1].update(date_ended="edf")

        # Send create request
        response = self.client.post(
            self.create_course_url, self.course_data_list, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error_list = response.data
        for error_dict in error_list:
            for field, field_errors in error_dict.items():
                self.assertEqual(field, "date_ended")

                for error in field_errors:
                    self.assertEqual(
                        error,
                        "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
                    )

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Omit required field
        self.course_data.update(result="")

        # Send create request
        response = self.client.post(
            self.create_course_url, self.course_data, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "result")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

    def test_omit_required_field_multiple_course(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")
        self.client.post(
            self.create_employee_url, self.other_employee_data, format="json"
        )

        self.course_data_list[1].update(date_ended="")

        # Send create request
        response = self.client.post(
            self.create_course_url, self.course_data_list, format="json"
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error_list = response.data
        for error_dict in error_list:
            for field, field_errors in error_dict.items():
                self.assertEqual(field, "date_ended")

                for error in field_errors:
                    self.assertEqual(
                        error,
                        "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
                    )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create request
        for _ in range(13):
            response = self.client.post(
                self.create_course_url, self.course_data, format="json"
            )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class EditCourseAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_course_url = reverse("create-course")
        self.edit_course_url = reverse("edit-course", kwargs={"pk": 1})

        self.course_data = {
            "employee": "000993",
            "course_type": "HEALTH PROFICIENCY",
            "authority": "CEM 20/24",
            "place": "KNUST",
            "date_commenced": "2025-09-07",
            "date_ended": "2027-09-07",
            "qualification": "HEALTH PROFICIENCY",
            "result": "SECOND CLASS UPPER DIVISION",
        }

        self.authenticate_standard_user()

    def test_successful_course_edit(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create course request
        self.client.post(self.create_course_url, self.course_data, format="json")

        edit_data = {"authority": "CEM 13/20", "result": "FIRST CLASS HONORS"}

        # Send edit course request
        response = self.client.patch(self.edit_course_url, edit_data, format="json")

        # Get Activity
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["authority"], "CEM 13/20")
        self.assertEqual(response.data["result"], "FIRST CLASS HONORS")
        self.assertIn(
            "Result: SECOND CLASS UPPER DIVISION → FIRST CLASS HONORS", activity_feed
        )
        self.assertIn("Authority: CEM 20/24 → CEM 13/20", activity_feed)

    def test_invalid_data(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create course request
        self.client.post(self.create_course_url, self.course_data, format="json")

        edit_data = {"date_commenced": "tyui"}

        # Send edit course request
        response = self.client.patch(self.edit_course_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "date_commenced")

            for error in field_errors:
                self.assertEqual(
                    error,
                    "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
                )

    def test_omit_required_field(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create course request
        self.client.post(self.create_course_url, self.course_data, format="json")

        edit_data = {"authority": ""}

        # Send edit course request
        response = self.client.patch(self.edit_course_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.data
        for field, field_errors in errors.items():
            self.assertEqual(field, "authority")

            for error in field_errors:
                self.assertEqual(error, "This field may not be blank.")

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create course request
        self.client.post(self.create_course_url, self.course_data, format="json")

        edit_data = {"authority": "CEM 23/24"}

        # Send edit course request
        for _ in range(13):
            response = self.client.patch(self.edit_course_url, edit_data, format="json")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RetrieveEmployeeCourseAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_course_url = reverse("create-course")
        self.retrieve_employee_course_url = reverse(
            "list-employee-courses", kwargs={"pk": "000993"}
        )

        self.course_data = {
            "employee": "000993",
            "course_type": "HEALTH PROFICIENCY",
            "authority": "CEM 20/24",
            "place": "KNUST",
            "date_commenced": "2025-09-07",
            "date_ended": "2027-09-07",
            "qualification": "HEALTH PROFICIENCY",
            "result": "SECOND CLASS UPPER DIVISION",
        }

        self.authenticate_standard_user()

    def test_successful_course_retrieval(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create course request
        for _ in range(5):
            self.client.post(self.create_course_url, self.course_data, format="json")

        # Send get employee courses request
        response = self.client.get(self.retrieve_employee_course_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_non_existing_employee(self):
        # Send create course request
        for _ in range(5):
            self.client.post(self.create_course_url, self.course_data, format="json")

        # Send get employee courses request
        response = self.client.get(self.retrieve_employee_course_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Employee matches the given query."
        )

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create course request
        self.client.post(self.create_course_url, self.course_data, format="json")

        # Send get employee courses request
        for _ in range(13):
            response = self.client.get(self.retrieve_employee_course_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeleteCourseAPITest(EmployeeBaseAPITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create-employee")
        self.create_course_url = reverse("create-course")
        self.delete_course_url = reverse("delete-course", kwargs={"pk": 1})

        self.course_data = {
            "employee": "000993",
            "course_type": "HEALTH PROFICIENCY",
            "authority": "CEM 20/24",
            "place": "KNUST",
            "date_commenced": "2025-09-07",
            "date_ended": "2027-09-07",
            "qualification": "HEALTH PROFICIENCY",
            "result": "SECOND CLASS UPPER DIVISION",
        }

        self.authenticate_standard_user()

    def test_successful_deletion(self):
        # Send create request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create course request
        self.client.post(self.create_course_url, self.course_data, format="json")

        # Send delete request
        response = self.client.delete(self.delete_course_url)

        # Get created activity feed
        activity = "The Course(HEALTH PROFICIENCY) was deleted by Standard User"
        activity_feed = ActivityFeeds.objects.last().activity

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(activity_feed, activity)

    def test_delete_non_existing_course(self):
        # Send delete course request
        response = self.client.delete(self.delete_course_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ActivityFeeds.objects.count(), 0)

    def test_throttling(self):
        # Send create employee request
        self.client.post(self.create_employee_url, self.employee_data, format="json")

        # Send create course request
        self.client.post(self.create_course_url, self.course_data, format="json")

        # Send delete course request
        for _ in range(13):
            response = self.client.delete(self.delete_course_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
