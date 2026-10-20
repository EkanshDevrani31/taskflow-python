"""Input checks. Each function raises ValueError with a clear message."""
import re
from datetime import datetime

PRIORITIES = ["low", "medium", "high"]


def parse_username(text):
    text = text.strip()
    if not re.fullmatch(r"[A-Za-z0-9_]{3,50}", text):
        raise ValueError("Username must be 3 to 50 characters: letters, numbers or underscore.")
    return text


def parse_password(text):
    if len(text) < 6:
        raise ValueError("Password must be at least 6 characters.")
    return text


def parse_title(text):
    text = text.strip()
    if not text:
        raise ValueError("Title cannot be empty.")
    if len(text) > 120:
        raise ValueError("Title must be 120 characters or fewer.")
    return text


def parse_description(text):
    return text.strip()


def parse_priority(text):
    """Accepts 1/2/3 or low/medium/high. Empty input means medium."""
    text = text.strip().lower()
    if not text:
        return "medium"
    if text.isdigit() and 1 <= int(text) <= 3:
        return PRIORITIES[int(text) - 1]
    if text in PRIORITIES:
        return text
    raise ValueError("Choose 1 (low), 2 (medium) or 3 (high).")


def parse_due_date(text):
    """Accepts YYYY-MM-DD. Empty input means no due date (returns None)."""
    text = text.strip()
    if not text:
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Due date must be in YYYY-MM-DD format, for example 2026-11-05.")


def parse_id(text):
    if not text.strip().isdigit():
        raise ValueError("Enter a valid task number.")
    return int(text)
