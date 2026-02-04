from rest_framework import serializers
from . import models
import logging


logger = logging.getLogger(__name__)


class BaseEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Employee
        fields = "__all__"

    def is_admin(self):
        request = self.context.get("request")
        return bool(
            request
            and request.user.is_staff
            and request.user.is_superuser
            and request.user.role == "ADMINISTRATOR"
        )

    @staticmethod
    def validate_name(field, value):
        if not value:
            logger.debug(f"{field} is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    f"{field} can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    f"{field} can only contain letters, spaces, hyphens, and periods."
                )

        return value

    @staticmethod
    def validate_other_text(field, value):
        if not value:
            logger.debug(f"{field} is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " ", ","}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    f"{field} can only contain letters, spaces, hyphens, commas, and periods."
                )

                raise serializers.ValidationError(
                    f"{field} can only contain letters, spaces, hyphens, commas, and periods."
                )

        return value

    @staticmethod
    def validate_other_text_with_digits(field, value):
        if not value:
            logger.debug(f"{field} is empty")
            return value

        import string

        VALID_CHARS = (
            set(string.ascii_letters) | set(string.digits) | {".", "-", " ", ","}
        )

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    f"{field} can only contain letters, numbers, spaces, hyphens, commas, and periods."
                )

                raise serializers.ValidationError(
                    f"{field} can only contain letters, numbers, spaces, hyphens, commas, and periods."
                )

        return value

    def assign_dob_and_age(self, attrs):
        if self.is_admin() and ("dob" in attrs or "age" in attrs):
            logger.debug("Admin provided DOB/Age — skipping auto-assignment.")
            return attrs

        social_security = attrs.get("social_security", None)

        if social_security and len(social_security) == 13:
            logger.debug("Social Security has 13 characters")

            dob_string = social_security[3:9]
            year, month, day = dob_string[:2], dob_string[2:4], dob_string[4:]

            from datetime import datetime
            from dateutil.relativedelta import relativedelta

            try:
                dob = datetime.strptime(f"{year}-{month}-{day}", "%y-%m-%d").date()
                today = datetime.now().date()

                if dob >= today:
                    logger.debug("Could not assign DOB. DOB cannot be a future date.")

                    self.warnings.append(
                        "Could not assign DOB. DOB cannot be a future date."
                    )

                else:
                    age = relativedelta(today, dob).years
                    required_age = 18

                    if age < required_age:
                        logger.debug(
                            "Could not assign DOB. Age is below the required age."
                        )

                        self.warnings.append(
                            "Could not assign DOB. Age is below the required age."
                        )
                    else:
                        attrs["dob"] = dob.strftime("%Y-%m-%d")
                        attrs["age"] = age

                        logger.debug("Successfully assigned DOB and Age.")

            except ValueError:
                logger.debug(
                    "DOB could not be inferred from the social security number."
                )

                self.warnings.append(
                    "DOB could not be inferred from the social security number."
                )

        return attrs

    def assign_station(self, attrs):
        if self.is_admin() and ("station" in attrs):
            logger.debug("Admin provided Station — skipping auto-assignment.")
            return attrs

        unit = attrs.get("unit", None)

        if unit:

            try:
                attrs["station"] = unit.city
                logger.debug("Successfully assigned Station.")

            except models.Units.DoesNotExist:
                logger.debug(
                    "Station could not be assigned because the unit is invalid."
                )

                self.warnings.append(
                    "Station could not be assigned because the unit is invalid."
                )

        return attrs

    def assign_probation(self, attrs):
        if self.is_admin() and ("probation" in attrs):
            logger.debug("Admin provided Probation — skipping auto-assignment.")
            return attrs

        appointment_date = attrs.get("appointment_date", None)
        confirmation_date = attrs.get("confirmation_date", None)

        if confirmation_date and appointment_date:
            logger.debug("Confirmation date and Appointment date both have values")

            if confirmation_date <= appointment_date:
                logger.debug(
                    "Could not assign probation. Confirmation date should be after appointment date."
                )

                self.warnings.append(
                    "Could not assign probation. Confirmation date should be after appointment date."
                )
            else:
                from dateutil.relativedelta import relativedelta

                delta = relativedelta(confirmation_date, appointment_date)
                probation_years = delta.years + (1 if delta.months else 0)
                attrs["probation"] = probation_years

                logger.debug("Successfully assigned Probation")

        return attrs

    def assign_category(self, attrs):
        if self.is_admin() and ("category" in attrs):
            logger.debug("Admin provided Category — skipping auto-assignment.")
            return attrs

        grade = attrs.get("grade", None)

        if grade:

            try:
                attrs["category"] = grade.rank.category_name
                logger.debug("Successfully assigned Category")

            except models.Grades.DoesNotExist:
                logger.debug(
                    "Category could not be assigned because the grade is invalid."
                )

                self.warnings.append(
                    "Category could not be assigned because the grade is invalid."
                )

            except models.Category.DoesNotExist:
                logger.debug("Category to be assigned is invalid.")

                self.warnings.append("Category to be assigned is invalid.")

        return attrs

    def assign_structure(self, attrs):
        if self.is_admin() and ("structure" in attrs):
            logger.debug("Admin provided Structure — skipping auto-assignment.")
            return attrs

        grade = attrs.get("grade", None)

        if grade:
            logger.debug("Grade has a value")

            try:
                attrs["structure"] = grade.structure
                logger.debug("Successfully assigned Structure")

            except models.Grades.DoesNotExist:
                logger.debug(
                    "Structure could not be assigned because the grade is invalid."
                )

                self.warnings.append(
                    "Structure could not be assigned because the grade is invalid."
                )

            except models.Structure.DoesNotExist:
                logger.debug("Structure to be assigned is invalid.")

                self.warnings.append("Structure to be assigned is invalid.")

        return attrs

    def validate_last_name(self, value):
        return self.validate_name("Last Name", value)

    def validate_other_names(self, value):
        return self.validate_name("Other Names", value)

    def validate_address(self, value):
        return self.validate_other_text_with_digits("Address", value)

    def validate_hometown(self, value):
        return self.validate_other_text("Hometown", value)

    def validate_nationality(self, value):
        return self.validate_other_text("Nationality", value)

    def validate_entry_qualification(self, value):
        return self.validate_other_text_with_digits("Entry Qualification", value)

    def validate_social_security(self, value):
        if not value:
            logger.debug("Social Security is empty")
            return value

        if not value.isalnum():
            logger.debug("Social Security can only contain letters and numbers.")

            raise serializers.ValidationError(
                "Field can only contain letters and numbers."
            )

        return value

    def validate_service_id(self, value):
        if not value:
            logger.debug("Service ID is empty")
            return value

        if not value.isdigit():
            logger.debug("Service ID can only contain numbers.")

            raise serializers.ValidationError("Field can only contain numbers.")

        if len(value) < 5:
            logger.debug("Service ID must have more than five(5) digits.")

            raise serializers.ValidationError(
                "Service ID must have more than five(5) digits."
            )

        return value

    def validate(self, attrs):
        self.warnings = []

        attrs = self.assign_dob_and_age(attrs)

        attrs = self.assign_station(attrs)

        attrs = self.assign_probation(attrs)

        attrs = self.assign_category(attrs)

        attrs = self.assign_structure(attrs)

        return super().validate(attrs)


class EmployeeCreateSerializer(BaseEmployeeSerializer):

    class Meta:
        model = models.Employee
        exclude = ("dob", "age", "station", "category", "structure", "probation")


class EmployeeUpdateSerializer(BaseEmployeeSerializer):

    class Meta(BaseEmployeeSerializer.Meta):
        pass


class EmployeeReadSerializer(serializers.ModelSerializer):
    gender_display = serializers.StringRelatedField(source="gender", read_only=True)
    region_display = serializers.StringRelatedField(source="region", read_only=True)
    religion_display = serializers.StringRelatedField(source="religion", read_only=True)
    marital_status_display = serializers.StringRelatedField(
        source="marital_status", read_only=True
    )
    unit_display = serializers.StringRelatedField(source="unit", read_only=True)
    grade_display = serializers.StringRelatedField(source="grade", read_only=True)
    structure_display = serializers.StringRelatedField(
        source="structure", read_only=True
    )
    blood_group_display = serializers.StringRelatedField(
        source="blood_group", read_only=True
    )
    created_by_display = serializers.StringRelatedField(
        source="created_by", read_only=True
    )
    updated_by_display = serializers.StringRelatedField(
        source="updated_by", read_only=True
    )

    class Meta:
        model = models.Employee
        exclude = ("search_vector",)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = "__all__"

    def validate_category_name(self, value):
        if not value:
            logger.debug("Category is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Category can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    "Category can only contain letters, spaces, hyphens, and periods."
                )

        return value


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Grades
        fields = "__all__"

    def validate_grade_name(self, value):
        if not value:
            logger.debug("Grade is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Grade can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    "Grade can only contain letters, spaces, hyphens, and periods."
                )

        return value


class GradeReadSerializer(serializers.ModelSerializer):
    rank_display = serializers.StringRelatedField(source="rank", read_only=True)
    structure_display = serializers.StringRelatedField(
        source="structure", read_only=True
    )

    class Meta:
        model = models.Grades
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Units
        fields = "__all__"

    def validate_unit_name(self, value):
        if not value:
            logger.debug("Unit is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | set(string.digits) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Unit can only contain letters, numbers, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    "Unit can only contain letters, numbers, spaces, hyphens, and periods."
                )

        return value

    def validate_city(self, value):
        if not value:
            logger.debug("City is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "City can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    "City can only contain letters, spaces, hyphens, and periods."
                )

        return value


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Gender
        fields = "__all__"

    def validate_sex(self, value):
        if not value:
            logger.debug("Gender is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Gender can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    "Gender can only contain letters, spaces, hyphens, and periods."
                )

        return value


class MaritalStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MaritalStatus
        fields = "__all__"

    def validate_marital_status_name(self, value):
        if not value:
            logger.debug("Marital Status is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Marital Status can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    "Marital Status can only contain letters, spaces, hyphens, and periods."
                )

        return value


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Region
        fields = "__all__"

    def validate_region_name(self, value):
        if not value:
            logger.debug("Region is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Region can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    "Region can only contain letters, spaces, hyphens, and periods."
                )

        return value


class ReligionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Religion
        fields = "__all__"

    def validate_religion_name(self, value):
        if not value:
            logger.debug("Religion is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Religion can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    "Religion can only contain letters, spaces, hyphens, and periods."
                )

        return value


class StructureSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Structure
        fields = "__all__"

    def validate_structure_name(self, value):
        if not value:
            logger.debug("Structure is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Structure can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    "Structure can only contain letters, spaces, hyphens, and periods."
                )

        return value


class BloodGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BloodGroup
        fields = "__all__"

    def validate_blood_group_name(self, value):
        if not value:
            logger.debug("Blood Group is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", "+", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Blood Group can only contain letters, spaces, hyphen(-) and plus(+) signs, and periods."
                )

                raise serializers.ValidationError(
                    "Blood Group can only contain letters, spaces, hyphen(-) and plus(+) signs, and periods."
                )

        return value


class DocumentFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DocumentFile
        fields = "__all__"


class UnregisteredEmployeesWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UnregisteredEmployees
        fields = "__all__"

    @staticmethod
    def validate_name(field, value):
        if not value:
            logger.debug(f"{field} is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    f"{field} can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    f"{field} can only contain letters, spaces, hyphens, and periods."
                )

        return value

    def validate_last_name(self, value):
        return self.validate_name("Last Name", value)

    def validate_other_names(self, value):
        return self.validate_name("Other Names", value)

    def validate_social_security(self, value):
        if not value:
            logger.debug("Social Security is empty")
            return value

        if not value.isalnum():
            logger.debug("Social Security can only contain letters and numbers.")

            raise serializers.ValidationError(
                "Field can only contain letters and numbers."
            )

        return value

    def validate_service_id(self, value):
        if not value:
            logger.debug("Service ID is empty")
            return value

        if not value.isdigit():
            logger.debug("Service ID can only contain numbers.")

            raise serializers.ValidationError("Field can only contain numbers.")

        if len(value) < 5:
            logger.debug("Service ID must have more than five(5) digits.")

            raise serializers.ValidationError(
                "Service ID must have more than five(5) digits."
            )

        return value

    def validate(self, attrs):
        system_fields = {"created_by", "updated_by"}

        has_value = any(
            value not in (None, "")
            for key, value in attrs.items()
            if key not in system_fields
        )

        if not has_value:
            raise serializers.ValidationError(
                "All fields for Unregistered Employee cannot be empty."
            )

        unit = attrs.get("unit")
        grade = attrs.get("grade")

        non_unit_grade_value = any(
            value not in (None, "")
            for key, value in attrs.items()
            if key not in system_fields | {"unit", "grade"}
        )

        if (unit or grade) and not non_unit_grade_value:
            raise serializers.ValidationError(
                "Cannot save Unregistered Employee with Grade or Unit as the only non-empty field."
            )

        return attrs


class UnregisteredEmployeeReadSerializer(serializers.ModelSerializer):
    unit_display = serializers.StringRelatedField(source="unit", read_only=True)
    grade_display = serializers.StringRelatedField(source="grade", read_only=True)
    created_by_display = serializers.StringRelatedField(
        source="created_by", read_only=True
    )
    updated_by_display = serializers.StringRelatedField(
        source="updated_by", read_only=True
    )

    class Meta:
        model = models.UnregisteredEmployees
        fields = "__all__"
