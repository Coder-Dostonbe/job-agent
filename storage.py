"""SQLite: ko'rilgan vakansiyalarni saqlash — bir vakansiya ikki marta hisobotga tushmaydi."""
import sqlite3
from datetime import datetime

import config


def _conn():
    conn = sqlite3.connect(config.DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            url TEXT PRIMARY KEY,
            source TEXT,
            title TEXT,
            score INTEGER,
            ai_score INTEGER,
            first_seen TEXT
        )
    """)
    return conn


def filter_new(vacancies: list[dict]) -> list[dict]:
    """Faqat oldin ko'rilmagan vakansiyalarni qaytaradi."""
    conn = _conn()
    seen = {row[0] for row in conn.execute("SELECT url FROM vacancies")}
    conn.close()
    unique, out = set(), []
    for v in vacancies:
        if v["url"] and v["url"] not in seen and v["url"] not in unique:
            unique.add(v["url"])
            out.append(v)
    return out


def save(vacancies: list[dict]) -> None:
    conn = _conn()
    now = datetime.now().isoformat()
    for v in vacancies:
        conn.execute(
            "INSERT OR IGNORE INTO vacancies VALUES (?,?,?,?,?,?)",
            (v["url"], v["source"], v["title"],
             v.get("score", 0), v.get("ai", {}).get("score", 0) if v.get("ai") else 0, now),
        )
    conn.commit()
    conn.close()


def skill_stats(vacancies: list[dict]) -> dict[str, int]:
    """Bugungi vakansiyalarda qaysi skill necha marta so'ralgani — CV maslahat uchun."""
    track = ["python", "django", "fastapi", "flask", "postgresql", "docker",
             "redis", "celery", "linux", "git", "rest", "javascript", "react",
             "kubernetes", "aws", "английск", "english"]
    counts = {}
    for v in vacancies:
        text = f"{v['title']} {v['text']}".lower()
        for s in track:
            if s in text:
                counts[s] = counts.get(s, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))
