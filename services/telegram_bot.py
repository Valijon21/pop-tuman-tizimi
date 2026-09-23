"""
Pop Tuman Tashkilotlari va INN Tizimi
Telegram Bot Xizmati (Telegram Bot Service)
Tuman mas'ullari va xodimlari uchun mobil qulaylik, tezkor qidiruv va ommaviy xabarnoma tarqatish.
Tashqi og'ir kutubxonalarsiz (standard urllib) toza, xavfsiz va ishonchli oqimda ishlaydi.
"""
import threading
import time
import json
import urllib.request
import urllib.parse
from typing import Any, Dict, List, Optional, Set

from core.logger import logger
from services.verification_service import build_verification_text
from services.cabinet_service import build_cabinet_access_text

class TelegramBotService:
    """Telegram Bot orqali tashkilotlar bazasini qidirish, verifikatsiya va ommaviy xabarnoma taqdim etish."""

    def __init__(self, arg1: Any = None, arg2: Any = None):
        # Parametrlar tartibiga nisbatan moslashuvchanlik (data_manager, token yoki token, data_manager)
        if isinstance(arg1, str) and not (isinstance(arg2, str) and arg2):
            self.token = arg1.strip()
            self.data_manager = arg2
        else:
            self.data_manager = arg1
            self.token = str(arg2 or "").strip()

        # Agar data_manager berilmagan bo'lsa, zaxiradan yaratish
        if not self.data_manager:
            try:
                from database.data_manager import DataManager
                self.data_manager = DataManager()
            except Exception:
                self.data_manager = None

        # Agar token berilmagan bo'lsa, muhit o'zgaruvchisi yoki settings dan olish
        if not self.token:
            self.token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        if not self.token and self.data_manager and hasattr(self.data_manager, "settings"):
            self.token = str(self.data_manager.settings.get("telegram_bot_token", "")).strip()

        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.last_update_id = 0
        self.subscribers: Set[int] = set()
        self._load_subscribers()

    def is_configured(self) -> bool:
        """Bot tokeni kiritilgan va sozlanganligini tekshirish."""
        return bool(self.token and len(self.token) > 15)

    def _load_subscribers(self) -> None:
        """Oldin saqlangan obunachilar (chat_id) ro'yxatini yuklash."""
        try:
            if hasattr(self.data_manager, "settings") and isinstance(self.data_manager.settings, dict):
                subs = self.data_manager.settings.get("telegram_subscribers", [])
                self.subscribers = set(int(s) for s in subs if str(s).isdigit())
        except Exception as e:
            logger.debug(f"[TELEGRAM BOT] Obunachilarni yuklashda xatolik: {e}")

    def _save_subscriber(self, chat_id: int) -> None:
        """Yangi foydalanuvchini obunachilar ro'yxatiga qo'shish."""
        if chat_id not in self.subscribers:
            self.subscribers.add(chat_id)
            try:
                if hasattr(self.data_manager, "settings") and isinstance(self.data_manager.settings, dict):
                    self.data_manager.settings["telegram_subscribers"] = list(self.subscribers)
                    if hasattr(self.data_manager, "save_settings"):
                        self.data_manager.save_settings()
            except Exception as e:
                logger.debug(f"[TELEGRAM BOT] Obunachini saqlashda xatolik: {e}")

    def start(self) -> None:
        """Botni fon rejimida ishga tushirish."""
        if self.running or not self.token:
            return
        self.running = True
        self.thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.thread.start()
        logger.info("[TELEGRAM BOT] Bot fon oqimida ishga tushirildi.")

    def start_polling(self) -> None:
        """Alias for start()."""
        self.start()

    def stop(self) -> None:
        """Botni to'xtatish."""
        self.running = False
        logger.info("[TELEGRAM BOT] Bot to'xtatildi.")

    def _api_call(self, method: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        url = self.base_url + method
        if params:
            encoded_params = urllib.parse.urlencode(params)
            url += f"?{encoded_params}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "PopTumanBot/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            logger.debug(f"[TELEGRAM API] Xatolik ({method}): {e}")
        return None

    def send_message(self, chat_id: int, text: str) -> bool:
        """Foydalanuvchiga HTML formatida xabar yuborish."""
        res = self._api_call("sendMessage", {"chat_id": chat_id, "text": text, "parse_mode": "HTML"})
        return bool(res and res.get("ok"))

    def broadcast_message(self, text: str) -> Dict[str, int]:
        """Barcha obuna bo'lgan mas'ullarga ommaviy xabarnoma tarqatish."""
        sent = 0
        failed = 0
        for chat_id in list(self.subscribers):
            ok = self.send_message(chat_id, text)
            if ok:
                sent += 1
            else:
                failed += 1
        return {"sent": sent, "failed": failed, "total": len(self.subscribers)}

    def _poll_loop(self) -> None:
        """Telegramdan yangi xabarlarni tinglash sikli (Long polling)."""
        while self.running:
            try:
                updates = self._api_call("getUpdates", {"offset": self.last_update_id + 1, "timeout": 10})
                if updates and updates.get("ok"):
                    for u in updates.get("result", []):
                        self.last_update_id = u.get("update_id", self.last_update_id)
                        msg = u.get("message")
                        if msg and "text" in msg:
                            self._handle_message(msg)
            except Exception as e:
                logger.debug(f"[TELEGRAM POLL] Siklda xatolik: {e}")
            time.sleep(1)

    def _handle_message(self, msg: Dict[str, Any]) -> None:
        chat_id = msg["chat"]["id"]
        text = str(msg.get("text", "")).strip()
        self._save_subscriber(chat_id)

        if text.startswith("/start"):
            welcome = (
                "👋 <b>Assalomu alaykum!</b>\n\n"
                "🏛 <b>Pop Tumani Smart Boshqaruv Tizimi</b> rasmiy yordamchi botiga xush kelibsiz.\n\n"
                "Siz tizimga muvaffaqiyatli ulandingiz va tuman xabarnomalarini qabul qilasiz.\n\n"
                "🔍 <b>Qidiruv buyruqlari:</b>\n"
                "• Mahalla yoki tashkilot nomini yozing (masalan: <code>Chorkesar</code>)\n"
                "• INN raqamini yozing (masalan: <code>203599806</code>)\n"
                "• <code>/verif [INN]</code> — Verifikatsiya shablon matni\n"
                "• <code>/cabinet [INN]</code> — Kabinetga dostup shablon matni\n"
                "• <code>/mahalla [Nomi]</code> — Mahalla 'Yettiligi' xodimlari ro'yxati"
            )
            self.send_message(chat_id, welcome)
            return

        if text.startswith("/verif"):
            parts = text.split(maxsplit=1)
            query = parts[1].strip() if len(parts) > 1 else ""
            item = self._find_first(query)
            if item:
                verif_text = build_verification_text(item)
                self.send_message(chat_id, f"🛡 <b>Verifikatsiya Shabloni:</b>\n\n<code>{verif_text}</code>")
            else:
                self.send_message(chat_id, "❌ Ushbu INN yoki nom bo'yicha tashkilot topilmadi.")
            return

        if text.startswith("/cabinet") or text.startswith("/kabinet"):
            parts = text.split(maxsplit=1)
            query = parts[1].strip() if len(parts) > 1 else ""
            item = self._find_first(query)
            if item:
                cab_text = build_cabinet_access_text(item)
                self.send_message(chat_id, f"🔑 <b>Kabinetga Dostup Shabloni:</b>\n\n<code>{cab_text}</code>")
            else:
                self.send_message(chat_id, "❌ Ushbu INN yoki nom bo'yicha tashkilot topilmadi.")
            return

        if text.startswith("/mahalla"):
            parts = text.split(maxsplit=1)
            query = parts[1].strip() if len(parts) > 1 else ""
            matches = [i for i in self.data_manager.data if query.lower() in str(i.get("m", "")).lower()]
            if matches:
                m_name = matches[0].get("m", "")
                res = f"🏘 <b>{m_name} Mas'ullari:</b>\n\n"
                for m in matches[:7]:
                    res += f"• <b>{m.get('s', '-')}:</b> {m.get('f', '-')}\n  📞 <a href='tel:{m.get('t', '')}'>{m.get('t', '-')}</a> | INN: <code>{m.get('inn', '-')}</code>\n"
                res += f"\n<i>Tezkor shablon olish: /verif {matches[0].get('inn', '')}</i>"
                self.send_message(chat_id, res)
            else:
                self.send_message(chat_id, "❌ Mahalla topilmadi.")
            return

        # Umumiy qidiruv (Nom, INN yoki F.I.SH bo'yicha)
        item = self._find_first(text)
        if item:
            card = (
                f"🏢 <b>{item.get('m', '-')}</b>\n"
                f"📌 Toifasi: {item.get('s', '-')}\n"
                f"👤 Mas'ul: <b>{item.get('f', '-')}</b>\n"
                f"📞 Tel: <a href='tel:{item.get('t', '')}'>{item.get('t', '-')}</a>\n"
                f"🆔 INN: <code>{item.get('inn', '-')}</code>\n"
            )
            if item.get("jshr"): card += f"🔢 JSHSHIR: <code>{item.get('jshr')}</code>\n"
            if item.get("izoh"): card += f"📝 Izoh: {item.get('izoh')}\n"
            card += (
                f"\n⚡ <b>Tezkor buyruqlar:</b>\n"
                f"• /verif_{item.get('inn')} — Verifikatsiya shabloni\n"
                f"• /cabinet_{item.get('inn')} — Kabinetga dostup"
            )
            self.send_message(chat_id, card)
        else:
            self.send_message(chat_id, f"❌ '<code>{text}</code>' bo'yicha ma'lumot topilmadi.\nINN yoki tashkilot nomini to'g'ri kiritganingizni tekshiring.")

    def _find_first(self, query: str) -> Optional[Dict[str, Any]]:
        if not query: return None
        q = query.strip().lower()
        # Handle /verif_123456789 format
        if "_" in q:
            q = q.split("_")[-1].strip()

        data = getattr(self.data_manager, "data", [])
        for item in data:
            if q == str(item.get("inn", "")).strip().lower():
                return item
            if q in str(item.get("m", "")).lower() or q in str(item.get("f", "")).lower():
                return item
        return None

_bot_singleton_instance: Optional[TelegramBotService] = None

def get_telegram_bot_service(data_manager: Any = None, token: Optional[str] = None) -> TelegramBotService:
    """Yagona TelegramBotService instansiyasini olish."""
    global _bot_singleton_instance
    if _bot_singleton_instance is None or token or data_manager:
        _bot_singleton_instance = TelegramBotService(data_manager, token)
    return _bot_singleton_instance

