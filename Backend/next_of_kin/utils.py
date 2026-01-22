def generate_text(fields):
    changes = [
        f'{label}: {"N/A" if old == "" or old is None else old} → {"N/A" if new == "" or new is None else new}'
        for label, old, new in fields
        if str(old) != str(new)
    ]
    return " — ".join(changes)


def next_of_kin_record_changes(previous, current):
    fields = [
        ("Name", previous.name, current.name),
        ("Relation", previous.relation, current.relation),
        ("Email", previous.next_of_kin_email, current.next_of_kin_email),
        ("Address", previous.address, current.address),
        ("Phone Number", previous.phone_number, current.phone_number),
        ("Emergency Contact", previous.emergency_contact, current.emergency_contact),
    ]
    changes = generate_text(fields)
    return changes
