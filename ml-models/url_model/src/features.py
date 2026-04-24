import re
from urllib.parse import urlparse

def extract_features(url: str):

    if not url.startswith("http"):
        url = "http://" + url

    p = urlparse(url)
    domain = p.netloc
    path = p.path

    words_host = [w for w in domain.split(".") if w]
    words_path = [w for w in path.split("/") if w]

    return {
        "google_index": 1,

        "ratio_digits_url": sum(c.isdigit() for c in url) / max(len(url), 1),

        "domain_in_title": 0,  # cannot extract without page content

        "phish_hints": int(any(w in url for w in [
            "login", "verify", "secure", "update", "account"
        ])),

        "ip": int(bool(re.match(r"\d+\.\d+\.\d+\.\d+", domain))),

        "nb_qm": url.count("?"),

        "length_url": len(url),

        "nb_slash": url.count("/"),

        "length_hostname": len(domain),

        "nb_eq": url.count("="),

        "ratio_digits_host": sum(c.isdigit() for c in domain) / max(len(domain), 1),

        "shortest_word_host": min([len(w) for w in words_host] or [0]),

        "prefix_suffix": int("-" in domain),

        "longest_word_path": max([len(w) for w in words_path] or [0]),

        "tld_in_subdomain": int(len(words_host) > 2),
    }