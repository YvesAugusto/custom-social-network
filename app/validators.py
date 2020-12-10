def validate_email(email):
    if '@' not in email:
        return False

    forbidden_chars = ['*', '!', '<', '>', '%']

    for f in forbidden_chars:
        if f in email:
            return False

    return True
    