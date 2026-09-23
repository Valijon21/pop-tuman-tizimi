from typing import List, Dict, Any
import openpyxl
from openpyxl.styles import Font, PatternFill

def export_organizations_to_excel(data: List[Dict[str, Any]], filepath: str, category_name: str = "Barchasi") -> int:
    """Tashkilotlar ro'yxatini zamonaviy formatlangan Excel (.xlsx) fayliga yuklash."""
    wb = openpyxl.Workbook()
    ws = wb.active
    
    # Sheet nomi (maksimal 31 belgi)
    sheet_title = f"Tashkilotlar - {category_name}"[:31]
    ws.title = sheet_title

    # Sarlavhalar
    headers = ["Turi", "Nomi", "Rahbar", "Tel", "INN", "Izoh"]
    ws.append(headers)

    # Sarlavha dizayni
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="2c3e50", end_color="2c3e50", fill_type="solid")

    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill

    # Ma'lumotlarni yozish
    for item in data:
        ws.append([
            item.get("s") or "",
            item.get("m") or "",
            item.get("f") or "",
            item.get("t") or "",
            str(item.get("inn") or ""),
            item.get("izoh") or ""
        ])

    # Ustun kengliklarini moslash
    for col in ws.columns:
        max_len = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                val_str = str(cell.value or "")
                if len(val_str) > max_len:
                    max_len = len(val_str)
            except Exception:
                pass
        ws.column_dimensions[col_letter].width = max(max_len + 3, 10)

    wb.save(filepath)
    return len(data)
