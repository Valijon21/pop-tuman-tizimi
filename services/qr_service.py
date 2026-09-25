import qrcode
from PIL import Image

def clean_phone_number(raw_tel: str) -> str:
    """Telefon raqamini tozalash va to'g'ri xalqaro E.164 formatga keltirish.
    
    Agar skaner yoki teruvchi xatosi tufayli raqam boshiga '835' (T-E-L harflarining
    T9 raqamlari) qo'shilib qolgan bo'lsa (masalan: 835998911234567), uni tozalaydi.
    """
    if not raw_tel:
        return ""

    digits = "".join(filter(str.isdigit, str(raw_tel)))
    if not digits:
        return ""

    # Skaner T-E-L (835) vanity xatosi sababli qo'shilgan prefiksni olib tashlash
    if digits.startswith("835998") and len(digits) >= 15:
        digits = digits[3:]

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
    """Telefon raqami uchun xotirada (RAM) toza QR-kod tasvirini yaratish.
    
    MUHIM (835 muammosi yechimi):
    Ko'pgina smartfonlar (Xiaomi/MIUI, Transsion, Samsung, Android dialer) QR-kodda 'tel:'
    yozuvini ko'rganda, uni 'vanity' harflar (T=8, E=3, L=5) deb qabul qilib '835' raqamini
    qo'shib yuboradi (835998...).
    as_uri=False (standart) bo'lganda, QR-kodga sof xalqaro formatdagi raqam (+998XXXXXXXXX)
    yoziladi. Unda hech qanday harf bo'lmagani sababli telefon kamerasida 835 muammosi
    100% bartaraf etiladi va to'g'ridan-to'g'ri toza raqam teriladi.
    """
    clean_p = clean_phone_number(phone_number) or str(phone_number).strip()
    if as_uri:
        data = f"tel:{clean_p}" if not clean_p.startswith("tel:") else clean_p
    else:
        data = clean_p

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


def generate_mecard_data(name: str = "", phone: str = "", org: str = "", title: str = "", inn: str = "") -> str:
    """NTT DoCoMo MeCard formati — mobil kameralar uchun eng xavfsiz va universal kontakt standarti.
    
    Smartfon kameralari (Google Lens, Samsung, iPhone, Xiaomi) ushbu formatni ko'rganda
    vanity harflarni (835) mutlaqo aralashtirmaydi va to'g'ridan-to'g'ri 'Kontaktga saqlash'
    oynasini toza +998... raqami bilan ochadi.
    """
    parts = ["MECARD:"]
    clean_n = name.strip().replace(";", " ").replace(":", " ")
    if clean_n:
        parts.append(f"N:{clean_n};")
    clean_p = clean_phone_number(phone)
    if clean_p:
        parts.append(f"TEL:{clean_p};")
    clean_o = org.strip().replace(";", " ").replace(":", " ")
    if clean_o:
        parts.append(f"ORG:{clean_o};")

    notes = []
    if title:
        notes.append(f"Lavozim: {title.strip()}")
    if inn:
        notes.append(f"INN: {inn.strip()}")
    if notes:
        note_str = " | ".join(notes).replace(";", " ").replace(":", " ")
        parts.append(f"NOTE:{note_str};")

    parts.append(";")
    return "".join(parts)


def generate_mecard_qr_image(
    name: str = "",
    phone: str = "",
    org: str = "",
    title: str = "",
    inn: str = "",
    size: int = 250
) -> Image.Image:
    """Mobil kontakt (MeCard) uchun toza QR-kod tasvirini yaratish."""
    mecard_text = generate_mecard_data(name=name, phone=phone, org=org, title=title, inn=inn)
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(mecard_text)
    qr.make(fit=True)
    pil_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return pil_img.resize((size, size))


def generate_vcard_data(name: str = "", phone: str = "", org: str = "", title: str = "", inn: str = "") -> str:
    """vCard 3.0 formatida kontakt ma'lumotlarini RFC 2426 standarti bo'yicha shakllantirish.
    
    Qatorlar oxiri RFC 2426 ga binoan qat'iy '\\r\\n' (CRLF) bilan tugaydi va majburiy
    'N' (Structured Name) maydoni to'ldiriladi. Bu orqali mobil tizimlar vCard ni
    buzilmasdan to'g'ri taniydi va matnli qidiruvdagi 835 vanity xatosi yuzaga kelmaydi.
    """
    lines = ["BEGIN:VCARD", "VERSION:3.0"]
    clean_n = name.strip()
    if clean_n:
        parts = clean_n.split()
        if len(parts) >= 2:
            last = parts[0]
            first = " ".join(parts[1:])
            lines.append(f"N:{last};{first};;;")
        else:
            lines.append(f"N:{clean_n};;;;")
        lines.append(f"FN:{clean_n}")
    else:
        lines.append("FN:Noma'lum")
        lines.append("N:;;;;")

    if org:
        lines.append(f"ORG:{org.strip()}")
    if title:
        lines.append(f"TITLE:{title.strip()}")
    if phone:
        clean_p = clean_phone_number(phone)
        lines.append(f"TEL;TYPE=CELL,VOICE:{clean_p}")
        lines.append(f"TEL;CELL:{clean_p}")
    if inn:
        lines.append(f"NOTE:INN: {inn.strip()}")
    lines.append("END:VCARD")
    return "\r\n".join(lines) + "\r\n"


def generate_vcard_qr_image(
    name: str = "",
    phone: str = "",
    org: str = "",
    title: str = "",
    inn: str = "",
    size: int = 250
) -> Image.Image:
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
