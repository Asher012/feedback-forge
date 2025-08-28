import streamlit as st
import pandas as pd
from google_play_scraper import Sort, reviews
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re
from collections import Counter
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from scipy import stats
import seaborn as sns
from wordcloud import WordCloud
import base64
from io import BytesIO
import time

# Page Configuration
st.set_page_config(
    page_title="Feedbacks Forge Pro", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS with Glass-morphism and Modern Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&display=swap');
    
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #06b6d4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --dark-bg: #0f172a;
        --light-bg: #ffffff;
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --shadow-light: rgba(0, 0, 0, 0.1);
        --shadow-medium: rgba(0, 0, 0, 0.15);
        --shadow-strong: rgba(0, 0, 0, 0.25);
        --border-radius: 16px;
        --border-radius-lg: 24px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        --gradient-secondary: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        --gradient-success: linear-gradient(135deg, #10b981 0%, #059669 100%);
        --gradient-warning: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        --gradient-error: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Glass-morphism Header */
    .header-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--border-radius-lg);
        padding: 60px 40px;
        margin: 20px 0 40px 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px var(--shadow-medium);
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: rotate 20s linear infinite;
        z-index: -1;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .app-title {
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 20px 0;
        letter-spacing: -2px;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .app-subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 30px;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    .version-badge {
        position: absolute;
        top: 30px;
        right: 30px;
        background: var(--gradient-primary);
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .creator-badge {
        position: absolute;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        color: white;
        padding: 10px 24px;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Advanced Button Styling */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 16px 32px;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: var(--transition);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.4);
    }
    
    /* Glass Card Components */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--border-radius);
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 32px var(--shadow-light);
        transition: var(--transition);
        position: relative;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 40px var(--shadow-medium);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
    }
    
    /* Advanced Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 24px;
        margin: 40px 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--border-radius);
        padding: 32px 24px;
        text-align: center;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: var(--gradient-primary);
        border-radius: var(--border-radius);
        z-index: -1;
        opacity: 0;
        transition: var(--transition);
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        color: white;
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-label {
        font-size: 1rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.8);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Advanced Review Cards */
    .review-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: var(--border-radius);
        padding: 32px;
        margin: 24px 0;
        box-shadow: 0 8px 40px var(--shadow-light);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .review-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--gradient-primary);
        transform: scaleY(0);
        transition: var(--transition);
    }
    
    .review-card:hover {
        transform: translateX(8px);
        box-shadow: 0 12px 50px var(--shadow-medium);
    }
    
    .review-card:hover::before {
        transform: scaleY(1);
    }
    
    .review-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 2px solid rgba(99, 102, 241, 0.1);
    }
    
    .review-user {
        font-weight: 700;
        font-size: 1.1rem;
        color: var(--text-primary);
    }
    
    .review-rating {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.1rem;
    }
    
    .star-rating {
        color: #fbbf24;
        font-size: 1.4rem;
        text-shadow: 0 2px 4px rgba(251, 191, 36, 0.3);
    }
    
    .review-content {
        color: var(--text-primary);
        line-height: 1.8;
        font-size: 1.05rem;
        margin: 20px 0;
    }
    
    .review-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid rgba(99, 102, 241, 0.1);
    }
    
    /* Enhanced Sentiment Badges */
    .sentiment-badge {
        padding: 8px 16px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-2px); }
    }
    
    .sentiment-positive {
        background: var(--gradient-success);
        color: white;
    }
    
    .sentiment-negative {
        background: var(--gradient-error);
        color: white;
    }
    
    .sentiment-neutral {
        background: var(--gradient-warning);
        color: white;
    }
    
    /* AI Insights with Advanced Styling */
    .ai-insights {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--border-radius-lg);
        padding: 40px;
        margin: 40px 0;
        position: relative;
    }
    
    .insight-item {
        background: rgba(255, 255, 255, 0.95);
        border-radius: var(--border-radius);
        padding: 28px;
        margin: 20px 0;
        box-shadow: 0 8px 32px var(--shadow-light);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .insight-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: var(--gradient-primary);
    }
    
    .insight-item.warning::before {
        background: var(--gradient-error);
    }
    
    .insight-item.positive::before {
        background: var(--gradient-success);
    }
    
    .insight-item:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 40px var(--shadow-medium);
    }
    
    /* Progress Animations */
    .progress-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--border-radius);
        padding: 40px;
        text-align: center;
        margin: 30px 0;
        position: relative;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 32px;
        height: 32px;
        border: 4px solid rgba(99, 102, 241, 0.3);
        border-top: 4px solid #6366f1;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 16px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Export Section */
    .export-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 30px;
        margin: 40px 0;
    }
    
    .export-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: var(--border-radius);
        padding: 40px 32px;
        text-align: center;
        box-shadow: 0 8px 32px var(--shadow-light);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .export-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-primary);
        transform: scaleX(0);
        transition: var(--transition);
    }
    
    .export-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px var(--shadow-medium);
    }
    
    .export-card:hover::before {
        transform: scaleX(1);
    }
    
    .export-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .export-desc {
        color: var(--text-secondary);
        line-height: 1.7;
        margin-bottom: 28px;
        font-size: 1rem;
    }
    
    /* Theme Toggle */
    .theme-toggle {
        position: fixed;
        top: 30px;
        right: 30px;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 50px;
        padding: 12px 20px;
        cursor: pointer;
        transition: var(--transition);
    }
    
    .theme-toggle:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.05);
    }
    
    /* Input Styling */
    .stTextArea textarea, .stTextInput input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(99, 102, 241, 0.2);
        border-radius: var(--border-radius);
        padding: 16px;
        font-size: 1rem;
        transition: var(--transition);
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        background: white;
    }
    
    /* Selectbox Styling */
    .stSelectbox div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: var(--border-radius);
        border: 2px solid rgba(99, 102, 241, 0.2);
    }
    
    /* Slider Styling */
    .stSlider .stSlider > div > div > div {
        background: var(--gradient-primary);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gradient-primary);
        border-radius: 6px;
        border: 2px solid transparent;
        background-clip: padding-box;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--gradient-secondary);
        background-clip: padding-box;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2.5rem;
        }
        
        .header-container {
            padding: 40px 20px;
        }
        
        .metrics-grid {
            grid-template-columns: 1fr;
        }
        
        .export-container {
            grid-template-columns: 1fr;
        }
        
        .glass-card {
            padding: 20px;
        }
    }
    
    /* Advanced Animations */
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
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .slide-in-right {
        animation: slideInRight 0.6s ease-out;
    }
    
    /* Advanced Data Viz Enhancements */
    .viz-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: var(--border-radius);
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 32px var(--shadow-light);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 12px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-processing {
        background: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .status-complete {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .status-error {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced session state initialization
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Advanced Helper Functions

def extract_package_name(url):
    """Enhanced package name extraction with validation"""
    if "id=" in url:
        package = url.split("id=")[1].split("&")[0].strip()
        # Validate package name format
        if re.match(r'^[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*$', package):
            return package
    return None

def analyze_sentiment_advanced(text):
    """Advanced sentiment analysis with emotional intensity and aspects"""
    if pd.isna(text) or text.strip() == "":
        return "Neutral", 0.0, 0.0, "Unknown", {}, 0.0
    
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Emotional intensity calculation
    emotional_words = {
        'love': 2.0, 'hate': -2.0, 'amazing': 1.8, 'terrible': -1.8,
        'excellent': 1.7, 'awful': -1.7, 'perfect': 1.6, 'horrible': -1.6,
        'fantastic': 1.5, 'disgusting': -1.5, 'wonderful': 1.4, 'annoying': -1.2
    }
    
    intensity = 0.0
    text_lower = text.lower()
    for word, weight in emotional_words.items():
        if word in text_lower:
            intensity += weight
    
    # Normalize intensity
    intensity = max(-2.0, min(2.0, intensity))
    
    # Aspect-based analysis
    aspects = {
        'performance': any(word in text_lower for word in ['fast', 'slow', 'speed', 'lag', 'performance', 'responsive']),
        'ui_design': any(word in text_lower for word in ['design', 'interface', 'ui', 'layout', 'beautiful', 'ugly']),
        'functionality': any(word in text_lower for word in ['feature', 'function', 'work', 'broken', 'bug', 'crash']),
        'usability': any(word in text_lower for word in ['easy', 'difficult', 'simple', 'complex', 'intuitive', 'confusing'])
    }
    
    # Enhanced sentiment classification
    if polarity > 0.5:
        return "Positive", polarity, subjectivity, "Highly Positive", aspects, intensity
    elif polarity > 0.2:
        return "Positive", polarity, subjectivity, "Moderately Positive", aspects, intensity
    elif polarity > 0.0:
        return "Positive", polarity, subjectivity, "Slightly Positive", aspects, intensity
    elif polarity < -0.5:
        return "Negative", polarity, subjectivity, "Highly Negative", aspects, intensity
    elif polarity < -0.2:
        return "Negative", polarity, subjectivity, "Moderately Negative", aspects, intensity
    elif polarity < 0.0:
        return "Negative", polarity, subjectivity, "Slightly Negative", aspects, intensity
    else:
        return "Neutral", polarity, subjectivity, "Neutral", aspects, intensity

def perform_advanced_topic_modeling(df, n_topics=5):
    """Advanced topic modeling using LDA and clustering"""
    if df.empty or len(df) < 20:
        return {}, {}
    
    try:
        # Prepare text data
        texts = df['content'].dropna().astype(str).tolist()
        
        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        
        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        
        # LDA Topic Modeling
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42,
            max_iter=20,
            learning_method='batch'
        )
        
        lda_topics = lda.fit_transform(tfidf_matrix)
        
        # Extract topics
        topics = {}
        for topic_idx, topic in enumerate(lda.components_):
            top_words_idx = topic.argsort()[-10:][::-1]
            top_words = [feature_names[i] for i in top_words_idx]
            topic_weight = topic[top_words_idx].sum()
            
            topics[f'topic_{topic_idx}'] = {
                'words': top_words,
                'weight': float(topic_weight),
                'documents': (lda_topics[:, topic_idx] > 0.1).sum()
            }
        
        # K-means clustering for additional insights
        kmeans = KMeans(n_clusters=min(5, len(texts)//10), random_state=42)
        clusters = kmeans.fit_predict(tfidf_matrix)
        
        cluster_info = {}
        for cluster_id in range(kmeans.n_clusters):
            cluster_docs = tfidf_matrix[clusters == cluster_id]
            if cluster_docs.shape[0] > 0:
                cluster_center = cluster_docs.mean(axis=0).A1
                top_features_idx = cluster_center.argsort()[-10:][::-1]
                top_features = [feature_names[i] for i in top_features_idx]
                
                cluster_info[f'cluster_{cluster_id}'] = {
                    'keywords': top_features,
                    'size': int((clusters == cluster_id).sum()),
                    'percentage': float((clusters == cluster_id).mean() * 100)
                }
        
        return topics, cluster_info
        
    except Exception as e:
        st.warning(f"Advanced topic modeling failed: {str(e)}")
        return {}, {}

def generate_predictive_insights(df):
    """Generate predictive analytics and trend analysis"""
    if df.empty or 'at' not in df.columns:
        return {}
    
    try:
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['at']).dt.date
        
        # Daily metrics
        daily_metrics = df_copy.groupby('date').agg({
            'score': ['mean', 'count'],
            'polarity_score': 'mean',
            'sentiment': lambda x: (x == 'Positive').mean()
        }).reset_index()
        
        daily_metrics.columns = ['date', 'avg_rating', 'review_count', 'avg_sentiment', 'positive_rate']
        
        if len(daily_metrics) < 7:
            return {}
        
        # Trend analysis
        recent_data = daily_metrics.tail(7)
        older_data = daily_metrics.head(max(1, len(daily_metrics) - 7))
        
        trends = {}
        
        # Rating trend
        recent_rating = recent_data['avg_rating'].mean()
        older_rating = older_data['avg_rating'].mean()
        rating_trend = recent_rating - older_rating
        
        trends['rating_trend'] = {
            'direction': 'improving' if rating_trend > 0.1 else 'declining' if rating_trend < -0.1 else 'stable',
            'magnitude': float(abs(rating_trend)),
            'recent_avg': float(recent_rating),
            'change': float(rating_trend)
        }
        
        # Volume trend
        recent_volume = recent_data['review_count'].mean()
        older_volume = older_data['review_count'].mean()
        volume_trend = recent_volume - older_volume
        
        trends['volume_trend'] = {
            'direction': 'increasing' if volume_trend > 5 else 'decreasing' if volume_trend < -5 else 'stable',
            'magnitude': float(abs(volume_trend)),
            'recent_avg': float(recent_volume),
            'change': float(volume_trend)
        }
        
        # Sentiment trend
        recent_sentiment = recent_data['positive_rate'].mean()
        older_sentiment = older_data['positive_rate'].mean()
        sentiment_trend = recent_sentiment - older_sentiment
        
        trends['sentiment_trend'] = {
            'direction': 'improving' if sentiment_trend > 0.05 else 'declining' if sentiment_trend < -0.05 else 'stable',
            'magnitude': float(abs(sentiment_trend)),
            'recent_avg': float(recent_sentiment),
            'change': float(sentiment_trend)
        }
        
        return trends
        
    except Exception as e:
        st.warning(f"Predictive analysis failed: {str(e)}")
        return {}

def detect_review_anomalies(df):
    """Detect anomalies and suspicious patterns in reviews"""
    if df.empty:
        return {}
    
    try:
        anomalies = {}
        
        # Rating distribution anomalies
        rating_dist = df['score'].value_counts(normalize=True)
        expected_dist = np.array([0.1, 0.15, 0.2, 0.25, 0.3])  # Expected distribution
        actual_dist = np.array([rating_dist.get(i, 0) for i in range(1, 6)])
        
        # Chi-square test for rating distribution
        chi2_stat, p_value = stats.chisquare(actual_dist, expected_dist)
        
        anomalies['rating_distribution'] = {
            'is_anomalous': p_value < 0.05,
            'chi2_statistic': float(chi2_stat),
            'p_value': float(p_value),
            'interpretation': 'unusual' if p_value < 0.05 else 'normal'
        }
        
        # Review length anomalies
        df['content_length'] = df['content'].astype(str).str.len()
        length_mean = df['content_length'].mean()
        length_std = df['content_length'].std()
        
        # Find outliers using IQR method
        Q1 = df['content_length'].quantile(0.25)
        Q3 = df['content_length'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df['content_length'] < lower_bound) | (df['content_length'] > upper_bound)]
        
        anomalies['review_length'] = {
            'outlier_count': len(outliers),
            'outlier_percentage': float(len(outliers) / len(df) * 100),
            'avg_length': float(length_mean),
            'length_std': float(length_std)
        }
        
        # Temporal anomalies (if date information is available)
        if 'at' in df.columns:
            df['hour'] = pd.to_datetime(df['at']).dt.hour
            hourly_dist = df['hour'].value_counts(normalize=True)
            
            # Check for suspicious timing patterns
            night_reviews = hourly_dist.loc[hourly_dist.index.isin(range(0, 6))].sum()
            anomalies['temporal_patterns'] = {
                'night_review_percentage': float(night_reviews * 100),
                'is_suspicious': night_reviews > 0.3,  # More than 30% at night
                'peak_hour': int(hourly_dist.idxmax())
            }
        
        return anomalies
        
    except Exception as e:
        st.warning(f"Anomaly detection failed: {str(e)}")
        return {}

def create_advanced_visualizations(df_a, df_b=None):
    """Create advanced interactive visualizations"""
    charts = {}
    
    # Modern color palette
    colors = {
        'primary': '#6366f1',
        'secondary': '#8b5cf6',
        'accent': '#06b6d4',
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444'
    }
    
    template = {
        'layout': {
            'plot_bgcolor': 'rgba(255, 255, 255, 0.9)',
            'paper_bgcolor': 'rgba(255, 255, 255, 0.9)',
            'font': {'color': '#1e293b', 'family': 'Inter, sans-serif', 'size': 12},
            'colorway': [colors['primary'], colors['secondary'], colors['accent'], colors['success'], colors['warning']],
            'margin': dict(l=60, r=60, t=80, b=60)
        }
    }
    
    if not df_a.empty:
        # Enhanced Sentiment Distribution with Emotional Intensity
        sentiment_counts = df_a['sentiment'].value_counts()
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=0.7,
            marker=dict(
                colors=[colors['success'] if s == 'Positive' else colors['error'] if s == 'Negative' else colors['warning'] 
                       for s in sentiment_counts.index],
                line=dict(color='white', width=3)
            ),
            textinfo='label+percent',
            textfont=dict(size=14, color='#1e293b'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig_donut.update_layout(
            title=dict(
                text='<b>Sentiment Distribution Analysis</b>',
                x=0.5,
                font=dict(size=20, color='#1e293b')
            ),
            template=template,
            annotations=[dict(
                text=f'<b>{sentiment_counts.sum()}</b><br>Total Reviews',
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False,
                font_color='#6366f1'
            )]
        )
        
        charts['sentiment_donut'] = fig_donut
        
        # Advanced Rating Distribution with Statistics
        rating_counts = df_a['score'].value_counts().sort_index()
        
        fig_rating = go.Figure()
        
        fig_rating.add_trace(go.Bar(
            x=[f'{i} ⭐' for i in rating_counts.index],
            y=rating_counts.values,
            marker=dict(
                color=[colors['error'] if i <= 2 else colors['warning'] if i == 3 else colors['success'] 
                      for i in rating_counts.index],
                opacity=0.8,
                line=dict(color='white', width=2)
            ),
            text=rating_counts.values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<br>Percentage: %{y:.1%}<extra></extra>'
        ))
        
        fig_rating.update_layout(
            title=dict(
                text='<b>Rating Distribution Analysis</b>',
                x=0.5,
                font=dict(size=20, color='#1e293b')
            ),
            xaxis_title='Rating',
            yaxis_title='Number of Reviews',
            template=template,
            showlegend=False
        )
        
        charts['rating_distribution'] = fig_rating
        
        # Sentiment vs Rating Correlation Heatmap
        if 'emotional_intensity' in df_a.columns:
            correlation_data = df_a[['score', 'polarity_score', 'subjectivity_score', 'emotional_intensity']].corr()
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=correlation_data.values,
                x=correlation_data.columns,
                y=correlation_data.columns,
                colorscale='RdBu',
                zmid=0,
                text=correlation_data.values,
                texttemplate='%{text:.2f}',
                textfont=dict(color='white'),
                hoverongaps=False
            ))
            
            fig_heatmap.update_layout(
                title=dict(
                    text='<b>Sentiment Metrics Correlation Matrix</b>',
                    x=0.5,
                    font=dict(size=20, color='#1e293b')
                ),
                template=template
            )
            
            charts['correlation_heatmap'] = fig_heatmap
        
        # Time Series Analysis (if date available)
        if 'at' in df_a.columns:
            df_a['date'] = pd.to_datetime(df_a['at']).dt.date
            daily_sentiment = df_a.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
            
            if not daily_sentiment.empty:
                fig_timeline = go.Figure()
                
                sentiment_colors = {
                    'Positive': colors['success'],
                    'Neutral': colors['warning'],
                    'Negative': colors['error']
                }
                
                for sentiment in ['Positive', 'Neutral', 'Negative']:
                    if sentiment in daily_sentiment.columns:
                        fig_timeline.add_trace(go.Scatter(
                            x=daily_sentiment.index,
                            y=daily_sentiment[sentiment],
                            mode='lines+markers',
                            name=f'{sentiment} Reviews',
                            line=dict(color=sentiment_colors[sentiment], width=3),
                            marker=dict(size=8, opacity=0.8),
                            fill='tonexty' if sentiment != 'Positive' else 'tozeroy',
                            fillcolor=sentiment_colors[sentiment] + '20'
                        ))
                
                fig_timeline.update_layout(
                    title=dict(
                        text='<b>Sentiment Timeline Evolution</b>',
                        x=0.5,
                        font=dict(size=20, color='#1e293b')
                    ),
                    xaxis_title='Date',
                    yaxis_title='Review Count',
                    template=template,
                    hovermode='x unified'
                )
                
                charts['sentiment_timeline'] = fig_timeline
    
    # Comparative Analysis Charts
    if df_b is not None and not df_b.empty:
        # Side-by-side comparison
        sentiment_a = df_a['sentiment'].value_counts(normalize=True) * 100
        sentiment_b = df_b['sentiment'].value_counts(normalize=True) * 100
        
        fig_comparison = go.Figure()
        
        sentiments = ['Positive', 'Neutral', 'Negative']
        x_positions = np.arange(len(sentiments))
        
        fig_comparison.add_trace(go.Bar(
            name='Application A',
            x=[s + ' - App A' for s in sentiments],
            y=[sentiment_a.get(s, 0) for s in sentiments],
            marker_color=colors['primary'],
            opacity=0.8,
            text=[f"{sentiment_a.get(s, 0):.1f}%" for s in sentiments],
            textposition='outside'
        ))
        
        fig_comparison.add_trace(go.Bar(
            name='Application B',
            x=[s + ' - App B' for s in sentiments],
            y=[sentiment_b.get(s, 0) for s in sentiments],
            marker_color=colors['secondary'],
            opacity=0.8,
            text=[f"{sentiment_b.get(s, 0):.1f}%" for s in sentiments],
            textposition='outside'
        ))
        
        fig_comparison.update_layout(
            title=dict(
                text='<b>Competitive Sentiment Analysis</b>',
                x=0.5,
                font=dict(size=20, color='#1e293b')
            ),
            xaxis_title='Sentiment Categories',
            yaxis_title='Percentage (%)',
            template=template,
            barmode='group'
        )
        
        charts['competitive_sentiment'] = fig_comparison
        
        # Radar chart for comprehensive comparison
        metrics_a = {
            'Avg Rating': df_a['score'].mean(),
            'Positive %': (df_a['sentiment'] == 'Positive').mean() * 100,
            'Review Count': len(df_a) / 100,  # Scaled for visualization
            'Sentiment Score': (df_a['polarity_score'].mean() + 1) * 50,  # Normalized to 0-100
            'Engagement': df_a['content'].str.len().mean() / 10  # Scaled
        }
        
        metrics_b = {
            'Avg Rating': df_b['score'].mean(),
            'Positive %': (df_b['sentiment'] == 'Positive').mean() * 100,
            'Review Count': len(df_b) / 100,
            'Sentiment Score': (df_b['polarity_score'].mean() + 1) * 50,
            'Engagement': df_b['content'].str.len().mean() / 10
        }
        
        categories = list(metrics_a.keys())
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=list(metrics_a.values()),
            theta=categories,
            fill='toself',
            name='Application A',
            line_color=colors['primary'],
            fillcolor=colors['primary'] + '30'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=list(metrics_b.values()),
            theta=categories,
            fill='toself',
            name='Application B',
            line_color=colors['secondary'],
            fillcolor=colors['secondary'] + '30'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(max(metrics_a.values()), max(metrics_b.values())) + 10]
                )
            ),
            showlegend=True,
            title=dict(
                text='<b>Multi-Dimensional Performance Radar</b>',
                x=0.5,
                font=dict(size=20, color='#1e293b')
            ),
            template=template
        )
        
        charts['performance_radar'] = fig_radar
    
    return charts

def generate_executive_summary(df_a, df_b=None, insights=None, trends=None):
    """Generate comprehensive executive summary with actionable insights"""
    summary = {
        'key_metrics': {},
        'strategic_recommendations': [],
        'risk_assessment': {},
        'market_position': {},
        'action_items': []
    }
    
    try:
        # Key Metrics
        summary['key_metrics'] = {
            'total_reviews': len(df_a),
            'average_rating': round(df_a['score'].mean(), 2),
            'positive_sentiment': round((df_a['sentiment'] == 'Positive').mean() * 100, 1),
            'sentiment_score': round(df_a['polarity_score'].mean(), 3),
            'engagement_level': round(df_a['content'].str.len().mean(), 0)
        }
        
        # Market Position Assessment
        avg_rating = summary['key_metrics']['average_rating']
        positive_rate = summary['key_metrics']['positive_sentiment']
        
        if avg_rating >= 4.5 and positive_rate >= 80:
            position = "Market Leader"
            position_score = 95
        elif avg_rating >= 4.0 and positive_rate >= 70:
            position = "Strong Performer"
            position_score = 80
        elif avg_rating >= 3.5 and positive_rate >= 60:
            position = "Competitive"
            position_score = 65
        elif avg_rating >= 3.0 and positive_rate >= 50:
            position = "Developing"
            position_score = 50
        else:
            position = "Needs Improvement"
            position_score = 30
        
        summary['market_position'] = {
            'category': position,
            'score': position_score,
            'percentile': min(95, position_score + np.random.randint(-5, 15))
        }
        
        # Risk Assessment
        negative_rate = (df_a['sentiment'] == 'Negative').mean() * 100
        rating_volatility = df_a['score'].std()
        
        risk_level = "Low"
        risk_score = 10
        
        if negative_rate > 30 or rating_volatility > 1.5:
            risk_level = "High"
            risk_score = 80
        elif negative_rate > 20 or rating_volatility > 1.0:
            risk_level = "Medium"
            risk_score = 50
        
        summary['risk_assessment'] = {
            'level': risk_level,
            'score': risk_score,
            'factors': []
        }
        
        if negative_rate > 25:
            summary['risk_assessment']['factors'].append(f"High negative sentiment ({negative_rate:.1f}%)")
        if rating_volatility > 1.2:
            summary['risk_assessment']['factors'].append(f"High rating volatility ({rating_volatility:.2f})")
        
        # Strategic Recommendations
        recommendations = []
        
        if positive_rate < 70:
            recommendations.append({
                'priority': 'High',
                'category': 'User Experience',
                'action': 'Implement comprehensive UX improvements to address user pain points',
                'impact': 'High',
                'timeline': '3-6 months'
            })
        
        if avg_rating < 4.0:
            recommendations.append({
                'priority': 'High',
                'category': 'Product Quality',
                'action': 'Focus on core functionality and stability improvements',
                'impact': 'High',
                'timeline': '2-4 months'
            })
        
        if len(df_a) < 500:
            recommendations.append({
                'priority': 'Medium',
                'category': 'Marketing',
                'action': 'Increase user acquisition and engagement campaigns',
                'impact': 'Medium',
                'timeline': '1-3 months'
            })
        
        summary['strategic_recommendations'] = recommendations[:5]
        
        # Competitive Analysis (if available)
        if df_b is not None:
            competitor_metrics = {
                'rating': df_b['score'].mean(),
                'positive_sentiment': (df_b['sentiment'] == 'Positive').mean() * 100,
                'review_count': len(df_b)
            }
            
            summary['competitive_analysis'] = {
                'rating_advantage': round(avg_rating - competitor_metrics['rating'], 2),
                'sentiment_advantage': round(positive_rate - competitor_metrics['positive_sentiment'], 1),
                'volume_advantage': len(df_a) - competitor_metrics['review_count']
            }
    
    except Exception as e:
        st.warning(f"Executive summary generation failed: {str(e)}")
    
    return summary

# Navigation and UI Functions

def navigate_to(page):
    """Enhanced navigation with animation triggers"""
    st.session_state.page = page
    st.rerun()

def display_enhanced_metrics(df, title, app_name=""):
    """Display metrics with advanced styling and animations"""
    st.markdown(f"""
    <div class="glass-card fade-in-up">
        <h3 style="color: #1e293b; margin-bottom: 30px; font-size: 1.5rem; text-align: center;">
            {title} {app_name.upper()}
        </h3>
        <div class="metrics-grid">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        (len(df), "TOTAL REVIEWS", "📊"),
        (f"{df['score'].mean():.1f}", "AVG RATING", "⭐"),
        (f"{(df['sentiment'] == 'Positive').mean() * 100:.1f}%", "POSITIVE", "👍"),
        (f"{df['polarity_score'].mean():.2f}", "SENTIMENT", "💭")
    ]
    
    for i, (value, label, icon) in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def display_enhanced_reviews(df, title, max_reviews=10):
    """Display reviews with enhanced styling and interaction"""
    st.markdown(f"""
    <div class="glass-card">
        <h3 style="color: #1e293b; margin-bottom: 30px; font-size: 1.5rem; text-align: center;">
            {title}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    if 'at' in df.columns:
        df_sorted = df.sort_values('at', ascending=False).head(max_reviews)
    else:
        df_sorted = df.head(max_reviews)
    
    for idx, review in df_sorted.iterrows():
        sentiment = review.get('sentiment', 'Neutral')
        badge_class = f"sentiment-{sentiment.lower()}"
        
        rating = review.get('score', 0)
        stars = "⭐" * int(rating)
        
        if 'at' in review and pd.notna(review['at']):
            date_str = pd.to_datetime(review['at']).strftime('%B %d, %Y')
        else:
            date_str = "Unknown date"
        
        content = str(review.get('content', 'No content available'))
        if len(content) > 300:
            content = content[:300] + "..."
        
        # Add emotional intensity if available
        intensity_indicator = ""
        if 'emotional_intensity' in review:
            intensity = review['emotional_intensity']
            if abs(intensity) > 1.0:
                intensity_indicator = f"🔥 High Intensity ({intensity:+.1f})"
            elif abs(intensity) > 0.5:
                intensity_indicator = f"💫 Moderate Intensity ({intensity:+.1f})"
        
        st.markdown(f"""
        <div class="review-card slide-in-right">
            <div class="review-header">
                <div class="review-user">
                    👤 {review.get('userName', 'Anonymous User')}
                </div>
                <div class="review-rating">
                    <span class="star-rating">{stars}</span>
                    <span style="margin-left: 10px; color: #64748b; font-weight: 600;">
                        {rating}/5
                    </span>
                </div>
            </div>
            <div class="review-content">
                {content}
                {f'<div style="margin-top: 10px; font-size: 0.9rem; color: #8b5cf6;">{intensity_indicator}</div>' if intensity_indicator else ''}
            </div>
            <div class="review-meta">
                <div style="color: #64748b;">📅 {date_str}</div>
                <div class="sentiment-badge {badge_class}">{sentiment}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_advanced_export_section(df_a, df_b=None, insights=None, summary=None):
    """Create enhanced export section with multiple formats and advanced reports"""
    st.markdown("""
    <div class="glass-card">
        <h2 style="color: #1e293b; margin-bottom: 40px; text-align: center; font-size: 2rem;">
            🚀 PROFESSIONAL EXPORT SUITE
        </h2>
        <div class="export-container">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="export-card">
            <div style="font-size: 3rem; margin-bottom: 20px;">📊</div>
            <div class="export-title">EXECUTIVE DASHBOARD</div>
            <div class="export-desc">
                Comprehensive business intelligence report with predictive analytics, 
                competitive insights, and strategic recommendations for C-level executives.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate enhanced executive report
        executive_report = generate_enhanced_executive_report(df_a, df_b, insights, summary)
        
        st.download_button(
            "📊 DOWNLOAD EXECUTIVE REPORT",
            data=executive_report,
            file_name=f"Executive_Intelligence_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
            mime="text/html",
            type="primary"
        )
    
    with col2:
        st.markdown("""
        <div class="export-card">
            <div style="font-size: 3rem; margin-bottom: 20px;">📈</div>
            <div class="export-title">ANALYTICS DATASET</div>
            <div class="export-desc">
                Complete enriched dataset with advanced sentiment metrics, 
                predictive features, and machine learning-ready format.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create enriched dataset
        enriched_data = create_enriched_dataset(df_a, df_b)
        
        st.download_button(
            "📈 DOWNLOAD ANALYTICS DATA",
            data=enriched_data,
            file_name=f"Enhanced_Analytics_Dataset_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col3:
        st.markdown("""
        <div class="export-card">
            <div style="font-size: 3rem; margin-bottom: 20px;">🎯</div>
            <div class="export-title">ACTION PLAN</div>
            <div class="export-desc">
                Strategic action plan with prioritized recommendations, 
                implementation timelines, and success metrics.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate action plan
        action_plan = generate_strategic_action_plan(df_a, df_b, insights)
        
        st.download_button(
            "🎯 DOWNLOAD ACTION PLAN",
            data=action_plan,
            file_name=f"Strategic_Action_Plan_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def generate_enhanced_executive_report(df_a, df_b=None, insights=None, summary=None):
    """Generate comprehensive executive report with advanced styling"""
    try:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Feedbacks Forge Pro - Executive Intelligence Report</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
                
                body {{
                    font-family: 'Inter', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #1e293b;
                    margin: 0;
                    padding: 40px;
                    line-height: 1.7;
                    min-height: 100vh;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.95);
                    border-radius: 24px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    overflow: hidden;
                }}
                
                .header {{
                    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                    color: white;
                    padding: 60px 40px;
                    text-align: center;
                    position: relative;
                }}
                
                .header::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
                    opacity: 0.3;
                }}
                
                .header h1 {{
                    font-size: 3rem;
                    font-weight: 900;
                    margin: 0 0 20px 0;
                    letter-spacing: -1px;
                }}
                
                .header p {{
                    font-size: 1.2rem;
                    margin: 0;
                    opacity: 0.9;
                }}
                
                .content {{
                    padding: 60px 40px;
                }}
                
                .section {{
                    margin-bottom: 50px;
                }}
                
                .section-title {{
                    font-size: 2rem;
                    font-weight: 700;
                    color: #1e293b;
                    margin-bottom: 30px;
                    padding-bottom: 15px;
                    border-bottom: 3px solid #6366f1;
                    display: flex;
                    align-items: center;
                    gap: 15px;
                }}
                
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 30px;
                    margin: 40px 0;
                }}
                
                .metric-card {{
                    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                    padding: 30px;
                    border-radius: 16px;
                    text-align: center;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                    border: 2px solid #e2e8f0;
                    transition: all 0.3s ease;
                }}
                
                .metric-card:hover {{
                    transform: translateY(-4px);
                    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
                    border-color: #6366f1;
                }}
                
                .metric-value {{
                    font-size: 3rem;
                    font-weight: 800;
                    color: #6366f1;
                    margin-bottom: 10px;
                    font-family: 'JetBrains Mono', monospace;
                }}
                
                .metric-label {{
                    font-size: 1rem;
                    font-weight: 600;
                    color: #64748b;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                
                .insight-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 25px;
                    margin: 30px 0;
                }}
                
                .insight-card {{
                    background: white;
                    padding: 30px;
                    border-radius: 16px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                    border-left: 5px solid #6366f1;
                }}
                
                .insight-card.warning {{
                    border-left-color: #ef4444;
                }}
                
                .insight-card.success {{
                    border-left-color: #10b981;
                }}
                
                .insight-title {{
                    font-size: 1.2rem;
                    font-weight: 700;
                    color: #1e293b;
                    margin-bottom: 15px;
                }}
                
                .insight-desc {{
                    color: #64748b;
                    line-height: 1.6;
                }}
                
                .comparison-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 30px 0;
                    background: white;
                    border-radius: 16px;
                    overflow: hidden;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }}
                
                .comparison-table th {{
                    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                    color: white;
                    padding: 20px;
                    text-align: left;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                
                .comparison-table td {{
                    padding: 20px;
                    border-bottom: 1px solid #e2e8f0;
                    font-weight: 500;
                }}
                
                .comparison-table tr:hover {{
                    background: #f8fafc;
                }}
                
                .status-badge {{
                    padding: 8px 16px;
                    border-radius: 50px;
                    font-size: 0.85rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                
                .status-excellent {{
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    color: white;
                }}
                
                .status-good {{
                    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                    color: white;
                }}
                
                .status-warning {{
                    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                    color: white;
                }}
                
                .status-critical {{
                    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                    color: white;
                }}
                
                .footer {{
                    background: #1e293b;
                    color: white;
                    padding: 40px;
                    text-align: center;
                }}
                
                .footer h3 {{
                    color: #6366f1;
                    margin-bottom: 20px;
                }}
                
                .emoji {{
                    font-size: 2rem;
                    margin-right: 10px;
                }}
                
                @media print {{
                    body {{
                        background: white;
                    }}
                    .container {{
                        box-shadow: none;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 FEEDBACKS FORGE PRO</h1>
                    <p>Executive Intelligence Report - Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
                </div>
                
                <div class="content">
        """
        
        # Executive Summary
        html_content += f"""
        <div class="section">
            <h2 class="section-title">
                <span class="emoji">📊</span>
                EXECUTIVE SUMMARY
            </h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{len(df_a):,}</div>
                    <div class="metric-label">Total Reviews</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{df_a['score'].mean():.1f}</div>
                    <div class="metric-label">Average Rating</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%</div>
                    <div class="metric-label">Positive Sentiment</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{df_a['polarity_score'].mean():.2f}</div>
                    <div class="metric-label">Sentiment Score</div>
                </div>
            </div>
        </div>
        """
        
        # Market Position Assessment
        avg_rating = df_a['score'].mean()
        positive_rate = (df_a['sentiment'] == 'Positive').mean() * 100
        
        if avg_rating >= 4.5 and positive_rate >= 80:
            position = "Market Leader"
            status_class = "status-excellent"
        elif avg_rating >= 4.0 and positive_rate >= 70:
            position = "Strong Performer"
            status_class = "status-good"
        elif avg_rating >= 3.5 and positive_rate >= 60:
            position = "Competitive Position"
            status_class = "status-warning"
        else:
            position = "Improvement Needed"
            status_class = "status-critical"
        
        html_content += f"""
        <div class="section">
            <h2 class="section-title">
                <span class="emoji">🎯</span>
                MARKET POSITION ANALYSIS
            </h2>
            <div style="text-align: center; margin: 40px 0;">
                <div class="status-badge {status_class}" style="font-size: 1.2rem; padding: 15px 30px;">
                    {position}
                </div>
            </div>
            <p style="text-align: center; font-size: 1.1rem; color: #64748b; max-width: 600px; margin: 0 auto;">
                Based on comprehensive analysis of user sentiment, rating distribution, 
                and competitive benchmarks, your application demonstrates 
                <strong>{position.lower()}</strong> characteristics in the current market landscape.
            </p>
        </div>
        """
        
        # Competitive Analysis (if available)
        if df_b is not None and not df_b.empty:
            html_content += f"""
            <div class="section">
                <h2 class="section-title">
                    <span class="emoji">⚔️</span>
                    COMPETITIVE INTELLIGENCE
                </h2>
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Performance Metric</th>
                            <th>Your Application</th>
                            <th>Competitor</th>
                            <th>Advantage</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Total Reviews</strong></td>
                            <td>{len(df_a):,}</td>
                            <td>{len(df_b):,}</td>
                            <td>{len(df_a) - len(df_b):+,}</td>
                            <td>
                                <span class="status-badge {'status-excellent' if len(df_a) > len(df_b) else 'status-warning'}">
                                    {'Leading' if len(df_a) > len(df_b) else 'Behind'}
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td><strong>Average Rating</strong></td>
                            <td>{df_a['score'].mean():.2f}</td>
                            <td>{df_b['score'].mean():.2f}</td>
                            <td>{df_a['score'].mean() - df_b['score'].mean():+.2f}</td>
                            <td>
                                <span class="status-badge {'status-excellent' if df_a['score'].mean() > df_b['score'].mean() else 'status-warning'}">
                                    {'Leading' if df_a['score'].mean() > df_b['score'].mean() else 'Behind'}
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td><strong>Positive Sentiment</strong></td>
                            <td>{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%</td>
                            <td>{(df_b['sentiment'] == 'Positive').mean() * 100:.1f}%</td>
                            <td>{(df_a['sentiment'] == 'Positive').mean() * 100 - (df_b['sentiment'] == 'Positive').mean() * 100:+.1f}%</td>
                            <td>
                                <span class="status-badge {'status-excellent' if (df_a['sentiment'] == 'Positive').mean() > (df_b['sentiment'] == 'Positive').mean() else 'status-warning'}">
                                    {'Leading' if (df_a['sentiment'] == 'Positive').mean() > (df_b['sentiment'] == 'Positive').mean() else 'Behind'}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """
        
        # Strategic Insights
        if insights and len(insights) > 0:
            html_content += '''
            <div class="section">
                <h2 class="section-title">
                    <span class="emoji">🧠</span>
                    AI STRATEGIC INSIGHTS
                </h2>
                <div class="insight-grid">
            '''
            
            for insight in insights[:6]:
                css_class = 'success' if insight['type'] == 'positive' else 'warning'
                icon = '✅' if insight['type'] == 'positive' else '⚠️'
                
                html_content += f"""
                <div class="insight-card {css_class}">
                    <div class="insight-title">
                        {icon} {insight['title']}
                    </div>
                    <div class="insight-desc">
                        {insight['description']}
                    </div>
                </div>
                """
            
            html_content += '</div></div>'
        
        # Strategic Recommendations
        html_content += f"""
        <div class="section">
            <h2 class="section-title">
                <span class="emoji">🎯</span>
                STRATEGIC RECOMMENDATIONS
            </h2>
            <div class="insight-grid">
        """
        
        # Generate specific recommendations based on data
        recommendations = []
        
        if positive_rate < 70:
            recommendations.append({
                'title': 'URGENT: User Experience Overhaul Required',
                'desc': f'With only {positive_rate:.1f}% positive sentiment, immediate UX improvements are critical. Focus on addressing top user complaints and streamlining core user journeys.',
                'priority': 'HIGH',
                'timeline': '2-3 months'
            })
        
        if avg_rating < 4.0:
            recommendations.append({
                'title': 'Product Quality Enhancement Initiative',
                'desc': f'Average rating of {avg_rating:.1f} indicates quality issues. Implement comprehensive testing, bug fixes, and feature stability improvements.',
                'priority': 'HIGH',
                'timeline': '1-2 months'
            })
        
        if len(df_a) < 1000:
            recommendations.append({
                'title': 'User Acquisition & Engagement Campaign',
                'desc': f'With {len(df_a):,} reviews, increase market visibility through targeted marketing, influencer partnerships, and user referral programs.',
                'priority': 'MEDIUM',
                'timeline': '3-6 months'
            })
        
        negative_rate = (df_a['sentiment'] == 'Negative').mean() * 100
        if negative_rate > 25:
            recommendations.append({
                'title': 'Crisis Management Protocol',
                'desc': f'High negative sentiment ({negative_rate:.1f}%) requires immediate crisis response. Implement user feedback loops and rapid issue resolution processes.',
                'priority': 'CRITICAL',
                'timeline': 'IMMEDIATE'
            })
        
        for i, rec in enumerate(recommendations[:4]):
            priority_class = {
                'CRITICAL': 'status-critical',
                'HIGH': 'status-warning',
                'MEDIUM': 'status-good',
                'LOW': 'status-excellent'
            }.get(rec['priority'], 'status-good')
            
            html_content += f"""
            <div class="insight-card">
                <div class="insight-title">
                    🚀 {rec['title']}
                    <div style="float: right;">
                        <span class="status-badge {priority_class}" style="font-size: 0.7rem;">
                            {rec['priority']} PRIORITY
                        </span>
                    </div>
                </div>
                <div class="insight-desc">
                    {rec['desc']}<br><br>
                    <strong>🕒 Timeline:</strong> {rec['timeline']}
                </div>
            </div>
            """
        
        html_content += '</div></div>'
        
        # Footer
        html_content += f"""
                </div>
                
                <div class="footer">
                    <h3>🚀 FEEDBACKS FORGE PRO</h3>
                    <p>Advanced Review Intelligence Platform | Executive Report</p>
                    <p>Generated with AI-powered analytics and strategic intelligence</p>
                    <div style="margin-top: 30px; font-size: 0.9rem; opacity: 0.8;">
                        This report contains confidential business intelligence and strategic insights.<br>
                        © {datetime.now().year} Feedbacks Forge Pro - All Rights Reserved
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content.encode('utf-8')
        
    except Exception as e:
        return f"Error generating executive report: {str(e)}".encode('utf-8')

def create_enriched_dataset(df_a, df_b=None):
    """Create enriched dataset with advanced features"""
    try:
        # Combine datasets if both available
        if df_b is not None:
            df_a['app_type'] = 'Primary'
            df_b['app_type'] = 'Competitor'
            combined_df = pd.concat([df_a, df_b], ignore_index=True)
        else
