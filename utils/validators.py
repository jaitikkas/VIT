"""
Input validation helpers.
Each function returns a tuple (is_valid, error_message).
"""

import re


def validate_name(name):
    """Name must not be empty and should only have letters, spaces, hyphens, apostrophes."""
    name = name.strip()
    if not name:
        return False, "Name cannot be empty."
    if not re.match(r"^[A-Za-z\s\-']+$", name):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes."
    return True, ""


def validate_email(email):
    """Basic check for user@domain.tld format."""
    email = email.strip()
    if not email:
        return False, "Email cannot be empty."
    pattern = r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"
    if not re.match(pattern, email):
        return False, "Invalid email format. Expected something like user@example.com"
    return True, ""


def validate_phone(phone):
    """Phone must have only digits/spaces/dashes/plus and be 7-15 digits long."""
    phone = phone.strip()
    if not phone:
        return False, "Phone number cannot be empty."
    cleaned = re.sub(r"[\s\-\+]", "", phone)
    if not cleaned.isdigit():
        return False, "Phone can only contain digits, spaces, dashes, and '+'."
    if not (7 <= len(cleaned) <= 15):
        return False, "Phone must be between 7 and 15 digits."
    return True, ""


def validate_isbn(isbn):
    """ISBN must be 10 or 13 digits (hyphens allowed but stripped for counting)."""
    isbn = isbn.strip()
    if not isbn:
        return False, "ISBN cannot be empty."
    cleaned = isbn.replace("-", "")
    if not cleaned.isdigit():
        return False, "ISBN must contain only digits and hyphens."
    if len(cleaned) not in (10, 13):
        return False, "ISBN must be 10 or 13 digits (excluding hyphens)."
    return True, ""


def validate_positive_int(value, field_name="Value"):
    """Value must be a non-negative integer."""
    value = value.strip()
    if not value:
        return False, f"{field_name} cannot be empty."
    if not value.isdigit():
        return False, f"{field_name} must be a non-negative integer."
    if int(value) < 0:
        return False, f"{field_name} cannot be negative."
    return True, ""


def validate_non_empty(value, field_name="Field"):
    """Generic non-empty check."""
    if not value.strip():
        return False, f"{field_name} cannot be empty."
    return True, ""
