from transformers import pipeline

# Pretrained model (fast demo)
classifier = pipeline("text-classification", model="distilbert-base-uncased")

text = "Your account is blocked click now"
result = classifier(text)

print(result)
