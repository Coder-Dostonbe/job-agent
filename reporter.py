"""Kunlik hisobotni Telegram botga yuborish."""
import logging
import requests

import config

log = logging.getLogger("reporter")

VERDICT_EMOJI = {
    "topshirish_kerak": "🟢",
    "urinib_korish": "🟡",
    "vaqt_sarflamaslik": "🔴",
}


def build_report(scored: list[dict], stats: dict, total_new: int) -> str:
    lines = [f"📊 <b>Kunlik ish hisoboti</b>\n"
             f"Yangi vakansiyalar: {total_new} ta, mos kelganlari: {len(scored)} ta\n"]

    for i, v in enumerate(scored[:10], 1):
        ai = v.get("ai")
        emoji = VERDICT_EMOJI.get(ai["verdict"], "⚪") if ai else "⚪"
        lines.append(f"{emoji} <b>{i}. {v['title'][:70]}</b>")
        meta = " | ".join(filter(None, [v["source"], v["company"], v["salary"]]))
        if meta:
            lines.append(f"   {meta}")
        if ai:
            lines.append(f"   AI: {ai['score']}/100 — {ai['reason']}")
            lines.append(f"   💡 CV: {ai['cv_tip']}")
        else:
            lines.append(f"   Keyword ball: {v['score']}/100")
        lines.append(f"   {v['url']}\n")

    if stats:
        top = ", ".join(f"{k} ({n})" for k, n in list(stats.items())[:8])
        lines.append(f"📈 <b>Bugun eng ko'p so'ralgan skillar:</b> {top}")

    return "\n".join(lines)


def send(text: str) -> None:
    if not (config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID):
        log.warning("Bot token/chat_id yo'q — hisobot konsolga chiqarildi:\n%s", text)
        return
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    # Telegram limiti 4096 belgi — bo'lib yuboramiz
    for chunk_start in range(0, len(text), 4000):
        chunk = text[chunk_start:chunk_start + 4000]
        try:
            requests.post(url, json={
                "chat_id": config.TELEGRAM_CHAT_ID,
                "text": chunk,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            }, timeout=15)
        except Exception as e:
            log.error("Telegram yuborishda xato: %s", e)
