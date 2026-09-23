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

def generate_phone_qr_image(phone_number: str, size: int = 250) -> Image.Image:
    """Telefon raqami uchun xotirada (RAM) toza QR-kod tasvirini yaratish."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(phone_number)
    qr.make(fit=True)
    pil_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return pil_img.resize((size, size))
