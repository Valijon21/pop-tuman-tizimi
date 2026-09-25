import json
import os
import shutil
import time
import uuid
from typing import List, Dict, Any, Optional

from core.config import (
    DB_FILE, SQLITE_DB_FILE, TRASH_FILE, BACKUP_DIR, LOG_FILE, SETTINGS_FILE,
    CATEGORIES_FILE, DEFAULT_CATEGORIES
)
from core.logger import logger
from core.security import hash_password
from database.sqlite_manager import SQLiteManager

class DataManager:
    """Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-sync)."""

    def __init__(
        self,
        db_file: Optional[str] = None,
        trash_file: Optional[str] = None,
        categories_file: Optional[str] = None,
        log_file: Optional[str] = None,
        settings_file: Optional[str] = None,
        backup_dir: Optional[str] = None,
        sqlite_file: Optional[str] = None
    ):
        self.db_file = db_file or DB_FILE
        self.sqlite_file = sqlite_file or SQLITE_DB_FILE
        self.trash_file = trash_file or TRASH_FILE
        self.categories_file = categories_file or CATEGORIES_FILE
        self.log_file = log_file or LOG_FILE
        self.settings_file = settings_file or SETTINGS_FILE
        self.backup_dir = backup_dir or BACKUP_DIR

        self.ensure_backup_dir()

        # SQLite menejerini ishga tushirish
        self.sqlite = SQLiteManager(self.sqlite_file)

        # Agar baza fayli ushbu papkada topilmasa yoki bo'sh bo'lsa (masalan, EXE ichidan ishga tushganda),
        # loyiha asosiy papkalaridan qidirib ko'ramiz
        if not os.path.exists(self.db_file) or os.path.getsize(self.db_file) < 10:
            candidate_dirs = [
                os.path.dirname(self.db_file),
                os.path.join(os.path.dirname(self.db_file), ".."),
                os.path.join(os.path.dirname(self.db_file), "..", ".."),
                os.getcwd()
            ]
            for c_dir in candidate_dirs:
                c_db = os.path.abspath(os.path.join(c_dir, "mahalla_bazasi.json"))
                if os.path.exists(c_db) and os.path.getsize(c_db) > 10:
                    try:
                        shutil.copy2(c_db, self.db_file)
                        logger.info(f"[TIKLASH] Asosiy baza topildi va nusxalandi: {c_db} -> {self.db_file}")
                        break
                    except Exception as e:
                        logger.warning(f"Baza nusxalashda xatolik: {e}")

        self.data: List[Dict[str, Any]] = self.load_json(self.db_file)

        # Agar hali ham bo'sh bo'lsa, zaxiradan yoki kandidatlardan tekshirib tiklash
        if not self.data:
            candidate_dirs = [
                os.path.dirname(self.db_file),
                os.path.join(os.path.dirname(self.db_file), ".."),
                os.path.join(os.path.dirname(self.db_file), "..", ".."),
                os.getcwd()
            ]
            for c_dir in candidate_dirs:
                c_db = os.path.abspath(os.path.join(c_dir, "mahalla_bazasi.json"))
                if os.path.exists(c_db) and os.path.getsize(c_db) > 10:
                    cand_data = self.load_json(c_db)
                    if cand_data:
                        self.data = cand_data
                        self.save_data()
                        logger.info(f"[TIKLASH] Baza {c_db} dan {len(self.data)} ta yozuv bilan qayta yuklandi.")
                        break
        self.trash: List[Dict[str, Any]] = self.load_json(self.trash_file)
        self.categories: List[str] = self.load_json(self.categories_file)
        self.activity_log: List[Dict[str, Any]] = self.load_json(self.log_file)
        self.settings: Dict[str, Any] = self.load_json(self.settings_file)

        # Standart sozlamalar
        if not isinstance(self.settings, dict):
            self.settings = {}

        if "font_size" not in self.settings:
            self.settings["font_size"] = 15

        # Standart parollar (Admin: 123, Operator: 1)
        if "passwords" not in self.settings:
            self.settings["passwords"] = {
                "admin": hash_password("123"),
                "operator": hash_password("1")
            }
            self.save_settings()

        # Standart toifalar
        if not self.categories:
            self.categories = list(DEFAULT_CATEGORIES)
            self.save_categories()

        # Har bir yozuvda unikal UUID bo'lishini kafolatlash
        has_new_ids = False
        for item in self.data:
            if not item.get("id"):
                item["id"] = item.get("uuid") or str(uuid.uuid4())
                has_new_ids = True

        for item in self.trash:
            if not item.get("id"):
                item["id"] = item.get("uuid") or str(uuid.uuid4())

        if has_new_ids:
            self.save_data()

        # SQLite bazasini tekshirish va sinxronlash
        if self.data:
            self.sqlite.seed_from_json_if_empty(self.db_file)
        else:
            sqlite_data = self.sqlite.get_all_organizations()
            if sqlite_data:
                self.data = sqlite_data
                self.save_json(self.db_file, self.data)
                logger.info(f"[SQLITE TIKLASH] {len(self.data)} ta tashkilot SQLite omboridan yuklandi.")

    def ensure_backup_dir(self) -> None:
        """Zaxira nusxalar papkasi mavjudligini ta'minlash."""
        if not os.path.exists(self.backup_dir):
            try:
                os.makedirs(self.backup_dir, exist_ok=True)
            except Exception as e:
                logger.error(f"Zaxira papkasini yaratishda xatolik: {e}")

    def load_json(self, filepath: str) -> Any:
        """Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)."""
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Fayl o'qishda xatolik ({filepath}): {e}")
                # Asosiy baza buzilgan bo'lsa, zaxiradan tiklashga urinish
                if filepath == self.db_file and os.path.exists(self.backup_dir):
                    backups = sorted([os.path.join(self.backup_dir, f) for f in os.listdir(self.backup_dir) if f.endswith(".json")])
                    if backups:
                        try:
                            latest_b = backups[-1]
                            logger.warning(f"Zaxira nusxadan tiklanmoqda: {latest_b}")
                            with open(latest_b, "r", encoding="utf-8") as bf:
                                return json.load(bf)
                        except Exception as be:
                            logger.error(f"Zaxiradan tiklash amalga oshmadi: {be}")
                return [] if filepath != self.settings_file else {}
        return [] if filepath != self.settings_file else {}

    def save_json(self, filepath: str, data: Any) -> None:
        """Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiriladi."""
        temp_file = f"{filepath}.tmp"
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            os.replace(temp_file, filepath)
            logger.debug(f"[SAQLANDI] Atomik yozish muvaffaqiyatli: {filepath} ({len(data) if isinstance(data, (list, dict)) else 'N/A'} ta element)")
        except Exception as e:
            logger.error(f"[XATO] Faylni atomik saqlashda xatolik ({filepath}): {e}")
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass

    def load_data(self) -> List[Dict[str, Any]]:
        """Baza ma'lumotlarini (SQLite yoki JSON) qayta yuklash."""
        sqlite_data = self.sqlite.get_all_organizations()
        if sqlite_data:
            self.data = sqlite_data
        else:
            self.data = self.load_json(self.db_file)
        return self.data

    def add_organization(self, item: Any, user: Optional[str] = "ADMIN") -> Dict[str, Any]:
        """Yangi tashkilot qo'shish (dict yoki Organization modeli qabul qiladi)."""
        if hasattr(item, "to_dict"):
            item = item.to_dict()
        else:
            item = dict(item)

        if not item.get("id"):
            item["id"] = str(uuid.uuid4())
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        if not item.get("updated_at"):
            item["updated_at"] = now

        self.data.append(item)
        self.save_data()
        self.log_activity(user, "Qo'shish", f"Yangi tashkilot: '{item.get('m')}' (INN: {item.get('inn', '-')})")
        logger.info(f"[QO'SHISH] Yangi tashkilot qo'shildi: {item.get('m')} (ID={item.get('id')})")
        return item

    def update_organization(self, item: Any, user: Optional[str] = "ADMIN") -> bool:
        """Mavjud tashkilot ma'lumotlarini yangilash (dict yoki Organization modeli qabul qiladi)."""
        if hasattr(item, "to_dict"):
            item = item.to_dict()
        else:
            item = dict(item)

        target_id = str(item.get("id") or "")
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        item["updated_at"] = now

        found_idx = -1
        if target_id:
            for idx, existing in enumerate(self.data):
                if str(existing.get("id")) == target_id:
                    found_idx = idx
                    break

        if found_idx >= 0:
            self.data[found_idx].update(item)
            self.save_data()
            self.log_activity(user, "Tahrirlash", f"Tashkilot yangilandi: '{item.get('m')}' (INN: {item.get('inn', '-')})")
            logger.info(f"[TAHRIRLASH] Tashkilot yangilandi: {item.get('m')} (ID={target_id})")
            return True
        else:
            self.add_organization(item, user=user)
            return True

    def get_organization_model(self, org_id: str) -> Optional[Any]:
        """Tashkilotni Organization dataclass modeli sifatida olish."""
        from database.models import Organization
        for item in self.data:
            if str(item.get("id")) == str(org_id):
                return Organization.from_dict(item)
        return None

    def save_data(self) -> None:
        self.save_json(self.db_file, self.data)
        try:
            self.sqlite.save_all_organizations(self.data)
        except Exception as e:
            logger.error(f"[SQLITE SAQLASH XATOSI] {e}")

    def save_trash(self) -> None:
        self.save_json(self.trash_file, self.trash)
        try:
            self.sqlite.save_all_trash(self.trash)
        except Exception as e:
            logger.error(f"[SQLITE CHIQINDI SAQLASH XATOSI] {e}")

    def save_categories(self) -> None:
        self.save_json(self.categories_file, self.categories)

    def add_category(self, category_name: str) -> bool:
        """Yangi toifa qo'shish va saqlash."""
        cat = category_name.strip()
        if not cat:
            return False
        if not hasattr(self, "categories") or self.categories is None:
            self.categories = []
        if cat not in self.categories:
            self.categories.append(cat)
            self.save_categories()
            logger.info(f"[TOIFA] Yangi toifa qo'shildi: {cat}")
            return True
        return False

    def save_settings(self) -> None:
        self.save_json(self.settings_file, self.settings)

    def log_activity(self, user: Optional[str], action: str, details: str) -> None:
        """Tizimdagi harakatlarni qayd etish (JSON + SQLite)."""
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            entry = {
                "time": timestamp,
                "user": user or "Tizim",
                "action": action,
                "details": details
            }
            self.activity_log.insert(0, entry)
            if len(self.activity_log) > 1000:
                self.activity_log.pop()
            self.save_json(self.log_file, self.activity_log)
            self.sqlite.log_activity(user or "Tizim", action, details)
            logger.info(f"[AUDIT] Foydalanuvchi: {user} | Amal: {action} | Tafsilot: {details}")
        except Exception as e:
            logger.error(f"Audit log yozishda xatolik: {e}")

    def add_staff_history(
        self, org_id: str, mahalla: str, role: str, full_name: str,
        phone: str = "", inn: str = "", jshr: str = "", seriya: str = "", note: str = ""
    ) -> None:
        """Xodim rotatsiyasi/almashinuvini qayd etish."""
        self.sqlite.add_staff_history(org_id, mahalla, role, full_name, phone, inn, jshr, seriya, note)

    def get_staff_history(self, org_id: Optional[str] = None, mahalla: Optional[str] = None) -> List[Dict[str, Any]]:
        """Xodimlar rotatsiyasi tarixini olish."""
        return self.sqlite.get_staff_history(org_id, mahalla)

    def move_to_trash(self, item: Dict[str, Any]) -> bool:
        """Yozuvni Chiqindi qutisiga ko'chirish."""
        target_id = item.get("id")
        target = next((x for x in self.data if x.get("id") and x.get("id") == target_id), None) if target_id else (item if item in self.data else None)
        if target:
            self.data.remove(target)
            target["deleted_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            self.trash.append(target)
            if target_id:
                try:
                    self.sqlite.delete_organization(str(target_id))
                except Exception as e:
                    logger.error(f"[SQLITE XATO] delete_organization: {e}")
            self.save_data()
            self.save_trash()
            logger.info(f"[CHIQINDI] Yozuv chiqindiga ko'chirildi: ID={target_id}, Nomi='{target.get('m')}'")
            return True
        logger.warning(f"[CHIQINDI] O'chirish uchun yozuv topilmadi: ID={target_id}")
        return False

    def restore_from_trash(self, item: Dict[str, Any]) -> bool:
        """Chiqindi qutisidan asosiy bazaga tiklash."""
        target_id = item.get("id")
        target = next((x for x in self.trash if x.get("id") and x.get("id") == target_id), None) if target_id else (item if item in self.trash else None)
        if target:
            self.trash.remove(target)
            if "deleted_at" in target:
                del target["deleted_at"]
            self.data.append(target)
            if target_id:
                try:
                    self.sqlite.delete_trash_item(str(target_id))
                except Exception as e:
                    logger.error(f"[SQLITE XATO] delete_trash_item: {e}")
            self.save_data()
            self.save_trash()
            logger.info(f"[TIKLASH] Yozuv bazaga tiklandi: ID={target_id}, Nomi='{target.get('m')}'")
            return True
        logger.warning(f"[TIKLASH] Tiklash uchun yozuv topilmadi: ID={target_id}")
        return False

    def permanent_delete(self, item: Dict[str, Any]) -> bool:
        """Chiqindi qutisidan butunlay o'chirish."""
        target_id = item.get("id")
        target = next((x for x in self.trash if x.get("id") and x.get("id") == target_id), None) if target_id else (item if item in self.trash else None)
        if target:
            self.trash.remove(target)
            if target_id:
                try:
                    self.sqlite.delete_trash_item(str(target_id))
                except Exception as e:
                    logger.error(f"[SQLITE XATO] delete_trash_item: {e}")
            self.save_trash()
            logger.info(f"[BUTUNLAY O'CHIRISH] Yozuv bazadan to'liq o'chirildi: ID={target_id}, Nomi='{target.get('m')}'")
            return True
        logger.warning(f"[BUTUNLAY O'CHIRISH] O'chirish uchun yozuv topilmadi: ID={target_id}")
        return False

    def backup_data(self) -> Dict[str, str]:
        """Ma'lumotlar bazasining zaxira nusxasini yaratish (oxirgi 10 ta JSON va 30 ta SQLite)."""
        res = {"json": "", "db": "", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
        if os.path.exists(self.db_file):
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}.json")
            try:
                shutil.copy2(self.db_file, backup_path)
                backups = sorted([os.path.join(self.backup_dir, f) for f in os.listdir(self.backup_dir) if f.endswith(".json")])
                logger.info(f"[ZAXIRA] Baza zaxiralandi: {backup_path} (Jami zaxiralar: {len(backups)})")
                while len(backups) > 10:
                    old_b = backups.pop(0)
                    os.remove(old_b)
                    logger.debug(f"[ZAXIRA] Eski zaxira tozalandi: {old_b}")
                res["json"] = backup_path
            except Exception as e:
                logger.error(f"[XATO] Zaxira olishda xatolik: {e}")

        # SQLite bazasini ham zaxiralash
        try:
            db_bak = self.sqlite.backup_database(self.backup_dir)
            if db_bak:
                res["db"] = db_bak
        except Exception as e:
            logger.error(f"[XATO] SQLite zaxira olishda xatolik: {e}")
        return res
