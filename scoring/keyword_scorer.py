"""1-bosqich: tez va bepul keyword scoring (0–100 ball)."""
import config

# Mos keladigan skillar (+ ball)
POSITIVE = {
    "python": 12, "django": 15, "drf": 10, "rest": 6, "api": 4,
    "postgresql": 6, "postgres": 6, "docker": 6, "jwt": 4,
    "backend": 8, "бэкенд": 8, "junior": 12, "джуниор": 12,
    "стажер": 10, "intern": 10, "telegram": 4, "bot": 3,
}

# Mos kelmaydigan talablar (- ball)
NEGATIVE = {
    "senior": -35, "сеньор": -35, "lead": -30, "тимлид": -30,
    "react": -15, "vue": -15, "angular": -15, "node": -15,
    "javascript": -10, "frontend": -12, "фронтенд": -12,
    "php": -20, "laravel": -20, "java ": -20, "c#": -20, ".net": -20,
    "golang": -20, "1с": -25, "5 лет": -20, "4 года": -15,
    "5 years": -20, "middle+": -15,
}


def score(vacancy: dict) -> tuple[int, list[str]]:
    """Ball va sabablar ro'yxatini qaytaradi."""
    text = f"{vacancy['title']} {vacancy['text']}".lower()
    total, reasons = 40, []  # neytral boshlang'ich ball

    for word, pts in POSITIVE.items():
        if word in text:
            total += pts
            reasons.append(f"+{pts} {word}")

    for word, pts in NEGATIVE.items():
        if word in text:
            total += pts
            reasons.append(f"{pts} {word}")

    # Django bor-u, boshqa til asosiy bo'lmasa — kuchli signal
    if "django" in text and "python" in text:
        total += 5
        reasons.append("+5 python+django juftligi")

    return max(0, min(100, total)), reasons
