from flask import Flask, render_template, request, redirect, url_for
from sentiment import analyze_sentiment
from database import collection
from bson import ObjectId
from datetime import datetime
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# ---------------- HOME ---------------- #
@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    review = ""

    if request.method == "POST":

        review = request.form.get("review", "")

        if review.strip():

            result = analyze_sentiment(review)

            collection.insert_one({
                "review": review,
                "sentiment": result["label"],
                "confidence": result["score"],
                "date": datetime.now().strftime("%d-%m-%Y %H:%M")
            })

    return render_template(
        "index.html",
        prediction=result["label"] if result else None,
        confidence=round(result["score"], 2) if result else None,
        review=review
    )
# ---------------- HISTORY ---------------- #

@app.route("/history")
def history():

    history = list(collection.find().sort("_id", -1))

    total = len(history)

    positive = sum(1 for r in history if r["sentiment"] == "Positive")
    negative = sum(1 for r in history if r["sentiment"] == "Negative")

    return render_template(
        "history.html",
        history=history,
        total=total,
        positive=positive,
        negative=negative
    )

# ---------- DELETE REVIEW ---------- #

@app.route("/delete/<id>")
def delete_review(id):

    collection.delete_one(
        {"_id": ObjectId(id)}
    )

    return redirect(url_for("history"))


# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    reviews = list(collection.find())

    total = len(reviews)

    positive = sum(
        1 for r in reviews
        if r["sentiment"] == "Positive"
    )

    negative = sum(
        1 for r in reviews
        if r["sentiment"] == "Negative"
    )

    if total > 0:
        avg_confidence = round(
            sum(r["confidence"] for r in reviews) / total,
            2
        )
    else:
        avg_confidence = 0

    df = pd.DataFrame({
        "Sentiment": ["Positive", "Negative"],
        "Count": [positive, negative]
    })

    pie = px.pie(
        df,
        values="Count",
        names="Sentiment",
        title="",
        color="Sentiment",
        color_discrete_map={
            "Positive": "#22c55e",
            "Negative": "#ef4444"
        }
    )

    pie.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=14)
    )

    bar = px.bar(
        df,
        x="Sentiment",
        y="Count",
        text="Count",
        title="",
        color="Sentiment",
        color_discrete_map={
            "Positive": "#22c55e",
            "Negative": "#ef4444"
        }
    )

    bar.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(size=14)
    )

    return render_template(
        "dashboard.html",
        total=total,
        positive=positive,
        negative=negative,
        avg=avg_confidence,
        pie_chart=pie.to_html(full_html=False),
        bar_chart=bar.to_html(full_html=False),
        history=reviews
    )

# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)