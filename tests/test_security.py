import unittest
from core.security import hash_password, authenticate_user

class TestSecurity(unittest.TestCase):
    """Xavfsizlik va parollarni tekshirish testlari."""

    def test_hash_password(self):
        h1 = hash_password("123")
        h2 = hash_password("123")
        self.assertEqual(h1, h2)
        # SHA-256 xesh uzunligi 64 ta belgidan iborat
        self.assertEqual(len(h1), 64)
        # Boshqa parol boshqa xesh berishi kerak
        self.assertNotEqual(hash_password("123"), hash_password("1234"))

    def test_authenticate_user(self):
        admin_hash = hash_password("admin_secret")
        operator_hash = hash_password("op_secret")
        stored = {
            "admin": admin_hash,
            "operator": operator_hash
        }

        # To'g'ri parollar
        self.assertEqual(authenticate_user("admin_secret", stored), "admin")
        self.assertEqual(authenticate_user("op_secret", stored), "operator")

        # Noto'g'ri parol
        self.assertIsNone(authenticate_user("wrong_password", stored))
        self.assertIsNone(authenticate_user("", stored))

if __name__ == "__main__":
    unittest.main()
