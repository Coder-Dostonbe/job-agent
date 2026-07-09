"""OLX.uz dan e'lonlarni scraping qilish.

Ogohlantirish: OLX'da rasmiy API yo'q, sayt tuzilishi o'zgarsa selectorlar
sinishi mumkin. Xato bo'lsa agent yiqilmaydi — shunchaki bu manba bo'sh qaytadi.
"""
import logging
import requests
from bs4 import BeautifulSoup

import config

log = logging.getLogger("olx")
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    )
}


def _parse_page(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = []
    # OLX kartochkalari odatda data-cy="l-card" atributi bilan keladi
    for card in soup.select('[data-cy="l-card"]'):
        link = card.select_one("a[href]")
        title = card.select_one("h4, h6")
        if not (link and title):
            continue
        href = link["href"]
        if href.startswith("/"):
            href = "https://www.olx.uz" + href
        items.append({
            "source": "olx.uz",
            "url": href.split("#")[0],
            "title": title.get_text(strip=True),
            "company": "",
            "salary": "",
            "experience": "",
            "text": card.get_text(" ", strip=True)[:800],
            "published_at": "",
        })
    return items


def collect() -> list[dict]:
    results = []
    for url in config.OLX_URLS:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            found = _parse_page(resp.text)
            log.info("OLX %s: %d ta e'lon", url.split("?q=")[-1], len(found))
            results.extend(found)
        except Exception as e:
            log.error("OLX xato (%s): %s", url, e)
    return results
