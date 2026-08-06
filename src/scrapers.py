"""
Scrapers module - best-effort scraping adapters for primary leagues.
This module contains initial implementations and placeholders for scraping odds and
match details from public websites. Web scraping is brittle and may fail for
some sites due to JS rendering or anti-bot measures. This is a starting point
and will be expanded for robustness.

Priority leagues: English Premier League, LaLiga, Bundesliga, Serie A, Ligue 1
"""
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; RedChild-GPT-WCM/1.0; +https://github.com/huibuliuqiu-a)'
}


def _safe_get(url, timeout=10):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        if r.status_code == 200:
            return r.text
    except Exception:
        return None
    return None


def search_flashscore(home, away):
    """Best-effort search Flashscore for a match page. Flashscore uses heavy JS;
    this will only work for simple HTML pages or when Flashscore provides server-side search results.
    Returns page HTML or None.
    """
    q = quote_plus(f"{home} {away}")
    url = f"https://www.flashscore.com/search/?q={q}"
    return _safe_get(url)


def parse_oddsportal(html):
    """Attempt to parse odds from an oddsportal-like page HTML. This is heuristic
    and will often need tuning per site structure.
    Returns a dict: { 'initial': {...}, 'live': {...}, 'history': [...] }
    """
    if not html:
        return None
    soup = BeautifulSoup(html, 'lxml')
    out = {'initial': None, 'live': None, 'history': [], 'source': 'scraping_stub'}
    # Heuristic: find odds tables
    try:
        # Example: look for elements that contain '1.5' style floats, pick first occurrences
        text = soup.get_text()
        floats = re.findall(r"\b\d+\.\d{1,3}\b", text)
        if floats:
            out['initial'] = {'sample_odds': floats[:3]}
    except Exception:
        pass
    return out


def find_match_odds(home, away, competition=None, date=None):
    """High-level function: try several sources for odds and return first usable result.
    Returns dict with keys: initial, live, history, source
    """
    # 1) Try Flashscore search
    html = search_flashscore(home, away)
    res = parse_oddsportal(html)
    if res:
        res['source'] = 'flashscore_scraping'
        return res

    # 2) Try OddsPortal generic search (placeholder URL pattern)
    slug = f"{home}-vs-{away}".lower().replace(' ', '-')
    url = f"https://www.oddsportal.com/search/results/?q={quote_plus(home + ' ' + away)}"
    html2 = _safe_get(url)
    res2 = parse_oddsportal(html2)
    if res2:
        res2['source'] = 'oddsportal_scraping'
        return res2

    # 3) Fallback: return empty structure with source noted
    return {'initial': None, 'live': None, 'history': [], 'source': 'no_scrape_result'}
