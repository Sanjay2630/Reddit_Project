import re
import hashlib
import numpy as np
from cryptography.fernet import Fernet
from config import ENCRYPTION_KEY
def remove_mentions(text):
    """Remove mentions from text."""
    if isinstance(text, str):
        return re.sub(r'u/\w+', '', text)
    return text

def remove_urls(text):
    """Remove URLs from text."""
    if isinstance(text, str):
        return re.sub(r'http\S+|www.\S+', '', text)
    return text

def clean_text(text):
    """Perform basic text cleaning."""
    text = remove_mentions(text)
    text = remove_urls(text)
    text = text.strip()  # Remove extra whitespace
    return text

def anonymize_username(username):
    """Anonymize usernames using a hashing function."""
    return hashlib.sha256(username.encode()).hexdigest()

def decrypt_title(encrypted_title):
    """Decrypt the encrypted title using the encryption key."""
    try:
        cipher = Fernet(ENCRYPTION_KEY)
        decrypted_title = cipher.decrypt(encrypted_title.encode()).decode()
        return decrypted_title
    except Exception as e:
        print(f"Error decrypting title: {e}")
        return "Decryption Failed"


def normalize(series):
    """
    Normalize a pandas Series (or a list-like object) to a range between 0 and 1.
    
    Args:
        series (pd.Series or list-like): The numerical data to normalize.

    Returns:
        pd.Series: A normalized series with values between 0 and 1.
    """
    series_min = series.min()
    series_max = series.max()
    
    if series_min == series_max:
        # Avoid division by zero if all values are the same
        return np.zeros(len(series))
    
    return (series - series_min) / (series_max - series_min)
