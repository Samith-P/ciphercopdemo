import ipaddress, socket, re
from urllib.parse import urlparse

PRIVATE_NETS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
]

HOST_REGEX = re.compile(r"^[A-Za-z0-9.-]+$")

class UrlError(ValueError): pass

def is_private_ip(ip: str) -> bool:
    try: ipa = ipaddress.ip_address(ip)
    except ValueError: return False
    return any(ipa in net for net in PRIVATE_NETS)

def guard_url(url: str) -> str:
    # Normalize URL - add https:// if no scheme provided
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    p = urlparse(url)
    if p.scheme not in {"http", "https"}: 
        raise UrlError("Only http/https allowed")
    if not p.hostname or not HOST_REGEX.match(p.hostname): 
        raise UrlError("Invalid hostname")
    
    try:
        infos = socket.getaddrinfo(p.hostname, None)
        for info in infos:
            ip = info[4][0]
            if is_private_ip(ip): 
                raise UrlError("Target resolves to private IP")
    except socket.gaierror:
        raise UrlError("DNS resolution failed")
    
    return url
