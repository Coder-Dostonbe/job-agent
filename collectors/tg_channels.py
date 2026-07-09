"""Telegram ish kanallaridan postlarni o'qish (Telethon, user-akkaunt orqali).

Eslatma: oddiy bot kanal tarixini o'qiy olmaydi, shuning uchun Telethon
sizning akkauntingiz bilan ulanadi. Birinchi ishga tushirishda telefon
raqam va kod so'raladi, keyin 'agent.session' fayli saqlanib qoladi.
"""
import logging
from datetime import datetime, timedelta, timezone

import config

log = logging.getLogger("tg")

KEYWORDS = ["python", "django", "backend", "бэкенд", "бекенд"]


async def collect() -> list[dict]:
    if not (config.TG_API_ID and config.TG_API_HASH):
        log.warning("TG_API_ID/TG_API_HASH yo'q — Telegram collector o'tkazib yuborildi")
        return []

    from telethon import TelegramClient  # import shu yerda: creds bo'lmasa kerak emas

    results = []
    since = datetime.now(timezone.utc) - timedelta(hours=config.TG_LOOKBACK_HOURS)

    async with TelegramClient("agent", int(config.TG_API_ID), config.TG_API_HASH) as client:
        for channel in config.TG_CHANNELS:
            try:
                async for msg in client.iter_messages(channel, limit=80):
                    if msg.date < since:
                        break
                    text = (msg.text or "").strip()
                    low = text.lower()
                    if text and any(k in low for k in KEYWORDS):
                        results.append({
                            "source": f"t.me/{channel}",
                            "url": f"https://t.me/{channel}/{msg.id}",
                            "title": text.split("\n")[0][:90],
                            "company": "",
                            "salary": "",
                            "experience": "",
                            "text": text[:1500],
                            "published_at": msg.date.isoformat(),
                        })
            except Exception as e:
                log.error("Kanal o'qishda xato (%s): %s", channel, e)
    log.info("Telegram: %d ta mos post", len(results))
    return results
