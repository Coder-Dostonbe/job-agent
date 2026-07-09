"""Job Search Agent — asosiy fayl.

Ishga tushirish: python main.py
Har kuni cron/Railway orqali avtomatik ishlaydi.
"""
import asyncio
import logging

import config
import storage
import reporter
from collectors import hh, olx, tg_channels
from scoring import keyword_scorer, ai_scorer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
log = logging.getLogger("main")


async def run():
    # 1. YIG'ISH — uchala manba
    vacancies = []
    vacancies += hh.collect()
    vacancies += olx.collect()
    vacancies += await tg_channels.collect()
    log.info("Jami yig'ildi: %d", len(vacancies))

    # 2. YANGILARNI AJRATISH
    new = storage.filter_new(vacancies)
    log.info("Yangi: %d", len(new))
    if not new:
        reporter.send("📊 Bugun yangi mos vakansiya topilmadi.")
        return

    # 3. KEYWORD SCORING
    for v in new:
        v["score"], v["score_reasons"] = keyword_scorer.score(v)
    relevant = sorted(
        (v for v in new if v["score"] >= config.REPORT_MIN_SCORE),
        key=lambda v: -v["score"],
    )

    # 4. AI SCORING — faqat eng yaxshilari (xarajat nazorati)
    for v in relevant[:config.AI_MAX_VACANCIES]:
        if v["score"] >= config.AI_SCORE_THRESHOLD:
            v["ai"] = ai_scorer.analyze(v)

    # AI ball bo'lsa, saralashda ustunlik beramiz
    relevant.sort(key=lambda v: -(v["ai"]["score"] if v.get("ai") else v["score"]))

    # 5. SAQLASH + HISOBOT
    storage.save(new)
    stats = storage.skill_stats(new)
    reporter.send(reporter.build_report(relevant, stats, len(new)))
    log.info("Hisobot yuborildi ✅")


if __name__ == "__main__":
    asyncio.run(run())
