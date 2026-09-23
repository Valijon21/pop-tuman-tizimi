"""
Pop Tuman Tashkilotlari va INN Tizimi
SQLite Tranzaksiyaviy Ma'lumotlar Bazasi Drayveri (SQLite Database Manager)
ACID kafolati, yuqori tezlik (WAL rejimi) va to'liq audit jurnali.
"""
import sqlite3
import os
import shutil
import time
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from core.logger import logger

class SQLiteManager:
    """SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_schema()

    def get_connection(self) -> sqlite3.Connection:
        """SQLite ulanishini olish va WAL rejimini faollashtirish."""
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def init_schema(self) -> None:
        """Baza jadvallari va indekslarini yaratish."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 1. Asosiy tashkilotlar jadvali
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS organizations (
                    id TEXT PRIMARY KEY,
                    s TEXT,
                    m TEXT,
                    f TEXT,
                    t TEXT,
                    inn TEXT,
                    izoh TEXT,
                    jshr TEXT,
                    seriya TEXT,
                    updated_at TEXT
                );
                """)
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_org_inn ON organizations(inn);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_org_m ON organizations(m);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_org_s ON organizations(s);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_org_f ON organizations(f);")

                # 2. Chiqindi qutisi (Trash) jadvali
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS trash (
                    id TEXT PRIMARY KEY,
                    s TEXT,
                    m TEXT,
                    f TEXT,
                    t TEXT,
                    inn TEXT,
                    izoh TEXT,
                    jshr TEXT,
                    seriya TEXT,
                    deleted_at TEXT
                );
                """)

                # 3. Xodimlar rotatsiyasi va kadrlar tarixi jadvali
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS staff_history (
                    id TEXT PRIMARY KEY,
                    org_id TEXT,
                    mahalla TEXT,
                    role TEXT,
                    full_name TEXT,
                    phone TEXT,
                    inn TEXT,
                    jshr TEXT,
                    seriya TEXT,
                    change_date TEXT,
                    note TEXT
                );
                """)
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_org ON staff_history(org_id);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_mahalla ON staff_history(mahalla);")

                # 4. Tizim harakatlari jurnali (Activity Log)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT,
                    action TEXT,
                    details TEXT,
                    timestamp TEXT
                );
                """)

                # 5. Sozlamalar jadvali
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                );
                """)

                # 6. Toifalar jadvali
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    name TEXT PRIMARY KEY,
                    sort_order INTEGER DEFAULT 0
                );
                """)
                conn.commit()
                logger.info(f"[SQLITE] Baza sxemasi tekshirildi/yaratildi: {self.db_path}")
        except Exception as e:
            logger.error(f"[SQLITE] Sxemani yaratishda xatolik: {e}")

    # ==================== ORGANIZATIONS ====================

    def get_all_organizations(self) -> List[Dict[str, Any]]:
        """Barcha faol tashkilotlarni ro'yxat ko'rinishida olish."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM organizations ORDER BY rowid ASC")
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"[SQLITE] Tashkilotlarni o'qishda xatolik: {e}")
            return []

    def save_all_organizations(self, orgs: List[Dict[str, Any]]) -> None:
        """Barcha tashkilotlarni atomik tranzaksiya bilan to'liq saqlash/yangilash."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM organizations;")
                cursor.executemany("""
                INSERT INTO organizations (id, s, m, f, t, inn, izoh, jshr, seriya, updated_at)
                VALUES (:id, :s, :m, :f, :t, :inn, :izoh, :jshr, :seriya, :updated_at);
                """, [
                    {
                        "id": str(o.get("id") or o.get("uuid") or ""),
                        "s": str(o.get("s") or ""),
                        "m": str(o.get("m") or ""),
                        "f": str(o.get("f") or ""),
                        "t": str(o.get("t") or ""),
                        "inn": str(o.get("inn") or ""),
                        "izoh": str(o.get("izoh") or ""),
                        "jshr": str(o.get("jshr") or ""),
                        "seriya": str(o.get("seriya") or ""),
                        "updated_at": o.get("updated_at") or now
                    } for o in orgs
                ])
                conn.commit()
                logger.debug(f"[SQLITE] {len(orgs)} ta tashkilot saqlandi.")
        except Exception as e:
            logger.error(f"[SQLITE] Tashkilotlarni saqlashda xatolik: {e}")

    def insert_or_replace_organization(self, o: Dict[str, Any]) -> None:
        """Bitta tashkilotni qo'shish yoki yangilash."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT OR REPLACE INTO organizations (id, s, m, f, t, inn, izoh, jshr, seriya, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    str(o.get("id") or o.get("uuid") or ""),
                    str(o.get("s") or ""),
                    str(o.get("m") or ""),
                    str(o.get("f") or ""),
                    str(o.get("t") or ""),
                    str(o.get("inn") or ""),
                    str(o.get("izoh") or ""),
                    str(o.get("jshr") or ""),
                    str(o.get("seriya") or ""),
                    now
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"[SQLITE] Tashkilotni yozishda xatolik: {e}")

    def upsert_organization(self, o: Dict[str, Any]) -> None:
        """Bitta tashkilotni qo'shish yoki yangilash (Alias)."""
        self.insert_or_replace_organization(o)

    def bulk_insert_organizations(self, orgs: List[Dict[str, Any]]) -> int:
        """Ommaviy tashkilotlarni saqlash va sonini qaytarish."""
        self.save_all_organizations(orgs)
        return len(orgs)

    def get_organization_by_id(self, org_id: str) -> Optional[Dict[str, Any]]:
        """Tashkilotni unikal ID si bo'yicha olish."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM organizations WHERE id = ? LIMIT 1;", (str(org_id),))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"[SQLITE] ID bo'yicha qidirishda xatolik: {e}")
            return None

    def get_organization_by_inn(self, inn: str) -> Optional[Dict[str, Any]]:
        """Tashkilotni INN si bo'yicha olish."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM organizations WHERE inn = ? LIMIT 1;", (str(inn),))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"[SQLITE] INN bo'yicha qidirishda xatolik: {e}")
            return None

    def delete_organization(self, org_id: str) -> None:
        """Tashkilotni ID bo'yicha o'chirish."""
        try:
            with self.get_connection() as conn:
                conn.execute("DELETE FROM organizations WHERE id = ?;", (str(org_id),))
                conn.commit()
        except Exception as e:
            logger.error(f"[SQLITE] Tashkilotni o'chirishda xatolik ({org_id}): {e}")

    # ==================== TRASH ====================

    def get_all_trash(self) -> List[Dict[str, Any]]:
        """Chiqindi qutisidagi barcha yozuvlarni olish."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM trash ORDER BY rowid DESC")
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"[SQLITE] Chiqindini o'qishda xatolik: {e}")
            return []

    def save_all_trash(self, trash_items: List[Dict[str, Any]]) -> None:
        """Chiqindi qutisini to'liq saqlash."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM trash;")
                cursor.executemany("""
                INSERT INTO trash (id, s, m, f, t, inn, izoh, jshr, seriya, deleted_at)
                VALUES (:id, :s, :m, :f, :t, :inn, :izoh, :jshr, :seriya, :deleted_at);
                """, [
                    {
                        "id": str(o.get("id") or o.get("uuid") or ""),
                        "s": str(o.get("s") or ""),
                        "m": str(o.get("m") or ""),
                        "f": str(o.get("f") or ""),
                        "t": str(o.get("t") or ""),
                        "inn": str(o.get("inn") or ""),
                        "izoh": str(o.get("izoh") or ""),
                        "jshr": str(o.get("jshr") or ""),
                        "seriya": str(o.get("seriya") or ""),
                        "deleted_at": str(o.get("deleted_at") or "")
                    } for o in trash_items
                ])
                conn.commit()
        except Exception as e:
            logger.error(f"[SQLITE] Chiqindini saqlashda xatolik: {e}")

    # ==================== STAFF HISTORY (KADRLAR TARIXI) ====================

    def add_staff_history(
        self,
        org_id: str = "",
        mahalla: str = "",
        role: str = "",
        full_name: str = "",
        phone: str = "",
        inn: str = "",
        jshr: str = "",
        seriya: str = "",
        note: str = "",
        old_fio: str = "",
        new_fio: str = "",
        old_phone: str = "",
        new_phone: str = "",
        changed_by: str = "",
        reason: str = "",
        org_name: str = ""
    ) -> None:
        """Xodim rotatsiyasi/almashinuvini tarix jadvaliga qo'shish (ko'p qirrali parametrlar bilan)."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        import uuid
        hist_id = str(uuid.uuid4())
        
        target_name = new_fio or full_name
        target_mahalla = mahalla or org_name
        target_phone = new_phone or phone
        
        note_parts = []
        if old_fio: note_parts.append(f"Sobiq: {old_fio}")
        if old_phone: note_parts.append(f"Eski tel: {old_phone}")
        if reason: note_parts.append(f"Sabab: {reason}")
        if changed_by: note_parts.append(f"Mas'ul: {changed_by}")
        if note: note_parts.append(note)
        full_note = " | ".join(note_parts)

        try:
            with self.get_connection() as conn:
                conn.execute("""
                INSERT INTO staff_history (id, org_id, mahalla, role, full_name, phone, inn, jshr, seriya, change_date, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (hist_id, org_id, target_mahalla, role, target_name, target_phone, inn, jshr, seriya, now, full_note))
                conn.commit()
                logger.info(f"[KADR TARIXI] Xodim tarixi yozildi: {target_mahalla} - {role} ({target_name})")
        except Exception as e:
            logger.error(f"[KADR TARIXI] Xodim tarixini saqlashda xatolik: {e}")

    def get_staff_history(self, org_id: Optional[str] = None, mahalla: Optional[str] = None) -> List[Dict[str, Any]]:
        """Xodimlar tarixini olish (tashkilot yoki mahalla bo'yicha)."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if org_id:
                    cursor.execute("SELECT * FROM staff_history WHERE org_id = ? ORDER BY change_date DESC", (org_id,))
                elif mahalla:
                    cursor.execute("SELECT * FROM staff_history WHERE mahalla LIKE ? ORDER BY change_date DESC", (f"%{mahalla}%",))
                else:
                    cursor.execute("SELECT * FROM staff_history ORDER BY change_date DESC LIMIT 200")
                
                rows = cursor.fetchall()
                results = []
                for row in rows:
                    d = dict(row)
                    # Parsing old_fio, new_fio, changed_by from note or fields for backward compatibility
                    d["new_fio"] = d.get("full_name", "")
                    note_str = d.get("note", "")
                    if "Sobiq: " in note_str:
                        part = note_str.split("Sobiq: ")[1].split(" | ")[0]
                        d["old_fio"] = part
                    else:
                        d["old_fio"] = ""
                    if "Mas'ul: " in note_str:
                        d["changed_by"] = note_str.split("Mas'ul: ")[1].split(" | ")[0]
                    else:
                        d["changed_by"] = "admin"
                    results.append(d)
                return results
        except Exception as e:
            logger.error(f"[KADR TARIXI] Tarixni olishda xatolik: {e}")
            return []

    # ==================== ACTIVITY LOG ====================

    def log_activity(self, user: str, action: str, details: str) -> None:
        """Tizimdagi harakatni SQLite jurnaliga qayd etish."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.get_connection() as conn:
                conn.execute("""
                INSERT INTO activity_log (user, action, details, timestamp)
                VALUES (?, ?, ?, ?);
                """, (user, action, details, now))
                conn.commit()
        except Exception as e:
            logger.error(f"[SQLITE LOG] Harakatni yozishda xatolik: {e}")

    def get_recent_activity(self, limit: int = 50) -> List[Dict[str, Any]]:
        """So'nggi faoliyat jurnallarini olish."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT user, action, details, timestamp as time FROM activity_log ORDER BY id DESC LIMIT ?", (limit,))
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"[SQLITE LOG] Jurnalni o'qishda xatolik: {e}")
            return []

    # ==================== SEED / MIGRATION ====================

    def seed_from_json_if_empty(self, json_filepath: str) -> int:
        """Agar SQLite jadvali bo'sh bo'lsa, JSON fayldan barcha yozuvlarni avtomatik ko'chirish."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM organizations;")
                count = cursor.fetchone()[0]
                if count > 0:
                    return count
                
                if not os.path.exists(json_filepath) or os.path.getsize(json_filepath) < 10:
                    return 0

                with open(json_filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if not isinstance(data, list) or len(data) == 0:
                    return 0

                self.save_all_organizations(data)
                logger.info(f"[MIGRATSIYA] {len(data)} ta tashkilot {json_filepath} dan SQLite bazasiga ko'chirildi!")
                return len(data)
        except Exception as e:
            logger.error(f"[MIGRATSIYA] JSON dan SQLite ga migratsiyada xatolik: {e}")
            return 0

    def backup_database(self, backup_dir: Optional[str] = None) -> str:
        """SQLite bazasini vaqt tamg'asi bilan zaxiralash."""
        if not backup_dir:
            backup_dir = os.path.join(os.path.dirname(self.db_path), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.db")
        try:
            with self.get_connection() as src_conn:
                with sqlite3.connect(backup_file) as dst_conn:
                    src_conn.backup(dst_conn)
            logger.info(f"[ZAXIRA] SQLite zaxira nusxasi olindi: {backup_file}")
            
            # 30 tadan ortiq zaxiralarni tozalash
            all_baks = sorted([os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.endswith(".db")])
            if len(all_baks) > 30:
                for old_bak in all_baks[:-30]:
                    try: os.remove(old_bak)
                    except Exception: pass

            return backup_file
        except Exception as e:
            logger.error(f"[ZAXIRA] SQLite zaxiralashda xatolik: {e}")
            return ""
