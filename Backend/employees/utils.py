def get_field_value(instance, field):
    value = getattr(instance, field, False)
    return False if value is False else str(value)


def exclude_fields(old_record, new_record):
    fields = [
        "gender_id",
        "region_id",
        "religion_id",
        "marital_status_id",
        "unit_id",
        "grade_id",
        "structure_id",
        "blood_group_id",
        "_state",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    ]

    for field in fields:
        old_record.pop(field, None)
        new_record.pop(field, None)

    return old_record, new_record


def get_records_changed(previous_record, current_record):
    id_fields = [
        "gender",
        "marital_status",
        "unit",
        "grade",
        "region",
        "religion",
        "structure",
        "blood_group",
    ]

    old_record = previous_record.__dict__.copy()
    new_record = current_record.__dict__.copy()

    # Retrieve actual names for foreign key field. Eg: gender_id: 1 -> gender: Male
    for field in id_fields:
        previous_value = get_field_value(previous_record, field)
        current_value = get_field_value(current_record, field)

        if previous_value is False and current_value is False:
            continue

        old_record[field] = get_field_value(previous_record, field)
        new_record[field] = get_field_value(current_record, field)

    # Remove unwanted fields
    old_record, new_record = exclude_fields(old_record, new_record)

    records_changed = []

    for key, value in old_record.items():
        new_record_value = new_record[key]

        if new_record_value != value:
            readable_key = key.replace("_", " ").capitalize()
            text = f"{readable_key}: {value or 'None'} → {new_record_value or 'None'}"
            records_changed.append(text)

    return ", ".join(records_changed)
