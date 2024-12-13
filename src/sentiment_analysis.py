import json
import os
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import download
import pymongo

# Download VADER lexicon
download('vader_lexicon')
client = pymongo.MongoClient("mongodb+srv://sandhiyag21102003:sanjayh@cluster0.yzw85.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["reddit_data"]
processed_collection = db["processed_posts"]
sentiment_collection = db["sentiment_analysis"]

def perform_sentiment_analysis():
    input_path = "data/cleaned_data.json"
    output_path = "data/sentiment_data.json"

    # Check if cleaned data exists
    if not os.path.exists(input_path):
        print("No cleaned data found. Please preprocess data first.")
        return

    # Load cleaned data
    with open(input_path, "r", encoding="utf-8") as infile:
        cleaned_data = json.load(infile)

    # Initialize Sentiment Analyzer
    sia = SentimentIntensityAnalyzer()

    # Analyze sentiment for each post
    sentiment_results = []
    for post in cleaned_data:
        title = post["Decrypted Title"]
        sentiment_scores = sia.polarity_scores(title)

        # Determine sentiment category
        if sentiment_scores["compound"] > 0.05:
            sentiment = "Positive"
        elif sentiment_scores["compound"] < -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        # Add sentiment to the post
        post["sentiment"] = sentiment
        post["sentiment_scores"] = sentiment_scores
        sentiment_results.append(post)

    # Save sentiment data
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(sentiment_results, outfile, indent=4)

    print(f"Sentiment analysis completed. Results saved to {output_path}")

    # Save to MongoDB
    sentiment_collection.delete_many({})  # Clear existing data if needed
    sentiment_collection.insert_many(sentiment_results)
    print("Sentiment analysis results saved to MongoDB collection 'sentiment_analysis'.")

if __name__ == "__main__":
    perform_sentiment_analysis()
