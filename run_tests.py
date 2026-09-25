"""
Pop Tuman Tashkilotlari va INN Tizimi (PRO)
Avtomatlashtirilgan testlarni ishga tushirish (Test Runner)
"""
import unittest
import sys
import os

# Windows konsolida UTF-8 ni to'g'ri ishlashini ta'minlash
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Loyiha papkasini yo'lga qo'shish
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Test muhiti sozlamalari
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["TESTING"] = "1"

def run_all_tests():
    print("=" * 60)
    print("[TEST] POP TUMAN TIZIMI: AVTOMATLASHTIRILGAN TESTLAR BOSHLANDI")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.join(BASE_DIR, "tests"), pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print(f"[OK] BARCHA TESTLAR MUVAFFAQIYATLI O'TDI! ({result.testsRun} ta test)")
        print("=" * 60)
        return 0
    else:
        print(f"[FAIL] XATOLIKLAR MAVJUD! ({len(result.failures)} ta failure, {len(result.errors)} ta error)")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
