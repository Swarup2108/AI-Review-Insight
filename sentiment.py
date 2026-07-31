from transformers import pipeline

# Lightweight model
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(text):

    result = classifier(text)[0]

    label = result["label"]
    score = round(result["score"] * 100, 2)

    if label == "POSITIVE":
        sentiment = "Positive"
        emoji = "😊"
    else:
        sentiment = "Negative"
        emoji = "😞"

    return {
        "emoji": emoji,
        "label": sentiment,
        "score": score
    }