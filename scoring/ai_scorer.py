"""2-bosqich: eng yaxshi vakansiyalarni Claude API bilan chuqur tahlil qilish."""
import json
import logging
import requests

import config

log = logging.getLogger("ai")
API_URL = "https://api.anthropic.com/v1/messages"

PROMPT = """Sen ish qidiruv bo'yicha maslahatchi agentsan. Quyida nomzod profili va bitta vakansiya bor.

NOMZOD PROFILI:
{profile}

VAKANSIYA:
Sarlavha: {title}
Kompaniya: {company}
Tajriba talabi: {experience}
Matn: {text}

Vazifa: nomzod shu vakansiyaga topshirsa, suhbatga chaqirilish ehtimolini baholab ber.
FAQAT quyidagi JSON formatida javob ber, boshqa hech narsa yozma:
{{"score": 0-100 oralig'ida son, "verdict": "topshirish_kerak" yoki "urinib_korish" yoki "vaqt_sarflamaslik", "reason": "1-2 jumlada o'zbekcha sabab", "cv_tip": "shu vakansiya uchun CV'da nimani ta'kidlash kerak, 1 jumla"}}"""


def analyze(vacancy: dict) -> dict | None:
    if not config.ANTHROPIC_API_KEY:
        return None
    try:
        resp = requests.post(
            API_URL,
            headers={
                "x-api-key": config.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-haiku-4-5-20251001",  # arzon va tez — bu vazifaga yetarli
                "max_tokens": 300,
                "messages": [{
                    "role": "user",
                    "content": PROMPT.format(
                        profile=config.PROFILE["summary"],
                        title=vacancy["title"],
                        company=vacancy["company"] or "noma'lum",
                        experience=vacancy["experience"] or "ko'rsatilmagan",
                        text=vacancy["text"][:2000],
                    ),
                }],
            },
            timeout=30,
        )
        resp.raise_for_status()
        raw = resp.json()["content"][0]["text"]
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except Exception as e:
        log.error("AI tahlilda xato (%s): %s", vacancy["title"][:40], e)
        return None
