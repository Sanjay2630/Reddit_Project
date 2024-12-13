from pymongo import MongoClient

def store_data(posts):
    """Store posts in MongoDB."""
    client = MongoClient("mongodb+srv://sandhiyag21102003:sanjayh@cluster0.yzw85.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    try:
        db = client["reddit_data"]
        collection = db["raw_collection"]
        if posts:
            collection.insert_many(posts)
            print(f"Stored {len(posts)} posts in MongoDB")
        else:
            print("No posts to store.")
    finally:
        client.close()  # Ensure the client is always closed
