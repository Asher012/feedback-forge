import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from google_play_scraper import Sort, reviews, search
from textblob import TextBlob
from datetime import datetime, timedelta
import re
from collections import Counter, defaultdict
import json
import base64
from io import BytesIO
import time
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import LatentDirichletAllocation, PCA
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from scipy import stats
from scipy.spatial.distance import cosine
import networkx as nx
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import warnings
import asyncio
import aiohttp
import concurrent.futures
from functools import lru_cache
import holidays
import pytz
from dateutil import parser
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Advanced Page Configuration
st.set_page_config(
    page_title="ReviewForge Analytics Pro",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "ReviewForge Analytics Pro - Advanced Review Analysis Platform"
    }
)

# Advanced CSS Styling with Modern Design
def apply_advanced_styling():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Root Variables */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #1e40af;
        --accent-color: #3b82f6;
        --success-color: #059669;
        --warning-color: #d97706;
        --error-color: #dc2626;
        --dark-bg: #0f172a;
        --light-bg: #f8fafc;
        --card-bg: rgba(255, 255, 255, 0.95);
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-lg: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    }

    /* Global Styles */
    .main, .block-container {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        min-height: 100vh;
    }

    /* Header Styles */
    .main-header {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: 8px;
        box-shadow: var(--shadow);
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
        text-align: center;
    }

    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }

    .header-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        margin-bottom: 1rem;
    }

    .developer-credit {
        background: var(--primary-color);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-weight: 600;
        display: inline-block;
        margin-top: 1rem;
        font-size: 0.9rem;
    }

    /* Card Styles */
    .metric-card, .analysis-card, .insight-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
        text-align: center;
    }

    .metric-card:hover, .analysis-card:hover, .insight-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        transition: all 0.3s ease;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }

    .metric-label {
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.8rem;
    }

    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--dark-bg) 0%, #1e293b 100%);
    }

    .sidebar-title {
        color: white;
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 1rem;
        text-align: center;
        padding: 1rem 0;
        background: var(--primary-color);
        border-radius: 4px;
    }

    /* Button Styles */
    .stButton button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
        width: 100%;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
    }

    /* Input Styles */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        border-radius: 6px;
        border: 2px solid var(--border-color);
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }

    .stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }

    /* Progress Bar */
    .stProgress .st-bo {
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        height: 6px;
        border-radius: 3px;
    }

    /* Success/Warning/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, var(--success-color), #10b981);
        color: white;
        border-radius: 6px;
        padding: 1rem;
    }

    .stWarning {
        background: linear-gradient(135deg, var(--warning-color), #f59e0b);
        color: white;
        border-radius: 6px;
        padding: 1rem;
    }

    .stError {
        background: linear-gradient(135deg, var(--error-color), #ef4444);
        color: white;
        border-radius: 6px;
        padding: 1rem;
    }

    /* Chart Containers */
    .chart-container {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }

    .chart-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        text-align: center;
    }

    /* Navigation Styles */
    .nav-item {
        background: var(--card-bg);
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        text-align: center;
    }

    .nav-item:hover {
        background: var(--primary-color);
        color: white;
        transform: translateX(5px);
    }

    .nav-item.active {
        background: var(--primary-color);
        color: white;
        border-color: var(--accent-color);
    }

    /* Table Styles */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: var(--shadow);
        width: 100%;
    }

    .dataframe th {
        background: var(--primary-color);
        color: white;
        font-weight: 600;
        padding: 1rem;
    }

    .dataframe td {
        padding: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--light-bg);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }

        .metric-card {
            padding: 1rem;
        }

        .metric-value {
            font-size: 2rem;
        }
    }

    /* Loading Animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }

    .loading {
        animation: pulse 2s infinite;
    }

    /* Data Table Enhancements */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: var(--shadow);
    }

    /* Sidebar Navigation Enhancement */
    .nav-section {
        background: var(--card-bg);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
    }

    .nav-section h3 {
        color: var(--primary-color);
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

apply_advanced_styling()

# Session State Management
def initialize_session_state():
    session_defaults = {
        'current_page': 'dashboard',
        'analyzed_data': None,
        'competitor_data': None,
        'analysis_history': [],
        'user_preferences': {},
        'ml_models': {},
        'advanced_insights': {},
        'export_data': None,
        'cached_reviews': {},
        'app_info': {},
        'user_authenticated': False,
        'user_role': 'viewer'
    }

    for key, default_value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

initialize_session_state()

# Performance Optimization: Caching
@st.cache_data(ttl=3600, show_spinner=False)
def cached_scrape_reviews(package_name, count=500, sort_by=Sort.NEWEST):
    """Cached version of review scraping to improve performance"""
    analyzer = ReviewAnalyzer()
    return analyzer.scrape_reviews(package_name, count, sort_by)

@st.cache_data(ttl=3600, show_spinner=False)
def cached_generate_ml_insights(df):
    """Cached version of ML insights generation"""
    analyzer = ReviewAnalyzer()
    return analyzer.generate_ml_insights(df)

# Advanced Helper Functions
class ReviewAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.ml_models = {
            'naive_bayes': MultinomialNB(),
            'logistic_regression': LogisticRegression(max_iter=1000),
            'random_forest': RandomForestClassifier(n_estimators=100)
        }

    def extract_package_name(self, url):
        """Extract package name from Google Play URL with validation"""
        if not url or not isinstance(url, str):
            return None

        patterns = [
            r'id=([a-zA-Z0-9_\.]+)',
            r'/store/apps/details\?id=([a-zA-Z0-9_\.]+)',
            r'play\.google\.com.*id=([a-zA-Z0-9_\.]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                package_name = match.group(1)
                if self.validate_package_name(package_name):
                    return package_name
        return None

    def validate_package_name(self, package_name):
        """Validate package name format"""
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)*$'
        return bool(re.match(pattern, package_name)) and len(package_name.split('.')) >= 2

    def get_app_name(self, package_name):
        """Extract readable app name from package name"""
        if not package_name:
            return "Unknown App"
        parts = package_name.split('.')
        return parts[-1].replace('_', ' ').title()

    def preprocess_text(self, text):
        """Advanced text preprocessing"""
        if pd.isna(text) or not isinstance(text, str):
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove URLs, mentions, hashtags
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        text = re.sub(r'@\w+|#\w+', '', text)

        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)

        # Tokenize
        tokens = word_tokenize(text)

        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words and len(token) > 2]

        return ' '.join(tokens)

    def advanced_sentiment_analysis(self, text):
        """Advanced sentiment analysis with multiple approaches"""
        if pd.isna(text) or text.strip() == "":
            return {
                'polarity': 0.0,
                'subjectivity': 0.0,
                'sentiment': 'Neutral',
                'confidence': 0.0,
                'emotional_intensity': 0.0,
                'aspects': {},
                'keywords': []
            }

        # TextBlob analysis
        blob = TextBlob(str(text))
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Emotional intensity calculation
        emotional_words = {
            'excellent': 2.0, 'amazing': 1.8, 'outstanding': 1.7, 'perfect': 1.6,
            'wonderful': 1.5, 'fantastic': 1.4, 'great': 1.2, 'good': 1.0,
            'terrible': -2.0, 'awful': -1.8, 'horrible': -1.7, 'worst': -1.6,
            'hate': -1.5, 'disgusting': -1.4, 'bad': -1.2, 'poor': -1.0
        }

        intensity = 0.0
        text_lower = text.lower()
        found_keywords = []

        for word, weight in emotional_words.items():
            if word in text_lower:
                intensity += weight
                found_keywords.append(word)

        # Normalize intensity
        intensity = max(-2.0, min(2.0, intensity))

        # Aspect-based analysis
        aspects = {
            'performance': any(word in text_lower for word in 
                             ['fast', 'slow', 'speed', 'lag', 'performance', 'responsive', 'quick']),
            'ui_design': any(word in text_lower for word in 
                           ['design', 'interface', 'ui', 'layout', 'beautiful', 'ugly', 'visual']),
            'functionality': any(word in text_lower for word in 
                               ['feature', 'function', 'work', 'broken', 'bug', 'crash', 'issue']),
            'usability': any(word in text_lower for word in 
                           ['easy', 'difficult', 'simple', 'complex', 'intuitive', 'confusing']),
            'reliability': any(word in text_lower for word in 
                             ['stable', 'crash', 'freeze', 'reliable', 'consistent', 'glitch'])
        }

        # Sentiment classification with confidence
        if polarity > 0.5:
            sentiment = "Highly Positive"
            confidence = min(1.0, abs(polarity) + 0.3)
        elif polarity > 0.2:
            sentiment = "Positive"
            confidence = min(1.0, abs(polarity) + 0.2)
        elif polarity > 0.0:
            sentiment = "Slightly Positive"
            confidence = min(1.0, abs(polarity) + 0.1)
        elif polarity < -0.5:
            sentiment = "Highly Negative"
            confidence = min(1.0, abs(polarity) + 0.3)
        elif polarity < -0.2:
            sentiment = "Negative"
            confidence = min(1.0, abs(polarity) + 0.2)
        elif polarity < 0.0:
            sentiment = "Slightly Negative"
            confidence = min(1.0, abs(polarity) + 0.1)
        else:
            sentiment = "Neutral"
            confidence = max(0.1, 1.0 - abs(subjectivity))

        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'sentiment': sentiment,
            'confidence': confidence,
            'emotional_intensity': intensity,
            'aspects': aspects,
            'keywords': found_keywords
        }

    def scrape_reviews(self, package_name, count=500, sort_by=Sort.NEWEST):
        """Enhanced review scraping with error handling"""
        try:
            with st.spinner(f"Extracting {count} reviews for analysis..."):
                result, continuation_token = reviews(
                    package_name,
                    lang='en',
                    country='us',
                    sort=sort_by,
                    count=count,
                    filter_score_with=None
                )

                if not result:
                    st.warning("No reviews found for this app")
                    return pd.DataFrame()

                # Convert to DataFrame
                df = pd.DataFrame(result)

                # Add advanced analysis
                progress_bar = st.progress(0)
                sentiments = []

                for idx, review in df.iterrows():
                    sentiment_data = self.advanced_sentiment_analysis(review['content'])
                    sentiments.append(sentiment_data)
                    progress_bar.progress((idx + 1) / len(df))

                # Flatten sentiment data
                for idx, sentiment in enumerate(sentiments):
                    for key, value in sentiment.items():
                        if key == 'aspects':
                            for aspect, present in value.items():
                                df.loc[idx, f'aspect_{aspect}'] = present
                        elif key == 'keywords':
                            df.loc[idx, 'keywords'] = ', '.join(value) if value else ''
                        else:
                            df.loc[idx, key] = value

                progress_bar.empty()
                return df

        except Exception as e:
            st.error(f"Error scraping reviews: {str(e)}")
            return pd.DataFrame()

    def generate_ml_insights(self, df):
        """Generate machine learning based insights"""
        if df.empty or 'content' not in df.columns:
            return {}

        try:
            # Prepare text data
            texts = df['content'].fillna('').astype(str)
            processed_texts = [self.preprocess_text(text) for text in texts]

            # TF-IDF Vectorization
            tfidf = TfidfVectorizer(max_features=1000, stop_words='english')
            X_tfidf = tfidf.fit_transform(processed_texts)

            # Topic Modeling with LDA
            lda = LatentDirichletAllocation(n_components=5, random_state=42)
            lda_topics = lda.fit_transform(X_tfidf)

            # Feature names for topics
            feature_names = tfidf.get_feature_names_out()

            # Extract topics
            topics = []
            for topic_idx, topic in enumerate(lda.components_):
                top_words = [feature_names[i] for i in topic.argsort()[-10:][::-1]]
                topics.append({
                    'topic_id': topic_idx + 1,
                    'keywords': top_words,
                    'weight': topic.sum()
                })

            # Clustering
            n_clusters = min(5, len(df) // 10) if len(df) > 50 else 3
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(X_tfidf.toarray())

            # Key phrases extraction
            count_vectorizer = CountVectorizer(ngram_range=(2, 3), max_features=20, stop_words='english')
            phrases = count_vectorizer.fit_transform(processed_texts)
            phrase_freq = zip(count_vectorizer.get_feature_names_out(), 
                            phrases.sum(axis=0).A1)
            key_phrases = sorted(phrase_freq, key=lambda x: x[1], reverse=True)[:10]

            return {
                'topics': topics,
                'clusters': clusters.tolist(),
                'n_clusters': n_clusters,
                'key_phrases': [{'phrase': phrase, 'frequency': freq} for phrase, freq in key_phrases],
                'tfidf_features': feature_names.tolist()[:50]
            }

        except Exception as e:
            st.error(f"Error generating ML insights: {str(e)}")
            return {}

    # NEW: Time series analysis
    def analyze_trends(self, df):
        """Analyze rating trends over time"""
        if df.empty or 'at' not in df.columns:
            return None
            
        df = df.copy()
        df['date'] = pd.to_datetime(df['at']).dt.date
        df['week'] = pd.to_datetime(df['at']).dt.to_period('W').apply(lambda r: r.start_time)
        df['month'] = pd.to_datetime(df['at']).dt.to_period('M').apply(lambda r: r.start_time)
        
        # Daily trends
        daily_stats = df.groupby('date').agg({
            'score': ['mean', 'count'],
            'polarity': 'mean',
            'emotional_intensity': 'mean'
        }).round(3)
        
        daily_stats.columns = ['avg_rating', 'review_count', 'avg_polarity', 'avg_intensity']
        
        # Weekly trends
        weekly_stats = df.groupby('week').agg({
            'score': ['mean', 'count'],
            'polarity': 'mean',
            'emotional_intensity': 'mean'
        }).round(3)
        
        weekly_stats.columns = ['avg_rating', 'review_count', 'avg_polarity', 'avg_intensity']
        
        return {
            'daily': daily_stats,
            'weekly': weekly_stats
        }

# Initialize analyzer
analyzer = ReviewAnalyzer()

def create_header():
    """Create modern header with developer credit"""
    st.markdown("""
    <div class="main-header">
        <h1 class="header-title">ReviewForge Analytics Pro</h1>
        <p class="header-subtitle">Advanced AI-Powered Review Analysis Platform</p>
        <div class="developer-credit">
            Developed by Ayush Pandey - Advanced Analytics & Machine Learning
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_navigation():
    """Create advanced navigation system"""
    st.sidebar.markdown('<div class="sidebar-title">Navigation Hub</div>', unsafe_allow_html=True)

    pages = {
        'dashboard': 'Analytics Dashboard',
        'deep_analysis': 'Deep Analysis Engine',
        'competitor': 'Competitive Intelligence',
        'ml_insights': 'ML Insights Laboratory',
        'trend_analysis': 'Trend Analysis',
        'export_reports': 'Export & Reporting',
        'settings': 'Advanced Settings'
    }

    for page_key, page_name in pages.items():
        if st.sidebar.button(page_name, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.current_page = page_key
            st.rerun()

    # Current page indicator
    st.sidebar.markdown(f"""
    <div class="nav-section">
        <h3>Current Page</h3>
        <p style="color: white; font-weight: 600;">{pages[st.session_state.current_page]}</p>
    </div>
    """, unsafe_allow_html=True)

    # User authentication section
    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="sidebar-title">User Access</div>', unsafe_allow_html=True)
    
    if not st.session_state.user_authenticated:
        if st.sidebar.button("Login", key="login_btn", use_container_width=True):
            st.session_state.user_authenticated = True
            st.session_state.user_role = "admin"
            st.rerun()
    else:
        st.sidebar.success(f"Logged in as: {st.session_state.user_role}")
        if st.sidebar.button("Logout", key="logout_btn", use_container_width=True):
            st.session_state.user_authenticated = False
            st.session_state.user_role = "viewer"
            st.rerun()

def create_metrics_dashboard(df):
    """Create comprehensive metrics dashboard"""
    if df.empty:
        return

    st.subheader("Key Performance Indicators")

    cols = st.columns(5)

    with cols[0]:
        avg_rating = df['score'].mean() if 'score' in df.columns else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_rating:.1f}</div>
            <div class="metric-label">Average Rating</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[1]:
        total_reviews = len(df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_reviews:,}</div>
            <div class="metric-label">Total Reviews</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[2]:
        if 'sentiment' in df.columns:
            positive_rate = (df['sentiment'].str.contains('Positive', na=False).sum() / len(df)) * 100
        else:
            positive_rate = 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{positive_rate:.1f}%</div>
            <div class="metric-label">Positive Rate</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[3]:
        if 'confidence' in df.columns:
            avg_confidence = df['confidence'].mean() * 100
        else:
            avg_confidence = 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_confidence:.1f}%</div>
            <div class="metric-label">Analysis Confidence</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[4]:
        if 'emotional_intensity' in df.columns:
            avg_intensity = abs(df['emotional_intensity'].mean())
        else:
            avg_intensity = 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_intensity:.2f}</div>
            <div class="metric-label">Emotional Intensity</div>
        </div>
        """, unsafe_allow_html=True)

def create_advanced_visualizations(df):
    """Create advanced interactive visualizations"""
    if df.empty:
        return

    # Color scheme
    colors = {
        'primary': '#2563eb',
        'secondary': '#3b82f6',
        'accent': '#1e40af',
        'success': '#059669',
        'warning': '#d97706',
        'error': '#dc2626',
        'positive': '#10b981',
        'negative': '#ef4444',
        'neutral': '#6b7280'
    }

    # 1. Enhanced Sentiment Distribution
    col1, col2 = st.columns(2)

    with col1:
        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts()

            fig_donut = go.Figure(data=[go.Pie(
                labels=sentiment_counts.index,
                values=sentiment_counts.values,
                hole=0.6,
                marker=dict(
                    colors=[colors['positive'] if 'Positive' in s else 
                           colors['negative'] if 'Negative' in s else colors['neutral'] 
                           for s in sentiment_counts.index]
                ),
                textinfo='label+percent+value',
                textfont=dict(size=14),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])

            fig_donut.update_layout(
                title=dict(
                    text='Sentiment Distribution Analysis',
                    x=0.5,
                    font=dict(size=20, color=colors['primary'])
                ),
                annotations=[dict(
                    text=f'Total<br>{sentiment_counts.sum()}',
                    x=0.5, y=0.5,
                    font_size=16,
                    showarrow=False
                )],
                showlegend=True,
                height=400
            )

            st.plotly_chart(fig_donut, use_container_width=True)

    with col2:
        if 'score' in df.columns:
            rating_dist = df['score'].value_counts().sort_index()

            fig_rating = go.Figure()
            fig_rating.add_trace(go.Bar(
                x=[f'{i} Stars' for i in rating_dist.index],
                y=rating_dist.values,
                marker=dict(
                    color=[colors['error'] if i <= 2 else 
                          colors['warning'] if i == 3 else colors['success'] 
                          for i in rating_dist.index]
                ),
                text=rating_dist.values,
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Count: %{y}<br>Percentage: %{y}<extra></extra>'
            ))

            fig_rating.update_layout(
                title=dict(
                    text='Rating Distribution',
                    x=0.5,
                    font=dict(size=20, color=colors['primary'])
                ),
                xaxis_title='Rating',
                yaxis_title='Number of Reviews',
                showlegend=False,
                height=400
            )

            st.plotly_chart(fig_rating, use_container_width=True)

    # 2. Emotional Intensity Heatmap
    if all(col in df.columns for col in ['score', 'emotional_intensity']):
        st.subheader("Emotional Intensity vs Rating Analysis")

        intensity_by_rating = df.groupby('score')['emotional_intensity'].agg(['mean', 'std', 'count']).reset_index()

        fig_intensity = go.Figure()

        fig_intensity.add_trace(go.Scatter(
            x=intensity_by_rating['score'],
            y=intensity_by_rating['mean'],
            mode='lines+markers',
            name='Average Intensity',
            line=dict(color=colors['primary'], width=3),
            marker=dict(size=10),
            error_y=dict(
                type='data',
                array=intensity_by_rating['std'],
                visible=True
            )
        ))

        fig_intensity.update_layout(
            title='Emotional Intensity by Rating',
            xaxis_title='Rating',
            yaxis_title='Average Emotional Intensity',
            height=400
        )

        st.plotly_chart(fig_intensity, use_container_width=True)

    # 3. Aspect Analysis Radar Chart
    aspect_cols = [col for col in df.columns if col.startswith('aspect_')]
    if aspect_cols:
        st.subheader("Aspect Analysis Overview")

        aspect_data = {}
        for col in aspect_cols:
            aspect_name = col.replace('aspect_', '').replace('_', ' ').title()
            aspect_data[aspect_name] = (df[col].sum() / len(df)) * 100

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=list(aspect_data.values()),
            theta=list(aspect_data.keys()),
            fill='toself',
            name='Aspect Coverage',
            line=dict(color=colors['primary'])
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(aspect_data.values()) * 1.1]
                )
            ),
            title='Aspect Coverage Analysis',
            height=500
        )

        st.plotly_chart(fig_radar, use_container_width=True)

def dashboard_page():
    """Main dashboard page"""
    create_header()

    # Input section
    st.subheader("Application Analysis Configuration")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        url_input = st.text_input(
            "Google Play Store URL or Package Name",
            placeholder="https://play.google.com/store/apps/details?id=com.example.app",
            help="Enter the full Google Play Store URL or just the package name"
        )

    with col2:
        review_count = st.selectbox(
            "Reviews to Analyze",
            options=[100, 250, 500, 1000, 2000],
            index=2,
            help="More reviews provide better insights but take longer to process"
        )

    with col3:
        sort_option = st.selectbox(
            "Sort Reviews By",
            options=["Newest", "Rating", "Helpfulness"],
            help="Choose how to sort the reviews for analysis"
        )

    # Convert sort option
    sort_mapping = {
        "Newest": Sort.NEWEST,
        "Rating": Sort.RATING,
        "Helpfulness": Sort.MOST_RELEVANT
    }

    if st.button("Analyze Application", type="primary", use_container_width=True):
        if url_input:
            package_name = analyzer.extract_package_name(url_input)

            if package_name:
                with st.spinner("Performing advanced analysis..."):
                    # Use cached version for better performance
                    df = cached_scrape_reviews(
                        package_name, 
                        count=review_count, 
                        sort_by=sort_mapping[sort_option]
                    )

                    if not df.empty:
                        st.session_state.analyzed_data = df
                        st.session_state.current_app_name = analyzer.get_app_name(package_name)
                        st.success(f"Successfully analyzed {len(df)} reviews!")
                    else:
                        st.error("No reviews found or failed to extract reviews")
            else:
                st.error("Invalid URL or package name format")
        else:
            st.warning("Please enter a valid Google Play Store URL or package name")

    # Display results
    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data

        st.markdown("---")
        st.subheader(f"Analysis Results: {st.session_state.get('current_app_name', 'Unknown App')}")

        # Metrics dashboard
        create_metrics_dashboard(df)

        # Visualizations
        create_advanced_visualizations(df)

        # Recent reviews table
        st.subheader("Recent Reviews Sample")
        display_columns = ['at', 'userName', 'score', 'sentiment', 'confidence', 'content']
        available_columns = [col for col in display_columns if col in df.columns]

        if available_columns:
            sample_df = df[available_columns].head(10).copy()
            if 'at' in sample_df.columns:
                sample_df['at'] = pd.to_datetime(sample_df['at']).dt.strftime('%Y-%m-%d')
            if 'content' in sample_df.columns:
                sample_df['content'] = sample_df['content'].str[:100] + '...'

            st.dataframe(sample_df, use_container_width=True, hide_index=True)

def deep_analysis_page():
    """Deep analysis page with advanced features"""
    st.title("Deep Analysis Engine")
    st.markdown("Advanced analytical tools and machine learning insights")

    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data

        # Generate ML insights if not already done
        if 'ml_insights' not in st.session_state or not st.session_state.ml_insights:
            with st.spinner("Generating machine learning insights..."):
                # Use cached version for better performance
                ml_insights = cached_generate_ml_insights(df)
                st.session_state.ml_insights = ml_insights

        ml_insights = st.session_state.ml_insights

        # Topic Analysis
        st.subheader("Topic Modeling Analysis")
        if 'topics' in ml_insights and ml_insights['topics']:
            topics_data = []
            for topic in ml_insights['topics']:
                topics_data.append({
                    'Topic ID': topic['topic_id'],
                    'Keywords': ', '.join(topic['keywords'][:5]),
                    'Relevance Score': f"{topic['weight']:.3f}"
                })

            topics_df = pd.DataFrame(topics_data)
            st.dataframe(topics_df, use_container_width=True, hide_index=True)

            # Topic visualization
            if len(ml_insights['topics']) > 1:
                topic_weights = [topic['weight'] for topic in ml_insights['topics']]
                topic_labels = [f"Topic {topic['topic_id']}" for topic in ml_insights['topics']]

                fig_topics = go.Figure(data=[go.Bar(
                    x=topic_labels,
                    y=topic_weights,
                    marker_color='rgba(37, 99, 235, 0.7)'
                )])

                fig_topics.update_layout(
                    title='Topic Importance Distribution',
                    xaxis_title='Topics',
                    yaxis_title='Relevance Score',
                    height=400
                )

                st.plotly_chart(fig_topics, use_container_width=True)

        # Key Phrases Analysis
        st.subheader("Key Phrases Extraction")
        if 'key_phrases' in ml_insights and ml_insights['key_phrases']:
            phrases_data = []
            for phrase_data in ml_insights['key_phrases'][:10]:
                phrases_data.append({
                    'Phrase': phrase_data['phrase'],
                    'Frequency': phrase_data['frequency'],
                    'Relevance': 'High' if phrase_data['frequency'] > 5 else 'Medium'
                })

            phrases_df = pd.DataFrame(phrases_data)
            st.dataframe(phrases_df, use_container_width=True, hide_index=True)

        # Correlation Analysis
        st.subheader("Advanced Correlation Analysis")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()

            fig_corr = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="Feature Correlation Matrix",
                color_continuous_scale='RdBu_r'
            )

            st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Please analyze an application first from the Dashboard page to access deep analysis features.")

def competitor_analysis_page():
    """Competitive intelligence page"""
    st.title("Competitive Intelligence")
    st.markdown("Compare your app against competitors with advanced benchmarking")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Primary App Analysis")
        if st.session_state.analyzed_data is not None:
            st.success(f"âœ“ {st.session_state.get('current_app_name', 'App')} analyzed")
            df_primary = st.session_state.analyzed_data

            # Primary app metrics
            if 'score' in df_primary.columns:
                avg_rating = df_primary['score'].mean()
                st.metric("Average Rating", f"{avg_rating:.1f}")

            if 'sentiment' in df_primary.columns:
                positive_rate = (df_primary['sentiment'].str.contains('Positive', na=False).sum() / len(df_primary)) * 100
                st.metric("Positive Sentiment", f"{positive_rate:.1f}%")
        else:
            st.info("Analyze your primary app first")

    with col2:
        st.subheader("Competitor App")
        competitor_url = st.text_input(
            "Competitor App URL",
            placeholder="Enter competitor's Google Play URL"
        )

        if st.button("Analyze Competitor", use_container_width=True):
            if competitor_url:
                package_name = analyzer.extract_package_name(competitor_url)

                if package_name:
                    with st.spinner("Analyzing competitor..."):
                        # Use cached version for better performance
                        competitor_df = cached_scrape_reviews(package_name, count=500)

                        if not competitor_df.empty:
                            st.session_state.competitor_data = competitor_df
                            st.session_state.competitor_app_name = analyzer.get_app_name(package_name)
                            st.success("Competitor analyzed successfully!")
                        else:
                            st.error("Failed to analyze competitor")
                else:
                    st.error("Invalid competitor URL")

    # Comparative Analysis
    if (st.session_state.analyzed_data is not None and 
        st.session_state.competitor_data is not None):

        st.markdown("---")
        st.subheader("Comparative Analysis Dashboard")

        df_primary = st.session_state.analyzed_data
        df_competitor = st.session_state.competitor_data

        # Side-by-side metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### Rating Comparison")
            primary_rating = df_primary['score'].mean() if 'score' in df_primary.columns else 0
            competitor_rating = df_competitor['score'].mean() if 'score' in df_competitor.columns else 0

            comparison_data = pd.DataFrame({
                'App': [st.session_state.get('current_app_name', 'Your App'), 
                       st.session_state.get('competitor_app_name', 'Competitor')],
                'Rating': [primary_rating, competitor_rating]
            })

            fig_rating_comp = px.bar(
                comparison_data,
                x='App',
                y='Rating',
                title='Average Rating Comparison',
                color='Rating',
                color_continuous_scale='RdYlGn'
            )

            st.plotly_chart(fig_rating_comp, use_container_width=True)

        with col2:
            st.markdown("### Sentiment Comparison")
            if all('sentiment' in df.columns for df in [df_primary, df_competitor]):
                primary_positive = (df_primary['sentiment'].str.contains('Positive', na=False).sum() / len(df_primary)) * 100
                competitor_positive = (df_competitor['sentiment'].str.contains('Positive', na=False).sum() / len(df_competitor)) * 100

                sentiment_data = pd.DataFrame({
                    'App': [st.session_state.get('current_app_name', 'Your App'), 
                           st.session_state.get('competitor_app_name', 'Competitor')],
                    'Positive Sentiment %': [primary_positive, competitor_positive]
                })

                fig_sentiment_comp = px.bar(
                    sentiment_data,
                    x='App',
                    y='Positive Sentiment %',
                    title='Positive Sentiment Comparison',
                    color='Positive Sentiment %',
                    color_continuous_scale='RdYlGn'
                )

                st.plotly_chart(fig_sentiment_comp, use_container_width=True)

        with col3:
            st.markdown("### Review Volume")
            volume_data = pd.DataFrame({
                'App': [st.session_state.get('current_app_name', 'Your App'), 
                       st.session_state.get('competitor_app_name', 'Competitor')],
                'Review Count': [len(df_primary), len(df_competitor)]
            })

            fig_volume_comp = px.bar(
                volume_data,
                x='App',
                y='Review Count',
                title='Review Volume Comparison',
                color='Review Count',
                color_continuous_scale='Blues'
            )

            st.plotly_chart(fig_volume_comp, use_container_width=True)

        # Detailed comparison table
        st.subheader("Detailed Comparison Matrix")

        comparison_metrics = {
            'Metric': ['Average Rating', 'Total Reviews', 'Positive Sentiment %', 'Average Confidence', 'Emotional Intensity'],
            st.session_state.get('current_app_name', 'Your App'): [
                f"{df_primary['score'].mean():.2f}" if 'score' in df_primary.columns else 'N/A',
                len(df_primary),
                f"{(df_primary['sentiment'].str.contains('Positive', na=False).sum() / len(df_primary)) * 100:.1f}%" if 'sentiment' in df_primary.columns else 'N/A',
                f"{df_primary['confidence'].mean() * 100:.1f}%" if 'confidence' in df_primary.columns else 'N/A',
                f"{abs(df_primary['emotional_intensity'].mean()):.2f}" if 'emotional_intensity' in df_primary.columns else 'N/A'
            ],
            st.session_state.get('competitor_app_name', 'Competitor'): [
                f"{df_competitor['score'].mean():.2f}" if 'score' in df_competitor.columns else 'N/A',
                len(df_competitor),
                f"{(df_competitor['sentiment'].str.contains('Positive', na=False).sum() / len(df_competitor)) * 100:.1f}%" if 'sentiment' in df_competitor.columns else 'N/A',
                f"{df_competitor['confidence'].mean() * 100:.1f}%" if 'confidence' in df_competitor.columns else 'N/A',
                f"{abs(df_competitor['emotional_intensity'].mean()):.2f}" if 'emotional_intensity' in df_competitor.columns else 'N/A'
            ]
        }

        comparison_df = pd.DataFrame(comparison_metrics)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

def trend_analysis_page():
    """Time series analysis page"""
    st.title("Trend Analysis")
    st.markdown("Analyze how reviews and ratings change over time")

    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data
        
        # Generate trend analysis
        trends = analyzer.analyze_trends(df)
        
        if trends:
            st.subheader("Rating Trends Over Time")
            
            # Daily trends chart
            daily_data = trends['daily'].reset_index()
            
            fig_daily = px.line(
                daily_data, 
                x='date', 
                y='avg_rating',
                title='Daily Average Rating Trend',
                labels={'date': 'Date', 'avg_rating': 'Average Rating'}
            )
            
            fig_daily.add_scatter(
                x=daily_data['date'],
                y=[daily_data['avg_rating'].mean()] * len(daily_data),
                mode='lines',
                name='Overall Average',
                line=dict(dash='dash', color='red')
            )
            
            st.plotly_chart(fig_daily, use_container_width=True)
            
            # Review volume over time
            st.subheader("Review Volume Over Time")
            
            fig_volume = px.bar(
                daily_data,
                x='date',
                y='review_count',
                title='Daily Review Volume',
                labels={'date': 'Date', 'review_count': 'Number of Reviews'}
            )
            
            st.plotly_chart(fig_volume, use_container_width=True)
            
            # Weekly trends
            st.subheader("Weekly Trends")
            
            weekly_data = trends['weekly'].reset_index()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_weekly_rating = px.line(
                    weekly_data,
                    x='week',
                    y='avg_rating',
                    title='Weekly Average Rating',
                    labels={'week': 'Week', 'avg_rating': 'Average Rating'}
                )
                st.plotly_chart(fig_weekly_rating, use_container_width=True)
                
            with col2:
                fig_weekly_volume = px.bar(
                    weekly_data,
                    x='week',
                    y='review_count',
                    title='Weekly Review Volume',
                    labels={'week': 'Week', 'review_count': 'Number of Reviews'}
                )
                st.plotly_chart(fig_weekly_volume, use_container_width=True)
                
            # Correlation between review volume and rating
            st.subheader("Volume vs Rating Correlation")
            
            correlation = daily_data['review_count'].corr(daily_data['avg_rating'])
            
            st.metric("Correlation Coefficient", f"{correlation:.3f}")
            
            if correlation > 0.3:
                st.info("Positive correlation: More reviews tend to coincide with higher ratings")
            elif correlation < -0.3:
                st.info("Negative correlation: More reviews tend to coincide with lower ratings")
            else:
                st.info("Weak correlation: Review volume and rating are not strongly related")
                
        else:
            st.warning("Insufficient data for trend analysis. Need reviews with timestamps.")
    else:
        st.info("Please analyze an application first to access trend analysis.")

def settings_page():
    """Advanced settings and preferences"""
    st.title("Advanced Settings")
    st.markdown("Customize your analysis preferences and export options")

    # Analysis Settings
    st.subheader("Analysis Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Sentiment Analysis Settings")
        sentiment_threshold = st.slider("Sentiment Confidence Threshold", 0.0, 1.0, 0.6, 0.1)
        enable_aspect_analysis = st.checkbox("Enable Aspect-Based Analysis", value=True)
        enable_emotion_detection = st.checkbox("Enable Emotional Intensity Analysis", value=True)

    with col2:
        st.markdown("#### Machine Learning Settings")
        enable_topic_modeling = st.checkbox("Enable Topic Modeling", value=True)
        topic_count = st.slider("Number of Topics", 3, 10, 5)
        enable_clustering = st.checkbox("Enable Review Clustering", value=True)

    # Export Settings
    st.subheader("Export & Reporting")

    export_format = st.selectbox(
        "Preferred Export Format",
        options=["CSV", "Excel", "JSON", "PDF Report"],
        index=0
    )

    include_raw_data = st.checkbox("Include Raw Review Data", value=True)
    include_visualizations = st.checkbox("Include Charts and Visualizations", value=True)

    # Save settings
    if st.button("Save Settings", type="primary"):
        settings = {
            'sentiment_threshold': sentiment_threshold,
            'enable_aspect_analysis': enable_aspect_analysis,
            'enable_emotion_detection': enable_emotion_detection,
            'enable_topic_modeling': enable_topic_modeling,
            'topic_count': topic_count,
            'enable_clustering': enable_clustering,
            'export_format': export_format,
            'include_raw_data': include_raw_data,
            'include_visualizations': include_visualizations
        }
        st.session_state.user_preferences = settings
        st.success("Settings saved successfully!")

    # System Information
    st.subheader("System Information")

    system_info = {
        'Application Version': '2.0.0 Pro',
        'Developer': 'Ayush Pandey',
        'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Python Version': '3.9+',
        'Streamlit Version': st.__version__ if hasattr(st, '__version__') else 'Latest',
        'Analysis Engine': 'Advanced ML-Powered'
    }

    for key, value in system_info.items():
        st.text(f"{key}: {value}")

def export_reports_page():
    """Export and reporting functionality"""
    st.title("Export & Reporting")
    st.markdown("Generate comprehensive reports and export your analysis data")

    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data
        app_name = st.session_state.get('current_app_name', 'Unknown App')

        st.subheader(f"Export Options for {app_name}")

        # Export format selection
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Export as CSV", use_container_width=True):
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV Report",
                    data=csv_data,
                    file_name=f"{app_name}_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

        with col2:
            if st.button("Export as Excel", use_container_width=True):
                try:
                    excel_buffer = BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='Analysis Results', index=False)

                        # Add summary sheet if we have sentiment data
                        if 'sentiment' in df.columns:
                            summary_data = {
                                'Metric': ['Total Reviews', 'Average Rating', 'Positive Sentiment %', 'Negative Sentiment %'],
                                'Value': [
                                    len(df),
                                    f"{df['score'].mean():.2f}" if 'score' in df.columns else 'N/A',
                                    f"{(df['sentiment'].str.contains('Positive', na=False).sum() / len(df)) * 100:.1f}%",
                                    f"{(df['sentiment'].str.contains('Negative', na=False).sum() / len(df)) * 100:.1f}%"
                                ]
                            }
                            summary_df = pd.DataFrame(summary_data)
                            summary_df.to_excel(writer, sheet_name='Summary', index=False)

                    excel_data = excel_buffer.getvalue()
                    st.download_button(
                        label="Download Excel Report",
                        data=excel_data,
                        file_name=f"{app_name}_analysis_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except Exception as e:
                    st.error(f"Error creating Excel file: {str(e)}")

        with col3:
            if st.button("Export as JSON", use_container_width=True):
                json_data = df.to_json(orient='records', date_format='iso')
                st.download_button(
                    label="Download JSON Data",
                    data=json_data,
                    file_name=f"{app_name}_analysis_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

        # Quick preview of export data
        st.subheader("Export Preview")

        export_columns = st.multiselect(
            "Select columns to include in export",
            options=df.columns.tolist(),
            default=[col for col in ['at', 'userName', 'score', 'sentiment', 'confidence', 'content'] 
                    if col in df.columns]
        )

        if export_columns:
            preview_df = df[export_columns].head(10)
            st.dataframe(preview_df, use_container_width=True, hide_index=True)

            st.info(f"Preview showing first 10 rows. Full export will contain {len(df)} rows.")

        # Generate comprehensive report
        st.subheader("Comprehensive Analysis Report")

        if st.button("Generate Full Report", type="primary"):
            with st.spinner("Generating comprehensive report..."):
                report_content = f"""
# {app_name} - Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Developed by: Ayush Pandey - ReviewForge Analytics Pro

## Executive Summary
- **Total Reviews Analyzed:** {len(df):,}
- **Analysis Period:** {df['at'].min() if 'at' in df.columns else 'N/A'} to {df['at'].max() if 'at' in df.columns else 'N/A'}
- **Average Rating:** {df['score'].mean():.2f} / 5.0 ({df['score'].std():.2f} std dev)
- **Sentiment Distribution:**
  - Positive: {(df['sentiment'].str.contains('Positive', na=False).sum() / len(df)) * 100:.1f}%
  - Neutral: {(df['sentiment'].str.contains('Neutral', na=False).sum() / len(df)) * 100:.1f}%
  - Negative: {(df['sentiment'].str.contains('Negative', na=False).sum() / len(df)) * 100:.1f}%

## Key Insights
- **Analysis Confidence:** {df['confidence'].mean() * 100:.1f}% average confidence
- **Emotional Intensity:** {abs(df['emotional_intensity'].mean()):.2f} average intensity
- **Most Common Rating:** {df['score'].mode().iloc[0] if 'score' in df.columns and not df['score'].mode().empty else 'N/A'} stars

## Recommendations
Based on the analysis of {len(df):,} reviews, the following strategic recommendations are suggested:

1. **Performance Optimization:** {'Focus on addressing performance issues mentioned in reviews' if any(df['content'].str.contains('slow|lag|crash', case=False, na=False)) else 'Current performance appears satisfactory based on user feedback'}

2. **User Experience:** {'Consider UI/UX improvements based on user feedback patterns' if any(df['content'].str.contains('interface|design|ui', case=False, na=False)) else 'User interface receives positive feedback overall'}

3. **Feature Development:** {'Users are requesting additional features - consider feature roadmap expansion' if any(df['content'].str.contains('feature|add|need', case=False, na=False)) else 'Current feature set appears to meet user expectations'}

---
*Report generated by ReviewForge Analytics Pro - Advanced Review Analysis Platform*
*Developer: Ayush Pandey*
                """

                st.markdown(report_content)

                st.download_button(
                    label="Download Full Report (Markdown)",
                    data=report_content,
                    file_name=f"{app_name}_full_report_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
    else:
        st.info("Please analyze an application first to access export functionality.")

# Main application logic
def main():
    """Main application controller"""
    create_navigation()

    # Page routing
    if st.session_state.current_page == 'dashboard':
        dashboard_page()
    elif st.session_state.current_page == 'deep_analysis':
        deep_analysis_page()
    elif st.session_state.current_page == 'competitor':
        competitor_analysis_page()
    elif st.session_state.current_page == 'ml_insights':
        deep_analysis_page()  # Reuse deep analysis for ML insights
    elif st.session_state.current_page == 'trend_analysis':
        trend_analysis_page()
    elif st.session_state.current_page == 'export_reports':
        export_reports_page()
    elif st.session_state.current_page == 'settings':
        settings_page()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; margin-top: 2rem;">
        <p><strong>ReviewForge Analytics Pro</strong> - Advanced AI-Powered Review Analysis Platform</p>
        <p>Developed by <strong>Ayush Pandey</strong> | Version 2.0.0 Pro | Â© 2024</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
