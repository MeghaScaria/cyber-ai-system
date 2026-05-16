from app.services.url_ml_service import predict_url

print("\n--- TEST ---\n")

print("Google:", predict_url("https://google.com"))
print("Bitly:", predict_url("http://bit.ly/verify-account"))
print("Fraud:", predict_url("http://free-money-now.com"))