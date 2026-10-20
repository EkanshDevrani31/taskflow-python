"""Run with:  python -m unittest discover tests   (no database needed)."""
import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import security
import validators as v


class PasswordTests(unittest.TestCase):
    def test_correct_password_verifies(self):
        stored = security.hash_password("secret123")
        self.assertTrue(security.verify_password("secret123", stored))

    def test_wrong_password_fails(self):
        stored = security.hash_password("secret123")
        self.assertFalse(security.verify_password("wrong", stored))

    def test_same_password_gets_different_hashes(self):
        self.assertNotEqual(security.hash_password("abc123"), security.hash_password("abc123"))

    def test_plain_text_is_not_stored(self):
        self.assertNotIn("secret123", security.hash_password("secret123"))

    def test_garbage_hash_is_rejected(self):
        self.assertFalse(security.verify_password("x", "not-a-valid-hash"))


class ValidatorTests(unittest.TestCase):
    def test_priority(self):
        self.assertEqual(v.parse_priority("3"), "high")
        self.assertEqual(v.parse_priority(""), "medium")
        self.assertEqual(v.parse_priority("LOW"), "low")
        with self.assertRaises(ValueError):
            v.parse_priority("9")

    def test_due_date(self):
        self.assertEqual(v.parse_due_date("2026-11-05"), date(2026, 11, 5))
        self.assertIsNone(v.parse_due_date(""))
        with self.assertRaises(ValueError):
            v.parse_due_date("05-11-2026")

    def test_title(self):
        with self.assertRaises(ValueError):
            v.parse_title("   ")
        with self.assertRaises(ValueError):
            v.parse_title("x" * 121)

    def test_username_and_password(self):
        self.assertEqual(v.parse_username("ekansh_1"), "ekansh_1")
        with self.assertRaises(ValueError):
            v.parse_username("a b")
        with self.assertRaises(ValueError):
            v.parse_password("123")


if __name__ == "__main__":
    unittest.main()
