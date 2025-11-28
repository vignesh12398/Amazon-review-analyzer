import numpy as np
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import helper  # contains all helper functions

df1 = pd.DataFrame()  # ✅ always initialize first

st.sidebar.title("Amazon Review Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv"])

# ✅ Load & preprocess dataset safely
if uploaded_file is not None:
    try:
        df1 = pd.read_csv(uploaded_file)
        df1 = df1.dropna(how="all").fillna("")  # clean NaN
        df1 = helper.preprocesor(df1)  # ✅ call correct function from helper
        st.write("Dataset Preview:")
        st.write(df1.head())
    except Exception as e:
        st.error("Failed to read the CSV file!")

    # ✅ Auto-Detect & rename columns
    # Detect user column
    user_candidates = ['reviewer', 'reviewer_name', 'profile', 'user', 'customer_name', 'name', 'user_name']
    for col in user_candidates:
        if col in df1.columns:
            df1 = df1.rename(columns={col: 'user_name'})
            break

    # Detect review text column
    text_candidates = ['review', 'review_text', 'feedback', 'comment', 'review_content', 'message', 'content']
    for col in text_candidates:
        if col in df1.columns:
            df1 = df1.rename(columns={col: 'review_content'})
            break

    # Detect product column
    product_candidates = ['title', 'item', 'product_title', 'product', 'product_name']
    for col in product_candidates:
        if col in df1.columns:
            df1 = df1.rename(columns={col: 'product_name'})
            break

    # ✅ Fill missing required columns safe fallback
    if 'product_name' not in df1.columns:
        df1['product_name'] = "Unknown Product"
    if 'user_name' not in df1.columns:
        df1['user_name'] = "Anonymous"
    if 'rating' not in df1.columns:
        df1['rating'] = 0  # numeric fallback

    # ✅ Sidebar selection setup
    user_list = df1['user_name'].unique().tolist()
    user_list = [u for u in user_list if str(u).lower() not in ['nan', 'none', '']]
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt user:", user_list)

    # ✅ Show analysis button block
    if st.sidebar.button('Show Analysis'):
        stats = helper.fetch_stats(selected_user, df1)
        if stats is None:
            st.warning("Stats could not be computed")
        else:
            num_reviews, total_words, avg_rating, total_products = stats

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Reviews", num_reviews)
            with col2:
                st.metric("Total Words", total_words)
            with col3:
                st.metric("Average Rating", round(avg_rating, 2))
            with col4:
                st.metric("Total products", total_products)

        # ---- WORDCLOUD ----
        st.title("Word Cloud")
        if 'review_content' in df1.columns and df1['review_content'].str.strip().any():
            wc_img = helper.create_wordcloud(selected_user, df1)
            if wc_img:
                fig, ax = plt.subplots()
                ax.imshow(wc_img)
                ax.axis("off")
                fig.tight_layout()
                st.pyplot(fig)
        else:
            st.warning("No review text column found for WordCloud!")

        # ---- BUSY PRODUCTS ----
        st.title("Busy Products")
        busy_series, busy_df = helper.most(df1)
        if not busy_series.empty:
            fig, ax = plt.subplots()
            ax.bar(busy_series.index, busy_series.values)
            plt.xticks(rotation='vertical')
            fig.tight_layout()
            st.pyplot(fig)
            st.dataframe(busy_df)
        else:
            st.warning("No product activity data!")

        # ---- TIMELINE ----
        st.title("Rating Timeline")
        timeline_df = helper.timeline(selected_user, df1)
        if not timeline_df.empty:
            fig, ax = plt.subplots(figsize=(10,4))
            ax.bar(timeline_df['review_timeline'], timeline_df['review_count'])
            plt.xticks(rotation=45, ha='right')
            fig.tight_layout()
            st.pyplot(fig)
            st.dataframe(timeline_df)
        else:
            st.warning("No timeline data!")

        # ---- EMOJI ANALYZER ----
        st.title("Emoji Analyzer")
        emoji_df = helper.emoji(selected_user, df1)
        if not emoji_df.empty and emoji_df['count'].sum() > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct='%1.1f%%')
                fig.tight_layout()
                st.pyplot(fig)
        else:
            st.warning("No emojis found in dataset!")

        # ---- CATEGORY vs RATING ----
        if 'category' in df1.columns:
            st.title("Category vs Rating")
            df1['main_category'] = df1['category'].apply(lambda x: str(x).split("|")[0] if "|" in str(x) else str(x))
            cat_rating = df1.groupby('main_category')['rating'].mean().round(2)
            fig, ax = plt.subplots()
            ax.bar(cat_rating.index, cat_rating.values)
            plt.xticks(rotation='vertical')
            fig.tight_layout()
            st.pyplot(fig)
            st.dataframe(cat_rating.reset_index())
        else:
            st.warning("No category column found!")

        # ---- PRICE SCATTER ----
        if 'discounted_price' in df1.columns and 'actual_price' in df1.columns:
            st.title("Discounted Price vs Actual Price")
            fig, ax = plt.subplots()
            ax.scatter(df1['discounted_price'], df1['actual_price'])
            fig.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("Price columns not found!")

        # ---- DISCOUNT PIE ----
        if 'discount_percentage' in df1.columns:
            st.title("Top Discounts")
            dta = df1['discount_percentage'].head()
            fig, ax = plt.subplots()
            ax.pie(dta, labels=df1['product_name'].head(len(dta)), autopct='%1.1f%%')
            fig.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("No discount_percentage column found!")

        # ---- HEATMAP TONE ----
        st.title("User vs Rating Tone Heatmap")

        if 'rating' in df1.columns:
            def rating_tone(x):
                if float(x) >= 4:
                    return "Positive 😊"
                elif float(x) == 3:
                    return "Neutral 😐"
                else:
                    return "Negative 😡"

            if 'rating_tone' not in df1.columns:
                df1['rating_tone'] = df1['rating'].apply(rating_tone)

            tone_matrix = pd.crosstab(df1['product_name'], df1['rating_tone'])

            if tone_matrix.empty:
                st.warning("Heatmap matrix is empty!")
            else:
                fig, ax = plt.subplots(figsize=(4, 7))
                ax.imshow(tone_matrix.values, aspect='auto')
                ax.set_xticks(range(len(tone_matrix.columns)))
                ax.set_xticklabels(tone_matrix.columns, rotation=25)
                ax.set_yticks(range(len(tone_matrix.index)))
                ax.set_yticklabels(tone_matrix.index, fontsize=8)
                plt.colorbar(ax.imshow(tone_matrix.values, aspect='auto'), ax=ax, fraction=0.035, pad=0.02)
                fig.tight_layout()
                st.pyplot(fig)
                st.dataframe(tone_matrix)
        else:
            st.warning("No rating column found — skipping tone heatmap!")






