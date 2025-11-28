# 🛍️ Amazon Review Analyzer    link:https://amazon-review-analyzer-app.streamlit.app/

A real-world  analytics dashboard built using **Python & Streamlit** to explore and analyse Amazon product reviews.  
Instead of chat media/emoji timeline (WhatsApp tutorial style), this project focuses on **review intensity, rating trends, category insights, product popularity, sentiment-like tone, and review depth.**

---

## 🚀 Features

### 📊 Dashboard Insights
- **Total Reviews Count**
- **Total Words in Reviews**
- **Average Rating (2 decimal precision)**
- **Number of Unique Products Reviewed**

### 🔍 User-Level Filters
- Dropdown to analyse by:
  - `Overall`
  - or any **reviewer/user column name** auto-detected from dataset  
    *(supports datasets using `user_name`, `review.user_name`, `reviewer`, `username`, `author`, etc.)*

### 🔥 Visual Analysis
- **Category vs Avg Rating Chart**
- **Most Reviewed Products**
- **Review Length Distribution**
- **Rating Tone (Positive/Neutral/Negative Buckets)**
- **Generosity/Harshness Index for Reviewers**
- **Discount Impact on Ratings**
- **Heatmap: User × Rating Tone Intensity**

---

## 🧠 Why this project is unique?

| Tutorial Style | This Project |
|---|---|
| WhatsApp chat timeline, emoji stats | Amazon reviews trend by ratings, categories, discounts |
| Message media data | Product performance & reviewer behaviour |
| Time-based heatmaps | Rating-intensity heatmaps & theme detection |

**You work with reviews that already exist in CSV, cleaning + analysing without timestamp dependency.**

---

## 🛠️ Tech Stack

- **Python 3.12 / 3.11**
- **Pandas & NumPy** for data processing
- **BeautifulSoup & Regex** for text cleaning
- **Streamlit** for interactive UI
- **Matplotlib** for charts
- Optional extension: sentiment or ML models can be added later

---

## 📦 Installation

1. Clone the project
2. Create and activate a virtual environment
3. Install required dependencies:

```bash
pip install -r requirements.txt
