import pymongo
from utils import clean_text, decrypt_title, normalize
import pandas as pd
import json

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://sandhiyag21102003:sanjayh@cluster0.yzw85.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["reddit_data"]

raw_collection = db["raw_collection"]  # Collection for raw data
processed_collection = db["processed_posts"]  # Collection for processed data

def preprocess_data():
    """Fetch data from MongoDB, preprocess, and save back to MongoDB."""
    # Fetch all posts
    posts = list(raw_collection.find())
    
    if not posts:
        print("No data to preprocess.")
        return
    
    # Convert to DataFrame for processing
    df = pd.DataFrame(posts)
    
    # Decrypt the title
    df["Decrypted Title"] = df["title"].apply(decrypt_title)

    # Clean the title text
    df["Cleaned Title"] = df["Decrypted Title"].apply(clean_text)

    # Clean the comments
    df["Cleaned Comments"] = df["comments"].apply(lambda x: clean_text(x) if isinstance(x, str) else x)

    # Normalize numerical fields
    df["Normalized Upvotes"] = normalize(df["upvotes"].astype(float))

    # Prepare the processed data for MongoDB
    processed_data = []
    for _, row in df.iterrows():
        processed_data.append({
            "title": row["Decrypted Title"],
            "author": row["author"],
            "comments": row["comments"],
            "cleaned_title": row["Cleaned Title"],
            "cleaned_comments": row["Cleaned Comments"],
            "upvotes": row["upvotes"],
            "normalized_upvotes": row["Normalized Upvotes"],
            "score": row.get("score", None)
        })

    # Insert processed data into the processed collection
    processed_collection.insert_many(processed_data)

    print(f"Preprocessing complete. Processed data saved to 'processed_posts' collection.")

    # Prepare cleaned data for JSON export
    cleaned_data = df[[
        "Decrypted Title", "author", "comments", "Cleaned Title",
        "Cleaned Comments", "upvotes", "Normalized Upvotes", "score"
    ]].to_dict(orient="records")

    # Save cleaned data
    output_path = "data/cleaned_data.json"
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(cleaned_data, outfile, indent=4, default=str)

    print(f"Data cleaned and saved to {output_path}")
    
    print("Preprocessing complete. Cleaned data updated in MongoDB.")

# Example usage
if __name__ == "__main__":
    preprocess_data()
