import os
import re
import uuid
from typing import List, Dict, Any, Tuple
import gspread

from core.logger import logger

def extract_sheet_id(val: str) -> str:
    """URL yoki matndan Google Sheet ID sini ajratib olish."""
    val = val.strip()
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", val)
    if match:
        return match.group(1)
    if len(val) > 20 and " " not in val and not val.startswith("http"):
        return val
    return val

def is_service_account_available(service_account_path: str = "") -> bool:
    """Service account kalit fayli mavjud va to'g'ri ekanligini tekshirish."""
    from core.config import SERVICE_ACCOUNT_FILE
    path = service_account_path or SERVICE_ACCOUNT_FILE
    return bool(path and os.path.isfile(path) and os.path.getsize(path) > 50)

def get_gspread_client(service_account_path: str) -> gspread.Client:
    """Google Sheets klientini yaratish (zamonaviy google-auth yoki oauth2client orqali)."""
    if not os.path.exists(service_account_path):
        raise FileNotFoundError(f"Google Cloud service account kalit fayli topilmadi:\n{service_account_path}")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # 1. Zamonaviy google.oauth2 kutubxonasini sinab ko'rish
    try:
        from google.oauth2.service_account import Credentials
        creds = Credentials.from_service_account_file(service_account_path, scopes=scope)
        return gspread.authorize(creds)
    except (ImportError, Exception):
        # 2. Eskiroq oauth2client bilan fallback
        from oauth2client.service_account import ServiceAccountCredentials
        creds = ServiceAccountCredentials.from_json_keyfile_name(service_account_path, scope)
        return gspread.authorize(creds)

def open_spreadsheet(client: gspread.Client, sheet_identifier: str) -> gspread.Spreadsheet:
    """ID, URL yoki nom orqali jadvalni ochish."""
    val = sheet_identifier.strip()
    sheet_id = extract_sheet_id(val)
    
    if "/" not in sheet_id and len(sheet_id) > 20:
        return client.open_by_key(sheet_id)
    elif val.startswith("http"):
        return client.open_by_url(val)
    else:
        return client.open(val)

def upload_data_to_sheet(client: gspread.Client, sheet_identifier: str, data: List[Dict[str, Any]]) -> str:
    """Ma'lumotlar ro'yxatini Google Sheetga yuklash (to'liq 13 ta ustun bilan)."""
    spreadsheet = open_spreadsheet(client, sheet_identifier)
    sheet = spreadsheet.sheet1

    headers = [
        "Turi", "Nomi", "Rahbar", "Tel", "INN",
        "Buxgalter Tel", "Apparat Soni", "Ulangan Soni",
        "JSHSHIR", "Pasport Seriya", "Lavozim", "Izoh", "ID"
    ]
    data_to_upload = [headers]
    for i in data:
        data_to_upload.append([
            i.get("s", ""),
            i.get("m", ""),
            i.get("f", ""),
            i.get("t", ""),
            str(i.get("inn", "")),
            str(i.get("bux_tel", "")),
            str(i.get("aparat_soni", "")),
            str(i.get("ulangan_soni", "")),
            str(i.get("jshr", "")),
            str(i.get("seriya", "")),
            str(i.get("lavozim", "")),
            i.get("izoh", ""),
            i.get("id") or i.get("uuid", "")
        ])

    sheet.clear()
    sheet.update(data_to_upload)
    return spreadsheet.id

def download_data_from_sheet(client: gspread.Client, sheet_identifier: str) -> List[Dict[str, Any]]:
    """Google Sheetdan ma'lumotlarni o'qib olish (to'liq 13 ta ustunni qo'llab-quvvatlaydi)."""
    spreadsheet = open_spreadsheet(client, sheet_identifier)
    sheet = spreadsheet.sheet1
    raw_data = sheet.get_all_records()

    new_db = []
    for row in raw_data:
        row_id = str(row.get("ID") or uuid.uuid4())
        new_db.append({
            "id": row_id,
            "s": str(row.get("Turi", "")),
            "m": str(row.get("Nomi", "")),
            "f": str(row.get("Rahbar", "")),
            "t": str(row.get("Tel", "")),
            "inn": str(row.get("INN", "")),
            "bux_tel": str(row.get("Buxgalter Tel", "") or row.get("bux_tel", "")),
            "aparat_soni": str(row.get("Apparat Soni", "") or row.get("aparat_soni", "")),
            "ulangan_soni": str(row.get("Ulangan Soni", "") or row.get("ulangan_soni", "")),
            "jshr": str(row.get("JSHSHIR", "") or row.get("jshr", "")),
            "seriya": str(row.get("Pasport Seriya", "") or row.get("seriya", "")),
            "lavozim": str(row.get("Lavozim", "") or row.get("lavozim", "")),
            "izoh": str(row.get("Izoh", ""))
        })
    return new_db
