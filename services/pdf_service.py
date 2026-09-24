"""
services.pdf_service: Pop Tuman Tashkilotlari va Mahalla Yettiligi A4 PDF Eksport Xizmati.
PyQt5 QPdfWriter va QTextDocument vositasida yuqori sifatli, chop etishga tayyor (A4 Print-Ready)
rasmiy hujjatlar va jadvallar generatsiyasi.
Tashqi og'ir kutubxonalarga (wkhtmltopdf, weasyprint va h.k.) mutlaqo ehtiyoj yo'q.
"""
import os
import io
import time
import base64
from typing import List, Dict, Any, Optional

from PyQt5.QtGui import QPdfWriter, QTextDocument, QPageSize, QPageLayout
from PyQt5.QtCore import QMarginsF
from core.logger import logger
from services.qr_service import generate_vcard_qr_image, clean_phone_number

def _image_to_base64_src(pil_image) -> str:
    """PIL tasvirni HTML <img> uchun base64 URI ga aylantirish."""
    try:
        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{b64}"
    except Exception as e:
        logger.warning(f"[PDF] QR kodni base64 ga aylantirishda xatolik: {e}")
        return ""

def export_mahalla_passport_pdf(
    mahalla_name: str,
    roles_data: List[Dict[str, Any]],
    output_path: str,
    district_name: str = "Pop tumani"
) -> bool:
    """
    Mahalla 'Yettiligi' 360° Pasportini A4 formatidagi rasmiy PDF hujjat ko'rinishida saqlash.
    
    :param mahalla_name: Mahalla fuqarolar yig'ini nomi (masalan, 'Chorkesar')
    :param roles_data: 7 ta mas'ul xodimlar ma'lumotlari ro'yxati (dict lar to'plami)
    :param output_path: Saqlanadigan PDF fayl to'liq yo'li
    :param district_name: Tuman nomi
    :return: Muvaffaqiyatli saqlansa True, aks holda False
    """
    try:
        # Chiqish papkasini ta'minlash
        out_dir = os.path.dirname(os.path.abspath(output_path))
        os.makedirs(out_dir, exist_ok=True)

        # Mahalla raisi yoki 1-mas'ul xodim ma'lumotlaridan QR vCard yasash
        rais_item = roles_data[0] if roles_data else {}
        rais_fio = rais_item.get("f", "")
        rais_phone = rais_item.get("t", "")
        rais_inn = rais_item.get("inn", "")
        qr_img = generate_vcard_qr_image(
            name=rais_fio,
            phone=rais_phone,
            org=f"{mahalla_name} MFY",
            title="Mahalla Raisi",
            inn=rais_inn,
            size=140
        )
        qr_base64 = _image_to_base64_src(qr_img)

        now_str = time.strftime("%d.%m.%Y %H:%M")
        year_str = time.strftime("%Y")

        # HTML shablonini shakllantirish
        html_rows = []
        for idx, r in enumerate(roles_data, 1):
            role_title = r.get("role_title") or r.get("s", "Mas'ul")
            fio = r.get("f", "") or "—"
            tel = r.get("t", "") or "—"
            clean_tel = clean_phone_number(tel) if tel != "—" else "—"
            inn = r.get("inn", "") or "—"
            jshr = r.get("jshr", "") or "—"
            seriya = r.get("seriya", "") or "—"

            status_badge = '<span style="color: #059669; font-weight: bold;">Faol</span>' if fio != "—" else '<span style="color: #dc2626; font-weight: bold;">Vakant</span>'

            bg_color = "#f8fafc" if idx % 2 == 0 else "#ffffff"

            row_html = f"""
            <tr style="background-color: {bg_color};">
                <td style="padding: 7px 5px; text-align: center; border: 1px solid #cbd5e1; font-weight: bold; font-size: 10pt;">{idx}</td>
                <td style="padding: 7px 8px; border: 1px solid #cbd5e1; font-weight: bold; color: #1e3a8a; font-size: 10pt;">{role_title}</td>
                <td style="padding: 7px 8px; border: 1px solid #cbd5e1; font-weight: 600; font-size: 10pt;">{fio}</td>
                <td style="padding: 7px 8px; border: 1px solid #cbd5e1; text-align: center; font-size: 10pt; font-family: monospace;">{clean_tel}</td>
                <td style="padding: 7px 8px; border: 1px solid #cbd5e1; text-align: center; font-size: 9.5pt; font-family: monospace;">{inn}<br><small style="color: #64748b;">{jshr}</small></td>
                <td style="padding: 7px 8px; border: 1px solid #cbd5e1; text-align: center; font-size: 9.5pt; font-family: monospace;">{seriya}</td>
                <td style="padding: 7px 6px; border: 1px solid #cbd5e1; text-align: center; font-size: 9.5pt;">{status_badge}</td>
            </tr>
            """
            html_rows.append(row_html)

        table_body = "\n".join(html_rows)

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    color: #0f172a;
                    margin: 0;
                    padding: 0;
                }}
                .header-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 12px;
                }}
                .title-main {{
                    font-size: 13pt;
                    font-weight: 800;
                    color: #1e293b;
                    text-align: center;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    line-height: 1.3;
                }}
                .title-sub {{
                    font-size: 15pt;
                    font-weight: 900;
                    color: #0284c7;
                    text-align: center;
                    text-transform: uppercase;
                    margin-top: 4px;
                    margin-bottom: 2px;
                }}
                .meta-badge {{
                    text-align: center;
                    font-size: 9.5pt;
                    color: #475569;
                    margin-bottom: 14px;
                }}
                .passport-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 16px;
                }}
                .passport-table th {{
                    background-color: #0284c7;
                    color: #ffffff;
                    padding: 8px 6px;
                    font-size: 9.5pt;
                    font-weight: bold;
                    text-align: center;
                    border: 1px solid #0369a1;
                }}
                .footer-box {{
                    width: 100%;
                    margin-top: 20px;
                    border-top: 2px solid #e2e8f0;
                    padding-top: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="title-main">
                O'ZBEKISTON RESPUBLIKASI NAMANGAN VILOYATI<br>
                {district_name.upper()} HOKIMLIGI
            </div>
            <div class="title-sub">
                «{mahalla_name.upper()}» MAHALLA FUQAROLAR YIG'INI<br>
                «YETTILIGI» 360° RASMIY RAQAMLI PASPORTI
            </div>
            <div class="meta-badge">
                📅 Shakllantirilgan sana: <b>{now_str}</b> &nbsp;|&nbsp; 🏛 Hudud: <b>{district_name}</b> &nbsp;|&nbsp; 📋 Yettilik tarkibi: <b>7 ta mas'ul lavozim</b>
            </div>

            <table class="passport-table">
                <thead>
                    <tr>
                        <th style="width: 5%;">№</th>
                        <th style="width: 22%;">Lavozimi</th>
                        <th style="width: 27%;">F.I.O (Mas'ul xodim)</th>
                        <th style="width: 16%;">Telefon raqami</th>
                        <th style="width: 15%;">INN / JSHSHIR</th>
                        <th style="width: 10%;">Pasport seriya</th>
                        <th style="width: 5%;">Holati</th>
                    </tr>
                </thead>
                <tbody>
                    {table_body}
                </tbody>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <tr>
                    <td style="width: 15%; text-align: center; vertical-align: middle;">
                        {"<img src='" + qr_base64 + "' width='85' height='85' style='border: 1px solid #cbd5e1; padding: 2px; border-radius: 4px;' />" if qr_base64 else ""}
                        <br><span style="font-size: 7.5pt; color: #64748b;">Raqamli vCard</span>
                    </td>
                    <td style="width: 55%; padding-left: 12px; vertical-align: middle; font-size: 8.5pt; color: #475569; line-height: 1.4;">
                        ℹ️ <b>Ma'lumot uchun:</b> Mazkur pasport Pop Tumani Tashkilotlari va INN Tizimi (Enterprise Pro) orqali rasman shakllantirilgan.<br>
                        QR-kod orqali mas'ullarning elektron tashrif qog'ozini smartfonga bir zumda saqlab olishingiz mumkin.
                    </td>
                    <td style="width: 30%; text-align: center; vertical-align: middle; font-size: 9pt; color: #1e293b;">
                        <b>MFY Raisi tasdig'i:</b><br><br>
                        _________________ (Imzo)<br>
                        <span style="font-size: 8pt; color: #64748b;">M.O' (Muhr o'rni)</span>
                    </td>
                </tr>
            </table>

            <div style="margin-top: 25px; text-align: center; font-size: 8pt; color: #94a3b8; border-top: 1px dashed #cbd5e1; padding-top: 6px;">
                «Pop Tumani Tashkilotlari va INN Tizimi v4.0 Pro» &bull; Namangan viloyati, {year_str}-yil
            </div>
        </body>
        </html>
        """

        # QPdfWriter va QTextDocument orqali A4 PDF yaratish
        writer = QPdfWriter(output_path)
        writer.setPageSize(QPageSize(QPageSize.A4))
        layout = QPageLayout(
            QPageSize(QPageSize.A4),
            QPageLayout.Portrait,
            QMarginsF(12, 12, 12, 12),
            QPageLayout.Millimeter
        )
        writer.setPageLayout(layout)
        writer.setResolution(300)

        doc = QTextDocument()
        doc.setDocumentMargin(10)
        doc.setHtml(html_content)
        doc.print_(writer)

        logger.info(f"[PDF] Mahalla pasporti muvaffaqiyatli saqlandi: {output_path} ({os.path.getsize(output_path)} bayt)")
        return True

    except Exception as e:
        logger.error(f"[PDF XATO] Mahalla pasportini yaratishda xatolik: {e}")
        return False


def export_organizations_pdf(
    organizations: List[Dict[str, Any]],
    title: str,
    output_path: str,
    district_name: str = "Pop tumani"
) -> bool:
    """
    Tashkilotlar ro'yxatini A4 formatidagi rasmiy PDF hisobot ko'rinishida eksport qilish.
    """
    try:
        out_dir = os.path.dirname(os.path.abspath(output_path))
        os.makedirs(out_dir, exist_ok=True)

        now_str = time.strftime("%d.%m.%Y %H:%M")
        year_str = time.strftime("%Y")

        html_rows = []
        for idx, org in enumerate(organizations, 1):
            nomi = org.get("m", "-")
            toifa = org.get("s", "-")
            rahbar = org.get("f", "-")
            tel = org.get("t", "-")
            inn = org.get("inn", "-")
            bg_color = "#f8fafc" if idx % 2 == 0 else "#ffffff"

            row = f"""
            <tr style="background-color: {bg_color}; font-size: 8.5pt;">
                <td style="padding: 5px; text-align: center; border: 1px solid #cbd5e1;">{idx}</td>
                <td style="padding: 5px; border: 1px solid #cbd5e1; font-weight: 600;">{nomi}</td>
                <td style="padding: 5px; border: 1px solid #cbd5e1; text-align: center;">{toifa}</td>
                <td style="padding: 5px; border: 1px solid #cbd5e1;">{rahbar}</td>
                <td style="padding: 5px; border: 1px solid #cbd5e1; text-align: center; font-family: monospace;">{tel}</td>
                <td style="padding: 5px; border: 1px solid #cbd5e1; text-align: center; font-family: monospace; font-weight: bold;">{inn}</td>
            </tr>
            """
            html_rows.append(row)

        table_body = "\n".join(html_rows)

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #0f172a; }}
                .title-main {{ font-size: 13pt; font-weight: 800; text-align: center; text-transform: uppercase; }}
                .title-sub {{ font-size: 11pt; font-weight: bold; color: #0284c7; text-align: center; margin-bottom: 8px; }}
                .meta {{ font-size: 8.5pt; color: #64748b; text-align: center; margin-bottom: 12px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th {{ background-color: #0284c7; color: #ffffff; padding: 6px; font-size: 8.5pt; border: 1px solid #0369a1; }}
            </style>
        </head>
        <body>
            <div class="title-main">{district_name.upper()} HOKIMLIGI TASHKILOTLARI VA INN REYESTRI</div>
            <div class="title-sub">{title.upper()}</div>
            <div class="meta">Sana: {now_str} &bull; Jami tashkilotlar: {len(organizations)} ta</div>
            <table>
                <thead>
                    <tr>
                        <th style="width: 4%;">№</th>
                        <th style="width: 30%;">Tashkilot Nomi</th>
                        <th style="width: 18%;">Toifasi</th>
                        <th style="width: 24%;">Mas'ul Rahbar</th>
                        <th style="width: 14%;">Telefon</th>
                        <th style="width: 10%;">INN</th>
                    </tr>
                </thead>
                <tbody>
                    {table_body}
                </tbody>
            </table>
            <div style="margin-top: 15px; text-align: center; font-size: 7.5pt; color: #94a3b8;">
                «Pop Tumani Tashkilotlari va INN Tizimi v4.0 Pro» &bull; {year_str}-yil
            </div>
        </body>
        </html>
        """

        writer = QPdfWriter(output_path)
        writer.setPageSize(QPageSize(QPageSize.A4))
        layout = QPageLayout(
            QPageSize(QPageSize.A4),
            QPageLayout.Portrait,
            QMarginsF(10, 10, 10, 10),
            QPageLayout.Millimeter
        )
        writer.setPageLayout(layout)
        writer.setResolution(300)

        doc = QTextDocument()
        doc.setDocumentMargin(8)
        doc.setHtml(html_content)
        doc.print_(writer)

        logger.info(f"[PDF] Tashkilotlar PDF hisoboti saqlandi: {output_path} ({os.path.getsize(output_path)} bayt)")
        return True

    except Exception as e:
        logger.error(f"[PDF XATO] Tashkilotlar PDF hisobotini yaratishda xatolik: {e}")
        return False
