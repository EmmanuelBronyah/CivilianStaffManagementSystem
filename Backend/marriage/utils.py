def generate_text(fields):
    changes = [
        f'{label}: {"N/A" if old == "" or old is None else old} → {"N/A" if new == "" or new is None else new}'
        for label, old, new in fields
        if str(old) != str(new)
    ]
    return " — ".join(changes)


def spouse_record_changes(previous, current):
    fields = [
        ("Spouse", previous.spouse_name, current.spouse_name),
        ("Phone Number", previous.phone_number, current.phone_number),
        ("Address", previous.address, current.address),
        (
            "Registration Number",
            previous.registration_number,
            current.registration_number,
        ),
        ("Marriage Date", previous.marriage_date, current.marriage_date),
        ("Marriage Place", previous.marriage_place, current.marriage_place),
    ]
    changes = generate_text(fields)
    return changes
