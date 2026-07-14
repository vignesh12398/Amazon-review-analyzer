import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from helper2 import find_column

amazon_review_cols = [
    'review_content',
    'review',
    'review_text',
    'reviewtext',
    'text',
    'content',
    'comment',
    'feedback',
    'reviews.text'
]

amazon_product_cols = [
    'product_name',
    'product',
    'product_title',
    'title',
    'item',
    'name'
]

amazon_rating_cols = [
    'rating',
    'ratings',
    'reviews.rating'
]

amazon_rating_count_cols = [
    'rating_count',
    'reviews.numHelpful'
]

def preprocesor(df):
    review_col = find_column(df, amazon_review_cols)
    product_col = find_column(df, amazon_product_cols)
    rating_col = find_column(df, amazon_rating_cols)
    rating_count_col = find_column(df, amazon_rating_count_cols)

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

    if review_col:
        df['clean_review'] = df[review_col].astype(str).apply(clean_text)
        df['word_count'] = df['clean_review'].str.split().apply(len)  # for later analysis

    # --- PRODUCT NAME SHORTENING ---
    if product_col:
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

        df[product_col] = df[product_col].apply(shorten_name)

    # --- NUMERIC CLEANING ---
    if rating_col:
        df[rating_col] = df[rating_col].apply(
            lambda x: re.sub(r"[^0-9.]", "", str(x))
        )

        df[rating_col] = df[rating_col].replace("", np.nan).astype(float)

        df[rating_col] = df[rating_col].fillna(df[rating_col].mean())

    if rating_count_col:
        df[rating_count_col] = df[rating_count_col].fillna("0")
        df[rating_count_col] = df[rating_count_col].apply(lambda x: re.sub(r"[^0-9]", "", str(x)))
        df[rating_count_col]= df[rating_count_col].replace("", "0").astype(int)

    amazon_price_cols = [
        'discounted_price',
        'actual_price',
        'price',
        'original_price',
        'sale_price',
        'selling_price',
        'list_price',
        'mrp',
        'discount_price',
        'product_price',
        'current_price',
        'price_inr',
        'price_usd',
        'discounted price',
        'actual price'
    ]
    price_col = find_column(df, amazon_price_cols)

    return df
