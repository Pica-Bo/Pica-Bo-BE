import re

def is_valid_phone(phone: str) -> bool:
    """
    Validates a phone number format. Accepts international numbers with +, spaces, dashes, and digits.
    Adjust the regex as needed for your requirements.
    """
    if not phone:
        return False
    pattern = re.compile(r"^\+?[0-9\-\s]{7,20}$")
    return bool(pattern.match(phone))
