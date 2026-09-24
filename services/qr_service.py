import qrcode
from PIL import Image

def clean_phone_number(raw_tel: str) -> str:
    """Telefon raqamini tozalash va to'g'ri xalqaro formatga keltirish."""
    digits = "".join(filter(str.isdigit, str(raw_tel)))
    if not digits:
        return ""

    if "998" in digits:
        start_index = digits.find("998")
        if len(digits[start_index:]) >= 12:
            return "+" + digits[start_index : start_index + 12]
        return "+" + digits[start_index:]
    elif len(digits) == 9:
        return "+998" + digits
    elif len(digits) > 9:
        return "+998" + digits[-9:]
    return digits

def generate_phone_qr_image(phone_number: str, size: int = 250, as_uri: bool = False) -> Image.Image:
    """Telefon raqami uchun xotirada (RAM) toza QR-kod tasvirini yaratish."""
    data = f"tel:{phone_number}" if as_uri and not phone_number.startswith("tel:") else phone_number
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    pil_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return pil_img.resize((size, size))

def generate_vcard_data(name: str = "", phone: str = "", org: str = "", title: str = "", inn: str = "") -> str:
    """vCard 3.0 formatida kontakt ma'lumotlarini shakllantirish."""
    lines = ["BEGIN:VCARD", "VERSION:3.0"]
    if name:
        lines.append(f"FN:{name.strip()}")
    if org:
        lines.append(f"ORG:{org.strip()}")
    if title:
        lines.append(f"TITLE:{title.strip()}")
    if phone:
        clean_p = clean_phone_number(phone)
        lines.append(f"TEL;TYPE=CELL:{clean_p}")
    if inn:
        lines.append(f"NOTE:INN: {inn.strip()}")
    lines.append("END:VCARD")
    return "\n".join(lines)

def generate_vcard_qr_image(name: str = "", phone: str = "", org: str = "", title: str = "", inn: str = "", size: int = 250) -> Image.Image:
    """Raqamli tashrif qog'ozi (vCard) uchun xotirada toza QR-kod tasvirini yaratish."""
    vcard_text = generate_vcard_data(name=name, phone=phone, org=org, title=title, inn=inn)
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(vcard_text)
    qr.make(fit=True)
    pil_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return pil_img.resize((size, size))
