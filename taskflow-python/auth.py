"""Register and log in users."""
import mysql.connector

from db import execute, fetch_all
from security import hash_password, verify_password


def register(username, password):
    """Create a user. Raises ValueError if the username is taken."""
    if fetch_all("SELECT id FROM users WHERE username = %s", (username,)):
        raise ValueError("That username is already taken.")
    try:
        user_id, _ = execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hash_password(password)),
        )
    except mysql.connector.IntegrityError:
        raise ValueError("That username is already taken.")
    return user_id


def login(username, password):
    """Returns the user id if the credentials are right, otherwise None."""
    rows = fetch_all("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    if rows and verify_password(password, rows[0][1]):
        return rows[0][0]
    return None
