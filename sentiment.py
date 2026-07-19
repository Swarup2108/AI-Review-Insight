from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(text):

    result = classifier(text)[0]

    label = result["label"]
    score = round(result["score"] * 100, 2)

    if label.lower() == "positive":
        emoji = "😊"
        sentiment = "Positive"

    elif label.lower() == "neutral":
        emoji = "😐"
        sentiment = "Neutral"

    else:
        emoji = "😞"
        sentiment = "Negative"

    return {
        "emoji": emoji,
        "label": sentiment,
        "score": score
    }