import os
from cryptography.fernet import Fernet
# Reddit API credentials

REDDIT_CLIENT_ID = "UVx6hvATxBYYQaHKQY5New"
REDDIT_CLIENT_SECRET = "fCUFnNZqXVOIrMOqIPO4rVL6KCDOvw"
REDDIT_USER_AGENT = "privacy_preserving_project"

# MongoDB credentials
MONGO_URI = "mongodb+srv://sandhiyag21102003:sanjayh@cluster0.yzw85.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB_NAME = "reddit_data"
MONGO_COLLECTION_NAME = "posts"

# Data collection settings
SUBREDDIT_NAME = "technology"  # Default subreddit
POST_LIMIT = 100              # Number of posts to fetch at a time

# Logging settings
LOG_FILE = "project.log"
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

#Encryption key
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY", Fernet.generate_key().decode())
