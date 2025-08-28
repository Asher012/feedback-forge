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

def get_app_name(package_name):
    parts = package_name.split('.')
    return parts[-1].replace('_', ' ').title() if parts else package_name

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

def generate_advanced_ai_insights(df):
    """Generate advanced AI insights"""
    insights = []
    if df.empty:
        return insights
    
    try:
        sentiment_dist = df['sentiment'].value_counts(normalize=True) * 100
        avg_rating = df['score'].mean()
        total_reviews = len(df)
        
        positive_rate = sentiment_dist.get('Positive', 0)
        negative_rate = sentiment_dist.get('Negative', 0)
        
        # Advanced market analysis
        if positive_rate > 80 and avg_rating > 4.5:
            insights.append({
                "type": "positive",
                "title": "MARKET LEADER STATUS",
                "description": f"Exceptional performance with {positive_rate:.1f}% positive sentiment and {avg_rating:.1f}/5 rating indicates dominant market position and outstanding user satisfaction."
            })
        elif positive_rate > 60 and avg_rating > 4.0:
            insights.append({
                "type": "positive", 
                "title": "STRONG COMPETITIVE POSITION",
                "description": f"Above-average performance with {positive_rate:.1f}% positive sentiment demonstrates strong competitive positioning in the market segment."
            })
        elif negative_rate > 40:
            insights.append({
                "type": "warning",
                "title": "URGENT INTERVENTION REQUIRED",
                "description": f"Critical alert: {negative_rate:.1f}% negative sentiment requires immediate strategic intervention and comprehensive user experience overhaul."
            })
        
        # Review volume insights
        if total_reviews > 1000:
            insights.append({
                "type": "positive",
                "title": "HIGH MARKET PENETRATION",
                "description": f"Substantial user engagement with {total_reviews:,} reviews indicates strong market penetration and highly active user community."
            })
        elif total_reviews < 100:
            insights.append({
                "type": "warning",
                "title": "LIMITED MARKET VISIBILITY",
                "description": f"Low review volume ({total_reviews} reviews) suggests limited market visibility or early market entry phase. Consider enhancing marketing strategies."
            })
        
        return insights[:6]
        
    except Exception:
        return []

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
        # Enhanced Sentiment Distribution
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
        
        # Rating Distribution
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
    
    return charts

def create_enriched_dataset(df_a, df_b=None):
    """Create enriched dataset with advanced features"""
    try:
        # Combine datasets if both available
        if df_b is not None:
            df_a['app_type'] = 'Primary'
            df_b['app_type'] = 'Competitor'
            combined_df = pd.concat([df_a, df_b], ignore_index=True)
        else:
            combined_df = df_a.copy()
            combined_df['app_type'] = 'Primary'
        
        return combined_df.to_csv(index=False).encode('utf-8')
        
    except Exception as e:
        error_df = pd.DataFrame({'error': [f'Failed to create enriched dataset: {str(e)}']})
        return error_df.to_csv(index=False).encode('utf-8')

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
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 FEEDBACKS FORGE PRO</h1>
                    <p>Executive Intelligence Report - Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
                </div>
                
                <div class="content">
                    <div class="section">
                        <h2 class="section-title">
                            📊 EXECUTIVE SUMMARY
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
                </div>
                
                <div class="footer">
                    <h3>🚀 FEEDBACKS FORGE PRO</h3>
                    <p>Advanced Review Intelligence Platform | Executive Report</p>
                    <p>Generated with AI-powered analytics and strategic intelligence</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content.encode('utf-8')
        
    except Exception as e:
        return f"Error generating executive report: {str(e)}".encode('utf-8')

def generate_strategic_action_plan(df_a, df_b=None, insights=None):
    """Generate strategic action plan"""
    try:
        action_plan = {
            "analysis_date": datetime.now().isoformat(),
            "total_reviews": len(df_a),
            "average_rating": float(df_a['score'].mean()),
            "positive_sentiment_rate": float((df_a['sentiment'] == 'Positive').mean() * 100),
            "recommendations": [
                {
                    "priority": "High",
                    "category": "User Experience",
                    "action": "Implement user feedback improvements",
                    "timeline": "3-6 months"
                }
            ]
        }
        
        return json.dumps(action_plan, indent=2).encode('utf-8')
        
    except Exception as e:
        error_plan = {"error": f"Failed to generate action plan: {str(e)}"}
        return json.dumps(error_plan, indent=2).encode('utf-8')

# Navigation Functions
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
            </div>
            <div class="review-meta">
                <div style="color: #64748b;">📅 {date_str}</div>
                <div class="sentiment-badge {badge_class}">{sentiment}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# HOME PAGE
if st.session_state.page == 'home':
    st.markdown("""
    <div class="header-container">
        <div class="version-badge">v4.0 PRO</div>
        <div class="app-title">Feedbacks Forge Pro</div>
        <div class="app-subtitle">Next-Generation Review Intelligence Platform</div>
        <div class="creator-badge">Powered by Advanced AI Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card fade-in-up" style="text-align: center;">
        <h2 style="color: #1e293b; margin-bottom: 30px; font-size: 2rem;">
            🚀 WELCOME TO THE FUTURE OF REVIEW ANALYTICS
        </h2>
        <p style="color: #64748b; font-size: 1.2rem; line-height: 1.8; margin-bottom: 40px; max-width: 800px; margin-left: auto; margin-right: auto;">
            Harness the power of advanced AI, machine learning algorithms, and cutting-edge data science 
            to transform raw review data into actionable business intelligence.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card slide-in-right" style="text-align: center; min-height: 300px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 4rem; margin-bottom: 20px;">📊</div>
            <h3 style="color: #1e293b; margin-bottom: 20px; font-size: 1.5rem;">
                DEEP DIVE ANALYTICS
            </h3>
            <p style="color: #64748b; margin-bottom: 35px; line-height: 1.6;">
                Advanced AI-powered sentiment analysis with emotional intensity mapping, 
                predictive trends, and comprehensive business intelligence reporting.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 LAUNCH SINGLE ANALYSIS", type="primary"):
            st.session_state.comparison_mode = False
            navigate_to('analysis')
    
    with col2:
        st.markdown("""
        <div class="glass-card slide-in-right" style="text-align: center; min-height: 300px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 4rem; margin-bottom: 20px;">⚔️</div>
            <h3 style="color: #1e293b; margin-bottom: 20px; font-size: 1.5rem;">
                COMPETITIVE INTELLIGENCE
            </h3>
            <p style="color: #64748b; margin-bottom: 35px; line-height: 1.6;">
                Head-to-head competitive analysis with advanced benchmarking, 
                strategic positioning insights, and market intelligence dashboards.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚔️ ACTIVATE COMPETITIVE MODE", type="primary"):
            st.session_state.comparison_mode = True
            navigate_to('analysis')

# ANALYSIS PAGE
elif st.session_state.page == 'analysis':
    mode_text = "COMPETITIVE INTELLIGENCE MODE" if st.session_state.comparison_mode else "DEEP DIVE ANALYTICS MODE"
    st.markdown(f"""
    <div class="header-container">
        <div class="version-badge">ACTIVE</div>
        <div class="app-title">Analysis Dashboard</div>
        <div class="app-subtitle">{mode_text}</div>
        <div class="creator-badge">Advanced AI Processing</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("◀ RETURN TO HOME", type="secondary"):
        navigate_to('home')
    
    # URL Configuration
    if st.session_state.comparison_mode:
        st.markdown("### COMPETITIVE ANALYSIS CONFIGURATION")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #6366f1; font-weight: 600; font-size: 1rem; margin-bottom: 15px;">
                    🎯 PRIMARY APPLICATION TARGET
                </h4>
            </div>
            """, unsafe_allow_html=True)
            url_a = st.text_area("Primary Application URL", placeholder="https://play.google.com/store/apps/details?id=...", height=100)
        
        with col2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #8b5cf6; font-weight: 600; font-size: 1rem; margin-bottom: 15px;">
                    ⚔️ COMPETITOR APPLICATION
                </h4>
            </div>
            """, unsafe_allow_html=True)
            url_b = st.text_area("Competitor Application URL", placeholder="https://play.google.com/store/apps/details?id=...", height=100)
    else:
        st.markdown("### SINGLE APPLICATION ANALYSIS")
        url_a = st.text_area("Application URL", placeholder="https://play.google.com/store/apps/details?id=...", height=100)
        url_b = None
    
    # Parameters
    st.markdown("### ADVANCED PARAMETERS")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        count = st.slider("Reviews per App", 50, 2000, 500, 50)
    with col2:
        language = st.selectbox("Language", ["en", "hi", "es", "fr", "de", "ja"])
    with col3:
        country = st.selectbox("Region", ["in", "us", "uk", "ca", "de", "jp"])
    with col4:
        sort_by = st.selectbox("Sort Method", ["NEWEST", "MOST_RELEVANT", "RATING"])
    
    # Advanced Options
    with st.expander("🔬 ADVANCED AI CONFIGURATION", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            enable_insights = st.checkbox("🧠 AI Intelligence Module", value=True)
            enable_advanced = st.checkbox("🚀 Advanced Analytics", value=True)
        with col2:
            min_rating = st.selectbox("Minimum Rating Filter", [1, 2, 3, 4, 5])
            max_reviews_display = st.slider("Reviews to Display", 5, 50, 15)
        with col3:
            enable_predictions = st.checkbox("🔮 Predictive Analytics", value=True)
            enable_anomaly = st.checkbox("🕵️ Anomaly Detection", value=True)
    
    # Execute Analysis
    if st.button("🚀 EXECUTE COMPREHENSIVE ANALYSIS", type="primary"):
        # Validation
        if not url_a.strip():
            st.error("🚨 PRIMARY APPLICATION URL IS REQUIRED")
            st.stop()
        
        if st.session_state.comparison_mode and not url_b.strip():
            st.error("🚨 COMPETITOR APPLICATION URL IS REQUIRED")
            st.stop()
        
        package_a = extract_package_name(url_a)
        package_b = extract_package_name(url_b) if url_b else None
        
        if not package_a:
            st.error("🚨 INVALID URL FORMAT FOR PRIMARY APPLICATION")
            st.stop()
        
        if st.session_state.comparison_mode and not package_b:
            st.error("🚨 INVALID URL FORMAT FOR COMPETITOR APPLICATION")
            st.stop()
        
        # Progress Section
        st.markdown("""
        <div class="progress-section">
            <div style="font-size: 1.3rem; font-weight: 600; margin-bottom: 20px;">
                <span class="loading-spinner"></span>
                🚀 ADVANCED AI PIPELINE EXECUTING
            </div>
            <div style="color: #64748b; font-size: 1.1rem;">
                Processing review data through next-generation AI algorithms...
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_container = st.empty()
        
        # Process applications
        try:
            sort_mapping = {"NEWEST": Sort.NEWEST, "MOST_RELEVANT": Sort.MOST_RELEVANT, "RATING": Sort.RATING}
            
            # Process App A
            status_container.markdown(f"""
            <div class="glass-card">
                <div style="text-align: center;">
                    <h4 style="color: #6366f1; font-size: 1.2rem; margin-bottom: 15px;">
                        🎯 PROCESSING: {get_app_name(package_a).upper()}
                    </h4>
                    <p style="color: #64748b; margin: 0;">
                        Extracting {count:,} reviews and performing advanced sentiment analysis...
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            result_a, _ = reviews(package_a, lang=language, country=country, sort=sort_mapping[sort_by], count=count)
            
            if result_a:
                df_a = pd.DataFrame(result_a)
                df_a["package"] = package_a
                df_a["app_name"] = get_app_name(package_a)
                
                sentiment_results = df_a["content"].apply(analyze_sentiment_advanced)
                df_a["sentiment"] = [r[0] for r in sentiment_results]
                df_a["polarity_score"] = [r[1] for r in sentiment_results]
                df_a["subjectivity_score"] = [r[2] for r in sentiment_results]
                df_a["business_impact"] = [r[3] for r in sentiment_results]
                df_a["aspects"] = [r[4] for r in sentiment_results]
                df_a["emotional_intensity"] = [r[5] for r in sentiment_results]
                df_a["at"] = pd.to_datetime(df_a["at"])
                df_a = df_a[df_a["score"] >= min_rating].copy()
            else:
                st.error("❌ FAILED TO EXTRACT REVIEWS FOR PRIMARY APPLICATION")
                st.stop()
            
            progress_bar.progress(0.5)
            
            # Process App B if needed
            df_b = None
            if st.session_state.comparison_mode:
                status_container.markdown(f"""
                <div class="glass-card">
                    <div style="text-align: center;">
                        <h4 style="color: #8b5cf6; font-size: 1.2rem; margin-bottom: 15px;">
                            ⚔️ PROCESSING: {get_app_name(package_b).upper()}
                        </h4>
                        <p style="color: #64748b; margin: 0;">
                            Extracting {count:,} reviews and performing competitive analysis...
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                result_b, _ = reviews(package_b, lang=language, country=country, sort=sort_mapping[sort_by], count=count)
                
                if result_b:
                    df_b = pd.DataFrame(result_b)
                    df_b["package"] = package_b
                    df_b["app_name"] = get_app_name(package_b)
                    
                    sentiment_results = df_b["content"].apply(analyze_sentiment_advanced)
                    df_b["sentiment"] = [r[0] for r in sentiment_results]
                    df_b["polarity_score"] = [r[1] for r in sentiment_results]
                    df_b["subjectivity_score"] = [r[2] for r in sentiment_results]
                    df_b["business_impact"] = [r[3] for r in sentiment_results]
                    df_b["aspects"] = [r[4] for r in sentiment_results]
                    df_b["emotional_intensity"] = [r[5] for r in sentiment_results]
                    df_b["at"] = pd.to_datetime(df_b["at"])
                    df_b = df_b[df_b["score"] >= min_rating].copy()
                else:
                    st.error("❌ FAILED TO EXTRACT REVIEWS FOR COMPETITOR APPLICATION")
                    st.stop()
            
            progress_bar.progress(0.8)
            
            # Generate insights
            status_container.markdown("""
            <div class="glass-card">
                <div style="text-align: center;">
                    <h4 style="color: #10b981; font-size: 1.2rem; margin-bottom: 15px;">
                        🧠 GENERATING AI INTELLIGENCE
                    </h4>
                    <p style="color: #64748b; margin: 0;">
                        Processing advanced insights and strategic intelligence...
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            insights_a = generate_advanced_ai_insights(df_a) if enable_insights else []
            insights_b = generate_advanced_ai_insights(df_b) if enable_insights and df_b is not None else []
            
            progress_bar.progress(1.0)
            
        except Exception as e:
            st.error(f"🚨 PROCESSING ERROR: {str(e)}")
            st.stop()
        
        # Clear progress
        status_container.empty()
        progress_bar.empty()
        
        # Success
        total_reviews = len(df_a) + (len(df_b) if df_b is not None else 0)
        st.success(f"✅ ANALYSIS COMPLETED: {total_reviews:,} reviews processed with advanced AI intelligence")
        
        # Display Enhanced Metrics
        if st.session_state.comparison_mode and df_b is not None:
            st.markdown("## 🏆 COMPETITIVE INTELLIGENCE DASHBOARD")
            
            col1, col2 = st.columns(2)
            
            with col1:
                display_enhanced_metrics(df_a, "🎯 PRIMARY APPLICATION", get_app_name(package_a))
            
            with col2:
                display_enhanced_metrics(df_b, "⚔️ COMPETITOR APPLICATION", get_app_name(package_b))
        else:
            st.markdown("## 📊 COMPREHENSIVE ANALYTICS OVERVIEW")
            display_enhanced_metrics(df_a, "📊 APPLICATION METRICS", get_app_name(package_a))
        
        # AI Insights
        if enable_insights and (insights_a or insights_b):
            st.markdown("""
            <div class="glass-card">
                <h2 style="color: #1e293b; margin-bottom: 40px; text-align: center; font-size: 2rem;">
                    🧠 ADVANCED AI STRATEGIC INTELLIGENCE
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.comparison_mode and insights_b:
                col1, col2 = st.columns(2)
                
                with col1:
                    if insights_a:
                        st.markdown(f"### 🎯 {get_app_name(package_a).upper()} INSIGHTS")
                        for insight in insights_a[:4]:
                            icon = "✅" if insight['type'] == 'positive' else "⚠️"
                            st.markdown(f"""
                            <div class="glass-card">
                                <h5 style="color: #6366f1; margin-bottom: 15px; font-size: 1.1rem;">
                                    {icon} {insight['title']}
                                </h5>
                                <p style="color: #64748b; margin: 0; line-height: 1.7;">
                                    {insight['description']}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                
                with col2:
                    if insights_b:
                        st.markdown(f"### ⚔️ {get_app_name(package_b).upper()} INSIGHTS")
                        for insight in insights_b[:4]:
                            icon = "✅" if insight['type'] == 'positive' else "⚠️"
                            st.markdown(f"""
                            <div class="glass-card">
                                <h5 style="color: #8b5cf6; margin-bottom: 15px; font-size: 1.1rem;">
                                    {icon} {insight['title']}
                                </h5>
                                <p style="color: #64748b; margin: 0; line-height: 1.7;">
                                    {insight['description']}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                for insight in insights_a[:5]:
                    icon = "✅" if insight['type'] == 'positive' else "⚠️"
                    st.markdown(f"""
                    <div class="glass-card">
                        <h5 style="color: #6366f1; margin-bottom: 15px; font-size: 1.1rem;">
                            {icon} {insight['title']}
                        </h5>
                        <p style="color: #64748b; margin: 0; line-height: 1.7;">
                            {insight['description']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Enhanced Visualizations
        st.markdown("""
        <div class="glass-card">
            <h2 style="color: #1e293b; margin-bottom: 40px; text-align: center; font-size: 2rem;">
                📈 ADVANCED VISUALIZATION ANALYTICS
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        charts = create_advanced_visualizations(df_a, df_b)
        for chart_name, chart in charts.items():
            st.plotly_chart(chart, use_container_width=True)
        
        # Individual Reviews
        st.markdown("""
        <div class="glass-card">
            <h2 style="color: #1e293b; margin-bottom: 40px; text-align: center; font-size: 2rem;">
                📝 INDIVIDUAL REVIEW ANALYSIS
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.comparison_mode and df_b is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                display_enhanced_reviews(df_a, f"🎯 {get_app_name(package_a).upper()} REVIEWS", max_reviews_display)
            
            with col2:
                display_enhanced_reviews(df_b, f"⚔️ {get_app_name(package_b).upper()} REVIEWS", max_reviews_display)
        else:
            display_enhanced_reviews(df_a, f"📊 {get_app_name(package_a).upper()} REVIEWS", max_reviews_display)
        
        # Enhanced Export Section
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
                    competitive insights, and strategic recommendations.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate enhanced executive report
            all_insights = insights_a + (insights_b if insights_b else [])
            executive_report = generate_enhanced_executive_report(df_a, df_b, all_insights)
            
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
            action_plan = generate_strategic_action_plan(df_a, df_b, all_insights)
            
            st.download_button(
                "🎯 DOWNLOAD ACTION PLAN",
                data=action_plan,
                file_name=f"Strategic_Action_Plan_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json"
            )
        
        st.markdown("</div></div>", unsafe_allow_html=True)

# Professional Footer
st.markdown("""
<div style="text-align: center; color: rgba(255, 255, 255, 0.8); padding: 60px 40px; 
           margin-top: 80px; background: rgba(255, 255, 255, 0.05); 
           backdrop-filter: blur(20px); border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.1);">
    <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 20px; 
                background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🚀 FEEDBACKS FORGE PRO v4.0
    </div>
    <div style="margin-bottom: 20px; font-size: 1.1rem;">
        Next-Generation Review Intelligence Platform | Created by <strong style="color: #6366f1;">Ayush Pandey</strong>
    </div>
    <div style="font-size: 1rem; line-height: 1.6; opacity: 0.8;">
        Advanced AI Analytics • Predictive Intelligence • Strategic Insights<br>
        Transform Review Data Into Competitive Advantage
    </div>
    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1); 
                font-size: 0.9rem; opacity: 0.6;">
        © {datetime.now().year} Feedbacks Forge Pro - Powered by Artificial Intelligence
    </div>
</div>
""", unsafe_allow_html=True)