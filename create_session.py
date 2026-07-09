"""Telethon StringSession yaratish skripti.

Ishga tushirish:
    python create_session.py

Telefon raqamingizni kiriting, SMS kodini kiriting.
Oxirida StringSession matni chiqadi — uni GitHub Secrets ga
TG_SESSION_STRING nomi bilan saqlang.
"""
import asyncio
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH", "")

if not API_ID or not API_HASH:
    print("XATO: .env faylida TG_API_ID va TG_API_HASH bo'lishi kerak!")
    exit(1)


async def main():
    print("Telethon StringSession yaratish...")
    print(f"API_ID: {API_ID}")
    print()

    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        session_string = client.session.save()
        print("\n" + "=" * 60)
        print("STRING SESSION (GitHub Secrets ga saqlang):")
        print("=" * 60)
        print(session_string)
        print("=" * 60)
        print("\nBu qatorni nusxalab GitHub -> Settings -> Secrets -> Actions ->")
        print("New secret -> Name: TG_SESSION_STRING ga kiriting.")


asyncio.run(main())
