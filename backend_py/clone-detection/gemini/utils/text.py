import re
from bs4 import BeautifulSoup

LOGIN_WORDS = {"login", "log in", "sign in", "password", "account", "verify"}

def extract_text_snippet(html: str, limit=2000):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text[:limit]

def contains_login_words(text: str) -> bool:
    low = text.lower()
    return any(w in low for w in LOGIN_WORDS)
