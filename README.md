# 🛍️ Amazon Review Analyzer  
🔗 Live App: https://amazon-review-analyzer-app.streamlit.app/

A real-world analytics dashboard built using **Python, Streamlit & Machine Learning** to explore and analyse Amazon product reviews.

This project extends traditional review analytics by integrating **Data Analaysis** and **Machine Learning-based Sentiment Prediction**.

---

## 🚀 Features

### 📊 Dashboard Insights
- **Total Reviews Count**
- **Total Words in Reviews**
- **Average Rating (2 decimal precision)**
- **Number of Unique Products Reviewed**

---

### 🔍 User-Level Filters
- Dropdown to analyse by:
  - `Overall`
  - or any **reviewer/user column name** auto-detected from dataset  
    *(supports datasets using `user_name`, `review.user_name`, `reviewer`, `username`, `author`, etc.)*

---

### 🔥 Visual Analysis
- **Category vs Avg Rating Chart**
- **Most Reviewed Products**
- **Review Length Distribution**
- **Rating Tone (Positive / Neutral / Negative Buckets)**
- **Discount Impact on Ratings**
- **Heatmap: Product × Rating Tone Intensity**
- **Word Cloud of Review Text**
- **Emoji Analysis of Reviews**
- **Review Timeline Trends**

---

## 🤖 Machine Learning Integration

### 🧠 Sentiment Prediction Model
The project includes a real-time NLP pipeline that predicts sentiment from user-entered reviews.

#### ML Pipeline:
1. Text Cleaning using Regex & BeautifulSoup  
2. Feature Extraction using **CountVectorizer (Bag-of-Words)**  
3. Sentiment Classification using **Logistic Regression**  
4. Live prediction via Streamlit UI  

#### Sentiment Classes:
- Positive 😊
- Neutral 😐
- Negative 😡

---

## 🧠 Why this project is unique?

| Basic Tutorials | This Project |
|---|---|
| Static data charts | Interactive analytics dashboard |
| Pure visualization | Visualization  + ML |
| Offline ML models | Live prediction web app |
| Chat dataset analysis | E-commerce product review intelligence |

---

## 🛠️ Tech Stack

- **Python 3.11 / 3.12**
- **Pandas & NumPy** – Data processing
- **BeautifulSoup & Regex** – Text preprocessing
- **Streamlit** – Interactive dashboard UI
- **Matplotlib** – Visualizations
- **Scikit-learn** – Machine Learning 

---

## 📦 Installation

### 1️⃣ Clone Repository
```bash
git clone <your_repo_link>
cd amazon-review-analyzer

pip install -r requirements.txt
