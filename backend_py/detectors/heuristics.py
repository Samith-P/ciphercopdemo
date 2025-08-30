import re
import tldextract
from urllib.parse import urlparse
from utils.text import contains_login_words

PUNYCODE = "xn--"

class HeuristicResult(dict): pass

def url_risk(url: str, page_text: str = "") -> HeuristicResult:
    p = urlparse(url)
    host = p.hostname or ""
    ext = tldextract.extract(url)
    registered = ".".join([ext.domain, ext.suffix]) if ext.suffix else ext.domain
    subdomain = ext.subdomain or ""

    risk = 0
    signals = {}

    if PUNYCODE in host: risk += 20; signals["punycode"] = True
    if re.search(r"\d+\.\d+\.\d+\.\d+", host): risk += 25; signals["ip_in_host"] = True
    if host.count("-") >= 3: risk += 10; signals["many_hyphens"] = True
    if len(subdomain) > 30: risk += 10; signals["long_subdomain"] = True
    if contains_login_words(page_text): risk += 10; signals["login_words"] = True

    return HeuristicResult({
        "risk": min(risk, 100),
        "host": host,
        "registered_domain": registered,
        "subdomain": subdomain,
        "signals": signals,
    })

def brand_mismatch_score(brand: str, detected_brand: str, domain: str, allowed_domains: list[str]) -> int:
    if not detected_brand: return 0
    if domain in allowed_domains: return 0
    return 80  # brand detected but wrong domain
