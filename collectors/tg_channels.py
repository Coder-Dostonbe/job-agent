"""Telegram ish kanallaridan postlarni o'qish (Telethon, user-akkaunt orqali).

GitHub Actions uchun: TG_SESSION_STRING env var orqali string session ishlatiladi.
Local uchun: 'agent.session' fayli ishlatiladi.
Session yaratish: python create_session.py
"""
import logging
import os
from datetime import datetime, timedelta, timezone

import config

log = logging.getLogger("tg")

KEYWORDS = ["python", "django", "backend", "бэкенд", "бекенд"]


async def collect() -> list[dict]:
    if not (config.TG_API_ID and config.TG_API_HASH):
        log.warning("TG_API_ID/TG_API_HASH yo'q — Telegram collector o'tkazib yuborildi")
        return []

    # Session mavjudligini tekshir
    has_string_session = bool(getattr(config, 'TG_SESSION_STRING', ''))
    has_session_file = os.path.exists("agent.session")

    if not has_string_session and not has_session_file:
        log.warning(
            "Telethon session yo'q (agent.session ham, TG_SESSION_STRING ham). "
            "Telegram kanallar o'tkazib yuborildi."
        )
        return []

    from telethon import TelegramClient
    from telethon.sessions import StringSession

    results = []
    since = datetime.now(timezone.utc) - timedelta(hours=config.TG_LOOKBACK_HOURS)

    if has_string_session:
        session = StringSession(config.TG_SESSION_STRING)
    else:
        session = "agent"

    async with TelegramClient(session, int(config.TG_API_ID), config.TG_API_HASH) as client:
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
