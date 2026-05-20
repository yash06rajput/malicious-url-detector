import re
import numpy as np
import tldextract
from scipy.sparse import csr_matrix


SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "secure",
    "update",
    "account",
    "bank",
    "paypal",
    "signin",
    "password",
    "confirm",
    "webscr",
    "ebayisapi",
    "wallet",
    "billing",
    "auth",
    "token",
    "admin",
    "invoice",
    "free",
    "bonus",
    "win",
    "gift"
]


SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "t.co",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "cutt.ly",
    "rebrand.ly"
]


def has_ip_address(url):
    """
    Detect raw IP address in URL
    """
    ip_pattern = r"(?:\d{1,3}\.){3}\d{1,3}"
    return 1 if re.search(ip_pattern, url) else 0


def count_suspicious_keywords(url):
    """
    Count suspicious phishing-related keywords
    """
    url_lower = url.lower()
    return sum(1 for keyword in SUSPICIOUS_KEYWORDS if keyword in url_lower)


def is_shortened_url(url):
    """
    Detect URL shorteners
    """
    url_lower = url.lower()
    return 1 if any(shortener in url_lower for shortener in SHORTENERS) else 0


def shannon_entropy(text):
    """
    Rough lexical entropy
    """
    if not text:
        return 0

    probabilities = [
        float(text.count(char)) / len(text)
        for char in set(text)
    ]

    entropy = -sum(
        p * np.log2(p)
        for p in probabilities
    )

    return entropy


def extract_url_features(url):
    """
    Extract engineered numeric features
    Returns scipy sparse matrix row
    """
    extracted = tldextract.extract(url)

    domain = extracted.domain or ""
    subdomain = extracted.subdomain or ""
    suffix = extracted.suffix or ""

    features = [
        len(url),                               # total length
        len(domain),                            # domain length
        len(subdomain),                         # subdomain length
        len(suffix),                            # TLD length
        url.count("."),                         # dot count
        url.count("-"),                         # hyphen count
        url.count("_"),                         # underscore count
        url.count("/"),                         # slash count
        url.count("?"),                         # query symbols
        url.count("="),                         # equals signs
        url.count("&"),                         # ampersands
        url.count("%"),                         # encoded chars
        sum(c.isdigit() for c in url),         # digit count
        sum(c.isalpha() for c in url),         # alpha count
        count_suspicious_keywords(url),         # phishing keywords
        has_ip_address(url),                    # IP usage
        1 if "https" in url.lower() else 0,    # HTTPS present
        is_shortened_url(url),                  # URL shortener
        shannon_entropy(url),                   # lexical randomness
        len(subdomain.split(".")) if subdomain else 0
    ]

    return csr_matrix([features])