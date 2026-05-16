import pandas as pd
import random

# 🔥 SAFE DOMAINS
safe_domains = [
    "google.com", "amazon.in", "microsoft.com", "github.com",
    "wikipedia.org", "linkedin.com", "apple.com", "netflix.com",
    "stackoverflow.com", "reddit.com", "whatsapp.com", "flipkart.com",
    "paytm.com", "irctc.co.in", "sbi.co.in", "hdfcbank.com",
    "icicibank.com", "axisbank.com", "adobe.com", "intel.com"
]

# 🔥 FRAUD KEYWORDS
fraud_keywords = [
    "login", "verify", "secure", "update", "account",
    "free", "win", "bonus", "claim", "reward",
    "alert", "bank", "password", "urgent"
]

shorteners = ["bit.ly", "tinyurl.com", "t.co"]

# 🔥 GENERATE SAFE URLs
def generate_safe(n=500):
    urls = []
    for _ in range(n):
        domain = random.choice(safe_domains)
        scheme = random.choice(["https://", "https://", "http://"])
        path = random.choice(["", "/home", "/about", "/products", "/contact"])
        urls.append(f"{scheme}{domain}{path}")
    return urls

# 🔥 GENERATE FRAUD URLs
def generate_fraud(n=500):
    urls = []
    for _ in range(n):
        keyword = random.choice(fraud_keywords)
        domain = f"{keyword}-{random.choice(fraud_keywords)}.com"

        # mix patterns
        if random.random() < 0.3:
            url = f"http://{random.choice(shorteners)}/{keyword}{random.randint(100,999)}"
        elif random.random() < 0.6:
            url = f"http://{domain}/login"
        else:
            url = f"http://{domain}"

        urls.append(url)
    return urls

# 🔥 BUILD DATASET
safe_urls = generate_safe(500)
fraud_urls = generate_fraud(500)

data = []

for u in safe_urls:
    data.append({"url": u, "label": 0})

for u in fraud_urls:
    data.append({"url": u, "label": 1})

# shuffle
random.shuffle(data)

df = pd.DataFrame(data)

# 🔥 SAVE
output_path = "../../data/processed/urls.csv"
df.to_csv(output_path, index=False)

print("✅ Dataset generated:", len(df))
print("📂 Saved at:", output_path)