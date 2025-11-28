import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def preprocesor(df):

    """
    Cleans Amazon review text and converts numeric-like fields.
    Also shortens product names if column exists.
    """

    # --- TEXT CLEANING ---
    def clean_text(data):
        text = str(data).lower()
        text = re.sub(r"http\S+", "", text)
        text = BeautifulSoup(text, "html.parser").get_text()
        text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    if 'review_content' in df.columns:
        df['clean_review'] = df['review_content'].apply(clean_text)
        df['word_count'] = df['clean_review'].str.split().apply(len)  # for later analysis

    # --- PRODUCT NAME SHORTENING ---
    if 'product_name' in df.columns:
        def shorten_name(name):
            name = str(name)
            # take first 2 words only (general shrink)
            short = " ".join(name.split()[:2])

            # optional meaningful overrides
            low = name.lower()
            if "wayona" in low:
                short = "Wayona Cable"
            elif "ambrane" in low or "ambrane" in low:
                short = "Ambrane Cable"
            elif "boat" in low:
                short = "boAt Cable"
            elif "sounce" in low:
                short = "Sounce Cable"

            return short

        df['product_name'] = df['product_name'].apply(shorten_name)

    # --- NUMERIC CLEANING ---
    if 'rating' in df.columns:
        df['rating'] = df['rating'].apply(lambda x: re.sub(r"[^0-9.]", "", str(x)))
        df['rating'] = df['rating'].replace("", np.nan).astype(float)
        df['rating'] = df['rating'].fillna(df['rating'].mean())

    if 'rating_count' in df.columns:
        df['rating_count'] = df['rating_count'].fillna("0")
        df['rating_count'] = df['rating_count'].apply(lambda x: re.sub(r"[^0-9]", "", str(x)))
        df['rating_count'] = df['rating_count'].replace("", "0").astype(int)

    amazon_price_cols = ['discounted_price', 'actual_price', 'discount_percentage']
    for col in amazon_price_cols:
        if col in df.columns:
            df[col] = df[col].fillna("0")
            df[col] = df[col].apply(lambda x: re.sub(r"[^0-9.]", "", str(x)))
            df[col] = df[col].replace("", "0").astype(float)

    return df
