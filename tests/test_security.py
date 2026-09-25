import unittest
from core.security import (
    hash_password, hash_password_salted, verify_password,
    authenticate_user, is_rate_limited, reset_failed_attempts,
    record_failed_attempt, verify_action_password, DEFAULT_PASSWORDS
)

class TestSecurity(unittest.TestCase):
    """Xavfsizlik va parollarni tekshirish testlari."""

    def setUp(self):
        reset_failed_attempts("test_user")
        reset_failed_attempts("global")
        reset_failed_attempts("test_action")

    def tearDown(self):
        reset_failed_attempts("test_user")
        reset_failed_attempts("global")
        reset_failed_attempts("test_action")

    def test_hash_password(self):
        h1 = hash_password("123")
        h2 = hash_password("123")
        self.assertEqual(h1, h2)
        # SHA-256 xesh uzunligi 64 ta belgidan iborat
        self.assertEqual(len(h1), 64)
        # Boshqa parol boshqa xesh berishi kerak
        self.assertNotEqual(hash_password("123"), hash_password("1234"))

    def test_pbkdf2_salted_password(self):
        salted = hash_password_salted("my_strong_pass")
        self.assertTrue(salted.startswith("pbkdf2:sha256:100000:"))
        # To'g'ri parol bilan tekshirish
        self.assertTrue(verify_password("my_strong_pass", salted))
        # Noto'g'ri parol bilan tekshirish
        self.assertFalse(verify_password("wrong_pass", salted))

    def test_authenticate_user(self):
        admin_hash = hash_password("admin_secret")
        operator_hash = hash_password("op_secret")
        stored = {
            "admin": admin_hash,
            "operator": operator_hash
        }

        # To'g'ri parollar
        self.assertEqual(authenticate_user("admin_secret", stored, identifier="test_user"), "admin")
        self.assertEqual(authenticate_user("op_secret", stored, identifier="test_user"), "operator")

        # Noto'g'ri parol
        self.assertIsNone(authenticate_user("wrong_password", stored, identifier="test_user"))
        self.assertIsNone(authenticate_user("", stored, identifier="test_user"))

    def test_verify_action_password(self):
        """Amallar bo'yicha parollarni (edit va settings) tekshirish."""
        # Standart parollar tekshiruvi
        ok, msg = verify_action_password("edit", DEFAULT_PASSWORDS["edit"], identifier="test_action")
        self.assertTrue(ok)

        ok, msg = verify_action_password("settings", DEFAULT_PASSWORDS["settings"], identifier="test_action")
        self.assertTrue(ok)

        # Noto'g'ri parol
        ok, msg = verify_action_password("edit", "noto_g_ri_parol", identifier="test_action")
        self.assertFalse(ok)
        self.assertIn("Noto'g'ri", msg)

        # Maxsus PBKDF2 hash bilan tekshirish
        custom_dict = {
            "edit": hash_password_salted("maxsus_edit_parol"),
            "settings": hash_password_salted("maxsus_settings_parol")
        }
        ok, msg = verify_action_password("edit", "maxsus_edit_parol", custom_dict, identifier="test_action")
        self.assertTrue(ok)

        ok, msg = verify_action_password("settings", "maxsus_settings_parol", custom_dict, identifier="test_action")
        self.assertTrue(ok)

    def test_brute_force_rate_limiting(self):
        stored = {"admin": hash_password("correct_admin")}
        ident = "test_brute"
        reset_failed_attempts(ident)

        # 5 marta xato kiritish
        for _ in range(5):
            self.assertIsNone(authenticate_user("bad_pwd", stored, identifier=ident))

        # Endi to'g'ri parol kiritilsa ham bloklangan bo'lishi kerak
        blocked, sec = is_rate_limited(ident)
        self.assertTrue(blocked)
        self.assertTrue(sec > 0)
        self.assertIsNone(authenticate_user("correct_admin", stored, identifier=ident))

        # Tozalangandan keyin yana kirishi mumkin
        reset_failed_attempts(ident)
        self.assertEqual(authenticate_user("correct_admin", stored, identifier=ident), "admin")

if __name__ == "__main__":
    unittest.main()
