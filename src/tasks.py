from celery import Celery
import asyncpraw
import asyncio
import json
from cryptography.fernet import Fernet
from config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    SUBREDDIT_NAME,
    POST_LIMIT,
    ENCRYPTION_KEY,
)
from storage import store_data  # Import the store_data function
from utils import anonymize_username
# Setup Celery
app = Celery('reddit_data_collection', broker='redis://localhost:6379/0')

#Initialize the encryption cipher
cipher=Fernet(ENCRYPTION_KEY)

# Define the task using Celery
@app.task
async def collect_data(subreddit_name=SUBREDDIT_NAME, limit=POST_LIMIT):
    """Fetch data from Reddit and store it."""
    async def fetch_reddit_data():
        async with asyncpraw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        ) as reddit:
          subreddit = await reddit.subreddit(subreddit_name)
          posts = []
          async for post in subreddit.hot(limit=limit):
            encrypted_title=cipher.encrypt(post.title.encode()).decode()

             # Anonymize the author's name using hashing
            anonymized_author = anonymize_username(post.author.name if post.author else "anonymous")

            posts.append({
                'title': encrypted_title,
                'author': anonymized_author,
                'url': post.url,
                'score': post.score,  # Upvotes (score)
                'upvotes': post.ups,
                'created_utc': post.created_utc,
                'comments': post.num_comments

            })
          # Save the collected data to raw_data.json
          output_path = "data/raw_data.json"
          with open(output_path, "w", encoding="utf-8") as f:
             json.dump(posts, f, indent=4)
 
          print(f"Data collected and saved to {output_path}")
          return posts

    # Run the asynchronous function inside Celery task using asyncio
    posts = await fetch_reddit_data()  # Directly use async/await here
    store_data(posts)  # Store the posts in MongoDB
    # Here you can store the posts in MongoDB or any other storage
    print(f"Collected {len(posts)} posts.")
    return len(posts)

# To run the task, you would call collect_data.delay()
