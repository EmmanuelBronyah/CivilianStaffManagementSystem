def generate_text(fields):
    changes = [
        f'{label}: {"N/A" if old == "" or old is None else old} → {"N/A" if new == "" or new is None else new}'
        for label, old, new in fields
        if str(old) != str(new)
    ]
    return " — ".join(changes)


def common_fields(previous, current):
    return [
        # Courses
        ("Course Type", previous.course_type, current.course_type),
        ("Place", previous.place, current.place),
        ("Date Commenced", previous.date_commenced, current.date_commenced),
        ("Date Commenced", previous.date_ended, current.date_ended),
        ("Qualification", previous.qualification, current.qualification),
        ("Result", previous.result, current.result),
        ("Authority", previous.authority, current.authority),
    ]


def course_record_changes(previous, current):
    fields = common_fields(previous, current)
    changes = generate_text(fields)
    return changes


def incomplete_course_changes(previous, current):
    fields = common_fields(previous, current)
    fields.append(("Service ID", previous.service_id, current.service_id))

    changes = generate_text(fields)
    return changes
