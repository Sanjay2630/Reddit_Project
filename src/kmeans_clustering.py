import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pymongo
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://sandhiyag21102003:sanjayh@cluster0.yzw85.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["reddit_data"]
sentiment_collection = db["sentiment_analysis"]

def kmeans_with_sentiment(n_clusters=3):
    """Perform K-Means clustering using sentiment scores and other features."""
    # Fetch processed data
    posts = list(sentiment_collection.find())
    if not posts:
        print("No processed data available.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(posts)

    # Ensure necessary columns exist
    if not all(col in df.columns for col in ["sentiment_scores", "upvotes", "score", "comments"]):
        print("Missing required columns in the dataset.")
        return

    # Extract sentiment scores and other numerical features
    df["compound"] = df["sentiment_scores"].apply(lambda x: x.get("compound", 0))
    df["positive"] = df["sentiment_scores"].apply(lambda x: x.get("pos", 0))
    df["neutral"] = df["sentiment_scores"].apply(lambda x: x.get("neu", 0))
    df["negative"] = df["sentiment_scores"].apply(lambda x: x.get("neg", 0))

    features = df[["compound", "positive", "neutral", "negative", "upvotes", "score", "comments"]]

    # Standardize features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Apply K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(scaled_features)

    # Visualize clusters with PCA
    pca = PCA(n_components=2)
    reduced_features = pca.fit_transform(scaled_features)
    df["pca_x"] = reduced_features[:, 0]
    df["pca_y"] = reduced_features[:, 1]

    plt.figure(figsize=(10, 6))
    for cluster in range(n_clusters):
        cluster_data = df[df["cluster"] == cluster]
        plt.scatter(cluster_data["pca_x"], cluster_data["pca_y"], label=f"Cluster {cluster}")
    plt.title("K-Means Clustering with Sentiment Features (PCA Reduced)")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend()
    plt.show()

    # Save clusters to MongoDB
    clustered_collection = db["clustered_posts"]
    clustered_collection.delete_many({})  # Clear existing data
    clustered_collection.insert_many(df.to_dict("records"))

    print(f"Clustering complete. Results saved to 'clustered_posts' collection.")

if __name__ == "__main__":
    kmeans_with_sentiment(n_clusters=3)
