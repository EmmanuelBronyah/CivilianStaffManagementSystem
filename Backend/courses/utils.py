def generate_text(fields):
    changes = [f"{label}: {old} → {new}" for label, old, new in fields if old != new]
    return " — ".join(changes)


def course_record_changes(previous, current):
    fields = [
        # Courses
        ("Course Type", previous.course_type, current.course_type),
        ("Place", previous.place, current.place),
        ("Date Commenced", previous.date_commenced, current.date_commenced),
        ("Date Commenced", previous.date_ended, current.date_ended),
        ("Qualification", previous.qualification, current.qualification),
        ("Result", previous.result, current.result),
        ("Authority", previous.authority, current.authority),
    ]
    changes = generate_text(fields)
    return changes
