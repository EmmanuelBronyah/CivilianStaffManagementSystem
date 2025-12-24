from rest_framework.response import Response
import logging
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.utils.serializer_helpers import ReturnList


logger = logging.getLogger(__name__)


def handle_validation_error(exc: ValidationError):

    if "file_data" in exc.detail:
        message = handle_file_data_validation_error()
        return message

    elif "employee" in exc.detail:
        message = handle_employee_validation_error()
        return message

    else:
        message = handle_field_validation_error(exc.detail)
        return message


def handle_file_data_validation_error():
    message = "A valid file must be uploaded."
    return message


def handle_employee_validation_error():
    message = "Employee is invalid or inactive."
    return message


FIELDS_VALIDATION_CRITERIA = {
    # numbers; 3, 7, 255 etc indicates max_length
    # ----- EMPLOYEE MODEL FIELDS -----
    "blood_group": ["Blood Group", 3],
    "service_id": ["Service ID", 7],
    "last_name": ["Last name", 255],
    "other_names": ["Other names", 255],
    "gender": ["Gender", ""],
    "dob": ["DOB", ""],
    "hometown": ["Hometown", 255],
    "region": ["Region", ""],
    "religion": ["Religion", ""],
    "nationality": ["Nationality", 100],
    "address": ["Address", 255],
    "email": ["Email", 255],
    "marital_status": ["Marital Status", ""],
    "unit": ["Unit", ""],
    "grade": ["Grade", ""],
    "station": ["Station", 100],
    "structure": ["Structure", ""],
    "disable": ["Disable", ""],
    "social_security": ["Social Security", 13],
    "category": ["Category", 25],
    "appointment_date": ["Appointment date", ""],
    "confirmation_date": ["Confirmation date", ""],
    "probation": ["Probation", ""],
    "entry_qualification": ["Entry qualification", 255],
    # ----- GENDER MODEL FIELD -----
    "sex": ["Sex", 50],
    # ----- GRADE MODEL FIELD -----
    "grade_name": ["Grade", 255],
    # ----- MARITAL STATUS MODEL FIELD -----
    "marital_status_name": ["Marital Status", 50],
    # ----- REGION MODEL FIELD -----
    "region_name": ["Region", 100],
    # ----- RELIGION MODEL FIELD -----
    "religion_name": ["Religion", 100],
    # ----- STRUCTURE MODEL FIELD -----
    "structure_name": ["Structure", 50],
    # ----- BLOOD GROUP MODEL FIELD -----
    "blood_group_name": ["Blood Group", 3],
    # ----- DOCUMENT FILE MODEL FIELD -----
    "file_data": ["File", ""],
    # ----- UNIT MODEL FIELDS -----
    "unit_name": ["Unit", 100],
    "city": ["Unit", 25],
    # ----- USER MODEL FIELDS -----
    "fullname": ["Full name", 255],
    "username": ["Username", 100],
    "password": ["Password", ""],
    "role": ["Role", ""],
    "division": ["Division", ""],
    # ----- DIVISION MODEL FIELD -----
    "division_name": ["Division", 255],
    # ----- FLAG MODEL FIELDS -----
    "content_type": ["Content Type", ""],
    "object_id": ["Object ID", ""],
    "flag_type": ["Flag Type", ""],
    "reason": ["Reason", ""],
    # ----- OCCURRENCE MODEL FIELDS -----
    "employee": ["Employee ID", ""],
    "authority": ["Authority", 10],
    "level_step": ["Level", 10],
    "monthly_salary": ["Monthly Salary", 15],
    "annual_salary": ["Annual Salary", 15],
    "event": ["Event", ""],
    "wef_date": ["Wef Date", ""],
    "reason": ["Reason", 255],
}


def handle_field_validation_error(detail):
    # detail = {'blood_group': [ErrorDetail(string='This field may not be blank.', code='blank')]}

    if isinstance(detail, list):
        result = handle_detail_as_list(detail)

        if isinstance(result, str):
            return result

        # Assign new detail obj to be used for the error message generations
        detail = result

    detail_key = list(detail.keys())[0]
    error_code = detail.get(detail_key)[0].code

    field = FIELDS_VALIDATION_CRITERIA.get(detail_key, None)[0]
    max_length = FIELDS_VALIDATION_CRITERIA.get(detail_key, None)[1]

    if error_code == "blank" or error_code == "null" or error_code == "required":
        message = f"{field} cannot be blank or is required."
        return message

    elif error_code == "max_length":
        message = f"{field} must not have more than {max_length} characters."
        return message

    elif error_code == "does_not_exist":
        message = f"The value for {field} does not exist."
        return message

    elif error_code == "incorrect_type":
        message = f"Incorrect value for {field}."
        return message

    elif error_code == "invalid":
        message = f"Invalid format for {field}."
        return message

    elif error_code == "invalid_choice":
        message = "Choice is invalid."
        return message

    elif error_code == "unique":
        message = f"{field} already exists."
        return message

    elif error_code == "max_digits":
        message = f"Ensure that {field} has no more than {max_length} digits in total."
        return message


def handle_detail_as_list(detail):
    # detail = [ErrorDetail(string='Simulate Validation Error', code='invalid')]

    # [{}, {'monthly_salary': [ErrorDetail(string='A valid number is required.', code='invalid')]}, {'annual_salary': [ErrorDetail(string='A valid number is required.', code='invalid')]}, {'grade': [ErrorDetail(string='Incorrect type. Expected pk value, received str.', code='incorrect_type')]}]

    # First detail object being a dictionary guarantees subsequent elements are dictionaries
    detail_obj = detail[0]

    if isinstance(detail_obj, dict):
        for obj in detail:
            keys_as_list = list(obj.keys())
            if keys_as_list:
                return obj
    else:
        message = str(detail_obj)
        return message
