import numpy as np
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt

from helper import timeline
from preprocessor import preprocesor  # your function
import helper
st.markdown("""
<style>

/* ---- ✅ MAIN PAGE BACKGROUND ---- */
.stApp {
    background: #0e1117;
}

/* ---- ✅ SIDEBAR BACKGROUND ---- */
section[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 2px solid #2d3748;
    padding-top: 10px;
}

/* ---- Sidebar Text Styling ---- */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #e2e8f0;
    font-weight: 500;
}

/* ---- Reduce extra space in main content ---- */
.block-container {
    padding-top: 25px;
    padding-left: 30px;
    padding-right: 30px;
}

/* ---- Make upload box clean ---- */
div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.08);
    padding: 10px;
    border-radius: 8px;
    border: 1px dashed #2563eb;
}

/* ---- Optional: scrollbar style for long sidebar ---- */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #1e293b;
}
::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background: #2563eb;
}
/* ---- Sidebar container ---- */
section[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 2px solid #3b82f6;
    padding: 12px;
}

/* ---- Sidebar title ---- */
section[data-testid="stSidebar"] h1 {
    text-align: center;
    font-size: 22px;
    color: #3b82f6;
    margin-bottom: 15px;
}

/* ---- Dropdown (selectbox) ---- */
section[data-testid="stSidebar"] select {
    background-color: #1f2937;
    color: white;
    border-radius: 6px;
    border: 1px solid #3b82f6;
    padding: 5px;
}

/* ---- Sidebar Buttons ---- */
section[data-testid="stSidebar"] button {
    width: 100%;
    background: #2563eb;
    color: white;
    padding: 8px;
    border-radius: 8px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

section[data-testid="stSidebar"] button:hover {
    background: #3b82f6;
    box-shadow: 0 0 10px rgba(59,130,246,0.5);
}

/* ---- File uploader box ---- */
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.07);
    padding: 10px;
    border-radius: 8px;
    border: 1px dashed #3b82f6;
    text-align: center;
}

/* ---- Sidebar text labels ---- */
section[data-testid="stSidebar"] label {
    font-size: 14px;
    color: #93c5fd;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ---- Main Page Background ---- */
.stApp {
    background-color: #0e1117;
    color: white;
}

/* ---- Sidebar Styling ---- */
[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 2px solid #2d3748;
}

/* ---- Metric Card Styling ---- */
[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 12px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 0 8px rgba(56,189,248,0.25);
}

/* ---- Headings Glow ---- */
h1, h2, h3 {
    font-family: 'Poppins', sans-serif;
    color: #60a5fa;
}

/* ---- Busy Products Table ---- */
table {
    font-size: 12px;
    background: #1a202c;
    border-radius: 6px;
}

/* ---- Buttons Styling ---- */
button {
    background: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 6px 14px;
    font-weight: bold;
}

/* ---- Fix Wordcloud Centering ---- */
.css-10trblm {
    text-align: center;
}

/* ---- Improve dataframe containers ---- */
[data-testid="stDataFrame"] {
    border: 1px solid #2563eb;
    border-radius: 10px;
    padding: 5px;
    background: #111827;
}

/* ---- Remove extra whitespace around plots ---- */
.css-ocqkz7 {
    gap: 1rem;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.title("Amazon review analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)  # ✅ fixed CSV read
    df = preprocesor(df)             # ✅ fixed function call
    st.write(df.head())

    # ✅ Detect user column
    possible_user_cols = ['reviewer', 'reviewer_name', 'profile', 'user', 'customer_name', 'name', 'user_name']
    for col in possible_user_cols:
       if col in df.columns:
          df = df.rename(columns={col: 'user_name'})
          break

    # ✅ Detect review text column
    possible_review_cols = ['review', 'review_text', 'content', 'feedback', 'comment', 'review_content']
    for col in possible_review_cols:
       if col in df.columns:
          df = df.rename(columns={col: 'review_content'})
          break

    # ✅ Detect product column
    possible_product_cols = ['title', 'item', 'product_title', 'product', 'product_name']
    for col in possible_product_cols:
       if col in df.columns:
          df = df.rename(columns={col: 'product_name'})
          break

    # ✅ Fill missing product/user columns if none detected to avoid later errors
    if 'product_name' not in df.columns:
       df['product_name'] = "Unknown Product"
    if 'user_name' not in df.columns:
       df['user_name'] = "Anonymous"

    # ✅ Now safely build sidebar list
    user_list = df['user_name'].unique().tolist()
    user_list = [u for u in map(str, user_list) if u.lower() not in ['nan', 'none', '']]
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)

    # Change inside your button block
    if st.sidebar.button('show analysis'):
       num_messages, total_words, avg_rating,total_products = helper.fetch_stats(selected_user, df)

       # ✅ Round rating now so you can display later safely

       col1, col2, col3,col4 = st.columns(4)

       with col1:
          st.metric("Total Reviews", num_messages)

       with col2:
          st.metric("Total Words", total_words)

       with col3:
          st.metric("Average Rating", round(avg_rating, 2))
       with col4:
          st.metric("Total products", total_products)

       if selected_user=='Overall':

          st.title('busy products')
          x,new_df=helper.most(df)
          fig,ax=plt.subplots()
          col1, col2 = st.columns(2)
          with col1:
             ax.bar(x.index,x.values,color='red')
             plt.xticks(rotation='vertical')
             st.pyplot(fig)
          with col2:
             st.dataframe(new_df)
       if selected_user == 'Overall':
          st.title('category vs rating')
          df['main_category'] = df['category'].apply(lambda x: x.split("|")[0])
          category_rating = df.groupby('main_category')['rating'].mean().round(2)
          fig, ax = plt.subplots()
          col1 ,col2= st.columns(2)
          d = {'category': category_rating.index, 'rating': category_rating.values}
          df1 = pd.DataFrame(data=d)
          with col1:
             ax.bar(category_rating.index,category_rating.values,color='red')
             plt.xticks(rotation='vertical')
             st.pyplot(fig)
          with col2:
             st.dataframe(df1)
       st.title("Word Cloud")
       df_wc=helper.create(selected_user, df)
       fig,ax=plt.subplots()
       ax.imshow(df_wc)
       st.pyplot(fig)

       timeline = helper.timeline(selected_user, df1)


       fig, ax = plt.subplots(figsize=(12, 5))
       ax.bar(timeline['review_timeline'], timeline['review_count'])

       plt.xlabel("Review Timeline (Rating–ReviewCount)")
       plt.ylabel("Number of Reviews")
       plt.title("Review Trend Based on review_timeline column")
       plt.xticks(rotation=45, ha='right')  # clean readable names ✅
       plt.grid(True)
       st.pyplot(fig)


       emoji_df=helper.emoji(selected_user, df)
       st.title("Emoji analyzer")
       col1,col2=st.columns(2)
       with col1:
            st.dataframe(emoji_df, use_container_width=False)
       with col2:
           fig,ax=plt.subplots()
           ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct='%1.1f%%')

           st.pyplot(fig)

           ###########################################

       if selected_user == 'Overall':
           if 'discounted_price' in df.columns and 'actual_price' in df.columns:
               st.title("discounted_price vs actual price")
               fig, ax = plt.subplots(figsize=(8, 5))
               ax.scatter(df['discounted_price'], df['actual_price'], color='orange', marker='s')
               plt.xlabel("Discounted Price (₹)")
               plt.ylabel("Actual Price (₹)")
               plt.title("Discounted vs Actual Price Comparison")
               plt.grid(True)
               st.pyplot(fig)

           #############################################################pie


       if selected_user == 'Overall':

           if 'discount_percentage' in df.columns :
               # ✅ Create main_category safely for entire dataframe
               if 'category' in df.columns:
                   df['main_category'] = df['category'].apply(lambda x: str(x).split("|")[0])
               else:
                   df['main_category'] = "Uncategorized"

               st.title("top 5 products discount percentage")
               cat1 = df['main_category']
               cat1_unique = np.unique(cat1)  # NumPy way
               cat1_unique.tolist()
               dta = df['discount_percentage'].head()
               labels = cat1_unique[:len(dta)]
               fig, ax = plt.subplots()
               ax.pie(dta, labels=labels, autopct='%1.1f%%')
               st.pyplot(fig)




###########################################################################




       user_col = 'user_name' if 'user_name' in df.columns else None
       if selected_user != 'Overall':
           df = df[df[user_col] == selected_user]
       st.title("User vs Rating tone heatmap")


       def rating_tone(x):
           if float(x) >= 4:
               return "positive 😊"
           elif float(x) == 3:
               return "Neutral 😐"
           else:
               return "Negative 😡"


       df['rating_tone'] = df['rating'].astype(float).apply(rating_tone)
       tone_matrix = pd.crosstab(df['product_name'], df['rating_tone'])

       # Optional: show only top 40 products for clean view
       if len(tone_matrix) > 40:
           top_products = df['product_name'].value_counts().head(40).index
           tone_matrix = tone_matrix.loc[top_products]

       # Plot heatmap
       fig, ax = plt.subplots(figsize=(4, 7))
       img = ax.imshow(tone_matrix.values, aspect='auto')

       # Axis labels
       ax.set_xticks(range(len(tone_matrix.columns)))
       ax.set_xticklabels(tone_matrix.columns, rotation=25)

       ax.set_yticks(range(len(tone_matrix.index)))
       ax.set_yticklabels(tone_matrix.index, fontsize=8)

       # ✅ Add color scale (measure bar) on right
       plt.colorbar(img, ax=ax, fraction=0.035, pad=0.02)

       st.pyplot(fig)




