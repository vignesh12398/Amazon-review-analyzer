from collections import Counter
from helper2 import find_column
import pandas as pd
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import emoji as em

amazon_review_cols = [
    'review_content',
    'review',
    'review_text',
    'reviewtext',
    'text',
    'content',
    'comment',
    'feedback',
    'clean_review',
    'reviews.text'
]
amazon_rating_cols = [
    'rating',
    'ratings',
    'score',
    'stars',
    'star_rating',
    'overall',
    'overall_rating',
    'review_rating',
    'reviews.rating'
]
amazon_product_cols = [
    'product_name',
    'title',
    'product_title',
    'product',
    'item',
    'name'
]

amazon_user_cols = [
    'user_name',
    'reviewer',
    'reviewer_name',
    'username',
    'reviews.username'
]
def fetch_stats(selected_user, df):
    # ✅ Detect review text column safely
    review_col = find_column(df, amazon_review_cols)
    # ✅ Detect product column safely
    product_col = find_column(df, amazon_product_cols)
    user_col = find_column(df, amazon_user_cols)
    rating_col = find_column(df, amazon_rating_cols)

    # If no review column exists, avoid crash
    if not review_col:
        total_words = 0
    else:
        total_words = sum(len(str(t).split()) for t in df[review_col])

    if selected_user == 'Overall':
        num_messages = df.shape[0]
        avg_rating = round(df[rating_col].mean(), 2) if rating_col else 0
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
        avg_rating = round(filtered_df[rating_col].mean(), 2) if rating_col else 0
        total_products = filtered_df[product_col].nunique() if product_col else 0
        return num_messages, total_words, avg_rating, total_products

def most(df):
    product_col = find_column(df, amazon_product_cols)

    x = df[product_col].value_counts().head()

    df1 = round(
        (df[product_col].value_counts()/df.shape[0])*100
    ).reset_index()

    df1.columns = ['Product','Percentage']

    return x, df1
def create(selected_user,df):
    # ✅ Detect review text column safely
    review_col = find_column(df, amazon_review_cols)
    user_col = find_column(df, amazon_user_cols)

    if selected_user!='Overall':
        filtered_df = df[df[user_col] == selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    if selected_user != 'Overall':
        df = df[df[user_col] == selected_user]

    df_wc = wc.generate(df[review_col].astype(str).str.cat(sep=" "))
    return df_wc
def emoji(selected_user,df):
    review_col = find_column(df, amazon_review_cols)
    user_col = find_column(df, amazon_user_cols)
    if selected_user!='Overall':
        df = df[df[user_col] == selected_user]
    emojis = []
    for review in df[review_col]:
        emojis.extend([c for c in str(review) if em.is_emoji(c)])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
def timeline(selected_user,df):
    review_col = find_column(df, amazon_review_cols)

    rating_col = find_column(df, amazon_rating_cols)

    rating_count_col = find_column(
        df,
        ['rating_count', 'reviews.numHelpful']
    )

    review_timeline = (
        df.groupby([rating_col, rating_count_col])
        .count()[review_col]
        .reset_index()
    )

    review_timeline = review_timeline.sort_values(
        by=rating_count_col,
        ascending=False
    )

    review_timeline['review_timeline'] = review_timeline.apply(
        lambda row: f"{row[rating_col]}-{int(row[rating_count_col])}",
        axis=1
    )

    return review_timeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_sentiment_model(df):

    review_col = find_column(df, amazon_review_cols)
    rating_col = find_column(df, amazon_rating_cols)

    if review_col is None:
        raise ValueError("No review column found.")

    if rating_col is None:
        raise ValueError("No rating column found.")

    df['sentiment'] = df[rating_col].apply(
        lambda x: "Positive" if float(x) >= 4
        else ("Neutral" if float(x) == 3 else "Negative")
    )

    cv = CountVectorizer(max_features=3000)

    X = cv.fit_transform(df[review_col].astype(str)).toarray()
    y = df['sentiment']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    models = {
        "Logistic Regression": (
            LogisticRegression(max_iter=1000),
            {"C": [0.1, 1, 10]}
        ),

        "Naive Bayes": (
            MultinomialNB(),
            {"alpha": [0.1, 0.5, 1]}
        ),

        "Random Forest": (
            RandomForestClassifier(),
            {"n_estimators": [50, 100], "max_depth": [None, 10]}
        )
    }

    best_accuracy = 0
    best_model = None

    for name, (model, params) in models.items():

        grid = GridSearchCV(model, params, cv=3)

        grid.fit(X_train, y_train)

        y_pred = grid.predict(X_test)

        acc = accuracy_score(y_test, y_pred)

        if acc > best_accuracy:
            best_accuracy = acc
            best_model = grid.best_estimator_

    return best_model, cv, best_accuracy