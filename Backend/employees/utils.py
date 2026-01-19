def generate_text(fields):
    changes = [
        f'{label}: {"N/A" if old == "" or old is None else old} → {"N/A" if new == "" or new is None else new}'
        for label, old, new in fields
        if str(old) != str(new)
    ]
    return " — ".join(changes)


def employee_record_changes(previous, current):
    fields = [
        ("Service ID", previous.service_id, current.service_id),
        ("Last Name", previous.last_name, current.last_name),
        ("Other Names", previous.other_names, current.other_names),
        (
            "Gender",
            getattr(previous.gender, "sex", None),
            getattr(current.gender, "sex", None),
        ),
        ("Date of Birth", previous.dob, current.dob),
        ("Age", previous.age, current.age),
        ("Hometown", previous.hometown, current.hometown),
        (
            "Region",
            getattr(previous.region, "region_name", None),
            getattr(current.region, "region_name", None),
        ),
        (
            "Religion",
            getattr(previous.religion, "religion_name", None),
            getattr(current.religion, "religion_name", None),
        ),
        ("Nationality", previous.nationality, current.nationality),
        ("Address", previous.address, current.address),
        ("Email", previous.email, current.email),
        (
            "Marital Status",
            previous.marital_status.marital_status_name,
            current.marital_status.marital_status_name,
        ),
        (
            "Unit",
            getattr(previous.unit, "unit_name", None),
            getattr(current.unit, "unit_name", None),
        ),
        (
            "Grade",
            getattr(previous.grade, "grade_name", None),
            getattr(current.grade, "grade_name", None),
        ),
        ("Station", previous.station, current.station),
        (
            "Structure",
            getattr(previous.structure, "structure_name", None),
            getattr(current.structure, "structure_name", None),
        ),
        (
            "Blood Group",
            getattr(previous.blood_group, "blood_group_name", None),
            getattr(current.blood_group, "blood_group_name", None),
        ),
        ("Disable", previous.disable, current.disable),
        ("Social Security", previous.social_security, current.social_security),
        ("Category", previous.category, current.category),
        ("Appointment Date", previous.appointment_date, current.appointment_date),
        ("Confirmation Date", previous.confirmation_date, current.confirmation_date),
        ("Probation", previous.probation, current.probation),
        (
            "Entry Qualification",
            previous.entry_qualification,
            current.entry_qualification,
        ),
    ]
    changes = generate_text(fields)
    return changes


def unregistered_employee_record_changes(previous, current):
    fields = [
        ("Service ID", previous.service_id, current.service_id),
        ("Last Name", previous.last_name, current.last_name),
        ("Other Names", previous.other_names, current.other_names),
        (
            "Unit",
            getattr(previous.unit, "unit_name", None),
            getattr(current.unit, "unit_name", None),
        ),
        (
            "Grade",
            getattr(previous.grade, "grade_name", None),
            getattr(current.grade, "grade_name", None),
        ),
        ("Social Security", previous.social_security, current.social_security),
    ]
    changes = generate_text(fields)
    return changes


def grade_record_changes(previous, current):
    fields = [
        ("Grade", previous.grade_name, current.grade_name),
        (
            "Rank",
            getattr(previous.rank, "category_name", None),
            getattr(current.rank, "category_name", None),
        ),
        (
            "Structure",
            getattr(previous.structure, "structure_name", None),
            getattr(current.structure, "structure_name", None),
        ),
    ]
    changes = generate_text(fields)
    return changes
