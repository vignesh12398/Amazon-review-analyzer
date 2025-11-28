from collections import Counter

import pandas as pd
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import emoji as em


def fetch_stats(selected_user, df):
    # ✅ Detect review text column safely
    if 'review_content' in df.columns:
        review_col = 'review_content'
    else:
        # Try common alternatives without renaming the df
        possible_review_cols = ['review', 'content', 'review_text', 'comment', 'feedback', 'clean_review']
        review_col = None
        for col in possible_review_cols:
            if col in df.columns:
                review_col = col
                break

    # ✅ Detect product column safely
    product_col = 'product_name' if 'product_name' in df.columns else None
    user_col = 'user_name' if 'user_name' in df.columns else None

    # If no review column exists, avoid crash
    if not review_col:
        total_words = 0
    else:
        total_words = sum(len(str(t).split()) for t in df[review_col])

    if selected_user == 'Overall':
        num_messages = df.shape[0]
        avg_rating = round(df['rating'].mean(),2) if 'rating' in df.columns else 0
        total_products = df[product_col].nunique() if product_col else 0
        return num_messages, total_words, avg_rating, total_products

    else:
        if user_col:
            filtered_df = df[df[user_col] == selected_user]
        else:
            filtered_df = df  # fallback if no user column

        if review_col:
            total_words = sum(len(str(t).split()) for t in filtered_df[review_col])
        else:
            total_words = 0

        num_messages = filtered_df.shape[0]
        avg_rating = round(filtered_df['rating'].mean(),2) if 'rating' in filtered_df.columns else 0
        total_products = filtered_df[product_col].nunique() if product_col else 0
        return num_messages, total_words, avg_rating, total_products

def most(df):
    x = df['product_name'].value_counts().head()
    df=round((df['product_name'].value_counts() / df.shape[0]) * 100).reset_index().rename(columns=
                                                                                        {'count': 'percentage'})
    return x,df
def create(selected_user, df):
    # auto-detect text/review column
    text_candidates = ['review_content', 'clean_review', 'review', 'text', 'reviews', 'message', 'content']

    review_col = None
    for col in text_candidates:
        if col in df.columns:
            review_col = col
            break

    if review_col is None:
        # prevent crash if no text column is found
        wc = WordCloud(width=500, height=500, background_color="white")
        return wc.generate("No review/text column found in dataset!")

    # optional user filter if first column is user-like
    if selected_user != "Overall" and selected_user in df[df.columns[0]].unique():
        df = df[df[df.columns[0]] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    cloud = wc.generate(df[review_col].astype(str).str.cat(sep=" "))
    return cloud

def emoji(selected_user, df):

    # Auto-detect a text column
    text_candidates = ['review_content', 'clean_review', 'review', 'text', 'reviews', 'message', 'content']
    review_col = None

    for col in text_candidates:
        if col in df.columns:
            review_col = col
            break

    if review_col is None:
        # return empty dataframe instead of crashing
        return pd.DataFrame({"emoji": ["❌ No text column found"], "count": [0]})

    # Optional user filtering
    user_col = df.columns[0]
    if selected_user != "Overall" and selected_user in df[user_col].unique():
        df = df[df[user_col] == selected_user]

    # Extract emojis safely
    import re
    emoji_pattern = re.compile("["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+", flags=re.UNICODE)

    all_emojis = []
    for review in df[review_col].astype(str):
        found = emoji_pattern.findall(review)
        all_emojis.extend(found)

    emoji_df = pd.Series(all_emojis).value_counts().reset_index()
    emoji_df.columns = ['emoji', 'count']
    return emoji_df

def timeline(selected_user, df):
    # auto detect count column
    count_candidates = ['rating_count', 'review_count', 'reviews', 'count']
    count_col = None
    for col in count_candidates:
        if col in df.columns:
            count_col = col
            break

    if 'rating' not in df.columns:
        # if rating column itself is missing
        df['rating'] = "N/A"

    if count_col is None:
        # fallback dummy output
        out = df.groupby('rating').size().reset_index(name='review_count')
        out['review_timeline'] = out['rating'].astype(str)
        return out

    # user filter (safe)
    if selected_user != "Overall" and selected_user in df[df.columns[0]].unique():
        df = df[df[df.columns[0]] == selected_user]

    review_timeline = df.groupby('rating')[count_col].sum().reset_index()
    review_timeline['review_timeline'] = review_timeline['rating'].astype(str)
    review_timeline = review_timeline.rename(columns={count_col: 'review_count'})
    return review_timeline

