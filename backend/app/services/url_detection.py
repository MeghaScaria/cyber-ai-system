import re

async def check_urls(message: str):
    urls = re.findall(r'https?://\S+', message)

    suspicious = False

    for url in urls:
        if any(word in url for word in ["login", "verify", "bank", "secure"]):
            suspicious = True

    return {
        "detected": suspicious,
        "urls": urls
    }