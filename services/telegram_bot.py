"""
Pop Tuman Tashkilotlari va INN Tizimi
Telegram Bot Xizmati (Telegram Bot Service)
Tuman mas'ullari va xodimlari uchun mobil qulaylik va tezkor ma'lumot taqdim etish.
Tashqi kutubxonalarsiz (standard urllib) toza va ishonchli oqimda ishlaydi.
"""
import threading
import time
import json
import urllib.request
import urllib.parse
from typing import Any, Dict, List, Optional

from core.logger import logger
from services.verification_service import build_verification_text

class TelegramBotService:
    """Telegram Bot orqali tashkilotlar bazasini qidirish va verifikatsiya taqdim etish."""

    def __init__(self, data_manager: Any, token: str):
        self.data_manager = data_manager
        self.token = token.strip()
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.last_update_id = 0

    def start(self) -> None:
        """Botni fon rejimida ishga tushirish."""
        if self.running or not self.token:
            return
        self.running = True
        self.thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.thread.start()
        logger.info("[TELEGRAM BOT] Bot fon oqimida ishga tushirildi.")

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

    def send_message(self, chat_id: int, text: str) -> None:
        """Foydalanuvchiga xabar yuborish."""
        self._api_call("sendMessage", {"chat_id": chat_id, "text": text, "parse_mode": "HTML"})

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

        if text.startswith("/start"):
            welcome = (
                "👋 <b>Assalomu alaykum!</b>\n\n"
                "🏛 <b>Pop Tumani Smart Boshqaruv Tizimi</b> rasmiy yordamchi botiga xush kelibsiz.\n\n"
                "🔍 <b>Qidiruv buyruqlari:</b>\n"
                "• Tashkilot yoki mahalla nomini yozing (masalan: <code>Chorkesar</code>)\n"
                "• INN raqamini yozing (masalan: <code>203599806</code>)\n"
                "• <code>/verif [INN]</code> — tayyor verifikatsiya matnini olish\n"
                "• <code>/mahalla [Nomi]</code> — Mahalla yettiligi ma'lumotlarini olish"
            )
            self.send_message(chat_id, welcome)
            return

        if text.startswith("/verif"):
            parts = text.split(maxsplit=1)
            query = parts[1].strip() if len(parts) > 1 else ""
            item = self._find_first(query)
            if item:
                verif_text = build_verification_text(item)
                self.send_message(chat_id, f"📋 <b>Verifikatsiya Shabloni:</b>\n\n<code>{verif_text}</code>")
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
                    res += f"• <b>{m.get('s', '-')}:</b> {m.get('f', '-')}\n  📞 {m.get('t', '-')}\n"
                self.send_message(chat_id, res)
            else:
                self.send_message(chat_id, "❌ Mahalla topilmadi.")
            return

        # Umumiy qidiruv
        item = self._find_first(text)
        if item:
            card = (
                f"🏢 <b>{item.get('m', '-')}</b>\n"
                f"📌 Turi: {item.get('s', '-')}\n"
                f"👤 Rahbar: {item.get('f', '-')}\n"
                f"📞 Tel: {item.get('t', '-')}\n"
                f"🆔 INN: {item.get('inn', '-')}\n"
            )
            if item.get("izoh"): card += f"📝 Izoh: {item.get('izoh')}\n"
            card += f"\n<i>Verifikatsiya matnini olish uchun: /verif {item.get('inn')}</i>"
            self.send_message(chat_id, card)
        else:
            self.send_message(chat_id, f"❌ '{text}' bo'yicha hech qanday tashkilot topilmadi.")

    def _find_first(self, query: str) -> Optional[Dict[str, Any]]:
        if not query: return None
        q = query.strip().lower()
        for item in self.data_manager.data:
            if q == str(item.get("inn", "")).strip().lower():
                return item
            if q in str(item.get("m", "")).lower() or q in str(item.get("f", "")).lower():
                return item
        return None
