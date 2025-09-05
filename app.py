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

# Enhanced CSS Styling with Premium Design
def apply_enhanced_styling():
    st.markdown("""
    <style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Advanced CSS Variables */
    :root {
        --primary-color: #6366f1;
        --primary-dark: #4f46e5;
        --primary-light: #8b5cf6;
        --secondary-color: #06b6d4;
        --accent-gold: #f59e0b;
        --accent-emerald: #10b981;
        --success-color: #22c55e;
        --warning-color: #f97316;
        --error-color: #ef4444;
        --info-color: #3b82f6;
        
        /* Background Gradients */
        --bg-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --bg-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --bg-dark: linear-gradient(135deg, #0c4a6e 0%, #1e3a8a 100%);
        --bg-glass: rgba(255, 255, 255, 0.25);
        --bg-glass-dark: rgba(15, 23, 42, 0.8);
        
        /* Modern Colors */
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #94a3b8;
        --text-white: #ffffff;
        --border-light: #e2e8f0;
        --border-primary: rgba(99, 102, 241, 0.3);
        
        /* Enhanced Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --shadow-glass: 0 8px 32px rgba(31, 38, 135, 0.37);
        
        /* Border Radius */
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 24px;
        --radius-full: 50px;
        
        /* Transitions */
        --transition-fast: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-normal: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Global Reset and Base Styles */
    * {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    .main, .block-container {
        background: var(--bg-primary);
        min-height: 100vh;
        padding-top: 2rem;
    }

    /* Enhanced Header Design */
    .modern-header {
        background: var(--bg-glass);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 3rem 2rem;
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-glass);
        margin-bottom: 3rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .modern-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        z-index: -1;
    }

    .header-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        animation: gradientShift 3s ease infinite;
        letter-spacing: -0.025em;
        line-height: 1.1;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .header-subtitle {
        font-size: 1.5rem;
        color: var(--text-white);
        font-weight: 400;
        margin-bottom: 2rem;
        opacity: 0.9;
        letter-spacing: 0.025em;
    }

    .developer-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
        color: white;
        padding: 1rem 2rem;
        border-radius: var(--radius-full);
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: var(--shadow-lg);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: var(--transition-normal);
    }

    .developer-badge:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-xl);
        background: linear-gradient(135deg, var(--primary-light), var(--secondary-color));
    }

    /* Premium Card Designs */
    .premium-card {
        background: var(--bg-glass);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--radius-lg);
        padding: 2rem;
        box-shadow: var(--shadow-glass);
        margin-bottom: 2rem;
        transition: var(--transition-normal);
        position: relative;
        overflow: hidden;
    }

    .premium-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color), var(--primary-light), var(--secondary-color));
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    }

    .premium-card:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: var(--shadow-xl), 0 0 40px rgba(99, 102, 241, 0.3);
        border-color: rgba(99, 102, 241, 0.4);
    }

    .metric-card {
        background: var(--bg-glass);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: var(--radius-lg);
        padding: 2rem;
        text-align: center;
        box-shadow: var(--shadow-glass);
        transition: var(--transition-normal);
        position: relative;
        overflow: hidden;
    }

    .metric-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05));
        pointer-events: none;
        border-radius: var(--radius-lg);
    }

    .metric-card:hover {
        transform: translateY(-6px);
        box-shadow: var(--shadow-xl), 0 0 30px rgba(99, 102, 241, 0.2);
        border-color: var(--primary-color);
    }

    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        line-height: 1;
    }

    .metric-label {
        color: var(--text-white);
        font-weight: 500;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        opacity: 0.9;
    }

    /* Enhanced Sidebar */
    .css-1d391kg {
        background: var(--bg-dark) !important;
        border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
    }

    .sidebar-section {
        background: var(--bg-glass-dark);
        backdrop-filter: blur(10px);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .sidebar-title {
        color: var(--text-white);
        font-weight: 700;
        font-size: 1.4rem;
        margin-bottom: 1.5rem;
        text-align: center;
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
        padding: 1rem;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-md);
    }

    .nav-button {
        background: rgba(255, 255, 255, 0.1) !important;
        color: var(--text-white) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.875rem 1.5rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: var(--transition-normal) !important;
        margin-bottom: 0.5rem !important;
        backdrop-filter: blur(10px) !important;
    }

    .nav-button:hover {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light)) !important;
        transform: translateX(8px) !important;
        box-shadow: var(--shadow-lg) !important;
        border-color: var(--primary-light) !important;
    }

    /* Enhanced Form Controls */
    .stTextInput input, .stSelectbox select, .stNumberInput input, .stTextArea textarea {
        background: var(--bg-glass) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: var(--transition-normal) !important;
        color: var(--text-primary) !important;
    }

    .stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
        outline: none !important;
    }

    .stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label {
        font-weight: 600 !important;
        color: var(--text-white) !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Premium Button Styles */
    .stButton button {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light)) !important;
        color: var(--text-white) !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.875rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: var(--transition-normal) !important;
        box-shadow: var(--shadow-lg) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: var(--shadow-xl), 0 0 30px rgba(99, 102, 241, 0.4) !important;
        background: linear-gradient(135deg, var(--primary-light), var(--secondary-color)) !important;
    }

    .stButton button:active {
        transform: translateY(-1px) !important;
    }

    /* Enhanced Charts and Visualizations */
    .chart-container {
        background: var(--bg-glass);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--radius-lg);
        padding: 2rem;
        box-shadow: var(--shadow-glass);
        margin-bottom: 2rem;
        transition: var(--transition-normal);
    }

    .chart-container:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-xl);
        border-color: var(--border-primary);
    }

    .chart-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-white);
        margin-bottom: 1.5rem;
        text-align: center;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Enhanced Data Tables */
    .stDataFrame {
        background: var(--bg-glass) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: var(--radius-lg) !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-glass) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    .stDataFrame table {
        background: transparent !important;
    }

    .stDataFrame thead tr th {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark)) !important;
        color: var(--text-white) !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-size: 0.9rem !important;
    }

    .stDataFrame tbody tr td {
        background: rgba(255, 255, 255, 0.1) !important;
        color: var(--text-white) !important;
        padding: 1rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-weight: 400 !important;
    }

    .stDataFrame tbody tr:hover td {
        background: rgba(99, 102, 241, 0.2) !important;
    }

    /* Enhanced Progress Indicators */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--primary-light)) !important;
        border-radius: var(--radius-full) !important;
        height: 12px !important;
        box-shadow: var(--shadow-md) !important;
    }

    /* Status Messages Enhancement */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: var(--radius-md) !important;
        padding: 1.25rem 1.5rem !important;
        font-weight: 500 !important;
        box-shadow: var(--shadow-lg) !important;
        border: none !important;
        backdrop-filter: blur(10px) !important;
    }

    .stSuccess {
        background: linear-gradient(135deg, var(--success-color), var(--accent-emerald)) !important;
        color: white !important;
    }

    .stWarning {
        background: linear-gradient(135deg, var(--warning-color), var(--accent-gold)) !important;
        color: white !important;
    }

    .stError {
        background: linear-gradient(135deg, var(--error-color), #dc2626) !important;
        color: white !important;
    }

    .stInfo {
        background: linear-gradient(135deg, var(--info-color), var(--secondary-color)) !important;
        color: white !important;
    }

    /* Enhanced Selectbox and Multiselect */
    .stSelectbox > div > div {
        background: var(--bg-glass) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: var(--radius-md) !important;
    }

    .stMultiSelect > div > div {
        background: var(--bg-glass) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: var(--radius-md) !important;
    }

    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-glass);
        backdrop-filter: blur(10px);
        border-radius: var(--radius-md);
        padding: 0.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-white);
        font-weight: 500;
        border-radius: var(--radius-sm);
        padding: 0.75rem 1.5rem;
        transition: var(--transition-fast);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light)) !important;
        color: white !important;
        box-shadow: var(--shadow-md);
    }

    /* Enhanced Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 3rem;
    }

    /* Navigation Enhancements */
    .nav-section {
        background: var(--bg-glass-dark);
        backdrop-filter: blur(10px);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: var(--shadow-md);
    }

    .nav-section h3 {
        color: var(--primary-light);
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .current-page-indicator {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
        color: white;
        padding: 1rem;
        border-radius: var(--radius-md);
        text-align: center;
        font-weight: 600;
        box-shadow: var(--shadow-lg);
        margin-top: 1rem;
    }

    /* Enhanced Sliders */
    .stSlider > div > div > div {
        background: var(--primary-color) !important;
    }

    .stSlider > div > div > div > div {
        background: var(--text-white) !important;
        box-shadow: var(--shadow-md) !important;
    }

    /* Loading Animation Enhancement */
    .stSpinner > div {
        border-top-color: var(--primary-light) !important;
        border-right-color: var(--primary-color) !important;
        border-bottom-color: var(--secondary-color) !important;
    }

    /* Enhanced Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-white) !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }

    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }

    p, div, span, label {
        color: var(--text-white) !important;
        line-height: 1.6 !important;
    }

    /* Code and Monospace */
    code, pre {
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        background: var(--bg-glass-dark) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Enhanced Scrollbars */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-sm);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
        border-radius: var(--radius-sm);
        box-shadow: var(--shadow-sm);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, var(--primary-light), var(--secondary-color));
    }

    /* Responsive Design Enhancements */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.5rem !important;
        }
        
        .header-subtitle {
            font-size: 1.2rem !important;
        }
        
        .metric-value {
            font-size: 2.2rem !important;
        }
        
        .premium-card {
            padding: 1.5rem !important;
        }
        
        .modern-header {
            padding: 2rem 1.5rem !important;
        }
    }

    /* Animation Classes */
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .slide-in {
        animation: slideIn 0.5s ease-out;
    }

    @keyframes slideIn {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    /* Footer Styling */
    .footer {
        background: var(--bg-glass-dark);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin-top: 3rem;
        text-align: center;
        color: var(--text-white);
        box-shadow: var(--shadow-lg);
    }

    .footer h4 {
        margin-bottom: 0.5rem;
        font-weight: 700;
        color: var(--primary-light);
    }

    .footer p {
        margin-bottom: 0.25rem;
        opacity: 0.8;
        font-size: 0.95rem;
    }

    /* Enhanced Plotly Charts */
    .js-plotly-plot {
        border-radius: var(--radius-md) !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-lg) !important;
    }
    </style>
    """, unsafe_allow_html=True)

apply_enhanced_styling()

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
        'export_data': None
    }

    for key, default_value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

initialize_session_state()

# Enhanced Helper Functions
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

# Initialize analyzer
analyzer = ReviewAnalyzer()

def create_modern_header():
    """Create enhanced modern header"""
    st.markdown("""
    <div class="modern-header fade-in">
        <h1 class="header-title">ReviewForge Analytics Pro</h1>
        <p class="header-subtitle">Advanced AI-Powered Review Analysis Platform</p>
        <div class="developer-badge">
            Developed by Ayush Pandey - Advanced Analytics & Machine Learning
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_enhanced_navigation():
    """Create premium navigation system"""
    st.sidebar.markdown('<div class="sidebar-title slide-in">Navigation Hub</div>', unsafe_allow_html=True)

    pages = {
        'dashboard': 'Analytics Dashboard',
        'deep_analysis': 'Deep Analysis Engine',
        'competitor': 'Competitive Intelligence',
        'ml_insights': 'ML Insights Laboratory',
        'sentiment_trends': 'Sentiment Trend Analysis',
        'export_reports': 'Export & Reporting',
        'settings': 'Advanced Settings'
    }

    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    
    for page_key, page_name in pages.items():
        button_class = "nav-button"
        if st.sidebar.button(page_name, key=f"nav_{page_key}", use_container_width=True, help=f"Navigate to {page_name}"):
            st.session_state.current_page = page_key
            st.rerun()

    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Enhanced current page indicator
    st.sidebar.markdown(f"""
    <div class="nav-section slide-in">
        <h3>Current Section</h3>
        <div class="current-page-indicator">
            {pages[st.session_state.current_page]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Add system status
    st.sidebar.markdown("""
    <div class="nav-section">
        <h3>System Status</h3>
        <div style="color: #10b981; font-weight: 600;">
            🟢 Online & Ready
        </div>
        <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.85rem; margin-top: 0.5rem;">
            All systems operational
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_enhanced_metrics_dashboard(df):
    """Create premium metrics dashboard"""
    if df.empty:
        return

    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.markdown("## Key Performance Indicators")

    cols = st.columns(5)

    metrics_data = [
        {
            'value': f"{df['score'].mean():.1f}" if 'score' in df.columns else "0.0",
            'label': "Average Rating",
            'icon': "⭐"
        },
        {
            'value': f"{len(df):,}",
            'label': "Total Reviews",
            'icon': "📊"
        },
        {
            'value': f"{(df['sentiment'].str.contains('Positive', na=False).sum() / len(df)) * 100:.1f}%" if 'sentiment' in df.columns else "0.0%",
            'label': "Positive Rate",
            'icon': "👍"
        },
        {
            'value': f"{df['confidence'].mean() * 100:.1f}%" if 'confidence' in df.columns else "0.0%",
            'label': "Analysis Confidence",
            'icon': "🎯"
        },
        {
            'value': f"{abs(df['emotional_intensity'].mean()):.2f}" if 'emotional_intensity' in df.columns else "0.00",
            'label': "Emotional Intensity",
            'icon': "🔥"
        }
    ]

    for i, (col, metric) in enumerate(zip(cols, metrics_data)):
        with col:
            st.markdown(f"""
            <div class="metric-card fade-in" style="animation-delay: {i * 0.1}s;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{metric['icon']}</div>
                <div class="metric-value">{metric['value']}</div>
                <div class="metric-label">{metric['label']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def create_premium_visualizations(df):
    """Create enhanced interactive visualizations"""
    if df.empty:
        return

    # Enhanced color palette
    colors = {
        'primary': '#6366f1',
        'secondary': '#8b5cf6',
        'accent': '#06b6d4',
        'success': '#22c55e',
        'warning': '#f97316',
        'error': '#ef4444',
        'positive': '#10b981',
        'negative': '#ef4444',
        'neutral': '#6b7280',
        'gradient': ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f97316']
    }

    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Row 1: Sentiment and Rating Analysis
    col1, col2 = st.columns(2)

    with col1:
        # Enhanced Key Phrases Analysis
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown("## Key Phrases Extraction")
        
        if 'key_phrases' in ml_insights and ml_insights['key_phrases']:
            phrases_data = []
            for i, phrase_data in enumerate(ml_insights['key_phrases'][:10]):
                phrases_data.append({
                    'Rank': i + 1,
                    'Phrase': phrase_data['phrase'],
                    'Frequency': phrase_data['frequency'],
                    'Relevance': 'High' if phrase_data['frequency'] > 5 else 'Medium' if phrase_data['frequency'] > 2 else 'Low'
                })

            phrases_df = pd.DataFrame(phrases_data)
            st.dataframe(phrases_df, use_container_width=True, hide_index=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Enhanced Correlation Analysis
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown("## Advanced Correlation Analysis")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()

            fig_corr = px.imshow(
                corr_matrix,
                text_auto='.2f',
                aspect="auto",
                title="",
                color_continuous_scale='RdBu_r',
                color_continuous_midpoint=0
            )
            
            fig_corr.update_layout(
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Poppins'),
                xaxis=dict(tickfont=dict(color='white')),
                yaxis=dict(tickfont=dict(color='white'))
            )

            st.plotly_chart(fig_corr, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.info("Please analyze an application first from the Dashboard page to access deep analysis features.")
        st.markdown('</div>', unsafe_allow_html=True)

def competitor_analysis_page():
    """Enhanced competitive intelligence page"""
    st.markdown('<div class="modern-header fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="header-title" style="font-size: 2.5rem;">Competitive Intelligence</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle" style="font-size: 1.2rem;">Compare your app against competitors with advanced benchmarking</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown("## Primary App Analysis")
        
        if st.session_state.analyzed_data is not None:
            st.success(f"✓ {st.session_state.get('current_app_name', 'App')} analyzed")
            df_primary = st.session_state.analyzed_data

            # Primary app metrics
            metrics_col1, metrics_col2 = st.columns(2)
            
            with metrics_col1:
                if 'score' in df_primary.columns:
                    avg_rating = df_primary['score'].mean()
                    st.metric("Average Rating", f"{avg_rating:.1f}", f"{avg_rating - 3.5:.1f}")

            with metrics_col2:
                if 'sentiment' in df_primary.columns:
                    positive_rate = (df_primary['sentiment'].str.contains('Positive', na=False).sum() / len(df_primary)) * 100
                    st.metric("Positive Sentiment", f"{positive_rate:.1f}%", f"{positive_rate - 50:.1f}%")
        else:
            st.info("Analyze your primary app first")
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown("## Competitor App")
        
        competitor_url = st.text_input(
            "Competitor App URL",
            placeholder="Enter competitor's Google Play URL"
        )

        if st.button("Analyze Competitor", use_container_width=True):
            if competitor_url:
                package_name = analyzer.extract_package_name(competitor_url)

                if package_name:
                    with st.spinner("Analyzing competitor..."):
                        competitor_df = analyzer.scrape_reviews(package_name, count=500)

                        if not competitor_df.empty:
                            st.session_state.competitor_data = competitor_df
                            st.session_state.competitor_app_name = analyzer.get_app_name(package_name)
                            st.success("Competitor analyzed successfully!")
                        else:
                            st.error("Failed to analyze competitor")
                else:
                    st.error("Invalid competitor URL")
            else:
                st.warning("Please enter a competitor URL")

        st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced Comparative Analysis
    if (st.session_state.analyzed_data is not None and 
        st.session_state.competitor_data is not None):

        st.markdown("---")
        st.markdown("## Comparative Analysis Dashboard")

        df_primary = st.session_state.analyzed_data
        df_competitor = st.session_state.competitor_data

        # Enhanced side-by-side comparison
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">Rating Comparison</h3>', unsafe_allow_html=True)
            
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
                title='',
                color='Rating',
                color_continuous_scale='RdYlGn',
                text='Rating'
            )

            fig_rating_comp.update_traces(
                texttemplate='%{text:.2f}',
                textposition='outside',
                textfont=dict(color='white', family='Poppins')
            )

            fig_rating_comp.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Poppins'),
                xaxis=dict(tickfont=dict(color='white')),
                yaxis=dict(tickfont=dict(color='white'), gridcolor='rgba(255,255,255,0.2)'),
                height=350
            )

            st.plotly_chart(fig_rating_comp, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">Sentiment Comparison</h3>', unsafe_allow_html=True)
            
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
                    title='',
                    color='Positive Sentiment %',
                    color_continuous_scale='RdYlGn',
                    text='Positive Sentiment %'
                )

                fig_sentiment_comp.update_traces(
                    texttemplate='%{text:.1f}%',
                    textposition='outside',
                    textfont=dict(color='white', family='Poppins')
                )

                fig_sentiment_comp.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', family='Poppins'),
                    xaxis=dict(tickfont=dict(color='white')),
                    yaxis=dict(tickfont=dict(color='white'), gridcolor='rgba(255,255,255,0.2)'),
                    height=350
                )

                st.plotly_chart(fig_sentiment_comp, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">Review Volume</h3>', unsafe_allow_html=True)
            
            volume_data = pd.DataFrame({
                'App': [st.session_state.get('current_app_name', 'Your App'), 
                       st.session_state.get('competitor_app_name', 'Competitor')],
                'Review Count': [len(df_primary), len(df_competitor)]
            })

            fig_volume_comp = px.bar(
                volume_data,
                x='App',
                y='Review Count',
                title='',
                color='Review Count',
                color_continuous_scale='Blues',
                text='Review Count'
            )

            fig_volume_comp.update_traces(
                texttemplate='%{text:,}',
                textposition='outside',
                textfont=dict(color='white', family='Poppins')
            )

            fig_volume_comp.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Poppins'),
                xaxis=dict(tickfont=dict(color='white')),
                yaxis=dict(tickfont=dict(color='white'), gridcolor='rgba(255,255,255,0.2)'),
                height=350
            )

            st.plotly_chart(fig_volume_comp, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Enhanced detailed comparison table
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("## Detailed Comparison Matrix")

        comparison_metrics = {
            'Metric': ['Average Rating', 'Total Reviews', 'Positive Sentiment %', 'Average Confidence', 'Emotional Intensity'],
            st.session_state.get('current_app_name', 'Your App'): [
                f"{df_primary['score'].mean():.2f}" if 'score' in df_primary.columns else 'N/A',
                f"{len(df_primary):,}",
                f"{(df_primary['sentiment'].str.contains('Positive', na=False).sum() / len(df_primary)) * 100:.1f}%" if 'sentiment' in df_primary.columns else 'N/A',
                f"{df_primary['confidence'].mean() * 100:.1f}%" if 'confidence' in df_primary.columns else 'N/A',
                f"{abs(df_primary['emotional_intensity'].mean()):.2f}" if 'emotional_intensity' in df_primary.columns else 'N/A'
            ],
            st.session_state.get('competitor_app_name', 'Competitor'): [
                f"{df_competitor['score'].mean():.2f}" if 'score' in df_competitor.columns else 'N/A',
                f"{len(df_competitor):,}",
                f"{(df_competitor['sentiment'].str.contains('Positive', na=False).sum() / len(df_competitor)) * 100:.1f}%" if 'sentiment' in df_competitor.columns else 'N/A',
                f"{df_competitor['confidence'].mean() * 100:.1f}%" if 'confidence' in df_competitor.columns else 'N/A',
                f"{abs(df_competitor['emotional_intensity'].mean()):.2f}" if 'emotional_intensity' in df_competitor.columns else 'N/A'
            ]
        }

        comparison_df = pd.DataFrame(comparison_metrics)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

def export_reports_page():
    """Enhanced export and reporting functionality"""
    st.markdown('<div class="modern-header fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="header-title" style="font-size: 2.5rem;">Export & Reporting</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle" style="font-size: 1.2rem;">Generate comprehensive reports and export your analysis data</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data
        app_name = st.session_state.get('current_app_name', 'Unknown App')

        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown(f"## Export Options for {app_name}")

        # Enhanced export format selection
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📊 Export as CSV", use_container_width=True):
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV Report",
                    data=csv_data,
                    file_name=f"{app_name}_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

        with col2:
            if st.button("📈 Export as Excel", use_container_width=True):
                try:
                    excel_buffer = BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='Analysis Results', index=False)

                        # Add summary sheet
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
            if st.button("🔗 Export as JSON", use_container_width=True):
                json_data = df.to_json(orient='records', date_format='iso')
                st.download_button(
                    label="Download JSON Data",
                    data=json_data,
                    file_name=f"{app_name}_analysis_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

        st.markdown('</div>', unsafe_allow_html=True)

        # Enhanced export preview
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("## Export Preview")

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

        st.markdown('</div>', unsafe_allow_html=True)

        # Enhanced comprehensive report generation
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("## Comprehensive Analysis Report")

        if st.button("📋 Generate Full Report", type="primary"):
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

## Strategic Recommendations
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

        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.info("Please analyze an application first to access export functionality.")
        st.markdown('</div>', unsafe_allow_html=True)

def settings_page():
    """Enhanced settings and preferences"""
    st.markdown('<div class="modern-header fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="header-title" style="font-size: 2.5rem;">Advanced Settings</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle" style="font-size: 1.2rem;">Customize your analysis preferences and export options</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced analysis settings
    st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
    st.markdown("## Analysis Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Sentiment Analysis Settings")
        sentiment_threshold = st.slider("Sentiment Confidence Threshold", 0.0, 1.0, 0.6, 0.1)
        enable_aspect_analysis = st.checkbox("Enable Aspect-Based Analysis", value=True)
        enable_emotion_detection = st.checkbox("Enable Emotional Intensity Analysis", value=True)

    with col2:
        st.markdown("### Machine Learning Settings")
        enable_topic_modeling = st.checkbox("Enable Topic Modeling", value=True)
        topic_count = st.slider("Number of Topics", 3, 10, 5)
        enable_clustering = st.checkbox("Enable Review Clustering", value=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced export settings
    st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
    st.markdown("## Export & Reporting")

    export_format = st.selectbox(
        "Preferred Export Format",
        options=["CSV", "Excel", "JSON", "PDF Report"],
        index=0
    )

    col1, col2 = st.columns(2)
    
    with col1:
        include_raw_data = st.checkbox("Include Raw Review Data", value=True)
        include_visualizations = st.checkbox("Include Charts and Visualizations", value=True)
    
    with col2:
        auto_backup = st.checkbox("Enable Automatic Backup", value=False)
        compress_exports = st.checkbox("Compress Large Exports", value=True)

    # Save settings
    if st.button("💾 Save Settings", type="primary"):
        settings = {
            'sentiment_threshold': sentiment_threshold,
            'enable_aspect_analysis': enable_aspect_analysis,
            'enable_emotion_detection': enable_emotion_detection,
            'enable_topic_modeling': enable_topic_modeling,
            'topic_count': topic_count,
            'enable_clustering': enable_clustering,
            'export_format': export_format,
            'include_raw_data': include_raw_data,
            'include_visualizations': include_visualizations,
            'auto_backup': auto_backup,
            'compress_exports': compress_exports
        }
        st.session_state.user_preferences = settings
        st.success("Settings saved successfully!")

    st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced system information
    st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
    st.markdown("## System Information")

    system_info = {
        'Application Version': '2.0.0 Pro Enhanced',
        'Developer': 'Ayush Pandey',
        'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Python Version': '3.9+',
        'Streamlit Version': st.__version__ if hasattr(st, '__version__') else 'Latest',
        'Analysis Engine': 'Advanced ML-Powered',
        'UI Framework': 'Premium Enhanced Design'
    }

    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        for i, (key, value) in enumerate(list(system_info.items())[:4]):
            st.text(f"{key}: {value}")
    
    with info_col2:
        for key, value in list(system_info.items())[4:]:
            st.text(f"{key}: {value}")

    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced main application logic
def main():
    """Enhanced main application controller"""
    create_enhanced_navigation()

    # Enhanced page routing with animations
    if st.session_state.current_page == 'dashboard':
        dashboard_page()
    elif st.session_state.current_page == 'deep_analysis':
        deep_analysis_page()
    elif st.session_state.current_page == 'competitor':
        competitor_analysis_page()
    elif st.session_state.current_page == 'ml_insights':
        deep_analysis_page()  # Reuse deep analysis for ML insights
    elif st.session_state.current_page == 'sentiment_trends':
        dashboard_page()  # Can be expanded with trend analysis
    elif st.session_state.current_page == 'export_reports':
        export_reports_page()
    elif st.session_state.current_page == 'settings':
        settings_page()

    # Enhanced footer
    st.markdown("---")
    st.markdown("""
    <div class="footer fade-in">
        <h4>ReviewForge Analytics Pro</h4>
        <p>Advanced AI-Powered Review Analysis Platform</p>
        <p>Developed by <strong>Ayush Pandey</strong> | Version 2.0.0 Pro Enhanced | © 2024</p>
        <p style="font-size: 0.8rem; opacity: 0.6;">Powered by Machine Learning & Advanced Analytics</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">Sentiment Distribution Analysis</h3>', unsafe_allow_html=True)
        
        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts()

            fig_donut = go.Figure(data=[go.Pie(
                labels=sentiment_counts.index,
                values=sentiment_counts.values,
                hole=0.65,
                marker=dict(
                    colors=[colors['positive'] if 'Positive' in s else 
                           colors['negative'] if 'Negative' in s else colors['neutral'] 
                           for s in sentiment_counts.index],
                    line=dict(color='rgba(255,255,255,0.8)', width=3)
                ),
                textinfo='label+percent',
                textfont=dict(size=14, color='white', family='Poppins'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])

            fig_donut.update_layout(
                title=dict(
                    text='',
                    x=0.5,
                    font=dict(size=20, color=colors['primary'])
                ),
                annotations=[dict(
                    text=f'<b>{sentiment_counts.sum():,}</b><br><span style="font-size:14px;">Total Reviews</span>',
                    x=0.5, y=0.5,
                    font=dict(size=18, color='white', family='Poppins'),
                    showarrow=False
                )],
                showlegend=True,
                height=450,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Poppins'),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5,
                    font=dict(color='white')
                )
            )

            st.plotly_chart(fig_donut, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">Rating Distribution</h3>', unsafe_allow_html=True)
        
        if 'score' in df.columns:
            rating_dist = df['score'].value_counts().sort_index()

            fig_rating = go.Figure()
            fig_rating.add_trace(go.Bar(
                x=[f'{i} ★' for i in rating_dist.index],
                y=rating_dist.values,
                marker=dict(
                    color=[colors['error'] if i <= 2 else 
                          colors['warning'] if i == 3 else 
                          colors['success'] if i >= 4 else colors['neutral']
                          for i in rating_dist.index],
                    line=dict(color='rgba(255,255,255,0.8)', width=2)
                ),
                text=[f'{val:,}' for val in rating_dist.values],
                textposition='outside',
                textfont=dict(color='white', family='Poppins', size=12),
                hovertemplate='<b>%{x}</b><br>Reviews: %{y:,}<extra></extra>'
            ))

            fig_rating.update_layout(
                title='',
                xaxis=dict(
                    title='Rating',
                    titlefont=dict(color='white', family='Poppins'),
                    tickfont=dict(color='white', family='Poppins'),
                    gridcolor='rgba(255,255,255,0.2)'
                ),
                yaxis=dict(
                    title='Number of Reviews',
                    titlefont=dict(color='white', family='Poppins'),
                    tickfont=dict(color='white', family='Poppins'),
                    gridcolor='rgba(255,255,255,0.2)'
                ),
                showlegend=False,
                height=450,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(fig_rating, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Row 2: Advanced Analytics
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Emotional Intensity vs Rating Analysis</h3>', unsafe_allow_html=True)
    
    if all(col in df.columns for col in ['score', 'emotional_intensity']):
        intensity_by_rating = df.groupby('score')['emotional_intensity'].agg(['mean', 'std', 'count']).reset_index()

        fig_intensity = go.Figure()

        # Add main line with enhanced styling
        fig_intensity.add_trace(go.Scatter(
            x=intensity_by_rating['score'],
            y=intensity_by_rating['mean'],
            mode='lines+markers',
            name='Average Intensity',
            line=dict(color=colors['primary'], width=4, shape='spline'),
            marker=dict(
                size=12, 
                color=colors['secondary'],
                line=dict(color='white', width=2),
                symbol='circle'
            ),
            error_y=dict(
                type='data',
                array=intensity_by_rating['std'],
                visible=True,
                color='rgba(255,255,255,0.5)',
                thickness=2
            ),
            hovertemplate='<b>%{x} Stars</b><br>Avg Intensity: %{y:.3f}<br>Reviews: %{customdata}<extra></extra>',
            customdata=intensity_by_rating['count']
        ))

        fig_intensity.update_layout(
            xaxis=dict(
                title='Rating',
                titlefont=dict(color='white', family='Poppins', size=14),
                tickfont=dict(color='white', family='Poppins'),
                gridcolor='rgba(255,255,255,0.2)',
                tickvals=list(range(1, 6))
            ),
            yaxis=dict(
                title='Average Emotional Intensity',
                titlefont=dict(color='white', family='Poppins', size=14),
                tickfont=dict(color='white', family='Poppins'),
                gridcolor='rgba(255,255,255,0.2)'
            ),
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Poppins'),
            showlegend=False
        )

        st.plotly_chart(fig_intensity, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Row 3: Aspect Analysis
    aspect_cols = [col for col in df.columns if col.startswith('aspect_')]
    if aspect_cols:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">Aspect Coverage Analysis</h3>', unsafe_allow_html=True)

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
            marker=dict(color=colors['secondary'], size=8),
            fillcolor=f'rgba({int(colors["primary"][1:3], 16)}, {int(colors["primary"][3:5], 16)}, {int(colors["primary"][5:7], 16)}, 0.3)',
            hovertemplate='<b>%{theta}</b><br>Coverage: %{r:.1f}%<extra></extra>'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(aspect_data.values()) * 1.2] if aspect_data else [0, 100],
                    tickfont=dict(color='white', family='Poppins'),
                    gridcolor='rgba(255,255,255,0.2)'
                ),
                angularaxis=dict(
                    tickfont=dict(color='white', family='Poppins', size=12),
                    gridcolor='rgba(255,255,255,0.2)'
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Poppins'),
            showlegend=False
        )

        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def dashboard_page():
    """Enhanced main dashboard page"""
    create_modern_header()

    # Enhanced input section
    st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
    st.markdown("## Application Analysis Configuration")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        url_input = st.text_input(
            "Google Play Store URL or Package Name",
            placeholder="https://play.google.com/store/apps/details?id=com.example.app",
            help="Enter the full Google Play Store URL or just the package name for analysis"
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
                    df = analyzer.scrape_reviews(
                        package_name, 
                        count=review_count, 
                        sort_by=sort_mapping[sort_option]
                    )

                    if not df.empty:
                        st.session_state.analyzed_data = df
                        st.session_state.current_app_name = analyzer.get_app_name(package_name)
                        st.success(f"Successfully analyzed {len(df)} reviews!")
                        st.rerun()
                    else:
                        st.error("No reviews found or failed to extract reviews")
            else:
                st.error("Invalid URL or package name format")
        else:
            st.warning("Please enter a valid Google Play Store URL or package name")

    st.markdown('</div>', unsafe_allow_html=True)

    # Display enhanced results
    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data

        st.markdown("---")
        st.markdown(f"## Analysis Results: {st.session_state.get('current_app_name', 'Unknown App')}")

        # Enhanced metrics dashboard
        create_enhanced_metrics_dashboard(df)

        # Enhanced visualizations
        create_premium_visualizations(df)

        # Enhanced recent reviews table
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("## Recent Reviews Sample")
        
        display_columns = ['at', 'userName', 'score', 'sentiment', 'confidence', 'content']
        available_columns = [col for col in display_columns if col in df.columns]

        if available_columns:
            sample_df = df[available_columns].head(10).copy()
            if 'at' in sample_df.columns:
                sample_df['at'] = pd.to_datetime(sample_df['at']).dt.strftime('%Y-%m-%d')
            if 'content' in sample_df.columns:
                sample_df['content'] = sample_df['content'].str[:100] + '...'

            st.dataframe(sample_df, use_container_width=True, hide_index=True)

        st.markdown('</div>', unsafe_allow_html=True)

def deep_analysis_page():
    """Enhanced deep analysis page"""
    st.markdown('<div class="modern-header fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="header-title" style="font-size: 2.5rem;">Deep Analysis Engine</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle" style="font-size: 1.2rem;">Advanced analytical tools and machine learning insights</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data

        # Generate ML insights if not already done
        if 'ml_insights' not in st.session_state or not st.session_state.ml_insights:
            with st.spinner("Generating machine learning insights..."):
                ml_insights = analyzer.generate_ml_insights(df)
                st.session_state.ml_insights = ml_insights

        ml_insights = st.session_state.ml_insights

        # Enhanced Topic Analysis
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown("## Topic Modeling Analysis")
        
        if 'topics' in ml_insights and ml_insights['topics']:
            topics_data = []
            for topic in ml_insights['topics']:
                topics_data.append({
                    'Topic ID': f"Topic {topic['topic_id']}",
                    'Keywords': ', '.join(topic['keywords'][:5]),
                    'Relevance Score': f"{topic['weight']:.3f}",
                    'Priority': 'High' if topic['weight'] > np.mean([t['weight'] for t in ml_insights['topics']]) else 'Medium'
                })

            topics_df = pd.DataFrame(topics_data)
            st.dataframe(topics_df, use_container_width=True, hide_index=True)

            # Enhanced topic visualization
            if len(ml_insights['topics']) > 1:
                topic_weights = [topic['weight'] for topic in ml_insights['topics']]
                topic_labels = [f"Topic {topic['topic_id']}" for topic in ml_insights['topics']]

                fig_topics = go.Figure(data=[go.Bar(
                    x=topic_labels,
                    y=topic_weights,
                    marker=dict(
                        color=colors['gradient'][:len(topic_labels)],
                        line=dict(color='rgba(255,255,255,0.8)', width=2)
                    ),
                    text=[f'{w:.3f}' for w in topic_weights],
                    textposition='outside',
                    textfont=dict(color='white', family='Poppins'),
                    hovertemplate='<b>%{x}</b><br>Relevance: %{y:.3f}<extra></extra>'
                )])

                fig_topics.update_layout(
                    title='',
                    xaxis=dict(
                        title='Topics',
                        titlefont=dict(color='white', family='Poppins'),
                        tickfont=dict(color='white', family='Poppins'),
                        gridcolor='rgba(255,255,255,0.2)'
                    ),
                    yaxis=dict(
                        title='Relevance Score',
                        titlefont=dict(color='white', family='Poppins'),
                        tickfont=dict(color='white', family='Poppins'),
                        gridcolor='rgba(255,255,255,0.2)'
                    ),
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', family='Poppins')
                )

                st.plotly_chart(fig_topics, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Enhanced Key Phrases Analysis
        st.markdown('<div class
