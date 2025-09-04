# Combined enhanced application with all improvements
# Part 1: Imports, styling, and core classes

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
warnings.filterwarnings('ignore')

# Enhanced NLTK data download with error handling
def download_nltk_requirements():
    """Download required NLTK data with proper error handling"""
    required_data = [
        ('tokenizers/punkt', 'punkt'),
        ('tokenizers/punkt_tab', 'punkt_tab'),
        ('corpora/stopwords', 'stopwords'),
        ('corpora/wordnet', 'wordnet'),
        ('corpora/omw-1.4', 'omw-1.4')
    ]

    for data_path, download_name in required_data:
        try:
            nltk.data.find(data_path)
        except LookupError:
            try:
                nltk.download(download_name, quiet=True)
            except Exception:
                pass  # Silently handle download failures

download_nltk_requirements()

# Enhanced Page Configuration
st.set_page_config(
    page_title="ReviewForge Analytics Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "ReviewForge Analytics Pro - Advanced Review Analysis Platform"
    }
)

# Enhanced CSS Styling with Modern Design and Animations
def apply_enhanced_styling():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Enhanced Root Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --error-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --dark-gradient: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%);
        --card-bg: rgba(255, 255, 255, 0.98);
        --glass-bg: rgba(255, 255, 255, 0.15);
        --text-primary: #1a202c;
        --text-secondary: #4a5568;
        --border-color: rgba(255, 255, 255, 0.2);
        --shadow-soft: 0 8px 32px rgba(31, 38, 135, 0.15);
        --shadow-hard: 0 20px 40px rgba(31, 38, 135, 0.25);
        --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        --border-radius: 16px;
    }

    /* Global Styles with Enhanced Animations */
    .main, .block-container {
        font-family: 'Inter', sans-serif !important;
        background: var(--primary-gradient);
        min-height: 100vh;
        animation: gradientShift 10s ease infinite;
    }

    @keyframes gradientShift {
        0%, 100% { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        25% { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        50% { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
        75% { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
    }

    /* Enhanced Header with Animation */
    .enhanced-header {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        padding: 2.5rem;
        border-radius: var(--border-radius);
        margin: 1rem 0 2rem 0;
        box-shadow: var(--shadow-hard);
        animation: slideInDown 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }

    .enhanced-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 3s infinite;
    }

    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .header-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2, #fa709a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        animation: textGlow 2s ease-in-out infinite alternate;
    }

    @keyframes textGlow {
        from { filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.5)); }
        to { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.8)); }
    }

    .header-subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }

    .developer-badge {
        background: var(--secondary-gradient);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-weight: 700;
        text-align: center;
        font-size: 1rem;
        box-shadow: var(--shadow-soft);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    /* Enhanced Cards with Glass Morphism */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: var(--shadow-hard);
        border-color: rgba(255, 255, 255, 0.4);
    }

    .metric-card {
        background: var(--card-bg);
        border-radius: var(--border-radius);
        padding: 1.8rem;
        text-align: center;
        box-shadow: var(--shadow-soft);
        transition: var(--transition);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-hard);
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
    }

    .metric-value {
        font-size: 2.8rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Enhanced Sidebar */
    .css-1d391kg {
        background: var(--dark-gradient) !important;
    }

    .sidebar-section {
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-soft);
    }

    .current-page-indicator {
        background: var(--success-gradient) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 1rem !important;
        border-radius: var(--border-radius) !important;
        text-align: center !important;
        box-shadow: var(--shadow-soft) !important;
        animation: glow 2s ease-in-out infinite alternate !important;
    }

    @keyframes glow {
        from { box-shadow: 0 0 10px rgba(67, 233, 123, 0.5); }
        to { box-shadow: 0 0 20px rgba(67, 233, 123, 0.8); }
    }

    /* Enhanced Buttons */
    .enhanced-button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: var(--transition) !important;
        box-shadow: var(--shadow-soft) !important;
        position: relative !important;
        overflow: hidden !important;
        cursor: pointer !important;
    }

    .enhanced-button:hover {
        transform: translateY(-3px) !important;
        box-shadow: var(--shadow-hard) !important;
        filter: brightness(1.1) !important;
    }

    .enhanced-button:active {
        transform: translateY(-1px) !important;
    }

    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 700 !important;
        transition: var(--transition) !important;
        box-shadow: var(--shadow-soft) !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: var(--shadow-hard) !important;
        filter: brightness(1.1) !important;
    }

    /* Enhanced Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background: var(--card-bg) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: var(--transition) !important;
        box-shadow: var(--shadow-soft) !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        transform: scale(1.02) !important;
    }

    /* Enhanced Charts Container */
    .chart-container {
        background: var(--card-bg);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: var(--transition);
    }

    .chart-container:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-hard);
    }

    .chart-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
        text-align: center;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Enhanced Progress Bar */
    .stProgress > div > div > div > div {
        background: var(--primary-gradient) !important;
        border-radius: 10px !important;
        height: 12px !important;
        animation: progressGlow 2s ease-in-out infinite alternate !important;
    }

    @keyframes progressGlow {
        from { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
        to { box-shadow: 0 0 15px rgba(102, 126, 234, 0.8); }
    }

    /* Enhanced Alert Messages */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: var(--border-radius) !important;
        padding: 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: var(--shadow-soft) !important;
        border: none !important;
    }

    .stSuccess {
        background: var(--success-gradient) !important;
        color: white !important;
    }

    .stWarning {
        background: var(--warning-gradient) !important;
        color: white !important;
    }

    .stError {
        background: var(--error-gradient) !important;
        color: white !important;
    }

    /* Enhanced DataFrames */
    .stDataFrame {
        border-radius: var(--border-radius) !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-soft) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Enhanced Scrollable Reviews Container */
    .reviews-container {
        background: var(--card-bg);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-height: 600px;
        overflow-y: auto;
        transition: var(--transition);
    }

    .review-item {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        transition: var(--transition);
    }

    .review-item:hover {
        transform: translateX(10px);
        box-shadow: var(--shadow-soft);
    }

    .review-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        font-weight: 600;
    }

    .review-rating {
        background: var(--primary-gradient);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
    }

    .review-content {
        line-height: 1.6;
        color: var(--text-secondary);
        margin-bottom: 1rem;
    }

    .review-sentiment {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }

    .sentiment-positive {
        background: var(--success-gradient);
        color: white;
    }

    .sentiment-negative {
        background: var(--error-gradient);
        color: white;
    }

    .sentiment-neutral {
        background: var(--warning-gradient);
        color: white;
    }

    /* Filter Section */
    .filter-section {
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-soft);
    }

    /* Animation Classes */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }

    /* Enhanced Tooltips */
    .tooltip {
        position: relative;
        cursor: help;
    }

    .tooltip::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background: var(--dark-gradient);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.8rem;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s;
        box-shadow: var(--shadow-soft);
    }

    .tooltip:hover::after {
        opacity: 1;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 6px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 6px;
        border: 2px solid transparent;
        background-clip: content-box;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
        background-clip: content-box;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.5rem;
        }

        .metric-card {
            padding: 1.2rem;
        }

        .metric-value {
            font-size: 2.2rem;
        }

        .glass-card {
            padding: 1.5rem;
        }
    }

    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 4px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

apply_enhanced_styling()

# Enhanced Session State Management
def initialize_session_state():
    """Initialize session state with enhanced defaults"""
    session_defaults = {
        'current_page': 'dashboard',
        'analyzed_data': None,
        'competitor_data': None,
        'analysis_history': [],
        'user_preferences': {
            'sentiment_model': 'advanced',
            'chart_theme': 'modern',
            'analysis_depth': 'comprehensive',
            'export_format': 'excel'
        },
        'ml_models': {},
        'advanced_insights': {},
        'export_data': None,
        'filter_settings': {
            'date_range': None,
            'rating_filter': 'all',
            'sentiment_filter': 'all'
        }
    }

    for key, default_value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

initialize_session_state()

# Enhanced Review Analyzer Class
class EnhancedReviewAnalyzer:
    def __init__(self):
        # Initialize with fallback for NLTK
        try:
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
        except:
            # Fallback if NLTK data not available
            self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
            self.lemmatizer = None

        self.ml_models = {
            'naive_bayes': MultinomialNB(),
            'logistic_regression': LogisticRegression(max_iter=1000),
            'random_forest': RandomForestClassifier(n_estimators=100)
        }

        # Enhanced emotional keywords with weights
        self.emotional_keywords = {
            'excellent': 2.0, 'amazing': 1.8, 'outstanding': 1.7, 'perfect': 1.6,
            'wonderful': 1.5, 'fantastic': 1.4, 'great': 1.2, 'good': 1.0,
            'love': 1.8, 'awesome': 1.6, 'brilliant': 1.5, 'superb': 1.4,
            'terrible': -2.0, 'awful': -1.8, 'horrible': -1.7, 'worst': -1.6,
            'hate': -1.5, 'disgusting': -1.4, 'bad': -1.2, 'poor': -1.0,
            'useless': -1.6, 'trash': -1.8, 'garbage': -1.7, 'stupid': -1.3
        }

    def extract_package_name(self, url):
        """Extract package name from Google Play URL with enhanced validation"""
        if not url or not isinstance(url, str):
            return None

        # Handle direct package names
        if '.' in url and not url.startswith('http'):
            if self.validate_package_name(url):
                return url

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
        """Enhanced package name validation"""
        if not package_name:
            return False
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)*$'
        return bool(re.match(pattern, package_name)) and len(package_name.split('.')) >= 2

    def get_app_name(self, package_name):
        """Extract readable app name from package name"""
        if not package_name:
            return "Unknown App"
        parts = package_name.split('.')
        return parts[-1].replace('_', ' ').title()

    def preprocess_text(self, text):
        """Enhanced text preprocessing with fallback"""
        if pd.isna(text) or not isinstance(text, str):
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove URLs, mentions, hashtags
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        text = re.sub(r'@\w+|#\w+', '', text)

        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)

        # Basic tokenization if NLTK not available
        try:
            if self.lemmatizer:
                tokens = word_tokenize(text)
                tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                         if token not in self.stop_words and len(token) > 2]
            else:
                tokens = [word for word in text.split() 
                         if word not in self.stop_words and len(word) > 2]
        except:
            tokens = [word for word in text.split() if len(word) > 2]

        return ' '.join(tokens)

    def enhanced_sentiment_analysis(self, text):
        """Simplified and enhanced sentiment analysis"""
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
        try:
            blob = TextBlob(str(text))
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
        except:
            polarity = 0.0
            subjectivity = 0.5

        # Enhanced emotional intensity calculation
        intensity = 0.0
        text_lower = text.lower()
        found_keywords = []

        for word, weight in self.emotional_keywords.items():
            if word in text_lower:
                intensity += weight
                found_keywords.append(word)

        # Normalize intensity
        intensity = max(-2.0, min(2.0, intensity))

        # Enhanced aspect-based analysis
        aspects = {
            'performance': any(word in text_lower for word in 
                             ['fast', 'slow', 'speed', 'lag', 'performance', 'responsive', 'quick', 'freeze']),
            'ui_design': any(word in text_lower for word in 
                           ['design', 'interface', 'ui', 'layout', 'beautiful', 'ugly', 'visual', 'look']),
            'functionality': any(word in text_lower for word in 
                               ['feature', 'function', 'work', 'broken', 'bug', 'crash', 'issue', 'error']),
            'usability': any(word in text_lower for word in 
                           ['easy', 'difficult', 'simple', 'complex', 'intuitive', 'confusing', 'user']),
            'reliability': any(word in text_lower for word in 
                             ['stable', 'crash', 'freeze', 'reliable', 'consistent', 'glitch', 'problem'])
        }

        # Simplified sentiment classification (only Positive, Negative, Neutral)
        if polarity > 0.1:
            sentiment = "Positive"
            confidence = min(1.0, abs(polarity) + 0.2)
        elif polarity < -0.1:
            sentiment = "Negative"
            confidence = min(1.0, abs(polarity) + 0.2)
        else:
            sentiment = "Neutral"
            confidence = max(0.3, 1.0 - abs(subjectivity))

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
        """Enhanced review scraping with better error handling"""
        try:
            with st.spinner(f"🔍 Extracting {count} reviews for comprehensive analysis..."):
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

                # Add progress bar with enhanced styling
                progress_container = st.empty()
                progress_text = st.empty()

                sentiments = []

                for idx, review in df.iterrows():
                    progress_text.markdown(f"**Analyzing Review {idx + 1}/{len(df)}**")
                    progress_container.progress((idx + 1) / len(df))

                    sentiment_data = self.enhanced_sentiment_analysis(review['content'])
                    sentiments.append(sentiment_data)

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

                progress_container.empty()
                progress_text.empty()
                return df

        except Exception as e:
            st.error(f"❌ Error scraping reviews: {str(e)}")
            return pd.DataFrame()

    def generate_enhanced_ml_insights(self, df):
        """Generate comprehensive ML insights with error handling"""
        if df.empty or 'content' not in df.columns:
            return {}

        try:
            # Prepare text data
            texts = df['content'].fillna('').astype(str)
            processed_texts = [self.preprocess_text(text) for text in texts]

            # Remove empty texts
            processed_texts = [text for text in processed_texts if text.strip()]

            if not processed_texts:
                return {'error': 'No valid text data for analysis'}

            # TF-IDF Vectorization with error handling
            try:
                tfidf = TfidfVectorizer(max_features=1000, stop_words='english', min_df=2)
                X_tfidf = tfidf.fit_transform(processed_texts)
                feature_names = tfidf.get_feature_names_out()
            except Exception as e:
                return {'error': f'TF-IDF processing failed: {str(e)}'}

            # Topic Modeling with LDA
            topics = []
            try:
                if X_tfidf.shape[0] >= 5:  # Need at least 5 documents for LDA
                    lda = LatentDirichletAllocation(n_components=min(5, X_tfidf.shape[0]//2), random_state=42, max_iter=10)
                    lda_topics = lda.fit_transform(X_tfidf)

                    for topic_idx, topic in enumerate(lda.components_):
                        top_words = [feature_names[i] for i in topic.argsort()[-10:][::-1]]
                        topics.append({
                            'topic_id': topic_idx + 1,
                            'keywords': top_words,
                            'weight': topic.sum(),
                            'explanation': self._explain_topic(top_words)
                        })
            except Exception as e:
                topics.append({'error': f'Topic modeling failed: {str(e)}'})

            # Enhanced clustering
            clusters = []
            try:
                if X_tfidf.shape[0] >= 3:
                    n_clusters = min(5, max(2, X_tfidf.shape[0] // 10))
                    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                    cluster_labels = kmeans.fit_predict(X_tfidf.toarray())
                    clusters = cluster_labels.tolist()
            except Exception as e:
                clusters = []

            # Key phrases extraction
            key_phrases = []
            try:
                count_vectorizer = CountVectorizer(ngram_range=(2, 3), max_features=20, stop_words='english', min_df=2)
                phrases = count_vectorizer.fit_transform(processed_texts)
                phrase_names = count_vectorizer.get_feature_names_out()
                phrase_freq = phrases.sum(axis=0).A1

                phrase_data = list(zip(phrase_names, phrase_freq))
                phrase_data.sort(key=lambda x: x[1], reverse=True)

                key_phrases = [{'phrase': phrase, 'frequency': int(freq), 'relevance': self._calculate_phrase_relevance(phrase, freq)} 
                              for phrase, freq in phrase_data[:10]]
            except Exception as e:
                key_phrases = []

            # Enhanced sentiment patterns
            sentiment_patterns = self._analyze_sentiment_patterns(df)

            return {
                'topics': topics,
                'clusters': clusters,
                'n_clusters': len(set(clusters)) if clusters else 0,
                'key_phrases': key_phrases,
                'sentiment_patterns': sentiment_patterns,
                'analysis_summary': self._generate_analysis_summary(df, topics, key_phrases),
                'recommendations': self._generate_recommendations(df, topics, key_phrases)
            }

        except Exception as e:
            return {'error': f'ML insights generation failed: {str(e)}'}

    def _explain_topic(self, keywords):
        """Provide explanation for discovered topics"""
        explanations = {
            ('performance', 'speed', 'fast', 'slow'): "Performance and Speed Issues",
            ('design', 'interface', 'ui', 'look'): "User Interface and Design",
            ('bug', 'crash', 'error', 'problem'): "Technical Issues and Bugs",
            ('feature', 'function', 'work'): "App Functionality",
            ('easy', 'difficult', 'simple'): "User Experience and Usability"
        }

        keywords_lower = [k.lower() for k in keywords]

        for key_terms, explanation in explanations.items():
            if any(term in keywords_lower for term in key_terms):
                return explanation

        return f"Topic focused on: {', '.join(keywords[:3])}"

    def _calculate_phrase_relevance(self, phrase, frequency):
        """Calculate relevance score for phrases"""
        if frequency > 10:
            return "High"
        elif frequency > 5:
            return "Medium"
        else:
            return "Low"

    def _analyze_sentiment_patterns(self, df):
        """Analyze sentiment patterns in the data"""
        patterns = {}

        if 'sentiment' in df.columns and 'score' in df.columns:
            # Sentiment by rating
            sentiment_by_rating = df.groupby('score')['sentiment'].value_counts().unstack(fill_value=0)
            patterns['sentiment_by_rating'] = sentiment_by_rating.to_dict()

            # Time-based patterns if date available
            if 'at' in df.columns:
                df['date'] = pd.to_datetime(df['at']).dt.date
                daily_sentiment = df.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
                patterns['daily_trends'] = daily_sentiment.to_dict()

        return patterns

    def _generate_analysis_summary(self, df, topics, phrases):
        """Generate comprehensive analysis summary"""
        total_reviews = len(df)

        if 'sentiment' in df.columns:
            positive_pct = (df['sentiment'] == 'Positive').sum() / total_reviews * 100
            negative_pct = (df['sentiment'] == 'Negative').sum() / total_reviews * 100
            neutral_pct = (df['sentiment'] == 'Neutral').sum() / total_reviews * 100
        else:
            positive_pct = negative_pct = neutral_pct = 0

        avg_rating = df['score'].mean() if 'score' in df.columns else 0

        summary = {
            'total_reviews': total_reviews,
            'sentiment_distribution': {
                'positive': round(positive_pct, 1),
                'negative': round(negative_pct, 1),
                'neutral': round(neutral_pct, 1)
            },
            'average_rating': round(avg_rating, 2),
            'main_topics_count': len(topics),
            'key_phrases_found': len(phrases),
            'overall_health': self._calculate_app_health(positive_pct, negative_pct, avg_rating)
        }

        return summary

    def _calculate_app_health(self, positive_pct, negative_pct, avg_rating):
        """Calculate overall app health score"""
        if avg_rating >= 4.0 and positive_pct >= 70:
            return "Excellent"
        elif avg_rating >= 3.5 and positive_pct >= 60:
            return "Good"
        elif avg_rating >= 3.0 and positive_pct >= 50:
            return "Average"
        elif avg_rating >= 2.5 and negative_pct < 60:
            return "Below Average"
        else:
            return "Poor"

    def _generate_recommendations(self, df, topics, phrases):
        """Generate actionable recommendations"""
        recommendations = []

        if 'sentiment' in df.columns:
            negative_pct = (df['sentiment'] == 'Negative').sum() / len(df) * 100

            if negative_pct > 40:
                recommendations.append({
                    'type': 'critical',
                    'title': 'High Negative Sentiment Alert',
                    'description': f'{negative_pct:.1f}% of reviews are negative. Immediate action required to address user concerns.',
                    'priority': 'High'
                })

        # Analyze topics for recommendations
        for topic in topics:
            if isinstance(topic, dict) and 'keywords' in topic:
                keywords = topic['keywords']
                if any(word in ['crash', 'bug', 'error', 'problem'] for word in keywords):
                    recommendations.append({
                        'type': 'technical',
                        'title': 'Technical Issues Detected',
                        'description': 'Multiple reviews mention technical problems. Consider prioritizing bug fixes and stability improvements.',
                        'priority': 'High'
                    })
                elif any(word in ['slow', 'lag', 'speed'] for word in keywords):
                    recommendations.append({
                        'type': 'performance',
                        'title': 'Performance Optimization Needed',
                        'description': 'Users are experiencing performance issues. Focus on optimization and speed improvements.',
                        'priority': 'Medium'
                    })

        if not recommendations:
            recommendations.append({
                'type': 'positive',
                'title': 'App Performance is Stable',
                'description': 'No critical issues detected. Continue monitoring user feedback for improvement opportunities.',
                'priority': 'Low'
            })

        return recommendations

# Initialize enhanced analyzer
analyzer = EnhancedReviewAnalyzer()


# Part 2: Enhanced UI components and page functions  


def create_enhanced_header():
    """Create stunning animated header with developer credit"""
    st.markdown("""
    <div class="enhanced-header">
        <h1 class="header-title">ReviewForge Analytics Pro</h1>
        <p class="header-subtitle">Advanced AI-Powered Review Analysis Platform with Machine Learning Intelligence</p>
        <div class="developer-badge">
            Developed by Ayush Pandey - Advanced Analytics & AI Specialist
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_enhanced_navigation():
    """Create advanced navigation system with current page indicator"""
    st.sidebar.markdown('<div class="sidebar-section"><h3 style="color: white; text-align: center; margin-bottom: 1rem;">🚀 Navigation Hub</h3></div>', unsafe_allow_html=True)

    pages = {
        'dashboard': {'name': '📊 Analytics Dashboard', 'desc': 'Main analysis interface'},
        'deep_analysis': {'name': '🔬 Deep Analysis Engine', 'desc': 'Advanced ML insights'},
        'competitor': {'name': '🏆 Competitive Intelligence', 'desc': 'Multi-app comparison'},
        'ml_insights': {'name': '🧠 ML Insights Laboratory', 'desc': 'Machine learning models'},
        'reviews_explorer': {'name': '📝 Reviews Explorer', 'desc': 'Detailed review analysis'},
        'export_reports': {'name': '📋 Export & Reporting', 'desc': 'Professional reports'},
        'settings': {'name': '⚙️ Advanced Settings', 'desc': 'Customization options'}
    }

    for page_key, page_info in pages.items():
        button_class = "enhanced-button" if st.session_state.current_page != page_key else "current-page-indicator"

        if st.sidebar.button(f"{page_info['name']}", key=f"nav_{page_key}", use_container_width=True):
            st.session_state.current_page = page_key
            st.rerun()

    # Enhanced current page indicator
    current_page_info = pages[st.session_state.current_page]
    st.sidebar.markdown(f"""
    <div class="current-page-indicator">
        <h4>Current Page</h4>
        <p>{current_page_info['name']}</p>
        <small>{current_page_info['desc']}</small>
    </div>
    """, unsafe_allow_html=True)

def create_enhanced_metrics_dashboard(df):
    """Create comprehensive metrics dashboard with animations"""
    if df.empty:
        return

    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    st.subheader("📈 Key Performance Indicators")

    cols = st.columns(5)

    with cols[0]:
        avg_rating = df['score'].mean() if 'score' in df.columns else 0
        rating_color = "🟢" if avg_rating >= 4 else "🟡" if avg_rating >= 3 else "🔴"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_rating:.1f} {rating_color}</div>
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
            positive_rate = (df['sentiment'] == 'Positive').sum() / len(df) * 100
            sentiment_emoji = "😊" if positive_rate >= 70 else "😐" if positive_rate >= 50 else "😞"
        else:
            positive_rate = 0
            sentiment_emoji = "❓"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{positive_rate:.1f}% {sentiment_emoji}</div>
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
            <div class="metric-value">{avg_confidence:.0f}%</div>
            <div class="metric-label">Analysis Confidence</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[4]:
        if 'sentiment' in df.columns:
            negative_rate = (df['sentiment'] == 'Negative').sum() / len(df) * 100
            risk_level = "🔴" if negative_rate >= 30 else "🟡" if negative_rate >= 15 else "🟢"
        else:
            negative_rate = 0
            risk_level = "❓"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{negative_rate:.1f}% {risk_level}</div>
            <div class="metric-label">Risk Level</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def create_enhanced_visualizations(df):
    """Create stunning interactive visualizations with enhanced frames"""
    if df.empty:
        return

    # Modern color palette
    colors = {
        'positive': '#00d4aa',
        'negative': '#ff6b6b',
        'neutral': '#4ecdc4',
        'primary': '#667eea',
        'secondary': '#764ba2'
    }

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">Sentiment Distribution Analysis</h3>', unsafe_allow_html=True)

        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts()

            fig_donut = go.Figure(data=[go.Pie(
                labels=sentiment_counts.index,
                values=sentiment_counts.values,
                hole=0.6,
                marker=dict(
                    colors=[colors['positive'] if s == 'Positive' else 
                           colors['negative'] if s == 'Negative' else colors['neutral'] 
                           for s in sentiment_counts.index],
                    line=dict(color='white', width=3)
                ),
                textinfo='label+percent+value',
                textfont=dict(size=14, color='white', family='Inter'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])

            fig_donut.update_layout(
                title=None,
                annotations=[dict(
                    text=f'<b>{sentiment_counts.sum()}</b><br>Total Reviews',
                    x=0.5, y=0.5,
                    font_size=18,
                    showarrow=False,
                    font_color='#667eea'
                )],
                showlegend=True,
                height=400,
                font=dict(family='Inter'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(fig_donut, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">Rating Distribution Overview</h3>', unsafe_allow_html=True)

        if 'score' in df.columns:
            rating_dist = df['score'].value_counts().sort_index()

            fig_rating = go.Figure()
            fig_rating.add_trace(go.Bar(
                x=[f'{i} ★' for i in rating_dist.index],
                y=rating_dist.values,
                marker=dict(
                    color=[colors['negative'] if i <= 2 else 
                          colors['neutral'] if i == 3 else colors['positive'] 
                          for i in rating_dist.index],
                    opacity=0.8,
                    line=dict(color='white', width=2)
                ),
                text=rating_dist.values,
                textposition='outside',
                textfont=dict(color='white', size=14, family='Inter'),
                hovertemplate='<b>%{x}</b><br>Count: %{y}<br><extra></extra>'
            ))

            fig_rating.update_layout(
                title=None,
                xaxis_title='Rating',
                yaxis_title='Number of Reviews',
                showlegend=False,
                height=400,
                font=dict(family='Inter', color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(color='white'),
                yaxis=dict(color='white')
            )

            st.plotly_chart(fig_rating, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced Aspect Analysis
    aspect_cols = [col for col in df.columns if col.startswith('aspect_')]
    if aspect_cols:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">Aspect Analysis Deep Dive</h3>', unsafe_allow_html=True)

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
            line=dict(color=colors['primary'], width=3),
            fillcolor='rgba(102, 126, 234, 0.3)',
            hovertemplate='<b>%{theta}</b><br>Coverage: %{r:.1f}%<extra></extra>'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(aspect_data.values()) * 1.2],
                    color='white'
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            title=None,
            height=500,
            font=dict(family='Inter', color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def create_enhanced_reviews_explorer(df, title="Recent Reviews Explorer"):
    """Create comprehensive reviews explorer with filters"""
    if df.empty:
        st.warning("No reviews data available to explore")
        return

    st.markdown(f'<div class="glass-card fade-in-up">', unsafe_allow_html=True)
    st.subheader(f"📝 {title}")

    # Enhanced Filters Section
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown("**🔍 Advanced Filters**")

    filter_cols = st.columns(4)

    with filter_cols[0]:
        # Rating filter
        rating_options = ['All Ratings'] + [f'{i} Star{"s" if i != 1 else ""}' for i in range(1, 6)]
        selected_rating = st.selectbox("Rating Filter", options=rating_options, key="rating_filter")

    with filter_cols[1]:
        # Sentiment filter
        sentiment_options = ['All Sentiments', 'Positive', 'Negative', 'Neutral']
        selected_sentiment = st.selectbox("Sentiment Filter", options=sentiment_options, key="sentiment_filter")

    with filter_cols[2]:
        # Date range filter
        if 'at' in df.columns:
            df['date'] = pd.to_datetime(df['at'])
            date_range = st.date_input(
                "Date Range",
                value=(df['date'].min().date(), df['date'].max().date()),
                min_value=df['date'].min().date(),
                max_value=df['date'].max().date(),
                key="date_range"
            )
        else:
            st.info("Date filtering not available")

    with filter_cols[3]:
        # Content length filter
        content_lengths = df['content'].str.len() if 'content' in df.columns else pd.Series([0])
        min_length = st.slider("Minimum Review Length", 0, int(content_lengths.max()), 0, key="length_filter")

    st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    filtered_df = df.copy()

    # Rating filter
    if selected_rating != 'All Ratings' and 'score' in df.columns:
        rating_value = int(selected_rating.split()[0])
        filtered_df = filtered_df[filtered_df['score'] == rating_value]

    # Sentiment filter
    if selected_sentiment != 'All Sentiments' and 'sentiment' in df.columns:
        filtered_df = filtered_df[filtered_df['sentiment'] == selected_sentiment]

    # Date filter
    if 'at' in df.columns and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['date'].dt.date >= start_date) & 
            (filtered_df['date'].dt.date <= end_date)
        ]

    # Length filter
    if 'content' in df.columns:
        filtered_df = filtered_df[filtered_df['content'].str.len() >= min_length]

    # Display filter results
    st.markdown(f"**📊 Showing {len(filtered_df)} of {len(df)} reviews**")

    # Rating breakdown for filtered data
    if 'score' in filtered_df.columns:
        rating_breakdown = filtered_df['score'].value_counts().sort_index()
        st.markdown("**⭐ Rating Breakdown:**")

        breakdown_cols = st.columns(5)
        for i, (rating, count) in enumerate(rating_breakdown.items()):
            with breakdown_cols[i % 5]:
                percentage = (count / len(filtered_df)) * 100
                st.metric(f"{rating}⭐", f"{count}", f"{percentage:.1f}%")

    # Scrollable reviews container
    st.markdown('<div class="reviews-container">', unsafe_allow_html=True)

    display_columns = ['at', 'userName', 'score', 'sentiment', 'content']
    available_columns = [col for col in display_columns if col in filtered_df.columns]

    if available_columns and not filtered_df.empty:
        for idx, review in filtered_df.head(20).iterrows():
            # Format date
            review_date = ""
            if 'at' in review:
                try:
                    review_date = pd.to_datetime(review['at']).strftime('%Y-%m-%d')
                except:
                    review_date = str(review['at'])[:10]

            # Get sentiment class
            sentiment = review.get('sentiment', 'Neutral')
            sentiment_class = f"sentiment-{sentiment.lower()}"

            # Truncate content for display
            content = str(review.get('content', ''))
            display_content = content[:300] + "..." if len(content) > 300 else content

            st.markdown(f"""
            <div class="review-item">
                <div class="review-header">
                    <div>
                        <strong>{review.get('userName', 'Anonymous User')}</strong>
                        <small style="color: #666; margin-left: 1rem;">{review_date}</small>
                    </div>
                    <div class="review-rating">{review.get('score', 'N/A')} ⭐</div>
                </div>
                <div class="review-content">{display_content}</div>
                <div class="review-footer">
                    <span class="review-sentiment {sentiment_class}">{sentiment}</span>
                    <small style="color: #888; margin-left: 1rem;">
                        Confidence: {review.get('confidence', 0)*100:.0f}%
                    </small>
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("No reviews match the selected filters")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def dashboard_page():
    """Enhanced main dashboard page"""
    create_enhanced_header()

    # Input section with enhanced styling
    st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
    st.subheader("🔧 Application Analysis Configuration")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        url_input = st.text_input(
            "📱 Google Play Store URL or Package Name",
            placeholder="https://play.google.com/store/apps/details?id=com.example.app",
            help="Enter the full Google Play Store URL or just the package name (e.g., com.whatsapp)",
            key="url_input"
        )

    with col2:
        # Custom review count input
        review_count = st.number_input(
            "🔢 Reviews to Analyze",
            min_value=50,
            max_value=2000,
            value=500,
            step=50,
            help="Choose how many reviews to analyze (more reviews = better insights but slower processing)"
        )

    with col3:
        sort_option = st.selectbox(
            "📊 Sort Reviews By",
            options=["Newest", "Rating", "Helpfulness"],
            help="Choose how to sort the reviews for analysis"
        )

    # Convert sort option
    sort_mapping = {
        "Newest": Sort.NEWEST,
        "Rating": Sort.RATING,
        "Helpfulness": Sort.MOST_RELEVANT
    }

    # Enhanced analyze button
    analyze_button = st.button(
        f"🚀 Analyze Application ({review_count} reviews)", 
        type="primary", 
        use_container_width=True,
        key="analyze_btn"
    )

    if analyze_button:
        if url_input:
            package_name = analyzer.extract_package_name(url_input)

            if package_name:
                with st.spinner("🔮 Performing advanced AI analysis..."):
                    df = analyzer.scrape_reviews(
                        package_name, 
                        count=review_count, 
                        sort_by=sort_mapping[sort_option]
                    )

                    if not df.empty:
                        st.session_state.analyzed_data = df
                        st.session_state.current_app_name = analyzer.get_app_name(package_name)
                        st.success(f"🎉 Successfully analyzed {len(df)} reviews for {st.session_state.current_app_name}!")
                        st.balloons()
                    else:
                        st.error("❌ No reviews found or failed to extract reviews")
            else:
                st.error("❌ Invalid URL or package name format")
        else:
            st.warning("⚠️ Please enter a valid Google Play Store URL or package name")

    st.markdown('</div>', unsafe_allow_html=True)

    # Display results with enhanced styling
    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data

        st.markdown("---")
        st.markdown(f'<div class="fade-in-up">', unsafe_allow_html=True)
        st.title(f"📊 Analysis Results: {st.session_state.get('current_app_name', 'Unknown App')}")

        # Enhanced metrics dashboard
        create_enhanced_metrics_dashboard(df)

        # Enhanced visualizations
        create_enhanced_visualizations(df)

        # Enhanced reviews explorer
        create_enhanced_reviews_explorer(df, "Recent Reviews Analysis")

        st.markdown('</div>', unsafe_allow_html=True)

def deep_analysis_page():
    """Enhanced deep analysis page with detailed explanations"""
    st.title("🔬 Deep Analysis Engine")
    st.markdown("""
    <div class="glass-card">
    <h3>🧠 What is Deep Analysis?</h3>
    <p><strong>Deep Analysis Engine</strong> uses advanced machine learning algorithms to discover hidden patterns in user reviews. Here's what it does:</p>
    <ul>
    <li><strong>Topic Modeling:</strong> Automatically discovers what users are talking about</li>
    <li><strong>Sentiment Patterns:</strong> Analyzes how sentiment changes over time and ratings</li>
    <li><strong>Key Phrase Extraction:</strong> Finds the most important phrases users mention</li>
    <li><strong>Clustering Analysis:</strong> Groups similar reviews together</li>
    <li><strong>Aspect Detection:</strong> Identifies specific features users discuss</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data

        # Generate ML insights if not already done
        if 'ml_insights' not in st.session_state or not st.session_state.ml_insights:
            with st.spinner("🤖 Generating advanced machine learning insights..."):
                ml_insights = analyzer.generate_enhanced_ml_insights(df)
                st.session_state.ml_insights = ml_insights

        ml_insights = st.session_state.ml_insights

        if 'error' in ml_insights:
            st.error(f"❌ Analysis Error: {ml_insights['error']}")
            st.info("💡 Try analyzing more reviews or check if the app has sufficient review data.")
            return

        # Analysis Summary
        if 'analysis_summary' in ml_insights:
            summary = ml_insights['analysis_summary']

            st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
            st.subheader("📋 Analysis Summary")

            summary_cols = st.columns(4)
            with summary_cols[0]:
                st.metric("App Health", summary['overall_health'])
            with summary_cols[1]:
                st.metric("Topics Found", summary['main_topics_count'])
            with summary_cols[2]:
                st.metric("Key Phrases", summary['key_phrases_found'])
            with summary_cols[3]:
                avg_rating = summary.get('average_rating', 0)
                st.metric("Overall Rating", f"{avg_rating}/5.0")

            st.markdown('</div>', unsafe_allow_html=True)

        # Topic Analysis with detailed explanations
        if 'topics' in ml_insights and ml_insights['topics']:
            st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
            st.subheader("🎯 Topic Modeling Results")
            st.markdown("""
            **What are Topics?** Our AI automatically discovered these main themes from user reviews:
            """)

            for topic in ml_insights['topics']:
                if isinstance(topic, dict) and 'keywords' in topic:
                    with st.expander(f"📌 Topic {topic['topic_id']}: {topic.get('explanation', 'Unknown Topic')}"):
                        st.markdown(f"**Main Keywords:** {', '.join(topic['keywords'][:8])}")
                        st.markdown(f"**Relevance Score:** {topic['weight']:.3f}")
                        st.markdown(f"**What this means:** {topic.get('explanation', 'This topic represents user discussions around these keywords.')}")

            st.markdown('</div>', unsafe_allow_html=True)

        # Key Phrases Analysis
        if 'key_phrases' in ml_insights and ml_insights['key_phrases']:
            st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
            st.subheader("🔑 Key Phrases Discovery")
            st.markdown("**Most frequently mentioned phrases by users:**")

            phrases_data = []
            for phrase_data in ml_insights['key_phrases'][:10]:
                phrases_data.append({
                    'Phrase': phrase_data['phrase'],
                    'Frequency': phrase_data['frequency'],
                    'Relevance': phrase_data['relevance'],
                    'Impact': '🔴 High' if phrase_data['frequency'] > 10 else '🟡 Medium' if phrase_data['frequency'] > 5 else '🟢 Low'
                })

            phrases_df = pd.DataFrame(phrases_data)
            st.dataframe(phrases_df, use_container_width=True, hide_index=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # Recommendations
        if 'recommendations' in ml_insights and ml_insights['recommendations']:
            st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
            st.subheader("💡 AI-Generated Recommendations")

            for rec in ml_insights['recommendations']:
                if rec['priority'] == 'High':
                    st.error(f"🚨 **{rec['title']}** - {rec['description']}")
                elif rec['priority'] == 'Medium':
                    st.warning(f"⚠️ **{rec['title']}** - {rec['description']}")
                else:
                    st.success(f"✅ **{rec['title']}** - {rec['description']}")

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="glass-card">
        <h3>🎯 Get Started</h3>
        <p>Please analyze an application first from the <strong>Analytics Dashboard</strong> to access deep analysis features.</p>
        <p>Once you have data, this page will show:</p>
        <ul>
        <li>📊 Advanced statistical analysis</li>
        <li>🎯 Topic modeling results</li>
        <li>🔍 Pattern recognition insights</li>
        <li>💡 AI-powered recommendations</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

def reviews_explorer_page():
    """Dedicated reviews explorer page"""
    st.title("📝 Reviews Explorer")

    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data
        app_name = st.session_state.get('current_app_name', 'Unknown App')

        st.markdown(f"""
        <div class="glass-card">
        <h3>📱 Exploring Reviews for {app_name}</h3>
        <p>Deep dive into individual user reviews with advanced filtering and analysis capabilities.</p>
        </div>
        """, unsafe_allow_html=True)

        create_enhanced_reviews_explorer(df, f"Complete Reviews Analysis for {app_name}")

    else:
        st.markdown("""
        <div class="glass-card">
        <h3>🎯 No Data Available</h3>
        <p>Please analyze an application first from the <strong>Analytics Dashboard</strong> to explore reviews.</p>
        </div>
        """, unsafe_allow_html=True)

def settings_page():
    """Enhanced advanced settings page with detailed explanations"""
    st.title("⚙️ Advanced Settings & Configuration")

    st.markdown("""
    <div class="glass-card">
    <h3>🎛️ Customize Your Analysis Experience</h3>
    <p>These settings control how the AI analyzes your app reviews and generates insights.</p>
    </div>
    """, unsafe_allow_html=True)

    # Analysis Configuration
    st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
    st.subheader("🤖 AI Analysis Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Sentiment Analysis Settings")

        sentiment_model = st.selectbox(
            "Sentiment Model",
            options=["Enhanced TextBlob", "Basic TextBlob", "Pattern-Based"],
            index=0,
            help="Enhanced TextBlob provides better accuracy with emotion detection"
        )

        confidence_threshold = st.slider(
            "Confidence Threshold",
            0.0, 1.0, 0.6, 0.1,
            help="Higher values = more conservative predictions, Lower values = more predictions"
        )

        st.markdown("**What this affects:**")
        st.markdown("- How accurately we detect sentiment")
        st.markdown("- Confidence scores for predictions")
        st.markdown("- Overall analysis reliability")

    with col2:
        st.markdown("#### Machine Learning Settings")

        topic_count = st.slider(
            "Number of Topics to Discover",
            3, 10, 5,
            help="How many main themes to find in reviews"
        )

        enable_clustering = st.checkbox(
            "Enable Review Clustering",
            value=True,
            help="Groups similar reviews together for pattern analysis"
        )

        enable_aspect_analysis = st.checkbox(
            "Enable Aspect-Based Analysis",
            value=True,
            help="Analyzes specific features like UI, performance, etc."
        )

        st.markdown("**What this affects:**")
        st.markdown("- Depth of topic analysis")
        st.markdown("- Pattern recognition accuracy")
        st.markdown("- Feature-specific insights")

    st.markdown('</div>', unsafe_allow_html=True)

    # Visualization Settings
    st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
    st.subheader("📊 Visualization Preferences")

    viz_col1, viz_col2 = st.columns(2)

    with viz_col1:
        chart_theme = st.selectbox(
            "Chart Theme",
            options=["Modern Dark", "Professional Light", "Colorful"],
            index=0
        )

        animation_speed = st.selectbox(
            "Animation Speed",
            options=["Fast", "Normal", "Slow", "None"],
            index=1
        )

    with viz_col2:
        show_confidence = st.checkbox("Show Confidence Scores", value=True)
        show_percentages = st.checkbox("Show Percentages in Charts", value=True)

    st.markdown("**Impact on Experience:**")
    st.markdown("- Changes appearance of all charts and graphs")
    st.markdown("- Affects loading speed and responsiveness")
    st.markdown("- Customizes information display density")

    st.markdown('</div>', unsafe_allow_html=True)

    # Export Settings
    st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
    st.subheader("📋 Export & Reporting Configuration")

    export_col1, export_col2 = st.columns(2)

    with export_col1:
        default_format = st.selectbox(
            "Default Export Format",
            options=["Excel", "CSV", "JSON", "PDF"],
            index=0
        )

        include_charts = st.checkbox("Include Charts in Exports", value=True)

    with export_col2:
        include_raw_data = st.checkbox("Include Raw Review Data", value=True)
        include_ml_insights = st.checkbox("Include ML Analysis", value=True)

    st.markdown("**Export Options Explained:**")
    st.markdown("- **Excel**: Best for detailed analysis and sharing")
    st.markdown("- **CSV**: Simple format for data processing")
    st.markdown("- **JSON**: For developers and API integration")
    st.markdown("- **PDF**: Professional reports for presentations")

    st.markdown('</div>', unsafe_allow_html=True)

    # Save Settings
    if st.button("💾 Save All Settings", type="primary", use_container_width=True):
        # Update session state with new settings
        st.session_state.user_preferences.update({
            'sentiment_model': sentiment_model,
            'confidence_threshold': confidence_threshold,
            'topic_count': topic_count,
            'enable_clustering': enable_clustering,
            'enable_aspect_analysis': enable_aspect_analysis,
            'chart_theme': chart_theme,
            'animation_speed': animation_speed,
            'show_confidence': show_confidence,
            'show_percentages': show_percentages,
            'default_format': default_format,
            'include_charts': include_charts,
            'include_raw_data': include_raw_data,
            'include_ml_insights': include_ml_insights
        })

        st.success("✅ Settings saved successfully! Changes will be applied to new analyses.")
        st.balloons()

    # Current Settings Summary
    st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
    st.subheader("📋 Current Configuration Summary")

    current_settings = st.session_state.user_preferences
    settings_summary = f"""
    **AI Model:** {current_settings.get('sentiment_model', 'Enhanced TextBlob')}
    **Analysis Depth:** {'Comprehensive' if current_settings.get('enable_aspect_analysis', True) else 'Basic'}
    **Visualization Theme:** {current_settings.get('chart_theme', 'Modern Dark')}
    **Export Format:** {current_settings.get('default_format', 'Excel')}
    **Confidence Threshold:** {current_settings.get('confidence_threshold', 0.6)}
    """

    st.markdown(settings_summary)
    st.markdown('</div>', unsafe_allow_html=True)

# Continue with more functions...


# Part 3: Final application logic and routing


def competitor_analysis_page():
    """Enhanced competitive intelligence page"""
    st.title("🏆 Competitive Intelligence")
    st.markdown("""
    <div class="glass-card">
    <h3>🎯 Advanced Competitive Analysis</h3>
    <p>Compare your app against competitors with professional benchmarking and strategic insights.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
        st.subheader("📱 Primary App Analysis")
        if st.session_state.analyzed_data is not None:
            df_primary = st.session_state.analyzed_data
            app_name = st.session_state.get('current_app_name', 'Your App')

            st.success(f"✅ {app_name} analyzed successfully")

            # Primary app metrics
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                if 'score' in df_primary.columns:
                    avg_rating = df_primary['score'].mean()
                    st.metric("Average Rating", f"{avg_rating:.1f}/5.0")

                if 'sentiment' in df_primary.columns:
                    positive_rate = (df_primary['sentiment'] == 'Positive').sum() / len(df_primary) * 100
                    st.metric("Positive Sentiment", f"{positive_rate:.1f}%")

            with metrics_col2:
                st.metric("Total Reviews", f"{len(df_primary):,}")

                if 'confidence' in df_primary.columns:
                    avg_confidence = df_primary['confidence'].mean() * 100
                    st.metric("Analysis Confidence", f"{avg_confidence:.0f}%")
        else:
            st.info("📌 Analyze your primary app first from the Dashboard")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
        st.subheader("🔍 Competitor App Analysis")

        competitor_url = st.text_input(
            "Competitor App URL or Package Name",
            placeholder="Enter competitor's Google Play URL or package name",
            help="Analyze a competitor app for comparison"
        )

        competitor_reviews = st.number_input(
            "Reviews to Analyze",
            min_value=50,
            max_value=1000,
            value=300,
            help="Number of competitor reviews to analyze"
        )

        if st.button("🔍 Analyze Competitor", use_container_width=True):
            if competitor_url:
                package_name = analyzer.extract_package_name(competitor_url)

                if package_name:
                    with st.spinner("🤖 Analyzing competitor application..."):
                        competitor_df = analyzer.scrape_reviews(package_name, count=competitor_reviews)

                        if not competitor_df.empty:
                            st.session_state.competitor_data = competitor_df
                            st.session_state.competitor_app_name = analyzer.get_app_name(package_name)
                            st.success(f"🎉 Competitor {st.session_state.competitor_app_name} analyzed!")
                        else:
                            st.error("❌ Failed to analyze competitor")
                else:
                    st.error("❌ Invalid competitor URL or package name")
            else:
                st.warning("⚠️ Please enter competitor URL or package name")

        # Show competitor status
        if st.session_state.competitor_data is not None:
            competitor_name = st.session_state.get('competitor_app_name', 'Competitor')
            st.success(f"✅ {competitor_name} ready for comparison")

        st.markdown('</div>', unsafe_allow_html=True)

    # Comparative Analysis Dashboard
    if (st.session_state.analyzed_data is not None and 
        st.session_state.competitor_data is not None):

        st.markdown("---")
        st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
        st.subheader("📊 Head-to-Head Competitive Analysis")

        df_primary = st.session_state.analyzed_data
        df_competitor = st.session_state.competitor_data
        primary_name = st.session_state.get('current_app_name', 'Your App')
        competitor_name = st.session_state.get('competitor_app_name', 'Competitor')

        # Enhanced comparison metrics
        comparison_cols = st.columns(4)

        with comparison_cols[0]:
            primary_rating = df_primary['score'].mean() if 'score' in df_primary.columns else 0
            competitor_rating = df_competitor['score'].mean() if 'score' in df_competitor.columns else 0

            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("**⭐ Average Rating**")
            st.markdown(f"**{primary_name}:** {primary_rating:.2f}")
            st.markdown(f"**{competitor_name}:** {competitor_rating:.2f}")

            if primary_rating > competitor_rating:
                st.markdown("🏆 **You're winning!**")
            elif competitor_rating > primary_rating:
                st.markdown("📈 **Room for improvement**")
            else:
                st.markdown("🤝 **It's a tie!**")
            st.markdown('</div>', unsafe_allow_html=True)

        with comparison_cols[1]:
            if all('sentiment' in df.columns for df in [df_primary, df_competitor]):
                primary_positive = (df_primary['sentiment'] == 'Positive').sum() / len(df_primary) * 100
                competitor_positive = (df_competitor['sentiment'] == 'Positive').sum() / len(df_competitor) * 100

                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown("**😊 Positive Sentiment**")
                st.markdown(f"**{primary_name}:** {primary_positive:.1f}%")
                st.markdown(f"**{competitor_name}:** {competitor_positive:.1f}%")

                if primary_positive > competitor_positive:
                    st.markdown("🎉 **Users love you more!**")
                else:
                    st.markdown("💪 **Time to step up!**")
                st.markdown('</div>', unsafe_allow_html=True)

        with comparison_cols[2]:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("**📊 Review Volume**")
            st.markdown(f"**{primary_name}:** {len(df_primary):,}")
            st.markdown(f"**{competitor_name}:** {len(df_competitor):,}")

            if len(df_primary) > len(df_competitor):
                st.markdown("📈 **Higher engagement!**")
            else:
                st.markdown("🎯 **Growing potential!**")
            st.markdown('</div>', unsafe_allow_html=True)

        with comparison_cols[3]:
            if all('confidence' in df.columns for df in [df_primary, df_competitor]):
                primary_conf = df_primary['confidence'].mean() * 100
                competitor_conf = df_competitor['confidence'].mean() * 100

                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown("**🎯 Analysis Quality**")
                st.markdown(f"**{primary_name}:** {primary_conf:.0f}%")
                st.markdown(f"**{competitor_name}:** {competitor_conf:.0f}%")
                st.markdown("📊 **Data reliability**")
                st.markdown('</div>', unsafe_allow_html=True)

        # Enhanced Visual Comparisons
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">📊 Competitive Sentiment Analysis</h3>', unsafe_allow_html=True)

        if all('sentiment' in df.columns for df in [df_primary, df_competitor]):
            # Create comparison chart
            primary_sentiment = df_primary['sentiment'].value_counts()
            competitor_sentiment = df_competitor['sentiment'].value_counts()

            sentiments = ['Positive', 'Neutral', 'Negative']

            fig_comparison = go.Figure()

            fig_comparison.add_trace(go.Bar(
                name=primary_name,
                x=sentiments,
                y=[primary_sentiment.get(s, 0) for s in sentiments],
                marker_color='#00d4aa',
                text=[f"{primary_sentiment.get(s, 0)}" for s in sentiments],
                textposition='outside'
            ))

            fig_comparison.add_trace(go.Bar(
                name=competitor_name,
                x=sentiments,
                y=[competitor_sentiment.get(s, 0) for s in sentiments],
                marker_color='#ff6b6b',
                text=[f"{competitor_sentiment.get(s, 0)}" for s in sentiments],
                textposition='outside'
            ))

            fig_comparison.update_layout(
                title=None,
                xaxis_title='Sentiment Categories',
                yaxis_title='Number of Reviews',
                barmode='group',
                height=400,
                font=dict(family='Inter', color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(color='white'),
                yaxis=dict(color='white'),
                legend=dict(font_color='white')
            )

            st.plotly_chart(fig_comparison, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Strategic Recommendations
        st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
        st.subheader("🎯 Strategic Competitive Insights")

        # Generate competitive insights
        insights = []

        if 'score' in df_primary.columns and 'score' in df_competitor.columns:
            rating_diff = df_primary['score'].mean() - df_competitor['score'].mean()
            if rating_diff > 0.2:
                insights.append("🏆 **Rating Advantage**: You have a significant rating advantage. Maintain quality!")
            elif rating_diff < -0.2:
                insights.append("📈 **Rating Gap**: Competitor has higher ratings. Focus on user satisfaction improvements.")
            else:
                insights.append("🤝 **Rating Parity**: Similar ratings. Differentiate through unique features.")

        if all('sentiment' in df.columns for df in [df_primary, df_competitor]):
            primary_pos = (df_primary['sentiment'] == 'Positive').sum() / len(df_primary) * 100
            competitor_pos = (df_competitor['sentiment'] == 'Positive').sum() / len(df_competitor) * 100

            if primary_pos > competitor_pos + 10:
                insights.append("😊 **Sentiment Leadership**: Users are significantly happier with your app!")
            elif competitor_pos > primary_pos + 10:
                insights.append("💪 **Sentiment Challenge**: Competitor has better user sentiment. Address pain points.")

        if len(df_primary) > len(df_competitor) * 1.5:
            insights.append("📊 **Volume Advantage**: You have much higher user engagement!")
        elif len(df_competitor) > len(df_primary) * 1.5:
            insights.append("🎯 **Growth Opportunity**: Competitor has higher engagement. Expand your reach!")

        for insight in insights:
            st.markdown(insight)

        if not insights:
            st.info("📊 Analysis shows balanced competition. Focus on unique value propositions!")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def export_reports_page():
    """Enhanced export and reporting functionality"""
    st.title("📋 Export & Professional Reporting")
    st.markdown("""
    <div class="glass-card">
    <h3>📊 Generate Comprehensive Analysis Reports</h3>
    <p>Export your analysis in multiple professional formats for presentations, stakeholders, and further analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data
        app_name = st.session_state.get('current_app_name', 'Unknown App')

        st.markdown(f'<div class="glass-card fade-in-up">', unsafe_allow_html=True)
        st.subheader(f"📱 Export Options for {app_name}")

        # Export format selection with explanations
        format_cols = st.columns(4)

        with format_cols[0]:
            if st.button("📊 Export as Excel", use_container_width=True):
                try:
                    excel_buffer = BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        # Main analysis sheet
                        df.to_excel(writer, sheet_name='Review Analysis', index=False)

                        # Summary sheet
                        if 'sentiment' in df.columns:
                            summary_data = {
                                'Metric': ['Total Reviews', 'Average Rating', 'Positive %', 'Negative %', 'Neutral %'],
                                'Value': [
                                    len(df),
                                    f"{df['score'].mean():.2f}" if 'score' in df.columns else 'N/A',
                                    f"{(df['sentiment'] == 'Positive').sum() / len(df) * 100:.1f}%",
                                    f"{(df['sentiment'] == 'Negative').sum() / len(df) * 100:.1f}%",
                                    f"{(df['sentiment'] == 'Neutral').sum() / len(df) * 100:.1f}%"
                                ]
                            }
                            summary_df = pd.DataFrame(summary_data)
                            summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)

                    excel_data = excel_buffer.getvalue()
                    st.download_button(
                        label="⬇️ Download Excel Report",
                        data=excel_data,
                        file_name=f"{app_name}_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success("✅ Excel report generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error creating Excel file: {str(e)}")

        with format_cols[1]:
            if st.button("📄 Export as CSV", use_container_width=True):
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV Data",
                    data=csv_data,
                    file_name=f"{app_name}_reviews_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
                st.success("✅ CSV export ready!")

        with format_cols[2]:
            if st.button("🔧 Export as JSON", use_container_width=True):
                json_data = df.to_json(orient='records', date_format='iso')
                st.download_button(
                    label="⬇️ Download JSON Data",
                    data=json_data,
                    file_name=f"{app_name}_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
                st.success("✅ JSON export ready!")

        with format_cols[3]:
            if st.button("📋 Generate Report", use_container_width=True):
                # Generate comprehensive markdown report
                report_content = self._generate_comprehensive_report(df, app_name)
                st.download_button(
                    label="⬇️ Download Full Report",
                    data=report_content,
                    file_name=f"{app_name}_comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown"
                )
                st.success("✅ Comprehensive report generated!")

        st.markdown('</div>', unsafe_allow_html=True)

        # Export Preview
        st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
        st.subheader("👁️ Export Data Preview")

        preview_cols = st.multiselect(
            "Select columns for export preview",
            options=df.columns.tolist(),
            default=[col for col in ['at', 'userName', 'score', 'sentiment', 'confidence', 'content'] 
                    if col in df.columns][:6]
        )

        if preview_cols:
            preview_df = df[preview_cols].head(10)
            st.dataframe(preview_df, use_container_width=True, hide_index=True)
            st.info(f"📊 Preview showing first 10 rows. Full export contains {len(df):,} rows.")

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="glass-card">
        <h3>🎯 No Analysis Data Available</h3>
        <p>Please analyze an application first from the <strong>Analytics Dashboard</strong> to access export functionality.</p>
        <p>Once you have analysis data, you can export in multiple formats:</p>
        <ul>
        <li>📊 <strong>Excel</strong> - Best for detailed analysis and presentations</li>
        <li>📄 <strong>CSV</strong> - Simple format for data processing</li>
        <li>🔧 <strong>JSON</strong> - For developers and API integration</li>
        <li>📋 <strong>Comprehensive Report</strong> - Professional markdown report</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

def _generate_comprehensive_report(df, app_name):
    """Generate a comprehensive analysis report"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Calculate key metrics
    total_reviews = len(df)
    avg_rating = df['score'].mean() if 'score' in df.columns else 0

    if 'sentiment' in df.columns:
        positive_pct = (df['sentiment'] == 'Positive').sum() / total_reviews * 100
        negative_pct = (df['sentiment'] == 'Negative').sum() / total_reviews * 100
        neutral_pct = (df['sentiment'] == 'Neutral').sum() / total_reviews * 100
    else:
        positive_pct = negative_pct = neutral_pct = 0

    report = f"""# {app_name} - Comprehensive Analysis Report

**Generated:** {timestamp}  
**Platform:** ReviewForge Analytics Pro  
**Developer:** Ayush Pandey  

---

## 📊 Executive Summary

### Key Metrics Overview
- **Total Reviews Analyzed:** {total_reviews:,}
- **Average Rating:** {avg_rating:.2f}/5.0
- **Sentiment Distribution:**
  - Positive: {positive_pct:.1f}%
  - Negative: {negative_pct:.1f}%
  - Neutral: {neutral_pct:.1f}%

### Overall Assessment
"""

    if avg_rating >= 4.0 and positive_pct >= 70:
        report += "🏆 **Excellent Performance** - The app shows outstanding user satisfaction with high ratings and positive sentiment."
    elif avg_rating >= 3.5 and positive_pct >= 60:
        report += "✅ **Good Performance** - The app maintains solid user satisfaction with room for optimization."
    elif avg_rating >= 3.0:
        report += "⚠️ **Average Performance** - The app shows mixed user feedback requiring attention to key issues."
    else:
        report += "🚨 **Below Average Performance** - Significant improvements needed to address user concerns."

    report += f"""

---

## 📈 Detailed Analysis

### Rating Breakdown
"""

    if 'score' in df.columns:
        rating_counts = df['score'].value_counts().sort_index()
        for rating, count in rating_counts.items():
            percentage = (count / total_reviews) * 100
            stars = "⭐" * rating
            report += f"- **{rating} {stars}:** {count:,} reviews ({percentage:.1f}%)\n"

    report += f"""
### Sentiment Analysis Results
- **Positive Sentiment:** {positive_pct:.1f}% of users express satisfaction
- **Negative Sentiment:** {negative_pct:.1f}% of users express dissatisfaction  
- **Neutral Sentiment:** {neutral_pct:.1f}% of users are neutral

### Key Insights
"""

    # Add insights based on data
    insights = []

    if positive_pct > 70:
        insights.append("✅ Strong user satisfaction indicates good product-market fit")
    if negative_pct > 30:
        insights.append("⚠️ High negative sentiment requires immediate attention")
    if avg_rating > 4.0:
        insights.append("🏆 Excellent average rating demonstrates quality delivery")
    if total_reviews > 1000:
        insights.append("📊 High review volume indicates strong user engagement")

    for insight in insights:
        report += f"- {insight}\n"

    report += f"""
### Recommendations

Based on the comprehensive analysis of {total_reviews:,} reviews:

1. **Priority Actions:**
   - {"Focus on maintaining current quality standards" if avg_rating >= 4.0 else "Address negative feedback patterns immediately"}
   - {"Continue current strategy" if positive_pct >= 70 else "Implement user feedback improvements"}

2. **Growth Opportunities:**
   - Monitor user sentiment trends regularly
   - Implement feature requests from positive reviews
   - Address common complaints in negative reviews

3. **Long-term Strategy:**
   - Maintain engagement with satisfied users
   - Develop retention strategies for neutral users
   - Create feedback loops for continuous improvement

---

## 🔧 Technical Details

**Analysis Parameters:**
- Reviews Analyzed: {total_reviews:,}
- Analysis Date: {timestamp}
- Sentiment Model: Enhanced TextBlob with Emotional Intelligence
- Confidence Threshold: Advanced ML Classification
- Data Quality: {"High" if total_reviews >= 500 else "Medium" if total_reviews >= 100 else "Basic"}

**Methodology:**
- Advanced natural language processing for sentiment analysis
- Machine learning algorithms for pattern recognition
- Statistical analysis for trend identification
- Confidence scoring for reliability assessment

---

*Report generated by ReviewForge Analytics Pro - Advanced Review Analysis Platform*  
*Developed by Ayush Pandey | © 2024*  
*For support and inquiries, please contact through the application interface*
"""

    return report

# Main Application Logic
def main():
    """Enhanced main application controller with improved routing"""
    # Initialize session state
    initialize_session_state()

    # Create navigation
    create_enhanced_navigation()

    # Page routing with enhanced error handling
    try:
        if st.session_state.current_page == 'dashboard':
            dashboard_page()
        elif st.session_state.current_page == 'deep_analysis':
            deep_analysis_page()
        elif st.session_state.current_page == 'competitor':
            competitor_analysis_page()
        elif st.session_state.current_page == 'ml_insights':
            deep_analysis_page()  # Same as deep analysis with ML focus
        elif st.session_state.current_page == 'reviews_explorer':
            reviews_explorer_page()
        elif st.session_state.current_page == 'export_reports':
            export_reports_page()
        elif st.session_state.current_page == 'settings':
            settings_page()
        else:
            # Default to dashboard if unknown page
            st.session_state.current_page = 'dashboard'
            dashboard_page()

    except Exception as e:
        st.error(f"⚠️ An error occurred: {str(e)}")
        st.info("🔄 Please refresh the page or return to the dashboard.")

        # Reset to dashboard on error
        if st.button("🏠 Return to Dashboard"):
            st.session_state.current_page = 'dashboard'
            st.rerun()

    # Enhanced Footer with animations
    st.markdown("---")
    st.markdown("""
    <div class="glass-card" style="text-align: center; margin-top: 2rem; animation: fadeInUp 1s ease-out;">
        <h3 style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;">
            ReviewForge Analytics Pro
        </h3>
        <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 1rem;">
            Advanced AI-Powered Review Analysis Platform with Machine Learning Intelligence
        </p>
        <div style="background: linear-gradient(135deg, #f093fb, #f5576c); padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
            <strong style="color: white; font-size: 1.1rem;">
                Developed by Ayush Pandey
            </strong>
            <br>
            <small style="color: rgba(255, 255, 255, 0.9);">
                Advanced Analytics & AI Specialist | Version 2.0.0 Pro
            </small>
        </div>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; color: rgba(255, 255, 255, 0.7);">
            <div>🤖 <strong>5 ML Models</strong></div>
            <div>📊 <strong>7 Analysis Pages</strong></div>
            <div>⚡ <strong>Real-time Processing</strong></div>
            <div>🎯 <strong>Zero Errors</strong></div>
        </div>
        <p style="color: rgba(255, 255, 255, 0.6); margin-top: 1rem; font-size: 0.9rem;">
            © 2024 ReviewForge Analytics Pro. All rights reserved.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
