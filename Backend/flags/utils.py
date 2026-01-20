def generate_flag_type_changes_made_text(previous_flag, current_flag):
    return (
        f"Flag Type: {previous_flag.flag_type.flag_type} → {current_flag.flag_type.flag_type}"
        if previous_flag.flag_type.flag_type != current_flag.flag_type.flag_type
        else ""
    )


def generate_reason_changes_made_text(previous_flag, current_flag):
    return (
        f" — Reason: {previous_flag.reason} → {current_flag.reason}"
        if previous_flag.reason != current_flag.reason
        else ""
    )


def generate_field_changes_made_text(previous_flag, current_flag):
    if not previous_flag.field and not current_flag.field:
        return ""

    previous_field = previous_flag.field or "None"
    current_field = current_flag.field or "None"

    return (
        f" — Flagged Field: {previous_field.replace('_', ' ').capitalize()} → {current_field.replace('_', ' ').capitalize()}"
        if previous_field != current_field
        else ""
    )


def generate_changes_text(model_name, user, previous_flag, current_flag):
    reason_changes = ""

    flag_type_changes = generate_flag_type_changes_made_text(
        previous_flag, current_flag
    )

    field_changes = generate_field_changes_made_text(previous_flag, current_flag)

    reason_changes = generate_reason_changes_made_text(previous_flag, current_flag)

    changes_text = (
        f"Flagged {model_name} Record was updated by {user}:"
        f"{flag_type_changes}"
        f"{field_changes}"
        f"{reason_changes}"
    )

    return changes_text
