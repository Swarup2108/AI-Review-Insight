from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
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