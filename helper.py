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
    # Try to auto-detect the review column
    possible_cols = ['review', 'review_content', 'text', 'reviews', 'clean_review']
    review_col = None

    for col in possible_cols:
        if col in df.columns:
            review_col = col
            break

    # If no valid column found, return empty image or warning text
    if review_col is None:
        wc = WordCloud(width=500, height=500, background_color="white")
        return wc.generate("No review column found in dataset")

    # Filter for user if needed
    if selected_user != 'Overall':
        if selected_user in df[df.columns[0]].unique():  # simple fallback user filter
            df = df[df[df.columns[0]] == selected_user]

    # Generate wordcloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    df_wc = wc.generate(df[review_col].astype(str).str.cat(sep=" "))
    return df_wc

def emoji(selected_user,df):
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
    user_col = 'user_name' if 'user_name' in df.columns else None
    if selected_user!='Overall':
        df = df[df[user_col] == selected_user]
    emojis = []
    for review in df['review_content']:
        emojis.extend([c for c in str(review) if em.is_emoji(c)])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
def timeline(selected_user,df):
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
    user_col = 'user_name' if 'user_name' in df.columns else None
    if selected_user!='Overall':
        df = df[df[user_col] == selected_user]
    # Rebuild timeline as DataFrame
    review_timeline = df.groupby(['rating', 'rating_count']) \
        .count()['review_content'] \
        .reset_index()

    # Sort (optional)
    review_timeline = review_timeline.sort_values(by='rating_count', ascending=False)

    # Now loop will work ✅
    for i in range(review_timeline.shape[0]):
        print(str(review_timeline['rating'][i]) + "-" + str(int(review_timeline['rating_count'][i])))
    review_timeline['review_timeline'] = review_timeline.apply(
        lambda row: f"{row['rating']}-{int(row['rating_count'])}", axis=1
    )

    return review_timeline
