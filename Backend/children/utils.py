def generate_text(fields):
    changes = [
        f"{label}: {old} → {new}" for label, old, new in fields if str(old) != str(new)
    ]
    return " — ".join(changes)


def child_record_changes(previous, current):
    fields = [
        # Children
        ("Child Name", previous.child_name, current.child_name),
        ("Date of Birth", previous.dob, current.dob),
        ("Gender", previous.gender.sex, current.gender.sex),
        ("Other Parent", previous.other_parent, current.other_parent),
        ("Authority", previous.authority, current.authority),
    ]
    changes = generate_text(fields)
    return changes
