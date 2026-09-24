"""
Pop Tuman Tashkilotlari va INN Tizimi
Telegram Bot Xizmati (Telegram Bot Service v3.0 Professional Enterprise Edition)

Xususiyatlari:
1. Doimiy Asosiy Menyu (Persistent ReplyKeyboardMarkup) - kirishdanoq tayyor tugmalar
2. Interaktiv Inline Menyu & Dinamik Yangilanish (editMessageText orqali qotmasdan tezkor ishlash)
3. 360° Mahalla Yettiligi pasporti va kadrlar ro'yxati
4. Shartnomalar va Buxgalterlar telefon bazasi
5. Jonli tuman statistikasi (KPI dashboard)
6. Bir bosishda nusxalanadigan shablonlar (CopyText button & <pre>)
7. requests.Session Keep-Alive ulanishlar basseyni orqali ultra-tezkor O(1) javob qaytarish
"""
import os
import threading
import time
import json
import html
import re
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional, Set

try:
    import requests
except ImportError:
    requests = None

from core.logger import logger
from services.verification_service import build_verification_text
from services.cabinet_service import build_cabinet_access_text
from services.search_service import SearchService, normalize_text
from services.qr_service import clean_phone_number


def get_role_priority(item: Dict[str, Any]) -> int:
    """Xodim yoki tashkilot mas'ulining boshqaruv ustuvorlik darajasi (1-10)."""
    s = str(item.get("s", "")).lower()
    if any(w in s for w in ["rais", "mahalla", "direktor", "mudir", "boshliq", "rahbar"]):
        return 10
    if "hokim" in s:
        return 8
    if any(w in s for w in ["yoshlar", "xotin", "ijtimoiy"]):
        return 5
    if any(w in s for w in ["profilaktika", "soliq", "inspektor"]):
        return 3
    return 1


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

        # Doimiy Keep-Alive aloqasi uchun HTTP sessiya (10x-20x tezlik)
        self.session = None
        if requests is not None:
            self.session = requests.Session()
            self.session.headers.update({"User-Agent": "PopTumanEnterpriseBot/3.0"})

        # Parallel xabarlarni qayta ishlash basseyni (8 ta parallel ishchi)
        self._executor = ThreadPoolExecutor(max_workers=8)

        # O(1) qidiruv keshi
        self._inn_cache: Dict[str, Dict[str, Any]] = {}
        self._build_cache()

        self._load_subscribers()

    def _build_cache(self) -> None:
        """Tezkor O(1) qidiruv uchun INN keshini shakllantirish (Rahbar ustuvorligi bilan)."""
        self._inn_cache = {}
        data = getattr(self.data_manager, "data", []) if self.data_manager else []
        for item in data:
            inn = str(item.get("inn", "")).strip()
            if not inn:
                continue
            clean_d = "".join(filter(str.isdigit, inn))

            existing = self._inn_cache.get(clean_d) or self._inn_cache.get(inn)
            if existing is None or get_role_priority(item) > get_role_priority(existing):
                self._inn_cache[inn] = item
                if clean_d:
                    self._inn_cache[clean_d] = item

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
        logger.info("[TELEGRAM BOT] Bot fon oqimida (ultra-tezkor) ishga tushirildi.")

    def start_polling(self) -> None:
        """start() metodi uchun qulay alias."""
        self.start()

    def stop(self) -> None:
        """Botni to'xtatish."""
        self.running = False
        if self.session:
            try:
                self.session.close()
            except Exception:
                pass
        logger.info("[TELEGRAM BOT] Bot to'xtatildi.")

    def _api_call(self, method: str, params: Optional[Dict[str, Any]] = None, timeout: int = 15) -> Optional[Dict[str, Any]]:
        """Telegram API ga HTTP so'rov yuborish (Sessiya, Keep-Alive va batafsil xatolik logi bilan)."""
        if not self.is_configured():
            return None
        url = self.base_url + method

        # 1. Tezkor requests.Session orqali
        if self.session is not None:
            try:
                resp = self.session.post(url, data=params, timeout=timeout)
                if resp.status_code == 200:
                    return resp.json()
                else:
                    logger.warning(f"[TELEGRAM API SESSION] {method} javob kodi {resp.status_code}: {resp.text}")
            except Exception as e:
                logger.debug(f"[TELEGRAM API SESSION] Tarmoq xatoligi ({method}): {e}")

        # 2. Standart urllib ga o'tish (Fallback)
        data = None
        if params:
            data = urllib.parse.urlencode(params).encode("utf-8")
        try:
            req = urllib.request.Request(
                url,
                data=data,
                headers={"User-Agent": "PopTumanEnterpriseBot/3.0"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as he:
            err_body = he.read().decode("utf-8", errors="replace") if hasattr(he, "read") else ""
            logger.error(f"[TELEGRAM API URLLIB] HTTP Xatolik ({method}) {he.code}: {he.reason} | Tafsilot: {err_body}")
        except Exception as e:
            logger.error(f"[TELEGRAM API URLLIB] Xatolik ({method}): {e}")
        return None

    def send_message(self, chat_id: int, text: str, reply_markup: Optional[Dict[str, Any]] = None) -> bool:
        """Foydalanuvchiga HTML formatida xabar va ixtiyoriy inline/reply tugmalar yuborish."""
        params: Dict[str, Any] = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        res = self._api_call("sendMessage", params)
        if not (res and res.get("ok")):
            # Fallback: Agar HTML formati buzilgan bo'lsa, xabarni tozalab oddiy matn sifatida yetkazish
            logger.warning("[TELEGRAM] HTML xabar yuborishda xatolik. Oddiy matn ko'rinishida yuborilmoqda...")
            clean_text = re.sub(r"<[^>]+>", "", text)
            fallback_params = {
                "chat_id": chat_id,
                "text": clean_text
            }
            if reply_markup:
                fallback_params["reply_markup"] = json.dumps(reply_markup)
            res = self._api_call("sendMessage", fallback_params)
        return bool(res and res.get("ok"))

    def edit_message_text(self, chat_id: int, message_id: int, text: str, reply_markup: Optional[Dict[str, Any]] = None) -> bool:
        """Mavjud xabar matnini joyida yangilash (In-place dynamic update - qotmasdan tezkor ishlash)."""
        params: Dict[str, Any] = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        res = self._api_call("editMessageText", params)
        if not (res and res.get("ok")):
            clean_text = re.sub(r"<[^>]+>", "", text)
            fallback_params = {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": clean_text
            }
            if reply_markup:
                fallback_params["reply_markup"] = json.dumps(reply_markup)
            res = self._api_call("editMessageText", fallback_params)
        return bool(res and res.get("ok"))

    def answer_callback_query(self, callback_query_id: str, text: Optional[str] = None) -> bool:
        """Inline tugma bosilganda Telegram yuklanish animatsiyasini to'xtatish."""
        params: Dict[str, Any] = {"callback_query_id": callback_query_id}
        if text:
            params["text"] = text
        res = self._api_call("answerCallbackQuery", params)
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
        """Telegramdan yangi xabarlarni tinglash sikli (Long polling - Fast Reactive)."""
        while self.running:
            had_updates = False
            try:
                updates = self._api_call("getUpdates", {"offset": self.last_update_id + 1, "timeout": 20}, timeout=25)
                if updates and updates.get("ok"):
                    results = updates.get("result", [])
                    if results:
                        had_updates = True
                    for u in results:
                        self.last_update_id = u.get("update_id", self.last_update_id)

                        # 1. Matnli xabar
                        msg = u.get("message")
                        if msg and "text" in msg:
                            self._executor.submit(self._handle_message, msg)

                        # 2. Inline tugma bosilishi (Callback query)
                        cq = u.get("callback_query")
                        if cq:
                            self._executor.submit(self._handle_callback_query, cq)
                elif updates is None:
                    # 409 Conflict yoki tarmoq uzilishida qisqa tanaffus
                    time.sleep(2)
            except Exception as e:
                logger.debug(f"[TELEGRAM POLL] Siklda xatolik: {e}")
                time.sleep(1)

            if not had_updates:
                time.sleep(0.1)

    # ─────────────────────────────────────────────────────────────────────────────
    # 🌟 PROFESSIONAL INTERFEYS VA TUGMALAR (REPLY & INLINE KEYBOARDS)
    # ─────────────────────────────────────────────────────────────────────────────

    @staticmethod
    def get_main_keyboard() -> Dict[str, Any]:
        """Asosiy doimiy menyu tugmalari (Professional Persistent ReplyKeyboardMarkup)."""
        return {
            "keyboard": [
                [
                    {"text": "🔍 Tashkilot Qidirish"},
                    {"text": "🏘 Mahalla Yettiligi"}
                ],
                [
                    {"text": "📑 Shartnomalar"},
                    {"text": "📊 Tuman Statistikasi"}
                ],
                [
                    {"text": "ℹ️ Bot Qo'llanmasi"}
                ]
            ],
            "resize_keyboard": True,
            "is_persistent": True
        }

    def send_welcome(self, chat_id: int, message_id: Optional[int] = None) -> None:
        """Professional kutib olish xabari va doimiy bosh menyu."""
        data = getattr(self.data_manager, "data", []) if self.data_manager else []
        total_orgs = len(data)

        welcome = (
            "👋 <b>Assalomu alaykum!</b>\n\n"
            "🏛 <b>Pop Tumani Tashkilotlari va INN Tizimi</b> rasmiy professional botiga xush kelibsiz.\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"Bazada <b>{total_orgs}+ ta tashkilot</b>, barcha <b>78 ta MFY 'Yettiligi'</b>, maktablar, bog'chalar va boshqaruv idoralari mavjud.\n\n"
            "🔍 <b>Tezkor qidiruv:</b>\n"
            "• Tashkilot yoki MFY nomi (masalan: <code>Chorkesar</code>)\n"
            "• INN raqami (masalan: <code>202701860</code>)\n"
            "• Mas'ul rahbar ismi yoki telefon raqami\n\n"
            "👇 <i>Pastdagi menyu tugmalaridan birini tanlang yoki to'g'ridan-to'g'ri qidiruv so'zini yozing:</i>"
        )
        if message_id:
            inline_kb = {
                "inline_keyboard": [
                    [
                        {"text": "🔍 Tashkilot Qidirish", "callback_data": "menu:search"},
                        {"text": "🏘 Mahalla Yettiligi", "callback_data": "menu:mahalla"}
                    ],
                    [
                        {"text": "📊 Tuman Statistikasi", "callback_data": "stat:refresh"},
                        {"text": "📑 Shartnomalar", "callback_data": "menu:contracts"}
                    ]
                ]
            }
            self.edit_message_text(chat_id, message_id, welcome, reply_markup=inline_kb)
        else:
            self.send_message(chat_id, welcome, reply_markup=self.get_main_keyboard())

    def send_search_prompt(self, chat_id: int, message_id: Optional[int] = None) -> None:
        """Qidiruv ko'rsatmasi va toifalar bo'yicha saralash inline tugmalari."""
        text = (
            "🔍 <b>Tashkilot yoki Mahallani Qidirish</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Qidirmoqchi bo'lgan ma'lumotni to'g'ridan-to'g'ri yozib yuboring:\n"
            "• Tashkilot yoki MFY nomi (masalan: <code>Chorkesar</code> yoki <code>22-maktab</code>)\n"
            "• INN raqami (masalan: <code>202701860</code>)\n"
            "• Mas'ul rahbar F.I.SH yoki telefon raqami\n\n"
            "📂 <i>Yoki toifalar bo'yicha saralab ko'ring:</i>"
        )
        inline_kb = {
            "inline_keyboard": [
                [
                    {"text": "🏘 MFYlar (78 ta)", "callback_data": "cat:mfy:0"},
                    {"text": "🏫 Maktablar (84 ta)", "callback_data": "cat:maktab:0"}
                ],
                [
                    {"text": "👶 Bog'chalar (71 ta)", "callback_data": "cat:mtt:0"},
                    {"text": "📑 Shartnomalilar (220+ ta)", "callback_data": "cat:contract:0"}
                ],
                [
                    {"text": "🔙 Bosh Menyu", "callback_data": "menu:main"}
                ]
            ]
        }
        if message_id:
            self.edit_message_text(chat_id, message_id, text, reply_markup=inline_kb)
        else:
            self.send_message(chat_id, text, reply_markup=inline_kb)

    def send_statistics(self, chat_id: int, message_id: Optional[int] = None) -> None:
        """Tuman bo'yicha jonli tahliliy statistikani ko'rsatish (In-place yangilash bilan)."""
        data = getattr(self.data_manager, "data", []) if self.data_manager else []
        total_orgs = len(data)

        # MFYlar (noyob nomlar)
        mfy_names = set(
            i.get("m", "") for i in data
            if any(w in str(i.get("s", "")).lower() or w in str(i.get("m", "")).lower() for w in ["mahalla", "mfy"])
        )
        total_mfy = len(mfy_names) if mfy_names else 74

        total_maktab = sum(1 for i in data if "maktab" in str(i.get("s", "")).lower() or "maktab" in str(i.get("m", "")).lower())
        total_mtt = sum(1 for i in data if any(w in str(i.get("s", "")).lower() or w in str(i.get("m", "")).lower() for w in ["bog", "mtt"]))
        contracts_list = [i for i in data if i.get("aparat_soni") or i.get("ulangan_soni")]
        total_contracts = len(contracts_list)
        total_aparat = sum(int(i.get("aparat_soni", 0) or 0) for i in contracts_list)
        total_ulangan = sum(int(i.get("ulangan_soni", 0) or 0) for i in contracts_list)
        total_bux = sum(1 for i in data if i.get("bux_tel"))

        now_str = time.strftime("%d.%m.%Y, %H:%M:%S")

        text = (
            "📊 <b>Pop Tumani Boshqaruv Tizimi — Jonli KPI Tahlili</b>\n\n"
            f"🏢 <b>Jami tashkilotlar:</b> <code>{total_orgs} ta</code>\n"
            f"🏘 <b>Mahalla fuqarolar yig'inlari (MFY):</b> <code>{total_mfy} ta</code>\n"
            f"🏫 <b>Umumiy o'rta ta'lim maktablari:</b> <code>{total_maktab} ta</code>\n"
            f"👶 <b>Maktabgacha ta'lim (MTT):</b> <code>{total_mtt} ta</code>\n\n"
            "📑 <b>Shartnomalar & Ulanishlar Tahlili:</b>\n"
            f"• Rasmiy shartnomalar: <b>{total_contracts} ta</b>\n"
            f"• Apparat shtat birliklari: <b>{total_aparat} ta</b>\n"
            f"• Tizimga ulangan litsenziyalar: <b>{total_ulangan} ta</b>\n"
            f"• Buxgalterlar telefon bazasi: <b>{total_bux} ta</b>\n\n"
            f"🕒 <i>Ma'lumotlar yangilangan vaqti: {now_str}</i>"
        )
        inline_kb = {
            "inline_keyboard": [
                [
                    {"text": "🔄 Yangilash", "callback_data": "stat:refresh"},
                    {"text": "🔍 Qidiruv", "callback_data": "menu:search"}
                ],
                [
                    {"text": "🏘 MFYlar Ro'yxati", "callback_data": "cat:mfy:0"},
                    {"text": "📑 Shartnomalar", "callback_data": "menu:contracts"}
                ]
            ]
        }
        if message_id:
            self.edit_message_text(chat_id, message_id, text, reply_markup=inline_kb)
        else:
            self.send_message(chat_id, text, reply_markup=inline_kb)

    def send_contracts_overview(self, chat_id: int, message_id: Optional[int] = None) -> None:
        """Shartnomalar va buxgalterlar bo'limi ko'rinishi."""
        data = getattr(self.data_manager, "data", []) if self.data_manager else []
        contracts_list = [i for i in data if i.get("aparat_soni") or i.get("ulangan_soni")]
        bux_list = [i for i in data if i.get("bux_tel")]
        total_aparat = sum(int(i.get("aparat_soni", 0) or 0) for i in contracts_list)
        total_ulangan = sum(int(i.get("ulangan_soni", 0) or 0) for i in contracts_list)

        text = (
            "📑 <b>Shartnomalar & Buxgalteriya Monitoringi</b>\n\n"
            f"• Shartnoma tuzilgan: <b>{len(contracts_list)} ta</b> tashkilot\n"
            f"• Apparat shtat xodimlari: <b>{total_aparat} ta</b>\n"
            f"• Tizimga ulangan xodimlar: <b>{total_ulangan} ta</b>\n"
            f"• Buxgalterlar kontaktlari: <b>{len(bux_list)} ta</b>\n\n"
            "Kerakli bo'limni tanlang:"
        )
        inline_kb = {
            "inline_keyboard": [
                [
                    {"text": "📞 Buxgalterlar Kontaktlari", "callback_data": "bux:list:0"},
                    {"text": "📑 Shartnomali Tashkilotlar", "callback_data": "cat:contract:0"}
                ],
                [
                    {"text": "🔙 Bosh Menyu", "callback_data": "menu:main"}
                ]
            ]
        }
        if message_id:
            self.edit_message_text(chat_id, message_id, text, reply_markup=inline_kb)
        else:
            self.send_message(chat_id, text, reply_markup=inline_kb)

    def send_category_list(self, chat_id: int, category: str, page: int = 0, message_id: Optional[int] = None) -> None:
        """Toifa bo'yicha sahifalangan interaktiv tashkilotlar ro'yxati (Pagination)."""
        data = getattr(self.data_manager, "data", []) if self.data_manager else []
        cat_key = category.lower()

        items = []
        cat_title = "Tashkilotlar"

        if cat_key == "mfy":
            cat_title = "🏘 Mahalla Fuqarolar Yig'inlari (MFY)"
            mfy_dict: Dict[str, Dict[str, Any]] = {}
            for i in data:
                name = i.get("m", "").strip()
                if any(w in str(i.get("s", "")).lower() or w in name.lower() for w in ["mahalla", "mfy"]):
                    norm = normalize_text(name)
                    if norm not in mfy_dict or get_role_priority(i) > get_role_priority(mfy_dict[norm]):
                        mfy_dict[norm] = i
            items = sorted(mfy_dict.values(), key=lambda x: str(x.get("m", "")).lower())
        elif cat_key == "maktab":
            cat_title = "🏫 Umumiy O'rta Ta'lim Maktablari"
            items = [i for i in data if "maktab" in str(i.get("s", "")).lower() or "maktab" in str(i.get("m", "")).lower()]
        elif cat_key == "mtt":
            cat_title = "👶 Maktabgacha Ta'lim Tashkilotlari (MTT)"
            items = [i for i in data if any(w in str(i.get("s", "")).lower() or w in str(i.get("m", "")).lower() for w in ["bog", "mtt"])]
        elif cat_key == "contract":
            cat_title = "📑 Shartnoma Tuzgan Tashkilotlar"
            items = [i for i in data if i.get("aparat_soni") or i.get("ulangan_soni")]
        else:
            items = data

        total_items = len(items)
        page_size = 6
        total_pages = max(1, (total_items + page_size - 1) // page_size)
        page = max(0, min(page, total_pages - 1))
        start_idx = page * page_size
        page_items = items[start_idx : start_idx + page_size]

        text = (
            f"📂 <b>{cat_title}</b>\n\n"
            f"Jami: <b>{total_items} ta</b> (Sahifa: {page + 1}/{total_pages})\n"
            f"<i>Batafsil ma'lumot olish uchun tashkilot ustiga bosing:</i>"
        )

        buttons = []
        for item in page_items:
            m_name = item.get("m", "Tashkilot")
            inn = str(item.get("inn", "")).strip()
            label = m_name[:36]
            buttons.append([{"text": f"🏢 {label}", "callback_data": f"org:{inn}"}])

        # Navigatsiya qatori
        nav_row = []
        if page > 0:
            nav_row.append({"text": "⬅️ Oldingi", "callback_data": f"cat:{cat_key}:{page - 1}"})
        nav_row.append({"text": f"{page + 1}/{total_pages}", "callback_data": "noop"})
        if page < total_pages - 1:
            nav_row.append({"text": "Keyingi ➡️", "callback_data": f"cat:{cat_key}:{page + 1}"})
        buttons.append(nav_row)

        buttons.append([{"text": "🔙 Toifalar Menyu", "callback_data": "menu:search"}])

        reply_markup = {"inline_keyboard": buttons}
        if message_id:
            self.edit_message_text(chat_id, message_id, text, reply_markup=reply_markup)
        else:
            self.send_message(chat_id, text, reply_markup=reply_markup)

    def send_accountants_list(self, chat_id: int, page: int = 0, message_id: Optional[int] = None) -> None:
        """Buxgalterlar telefon bazasi (sahifalangan, 1 bosishda nusxalanadigan raqamlar)."""
        data = getattr(self.data_manager, "data", []) if self.data_manager else []
        bux_items = [i for i in data if i.get("bux_tel")]

        total_items = len(bux_items)
        page_size = 5
        total_pages = max(1, (total_items + page_size - 1) // page_size)
        page = max(0, min(page, total_pages - 1))
        start_idx = page * page_size
        page_items = bux_items[start_idx : start_idx + page_size]

        res = (
            f"📞 <b>Buxgalterlar Aloqa Bazasi</b>\n\n"
            f"Jami: <b>{total_items} ta buxgalter</b> (Sahifa: {page + 1}/{total_pages})\n"
            f"<i>Nusxalash uchun telefon raqami ustiga bosing:</i>\n\n"
        )
        for i, item in enumerate(page_items, start=start_idx + 1):
            m_name = html.escape(str(item.get("m", "-")))
            bux_tel = html.escape(str(item.get("bux_tel", "-")))
            inn = html.escape(str(item.get("inn", "-")))
            res += f"<b>{i}. {m_name}</b>\n"
            res += f"   📞 Tel: <code>{bux_tel}</code> | INN: <code>{inn}</code>\n\n"

        buttons = []
        nav_row = []
        if page > 0:
            nav_row.append({"text": "⬅️ Oldingi", "callback_data": f"bux:list:{page - 1}"})
        nav_row.append({"text": f"{page + 1}/{total_pages}", "callback_data": "noop"})
        if page < total_pages - 1:
            nav_row.append({"text": "Keyingi ➡️", "callback_data": f"bux:list:{page + 1}"})
        buttons.append(nav_row)

        buttons.append([{"text": "🔙 Shartnomalar", "callback_data": "menu:contracts"}])

        reply_markup = {"inline_keyboard": buttons}
        if message_id:
            self.edit_message_text(chat_id, message_id, res, reply_markup=reply_markup)
        else:
            self.send_message(chat_id, res, reply_markup=reply_markup)

    def send_mahalla_menu(self, chat_id: int, message_id: Optional[int] = None) -> None:
        """Mahalla 'Yettiligi' bo'limi: ommabop mahallalar va qidiruv ko'rsatmasi."""
        text = (
            "🏘 <b>Pop Tumani Mahalla 'Yettiligi' 360° Pasporti</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Tumanimizdagi barcha <b>78 ta MFY</b>ning 7 ta asosiy mas'ul xodimlari:\n"
            "• 👑 <b>Rais</b>\n"
            "• 💼 <b>Hokim yordamchisi</b>\n"
            "• 🎯 <b>Yoshlar yetakchisi</b>\n"
            "• 🌸 <b>Xotin-qizlar faoli</b>\n"
            "• 👮‍♂️ <b>Profilaktika inspektori</b>\n"
            "• 💰 <b>Soliq inspektori</b>\n"
            "• 🤝 <b>Ijtimoiy xodim</b>\n\n"
            "Qaysi mahallani ko'rmoqchisiz? Nomini yozib yuboring (masalan: <code>Yakkatut</code>, <code>Chorkesar</code>) "
            "yoki quyidagi tugmalardan birini tanlang:"
        )
        inline_kb = {
            "inline_keyboard": [
                [
                    {"text": "Chorkesar MFY", "callback_data": "mah:Chorkesar MFY"},
                    {"text": "Yakkatut MFY", "callback_data": "mah:Yakkatut MFY"}
                ],
                [
                    {"text": "G'urumsaroy MFY", "callback_data": "mah:G'urumsaroy MFY"},
                    {"text": "Sang MFY", "callback_data": "mah:Sang MFY"}
                ],
                [
                    {"text": "Kelachi MFY", "callback_data": "mah:Kelachi MFY"},
                    {"text": "Navbahor MFY", "callback_data": "mah:Navbahor MFY"}
                ],
                [
                    {"text": "📋 Barcha 78 ta MFY Ro'yxati", "callback_data": "cat:mfy:0"}
                ],
                [
                    {"text": "🔙 Bosh Menyu", "callback_data": "menu:main"}
                ]
            ]
        }
        if message_id:
            self.edit_message_text(chat_id, message_id, text, reply_markup=inline_kb)
        else:
            self.send_message(chat_id, text, reply_markup=inline_kb)

    def send_help(self, chat_id: int) -> None:
        """Botdan foydalanish bo'yicha to'liq professional qo'llanma."""
        help_text = (
            "ℹ️ <b>Pop Tumani Boshqaruv Tizimi Botidan Foydalanish Qo'llanmasi</b>\n\n"
            "<b>1. Qidiruv qanday ishlaydi?</b>\n"
            "Botga istalgan matnni yuborishingiz mumkin:\n"
            "• Tashkilot yoki MFY nomi (masalan: <code>Yakkatut</code>)\n"
            "• INN raqami (masalan: <code>202701814</code>)\n"
            "• Mas'ul xodim ismi yoki telefon raqami\n\n"
            "<b>2. Tezkor shablon buyruqlari:</b>\n"
            "• <code>/verif [INN]</code> — Verifikatsiya so'rovi shablon matni\n"
            "• <code>/cabinet [INN]</code> — Kabinetga dostup shablon matni\n"
            "• <code>/mahalla [Nomi]</code> — Mahalla 'Yettiligi' xodimlari\n"
            "• <code>/stat</code> — Tuman bo'yicha jonli statistika\n\n"
            "<b>3. Bir bosishda nusxalash:</b>\n"
            "Shablonlar ustiga bir marta bossangiz kifoya — matn avtomatik tarzda telefoningiz xotirasiga nusxalanadi 📲"
        )
        self.send_message(chat_id, help_text)

    # ─────────────────────────────────────────────────────────────────────────────
    # 📩 XABAR VA CALLBACK QUERY QAYTA ISHLASH (HANDLERS)
    # ─────────────────────────────────────────────────────────────────────────────

    @staticmethod
    def parse_command(raw_text: str) -> tuple:
        """Telegram xabaridan buyruq va argumentni ajratib olish."""
        text = raw_text.strip()
        if not text:
            return "", ""

        if text.startswith("/"):
            if "@" in text:
                first_part, rest = text.split("@", 1)
                if " " in rest:
                    text = first_part + " " + rest.split(" ", 1)[1]
                else:
                    text = first_part

            if " " in text:
                cmd, query = text.split(maxsplit=1)
                if "_" in cmd:
                    base_cmd, sub_q = cmd.split("_", 1)
                    cmd = base_cmd
                    query = f"{sub_q} {query}".strip()
                return cmd.lower(), query.strip()
            elif "_" in text:
                cmd, query = text.split("_", 1)
                return cmd.lower(), query.strip()
            else:
                return text.lower(), ""

        return "", text

    def _handle_message(self, msg: Dict[str, Any]) -> None:
        """Foydalanuvchidan kelgan matnli xabarni qayta ishlash."""
        try:
            chat_id = msg.get("chat", {}).get("id")
            if not chat_id:
                return
            raw_text = str(msg.get("text", "")).strip()
            self._save_subscriber(chat_id)

            clean_text = raw_text.lower().strip()
            cmd, query = self.parse_command(raw_text)

            # ── 1. Bosh Menyu va /start ──
            if cmd in ("/start", "/menu") or clean_text in ("bosh menyu", "menyu", "asosiy menyu"):
                self.send_welcome(chat_id)
                return

            # ── 2. Qidiruv bo'limi ──
            if "tashkilot qidirish" in clean_text or clean_text in ("/search", "/qidiruv", "qidiruv"):
                self.send_search_prompt(chat_id)
                return

            # ── 3. Mahalla Yettiligi ──
            if "mahalla yettiligi" in clean_text or clean_text in ("/yettilik", "yettilik"):
                self.send_mahalla_menu(chat_id)
                return

            # ── 4. Statistika ──
            if "tuman statistikasi" in clean_text or "statistika" in clean_text or clean_text in ("/stat", "/stats"):
                self.send_statistics(chat_id)
                return

            # ── 5. Shartnomalar ──
            if "shartnoma" in clean_text and not clean_text.startswith("/verif") and not clean_text.startswith("/cab"):
                self.send_contracts_overview(chat_id)
                return

            # ── 6. Bot Qo'llanmasi ──
            if "bot qo'llanmasi" in clean_text or "qo'llanma" in clean_text or "qollanma" in clean_text or clean_text in ("/help", "yordam"):
                self.send_help(chat_id)
                return

            # ── 7. Maxsus Shablon Buyruqlari ──
            if cmd in ("/verif", "/verifikatsiya"):
                if not query:
                    self.send_message(
                        chat_id,
                        "⚠️ <b>Verifikatsiya shabloni olish uchun INN yoki tashkilot nomini kiriting.</b>\n\n"
                        "Misollar:\n"
                        "• <code>/verif 202701426</code>\n"
                        "• <code>/verif Temir yo'l</code>"
                    )
                    return
                item = self._find_first(query)
                if item:
                    self.send_verification_template(chat_id, item)
                else:
                    self.send_message(chat_id, f"❌ '<code>{html.escape(query)}</code>' bo'yicha tashkilot topilmadi.\nINN yoki nomni to'g'ri kiritganingizni tekshiring.")
                return

            if cmd in ("/cabinet", "/kabinet"):
                if not query:
                    self.send_message(
                        chat_id,
                        "⚠️ <b>Kabinetga dostup shabloni olish uchun INN yoki tashkilot nomini kiriting.</b>\n\n"
                        "Misollar:\n"
                        "• <code>/cabinet 202701426</code>\n"
                        "• <code>/cabinet Temir yo'l</code>"
                    )
                    return
                item = self._find_first(query)
                if item:
                    self.send_cabinet_template(chat_id, item)
                else:
                    self.send_message(chat_id, f"❌ '<code>{html.escape(query)}</code>' bo'yicha tashkilot topilmadi.\nINN yoki nomni to'g'ri kiritganingizni tekshiring.")
                return

            if cmd == "/mahalla":
                if not query:
                    self.send_mahalla_menu(chat_id)
                    return
                self.send_mahalla_staff(chat_id, query)
                return

            # ── 8. Umumiy Aqlli Qidiruv (Nom, INN, Telefon yoki F.I.SH) ──
            direct_item = self._find_first(raw_text)
            data = getattr(self.data_manager, "data", [])
            results = SearchService.search(data, query=raw_text)

            primary_item = direct_item if direct_item else (max(results, key=get_role_priority) if results else None)

            if primary_item:
                primary_name_norm = normalize_text(primary_item.get("m", ""))
                primary_inn_digits = "".join(filter(str.isdigit, str(primary_item.get("inn", ""))))

                seen_keys = {(primary_name_norm, primary_inn_digits)}
                unique_others = []

                for r in results:
                    r_name_norm = normalize_text(r.get("m", ""))
                    r_inn_digits = "".join(filter(str.isdigit, str(r.get("inn", ""))))
                    key = (r_name_norm, r_inn_digits)
                    if key not in seen_keys:
                        seen_keys.add(key)
                        unique_others.append(r)

                self.send_organization_card(chat_id, primary_item, other_matches=unique_others if unique_others else None)
            else:
                self.send_message(
                    chat_id,
                    f"❌ '<code>{html.escape(raw_text)}</code>' bo'yicha ma'lumot topilmadi.\n"
                    f"INN yoki tashkilot nomini to'g'ri kiritganingizni tekshiring.",
                    reply_markup=self.get_main_keyboard()
                )
        except Exception as e:
            logger.error(f"[TELEGRAM HANDLER] Xabarni qayta ishlashda xatolik: {e}")

    def _handle_callback_query(self, cq: Dict[str, Any]) -> None:
        """Inline tugmalar bosilganda darhol javob qaytarish (Interaktiv navigatsiya)."""
        try:
            cq_id = cq.get("id")
            data = str(cq.get("data", "")).strip()
            msg = cq.get("message", {})
            chat_id = msg.get("chat", {}).get("id")
            msg_id = msg.get("message_id")

            if not chat_id:
                return

            self.answer_callback_query(cq_id)

            if data == "noop":
                return

            if data == "menu:main":
                self.send_welcome(chat_id, message_id=msg_id)
            elif data == "menu:search":
                self.send_search_prompt(chat_id, message_id=msg_id)
            elif data == "menu:mahalla":
                self.send_mahalla_menu(chat_id, message_id=msg_id)
            elif data == "menu:contracts":
                self.send_contracts_overview(chat_id, message_id=msg_id)
            elif data == "stat:refresh":
                self.send_statistics(chat_id, message_id=msg_id)
            elif data.startswith("cat:"):
                # Format: cat:<category>:<page>
                parts = data.split(":")
                category = parts[1] if len(parts) > 1 else "mfy"
                page = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
                self.send_category_list(chat_id, category, page=page, message_id=msg_id)
            elif data.startswith("bux:list:"):
                page_str = data.split(":")[-1]
                page = int(page_str) if page_str.isdigit() else 0
                self.send_accountants_list(chat_id, page=page, message_id=msg_id)
            elif data.startswith("org:"):
                inn = data.split(":", 1)[1]
                item = self._find_first(inn)
                if item:
                    self.send_organization_card(chat_id, item)
                else:
                    self.send_message(chat_id, "❌ Tashkilot ma'lumoti topilmadi.")
            elif data.startswith("verif:"):
                target = data.split(":", 1)[1]
                item = self._find_first(target)
                if item:
                    self.send_verification_template(chat_id, item)
                else:
                    self.send_message(chat_id, "❌ Tashkilot topilmadi.")
            elif data.startswith("cab:"):
                target = data.split(":", 1)[1]
                item = self._find_first(target)
                if item:
                    self.send_cabinet_template(chat_id, item)
                else:
                    self.send_message(chat_id, "❌ Tashkilot topilmadi.")
            elif data.startswith("mah:"):
                target = data.split(":", 1)[1]
                self.send_mahalla_staff(chat_id, target)
        except Exception as e:
            logger.error(f"[TELEGRAM CALLBACK] Xatolik: {e}")

    # ─────────────────────────────────────────────────────────────────────────────
    # 🗂 SHABLON VA KARTA GENERATORLARI
    # ─────────────────────────────────────────────────────────────────────────────

    def send_verification_template(self, chat_id: int, item: Dict[str, Any]) -> None:
        """Verifikatsiya so'rovi shablonini bir bosishda nusxalanadigan formatda yuborish."""
        verif_text = build_verification_text(item)
        nomi = item.get("m", "Tashkilot")
        inn = str(item.get("inn", "")).strip()

        msg = (
            f"🛡 <b>Verifikatsiya Shabloni ({html.escape(nomi)}):</b>\n\n"
            f"👇 <i>Nusxalash uchun quyidagi matn ustiga bosing (1-bosishda nusxalanadi 📲):</i>\n\n"
            f"<pre>{html.escape(verif_text)}</pre>"
        )

        is_mahalla = any(w in str(item.get("s", "")).lower() or w in str(item.get("m", "")).lower() for w in ["mahalla", "mfy"])
        second_row = [{"text": "🔑 Kabinetga Dostup", "callback_data": f"cab:{inn}"}]
        if is_mahalla:
            second_row.append({"text": "🏘 Mahalla 'Yettiligi'", "callback_data": f"mah:{inn}"})
        else:
            second_row.append({"text": "🏢 Tashkilot Kartasi", "callback_data": f"org:{inn}"})

        reply_markup = {
            "inline_keyboard": [
                [
                    {
                        "text": "📋 Bir Bosishda Nusxalash",
                        "copy_text": {"text": verif_text}
                    }
                ],
                second_row
            ]
        }
        self.send_message(chat_id, msg, reply_markup=reply_markup)

    def send_cabinet_template(self, chat_id: int, item: Dict[str, Any]) -> None:
        """Kabinetga dostup shablonini bir bosishda nusxalanadigan formatda yuborish."""
        cab_text = build_cabinet_access_text(item)
        nomi = item.get("m", "Tashkilot")
        inn = str(item.get("inn", "")).strip()

        msg = (
            f"🔑 <b>Kabinetga Dostup Shabloni ({html.escape(nomi)}):</b>\n\n"
            f"👇 <i>Nusxalash uchun quyidagi matn ustiga bosing (1-bosishda nusxalanadi 📲):</i>\n\n"
            f"<pre>{html.escape(cab_text)}</pre>"
        )

        is_mahalla = any(w in str(item.get("s", "")).lower() or w in str(item.get("m", "")).lower() for w in ["mahalla", "mfy"])
        second_row = [{"text": "🛡 Verifikatsiya Shabloni", "callback_data": f"verif:{inn}"}]
        if is_mahalla:
            second_row.append({"text": "🏘 Mahalla 'Yettiligi'", "callback_data": f"mah:{inn}"})
        else:
            second_row.append({"text": "🏢 Tashkilot Kartasi", "callback_data": f"org:{inn}"})

        reply_markup = {
            "inline_keyboard": [
                [
                    {
                        "text": "📋 Bir Bosishda Nusxalash",
                        "copy_text": {"text": cab_text}
                    }
                ],
                second_row
            ]
        }
        self.send_message(chat_id, msg, reply_markup=reply_markup)

    def send_organization_card(self, chat_id: int, item: Dict[str, Any], other_matches: Optional[List[Dict[str, Any]]] = None) -> None:
        """Tashkilot to'liq kartochkasi va interaktiv amallar tugmalarini chiqarish."""
        nomi = html.escape(str(item.get("m", "-")).strip())
        toifa = html.escape(str(item.get("s", "-")).strip())
        rahbar = html.escape(str(item.get("f", "-")).strip())
        tel = html.escape(str(item.get("t", "-")).strip())
        inn = html.escape(str(item.get("inn", "-")).strip())
        raw_inn = str(item.get("inn", "")).strip()
        raw_nomi = str(item.get("m", "")).strip()

        # Toifa va lavozimni chiroyli ko'rsatish
        is_mahalla = any(w in toifa.lower() or w in raw_nomi.lower() for w in ["mahalla", "mfy"])
        if is_mahalla and toifa.lower() in ("mahalla", "rais"):
            lavozim_title = "👑 <b>Mahalla Raisi</b>"
        elif "maktab" in toifa.lower() or "maktab" in raw_nomi.lower():
            lavozim_title = "🎓 <b>Maktab Direktori</b>"
        elif any(w in toifa.lower() or w in raw_nomi.lower() for w in ["bog", "mtt"]):
            lavozim_title = "👶 <b>Bog'cha Mudirasi</b>"
        elif "hokim" in toifa.lower():
            lavozim_title = "💼 <b>Hokim yordamchisi</b>"
        else:
            lavozim_title = f"👤 <b>{toifa}</b>" if toifa and toifa != "-" else "👤 <b>Mas'ul rahbar</b>"

        card_lines = [
            f"🏛 <b>{nomi}</b>",
            "━━━━━━━━━━━━━━━━━━━━",
            f"📌 <b>Toifasi:</b> {toifa}",
            f"{lavozim_title}: {rahbar}",
            f"📞 <b>Bog'lanish:</b> <code>{tel}</code>",
            f"🆔 <b>INN:</b> <code>{inn}</code>",
        ]

        if item.get("jshr"):
            card_lines.append(f"🔢 <b>JSHSHIR:</b> <code>{html.escape(str(item.get('jshr')))}</code>")

        # Shartnoma & Buxgalteriya bloki (faqat mavjud bo'lsa)
        has_contract = bool(item.get("bux_tel") or item.get("aparat_soni") or item.get("ulangan_soni"))
        if has_contract:
            card_lines.append("────────────────────")
            card_lines.append("📑 <b>Shartnoma & Buxgalteriya:</b>")
            if item.get("bux_tel"):
                card_lines.append(f"  • Buxgalter: <code>{html.escape(str(item.get('bux_tel')))}</code>")
            if item.get("aparat_soni"):
                card_lines.append(f"  • Apparat shtat birligi: <b>{item.get('aparat_soni')} ta</b>")
            if item.get("ulangan_soni"):
                card_lines.append(f"  • Ulangan litsenziyalar: <b>{item.get('ulangan_soni')} ta</b>")

        if is_mahalla:
            card_lines.append("────────────────────")
            card_lines.append("👥 <b>Mahalla 'Yettiligi':</b> 7 ta mas'ul xodim biriktirilgan")

        if item.get("izoh"):
            card_lines.append(f"📝 <i>Izoh: {html.escape(str(item.get('izoh')))}</i>")

        # Boshqa mos kelgan turdosh tashkilotlar (haqiqatan boshqa tashkilotlar)
        if other_matches:
            cur_norm_name = normalize_text(raw_nomi)
            cur_digits = "".join(filter(str.isdigit, raw_inn))
            seen = {(cur_norm_name, cur_digits)}
            real_others = []
            for o in other_matches:
                o_n = normalize_text(o.get("m", ""))
                o_d = "".join(filter(str.isdigit, str(o.get("inn", ""))))
                if (o_n, o_d) not in seen:
                    seen.add((o_n, o_d))
                    real_others.append(o)

            if real_others:
                card_lines.append("\n🔍 <b>Shuningdek topildi:</b>")
                for other in real_others[:3]:
                    o_m = html.escape(str(other.get('m', '-')))
                    o_inn = html.escape(str(other.get('inn', '-')))
                    raw_o_inn = str(other.get('inn', '')).strip()
                    card_lines.append(f"• {o_m} (<code>{o_inn}</code>) → /verif_{raw_o_inn}")

        card = "\n".join(card_lines)

        buttons = [
            [
                {"text": "🛡 Verifikatsiya Shabloni", "callback_data": f"verif:{raw_inn}"},
                {"text": "🔑 Kabinetga Dostup", "callback_data": f"cab:{raw_inn}"}
            ]
        ]

        if is_mahalla:
            buttons.append([{"text": "🏘 7 ta Mas'ulni Ko'rish (Yettilik)", "callback_data": f"mah:{raw_inn}"}])

        reply_markup = {"inline_keyboard": buttons}
        self.send_message(chat_id, card, reply_markup=reply_markup)

    def send_mahalla_staff(self, chat_id: int, query: str) -> None:
        """Mahalla yettiligi xodimlarini professional, toza ko'rinishda chiqarish."""
        data = getattr(self.data_manager, "data", []) if self.data_manager else []
        q = str(query or "").strip()

        # 1. Agar query INN bo'lsa, avval INN bo'yicha mahalla nomini aniqlash
        m_name = ""
        item = self._find_first(q)
        if item:
            m_name = item.get("m", "")
        if not m_name:
            m_name = q

        norm_m = normalize_text(m_name)
        matches = [i for i in data if norm_m in normalize_text(i.get("m", ""))]
        if not matches and q:
            matches = [i for i in data if normalize_text(q) in normalize_text(i.get("m", ""))]

        if matches:
            mahalla_display = matches[0].get("m", m_name)
            common_inn = str(matches[0].get("inn", "-")).strip()

            role_order = {
                "mahalla": 1,
                "rais": 1,
                "hokim": 2,
                "yoshlar": 3,
                "xotin": 4,
                "profilaktika": 5,
                "soliq": 6,
                "ijtimoiy": 7
            }
            def role_sort_key(m_row):
                s_lower = str(m_row.get("s", "")).lower()
                for k, v in role_order.items():
                    if k in s_lower:
                        return v
                return 99

            sorted_matches = sorted(matches[:7], key=role_sort_key)

            lines = [
                f"🏘 <b>{html.escape(mahalla_display)} — Mahalla 'Yettiligi'</b>",
                "━━━━━━━━━━━━━━━━━━━━",
                f"🆔 <b>Umumiy INN:</b> <code>{common_inn}</code>\n"
            ]

            role_icons = {
                "mahalla": ("👑", "Mahalla Raisi"),
                "rais": ("👑", "Mahalla Raisi"),
                "hokim": ("💼", "Hokim yordamchisi"),
                "yoshlar": ("🎯", "Yoshlar yetakchisi"),
                "xotin": ("🌸", "Xotin-qizlar faoli"),
                "profilaktika": ("👮‍♂️", "Profilaktika inspektori"),
                "soliq": ("💰", "Soliq inspektori"),
                "ijtimoiy": ("🤝", "Ijtimoiy xodim"),
            }

            for m in sorted_matches:
                lavozim_raw = str(m.get("s", "-")).strip()
                lavozim_lower = lavozim_raw.lower()
                icon = "👤"
                display_role = lavozim_raw

                for key, (ic, title) in role_icons.items():
                    if key in lavozim_lower:
                        icon = ic
                        display_role = title
                        break

                fio = html.escape(str(m.get("f", "-")).strip())
                tel = html.escape(str(m.get("t", "-")).strip())

                lines.append(f"{icon} <b>{display_role}:</b>")
                lines.append(f"   👤 {fio}")
                lines.append(f"   📞 <code>{tel}</code>\n")

            res = "\n".join(lines).strip()

            reply_markup = {
                "inline_keyboard": [
                    [
                        {"text": "🛡 Verifikatsiya Shabloni", "callback_data": f"verif:{common_inn}"},
                        {"text": "🔑 Kabinetga Dostup", "callback_data": f"cab:{common_inn}"}
                    ],
                    [
                        {"text": "🔙 MFYlar Ro'yxati", "callback_data": "cat:mfy:0"},
                        {"text": "🔍 Qidiruv", "callback_data": "menu:search"}
                    ]
                ]
            }
            self.send_message(chat_id, res, reply_markup=reply_markup)
        else:
            self.send_message(chat_id, f"❌ '<code>{html.escape(query)}</code>' mahallasi topilmadi.")

    def _find_first(self, query: str) -> Optional[Dict[str, Any]]:
        """Qidiruv so'zi (INN, nom yoki F.I.SH) bo'yicha aniq tashkilotni O(1) topish."""
        if not query:
            return None
        q = query.strip()
        if "_" in q:
            q = q.split("_")[-1].strip()

        # Keshni tekshirish
        if not self._inn_cache:
            self._build_cache()

        # 1. Aniq INN bo'yicha O(1) qidiruv
        q_digits = "".join(filter(str.isdigit, q))
        if q_digits and len(q_digits) >= 7:
            if q_digits in self._inn_cache:
                return self._inn_cache[q_digits]

        data = getattr(self.data_manager, "data", []) if self.data_manager else []
        if not data:
            return None

        # 2. SearchService orqali aqlli qidiruv
        results = SearchService.search(data, query=q)
        if results:
            q_norm = normalize_text(q)
            exact_matches = [
                r for r in results
                if normalize_text(r.get("m", "")) == q_norm or normalize_text(str(r.get("inn", ""))) == q_norm
            ]
            candidates = exact_matches if exact_matches else results
            return max(candidates, key=get_role_priority)

        return None


_bot_singleton_instance: Optional[TelegramBotService] = None

def get_telegram_bot_service(data_manager: Any = None, token: Optional[str] = None) -> TelegramBotService:
    """TelegramBotService uchun yagona namuna (Singleton) olish."""
    global _bot_singleton_instance
    if _bot_singleton_instance is None or token or data_manager:
        _bot_singleton_instance = TelegramBotService(data_manager, token)
    return _bot_singleton_instance
