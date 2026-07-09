# Job Search Agent 🤖

Har kuni hh.uz, Telegram kanallar va OLX'dan vakansiyalarni yig'ib, Doston profiliga
moslik balini hisoblaydi (keyword + Claude AI) va Telegram'ga hisobot yuboradi.

## O'rnatish

```bash
pip install -r requirements.txt
```

## Kalitlarni olish (.env.example → .env)

1. **TELEGRAM_BOT_TOKEN** — @BotFather'da yangi bot yarating
2. **TELEGRAM_CHAT_ID** — botingizga xabar yozing, keyin brauzerda oching:
   `https://api.telegram.org/bot<TOKEN>/getUpdates` — `chat.id` ni ko'rasiz
3. **TG_API_ID / TG_API_HASH** — https://my.telegram.org → API development tools
4. **ANTHROPIC_API_KEY** — https://console.anthropic.com (ixtiyoriy; bo'lmasa
   faqat keyword scoring ishlaydi, agent baribir to'liq ishlayveradi)

## Birinchi ishga tushirish

```bash
python main.py
```

Telethon birinchi safar telefon raqam va kod so'raydi — bu bir marta,
keyin `agent.session` fayli saqlanadi. **Muhim:** Railway'ga deploy qilishdan
oldin sessionni lokalda yaratib, faylni loyiha bilan birga yuklang.

## Sozlash (config.py)

- `TG_CHANNELS` — o'zingiz kuzatadigan ish kanallarini qo'shing/o'zgartiring
- `SEARCH_QUERIES` — qidiruv so'zlari
- `AI_MAX_VACANCIES` — kunlik AI tahlil limiti (xarajat nazorati)

## Railway'da har kuni avtomatik ishlatish

1. GitHub'ga push qiling, Railway'da yangi loyiha yarating
2. Variables bo'limiga .env dagi kalitlarni kiriting
3. Settings → Cron Schedule: `0 4 * * *` (har kuni 09:00 Toshkent vaqti)
4. Start command: `python main.py`

## Hisobot namunasi

```
📊 Kunlik ish hisoboti
Yangi vakansiyalar: 14 ta, mos kelganlari: 4 ta

🟢 1. Junior Python Developer
   hh.uz | FinTech LLC | 5000000–8000000 UZS
   AI: 82/100 — Django va DRF talab qilinadi, tajriba talabi past.
   💡 CV: Fezot Shop production loyihangizni birinchi qatorga chiqaring
   https://hh.uz/vacancy/...

📈 Bugun eng ko'p so'ralgan skillar: python (11), django (7), docker (5)...
```
