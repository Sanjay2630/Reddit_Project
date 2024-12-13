import pymongo
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://sandhiyag21102003:sanjayh@cluster0.yzw85.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["reddit_data"]
collection = db["posts"]

def analyze_data():
    """Analyze the data stored in MongoDB."""
    try:
        db = client["reddit_data"]
        collection = db["posts"]

        # Fetch all posts
        posts = list(collection.find({"cleaned_text": {"$exists": True}}))
        if not posts:
            print("No cleaned data to analyze.")
            return

        # Convert to DataFrame
        df = pd.DataFrame(posts)

        # Combine all text for word cloud
        all_text = " ".join(df["cleaned_text"].dropna().tolist())

        # Generate and display word cloud
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Word Cloud of Reddit Posts")
        plt.show()
    finally:
        client.close()  # Always close the MongoDB client


# Example usage
if __name__ == "__main__":
    analyze_data()
