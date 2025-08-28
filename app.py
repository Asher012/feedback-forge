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
from io import BytesIO
import base64

# Page Configuration
st.set_page_config(
    page_title="Feedback Forge", 
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Departure Mono Inspired CSS - Terminal Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
    
    /* Global Dark Terminal Theme */
    .stApp {
        background: #0a0e1a;
        color: #e0e6ed;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Terminal Window Header */
    .terminal-header {
        background: linear-gradient(135deg, #1a1d29 0%, #0f1419 100%);
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 2rem;
        margin-bottom: 2rem;
        position: relative;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .terminal-header::before {
        content: '';
        position: absolute;
        top: 12px;
        left: 16px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #ff5f56;
        box-shadow: 20px 0 0 #ffbd2e, 40px 0 0 #27ca3f;
    }
    
    .terminal-title {
        font-family: 'Space Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #58a6ff;
        margin: 1rem 0 0.5rem 0;
        text-shadow: 0 0 10px rgba(88, 166, 255, 0.3);
    }
    
    .terminal-subtitle {
        color: #8b949e;
        font-size: 1rem;
        margin: 0;
        font-weight: 400;
    }
    
    .creator-tag {
        position: absolute;
        top: 16px;
        right: 16px;
        background: #21262d;
        border: 1px solid #30363d;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        color: #7d8590;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Sidebar Terminal Style */
    .sidebar .sidebar-content {
        background: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    
    .control-group {
        background: #0d1117;
        border: 1px solid #21262d;
        border-radius: 6px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    
    .control-header {
        color: #f0f6fc;
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 1px solid #30363d;
        padding-bottom: 0.5rem;
    }
    
    /* Comparison Section */
    .comparison-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .app-input-section {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 1.5rem;
        position: relative;
    }
    
    .app-input-section::before {
        content: 'APP A';
        position: absolute;
        top: -8px;
        left: 12px;
        background: #0d1117;
        color: #58a6ff;
        padding: 0 8px;
        font-size: 0.75rem;
        font-weight: 700;
        font-family: 'Space Mono', monospace;
    }
    
    .app-input-section:nth-child(2)::before {
        content: 'APP B';
        color: #39d353;
    }
    
    /* Metrics Grid */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .metric-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-box:hover {
        border-color: #58a6ff;
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.1);
    }
    
    .metric-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #58a6ff, #39d353, #f85149);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #f0f6fc;
        font-family: 'Space Mono', monospace;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #8b949e;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    /* Content Sections */
    .content-panel {
        background: #0d1117;
        border: 1px solid #21262d;
        border-radius: 6px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }
    
    .panel-header {
        font-family: 'Space Mono', monospace;
        font-size: 1.3rem;
        font-weight: 700;
        color: #f0f6fc;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #30363d;
    }
    
    /* Progress Section */
    .progress-panel {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    .status-item {
        background: rgba(88, 166, 255, 0.1);
        border: 1px solid #30363d;
        border-left: 3px solid #58a6ff;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        text-align: left;
    }
    
    /* Insights Panel */
    .insights-panel {
        background: linear-gradient(135deg, rgba(57, 211, 83, 0.05) 0%, rgba(88, 166, 255, 0.05) 100%);
        border: 1px solid #30363d;
        border-left: 4px solid #39d353;
        border-radius: 6px;
        padding: 2rem;
        margin: 2rem 0;
        position: relative;
    }
    
    .insights-panel::before {
        content: '> AI_INSIGHTS';
        position: absolute;
        top: -12px;
        left: 12px;
        background: #0d1117;
        color: #39d353;
        padding: 0 8px;
        font-size: 0.75rem;
        font-family: 'Space Mono', monospace;
        font-weight: 700;
    }
    
    .insight-item {
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid #30363d;
        border-radius: 4px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 3px solid #f85149;
    }
    
    .insight-item.positive {
        border-left-color: #39d353;
    }
    
    .insight-item.warning {
        border-left-color: #d29922;
    }
    
    /* Interactive Elements */
    .stButton>button {
        background: linear-gradient(135deg, #21262d 0%, #30363d 100%);
        color: #f0f6fc;
        border: 1px solid #58a6ff;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #58a6ff 0%, #39d353 100%);
        border-color: #39d353;
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.3);
    }
    
    /* Comparison Grid */
    .comparison-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .comparison-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 2rem;
        position: relative;
    }
    
    .comparison-card.app-a {
        border-left: 4px solid #58a6ff;
    }
    
    .comparison-card.app-b {
        border-left: 4px solid #39d353;
    }
    
    .comparison-card::before {
        position: absolute;
        top: -12px;
        left: 12px;
        background: #161b22;
        padding: 0 8px;
        font-size: 0.75rem;
        font-family: 'Space Mono', monospace;
        font-weight: 700;
    }
    
    .comparison-card.app-a::before {
        content: 'APPLICATION_A';
        color: #58a6ff;
    }
    
    .comparison-card.app-b::before {
        content: 'APPLICATION_B';
        color: #39d353;
    }
    
    /* Topic Grid */
    .topic-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .topic-item {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 1.5rem;
        transition: all 0.2s ease;
    }
    
    .topic-item:hover {
        border-color: #58a6ff;
        box-shadow: 0 0 15px rgba(88, 166, 255, 0.1);
    }
    
    .topic-title {
        color: #f0f6fc;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 1rem;
        font-family: 'Space Mono', monospace;
    }
    
    .topic-terms {
        color: #8b949e;
        font-size: 0.8rem;
        line-height: 1.5;
    }
    
    .topic-stats {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #30363d;
    }
    
    .topic-count {
        color: #7d8590;
        font-size: 0.75rem;
    }
    
    .topic-percentage {
        background: #58a6ff;
        color: #0d1117;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 700;
    }
    
    /* Export Section */
    .export-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .export-option {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 2rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .export-option:hover {
        border-color: #39d353;
        box-shadow: 0 0 20px rgba(57, 211, 83, 0.1);
    }
    
    .export-title {
        color: #f0f6fc;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        font-family: 'Space Mono', monospace;
    }
    
    .export-desc {
        color: #8b949e;
        font-size: 0.8rem;
        line-height: 1.5;
        margin-bottom: 1.5rem;
    }
    
    /* Home Page Styles */
    .hero-section {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 4rem 3rem;
        text-align: center;
        margin: 2rem 0;
        position: relative;
    }
    
    .hero-title {
        font-family: 'Space Mono', monospace;
        font-size: 3rem;
        font-weight: 700;
        color: #f0f6fc;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(240, 246, 252, 0.3);
    }
    
    .hero-subtitle {
        color: #8b949e;
        font-size: 1.1rem;
        line-height: 1.6;
        max-width: 600px;
        margin: 0 auto 2rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .feature-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 2rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .feature-card:hover {
        border-color: #58a6ff;
        box-shadow: 0 0 25px rgba(88, 166, 255, 0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        color: #f0f6fc;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        font-family: 'Space Mono', monospace;
    }
    
    .feature-description {
        color: #8b949e;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0d1117;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #58a6ff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False

# Navigation
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Helper Functions
def extract_package_name(url):
    """Extract package name from Google Play URL"""
    if "id=" in url:
        return url.split("id=")[1].split("&")[0].strip()
    return None

def analyze_sentiment_advanced(text):
    """Advanced sentiment analysis with business intelligence"""
    if pd.isna(text) or text.strip() == "":
        return "Neutral", 0.0, 0.0, "Unknown"
    
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.3:
        business_impact = "High Positive"
        sentiment = "Positive"
    elif polarity > 0.1:
        business_impact = "Moderate Positive"
        sentiment = "Positive"
    elif polarity < -0.3:
        business_impact = "High Negative"
        sentiment = "Negative"
    elif polarity < -0.1:
        business_impact = "Moderate Negative" 
        sentiment = "Negative"
    else:
        business_impact = "Neutral"
        sentiment = "Neutral"
    
    return sentiment, polarity, subjectivity, business_impact

def get_app_name(package_name):
    """Extract readable app name"""
    parts = package_name.split('.')
    return parts[-1].replace('_', ' ').title() if parts else package_name

def perform_topic_analysis(df, n_topics=5):
    """Advanced topic analysis"""
    if df.empty or len(df) < 5:
        return {}
    
    try:
        all_text = ' '.join(df['content'].dropna().astype(str).tolist())
        
        stop_words = set([
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
            'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his',
            'its', 'our', 'their', 'app', 'good', 'bad', 'very', 'much', 'more', 'most', 'get',
            'go', 'come', 'like', 'just', 'time', 'way', 'work', 'use', 'make', 'see', 'know'
        ])
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', all_text.lower())
        words = [word for word in words if word not in stop_words]
        word_counts = Counter(words)
        top_words = word_counts.most_common(50)
        
        topics = {
            "performance_issues": {
                "title": "PERFORMANCE_ANALYSIS",
                "terms": [word for word, count in top_words if any(keyword in word for keyword in ['fast', 'slow', 'speed', 'quick', 'performance', 'lag', 'freeze'])],
                "count": sum(count for word, count in top_words if any(keyword in word for keyword in ['fast', 'slow', 'speed', 'quick', 'performance', 'lag', 'freeze'])),
                "percentage": 0
            },
            "user_experience": {
                "title": "USER_INTERFACE",
                "terms": [word for word, count in top_words if any(keyword in word for keyword in ['easy', 'difficult', 'interface', 'design', 'user', 'experience', 'navigation'])],
                "count": sum(count for word, count in top_words if any(keyword in word for keyword in ['easy', 'difficult', 'interface', 'design', 'user', 'experience', 'navigation'])),
                "percentage": 0
            },
            "functionality": {
                "title": "FEATURES_FUNCTIONS",
                "terms": [word for word, count in top_words if any(keyword in word for keyword in ['feature', 'function', 'option', 'setting', 'tool', 'capability'])],
                "count": sum(count for word, count in top_words if any(keyword in word for keyword in ['feature', 'function', 'option', 'setting', 'tool', 'capability'])),
                "percentage": 0
            },
            "technical_issues": {
                "title": "BUG_REPORTS",
                "terms": [word for word, count in top_words if any(keyword in word for keyword in ['bug', 'issue', 'problem', 'error', 'crash', 'fix', 'broken'])],
                "count": sum(count for word, count in top_words if any(keyword in word for keyword in ['bug', 'issue', 'problem', 'error', 'crash', 'fix', 'broken'])),
                "percentage": 0
            },
            "satisfaction": {
                "title": "SATISFACTION_RATING",
                "terms": [word for word, count in top_words if any(keyword in word for keyword in ['excellent', 'amazing', 'awesome', 'terrible', 'horrible', 'love', 'hate', 'perfect', 'worst'])],
                "count": sum(count for word, count in top_words if any(keyword in word for keyword in ['excellent', 'amazing', 'awesome', 'terrible', 'horrible', 'love', 'hate', 'perfect', 'worst'])),
                "percentage": 0
            }
        }
        
        total_words = len(words)
        clean_topics = {}
        for topic_key, topic_data in topics.items():
            if topic_data['count'] > 0 and topic_data['terms']:
                topic_data['percentage'] = (topic_data['count'] / total_words) * 100
                topic_data['terms'] = topic_data['terms'][:5]
                clean_topics[topic_key] = topic_data
        
        return clean_topics
        
    except Exception as e:
        return {}

def generate_ai_insights(df):
    """Generate comprehensive AI insights"""
    insights = []
    
    if df.empty:
        return insights
    
    try:
        sentiment_dist = df['sentiment'].value_counts(normalize=True) * 100
        avg_rating = df['score'].mean()
        
        # Sentiment insights
        if sentiment_dist.get('Positive', 0) > 75:
            insights.append({
                "type": "positive",
                "title": "EXCEPTIONAL_USER_SATISFACTION",
                "description": f"Outstanding performance with {sentiment_dist.get('Positive', 0):.1f}% positive sentiment indicates strong market leadership and user loyalty."
            })
        elif sentiment_dist.get('Negative', 0) > 35:
            insights.append({
                "type": "warning", 
                "title": "CRITICAL_ATTENTION_REQUIRED",
                "description": f"High negative sentiment ({sentiment_dist.get('Negative', 0):.1f}%) requires immediate strategic intervention for user experience optimization."
            })
        
        # Rating insights
        if avg_rating >= 4.5:
            insights.append({
                "type": "positive",
                "title": "PREMIUM_QUALITY_RECOGNITION",
                "description": f"Superior rating of {avg_rating:.1f}/5.0 demonstrates exceptional product quality and market positioning."
            })
        elif avg_rating < 3.5:
            insights.append({
                "type": "warning",
                "title": "QUALITY_IMPROVEMENT_PRIORITY",
                "description": f"Current rating of {avg_rating:.1f}/5.0 indicates significant improvement opportunities for competitive advantage."
            })
        
        # Volume insights
        if len(df) > 500:
            insights.append({
                "type": "positive",
                "title": "HIGH_MARKET_ENGAGEMENT",
                "description": f"Strong user engagement with {len(df):,} reviews demonstrates active community and market presence."
            })
        
        return insights
        
    except Exception:
        return []

def create_terminal_charts(df_a, df_b=None):
    """Create terminal-styled charts"""
    charts = {}
    
    # Dark terminal theme for charts
    template = {
        'layout': {
            'plot_bgcolor': '#0d1117',
            'paper_bgcolor': '#0d1117',
            'font': {'color': '#f0f6fc', 'family': 'JetBrains Mono, monospace'},
            'colorway': ['#58a6ff', '#39d353', '#f85149', '#d29922', '#bc8cff']
        }
    }
    
    # Sentiment comparison
    if df_b is not None and not df_b.empty:
        # Comparative sentiment analysis
        sentiment_a = df_a['sentiment'].value_counts(normalize=True) * 100
        sentiment_b = df_b['sentiment'].value_counts(normalize=True) * 100
        
        comparison_data = pd.DataFrame({
            'APPLICATION_A': [sentiment_a.get('Positive', 0), sentiment_a.get('Neutral', 0), sentiment_a.get('Negative', 0)],
            'APPLICATION_B': [sentiment_b.get('Positive', 0), sentiment_b.get('Neutral', 0), sentiment_b.get('Negative', 0)]
        }, index=['POSITIVE', 'NEUTRAL', 'NEGATIVE'])
        
        fig = px.bar(
            comparison_data,
            title="COMPARATIVE_SENTIMENT_ANALYSIS",
            color_discrete_sequence=['#58a6ff', '#39d353'],
            template=template
        )
        fig.update_layout(
            xaxis_title="SENTIMENT_CATEGORIES",
            yaxis_title="PERCENTAGE_DISTRIBUTION",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        charts['comparison_sentiment'] = fig
        
        # Rating distribution comparison
        fig_rating = go.Figure()
        
        for rating in range(1, 6):
            count_a = (df_a['score'] == rating).sum()
            count_b = (df_b['score'] == rating).sum()
            
            fig_rating.add_trace(go.Bar(
                name=f'APP_A',
                x=[f'{rating}_STAR'],
                y=[count_a],
                marker_color='#58a6ff'
            ))
            
            fig_rating.add_trace(go.Bar(
                name=f'APP_B', 
                x=[f'{rating}_STAR'],
                y=[count_b],
                marker_color='#39d353'
            ))
        
        fig_rating.update_layout(
            title="RATING_DISTRIBUTION_COMPARISON",
            xaxis_title="STAR_RATINGS",
            yaxis_title="REVIEW_COUNT",
            barmode='group',
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font={'color': '#f0f6fc', 'family': 'JetBrains Mono, monospace'}
        )
        charts['comparison_rating'] = fig
        
    else:
        # Single app analysis
        if not df_a.empty:
            # Sentiment timeline
            if 'at' in df_a.columns:
                df_copy = df_a.copy()
                df_copy['date'] = pd.to_datetime(df_copy['at']).dt.date
                daily_sentiment = df_copy.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
                
                if not daily_sentiment.empty:
                    fig = go.Figure()
                    
                    colors = {'Positive': '#39d353', 'Neutral': '#d29922', 'Negative': '#f85149'}
                    
                    for sentiment in ['Positive', 'Neutral', 'Negative']:
                        if sentiment in daily_sentiment.columns:
                            fig.add_trace(go.Scatter(
                                x=daily_sentiment.index,
                                y=daily_sentiment[sentiment],
                                mode='lines+markers',
                                name=f'{sentiment.upper()}_SENTIMENT',
                                line=dict(color=colors[sentiment], width=2),
                                marker=dict(size=6)
                            ))
                    
                    fig.update_layout(
                        title='SENTIMENT_EVOLUTION_TIMELINE',
                        xaxis_title='DATE_RANGE',
                        yaxis_title='REVIEW_COUNT',
                        hovermode='x unified',
                        plot_bgcolor='#0d1117',
                        paper_bgcolor='#0d1117',
                        font={'color': '#f0f6fc', 'family': 'JetBrains Mono, monospace'},
                        showlegend=True
                    )
                    
                    charts['sentiment_timeline'] = fig
    
    return charts

def generate_pdf_report(df_a, df_b=None, insights=None, topics=None):
    """Generate comprehensive PDF report"""
    try:
        # Create HTML content for PDF
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
                body {{
                    font-family: 'JetBrains Mono', monospace;
                    background: #0a0e1a;
                    color: #e0e6ed;
                    margin: 0;
                    padding: 20px;
                    font-size: 12px;
                    line-height: 1.6;
                }}
                .header {{
                    background: #1a1d29;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    border: 1px solid #30363d;
                }}
                .title {{
                    font-size: 24px;
                    color: #58a6ff;
                    font-weight: 700;
                    text-align: center;
                    margin-bottom: 10px;
                }}
                .section {{
                    background: #0d1117;
                    border: 1px solid #21262d;
                    border-radius: 6px;
                    padding: 15px;
                    margin-bottom: 15px;
                }}
                .section-title {{
                    color: #f0f6fc;
                    font-size: 16px;
                    font-weight: 700;
                    margin-bottom: 10px;
                    border-bottom: 1px solid #30363d;
                    padding-bottom: 5px;
                }}
                .metric {{
                    display: inline-block;
                    background: #161b22;
                    border: 1px solid #30363d;
                    padding: 10px;
                    margin: 5px;
                    border-radius: 4px;
                    text-align: center;
                    width: 140px;
                }}
                .metric-value {{
                    font-size: 18px;
                    color: #58a6ff;
                    font-weight: 700;
                }}
                .metric-label {{
                    color: #8b949e;
                    font-size: 10px;
                    text-transform: uppercase;
                }}
                .insight {{
                    background: rgba(57, 211, 83, 0.1);
                    border-left: 3px solid #39d353;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 4px;
                }}
                .insight.warning {{
                    background: rgba(210, 153, 34, 0.1);
                    border-left-color: #d29922;
                }}
                .topic {{
                    background: #161b22;
                    border: 1px solid #30363d;
                    padding: 10px;
                    margin: 5px;
                    border-radius: 4px;
                    display: inline-block;
                    width: 200px;
                    vertical-align: top;
                }}
                .topic-title {{
                    color: #58a6ff;
                    font-weight: 700;
                    font-size: 12px;
                }}
                .topic-terms {{
                    color: #8b949e;
                    font-size: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">REVIEWANALYZER_PRO_REPORT</div>
                <div style="text-align: center; color: #8b949e;">
                    Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Created by Ayush Pandey
                </div>
            </div>
        """
        
        # Executive Summary
        html_content += f"""
        <div class="section">
            <div class="section-title">EXECUTIVE_SUMMARY</div>
            <div class="metric">
                <div class="metric-value">{len(df_a):,}</div>
                <div class="metric-label">Total Reviews</div>
            </div>
            <div class="metric">
                <div class="metric-value">{df_a['score'].mean():.1f}</div>
                <div class="metric-label">Avg Rating</div>
            </div>
            <div class="metric">
                <div class="metric-value">{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%</div>
                <div class="metric-label">Positive Rate</div>
            </div>
            <div class="metric">
                <div class="metric-value">{df_a['polarity_score'].mean():.2f}</div>
                <div class="metric-label">Sentiment Score</div>
            </div>
        </div>
        """
        
        # AI Insights
        if insights:
            html_content += '<div class="section"><div class="section-title">AI_POWERED_INSIGHTS</div>'
            for insight in insights[:5]:
                css_class = 'insight positive' if insight['type'] == 'positive' else 'insight warning'
                html_content += f'<div class="{css_class}"><strong>{insight["title"]}</strong><br>{insight["description"]}</div>'
            html_content += '</div>'
        
        # Topic Analysis
        if topics:
            html_content += '<div class="section"><div class="section-title">TOPIC_ANALYSIS</div>'
            for topic_key, topic_data in topics.items():
                html_content += f'''
                <div class="topic">
                    <div class="topic-title">{topic_data["title"]}</div>
                    <div class="topic-terms">Key Terms: {", ".join(topic_data["terms"][:3])}</div>
                    <div style="margin-top: 5px; color: #58a6ff; font-size: 10px;">
                        {topic_data["count"]} mentions ({topic_data["percentage"]:.1f}%)
                    </div>
                </div>
                '''
            html_content += '</div>'
        
        # Comparative Analysis (if two apps)
        if df_b is not None and not df_b.empty:
            html_content += f"""
            <div class="section">
                <div class="section-title">COMPETITIVE_COMPARISON</div>
                <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                    <tr style="background: #161b22;">
                        <th style="border: 1px solid #30363d; padding: 8px; color: #58a6ff;">METRIC</th>
                        <th style="border: 1px solid #30363d; padding: 8px; color: #58a6ff;">APPLICATION_A</th>
                        <th style="border: 1px solid #30363d; padding: 8px; color: #39d353;">APPLICATION_B</th>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #30363d; padding: 8px;">Reviews Count</td>
                        <td style="border: 1px solid #30363d; padding: 8px;">{len(df_a):,}</td>
                        <td style="border: 1px solid #30363d; padding: 8px;">{len(df_b):,}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #30363d; padding: 8px;">Average Rating</td>
                        <td style="border: 1px solid #30363d; padding: 8px;">{df_a['score'].mean():.2f}</td>
                        <td style="border: 1px solid #30363d; padding: 8px;">{df_b['score'].mean():.2f}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #30363d; padding: 8px;">Positive Sentiment</td>
                        <td style="border: 1px solid #30363d; padding: 8px;">{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%</td>
                        <td style="border: 1px solid #30363d; padding: 8px;">{(df_b['sentiment'] == 'Positive').mean() * 100:.1f}%</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #30363d; padding: 8px;">Sentiment Score</td>
                        <td style="border: 1px solid #30363d; padding: 8px;">{df_a['polarity_score'].mean():.3f}</td>
                        <td style="border: 1px solid #30363d; padding: 8px;">{df_b['polarity_score'].mean():.3f}</td>
                    </tr>
                </table>
            </div>
            """
        
        html_content += "</body></html>"
        
        # Convert HTML to bytes for download
        return html_content.encode('utf-8')
        
    except Exception as e:
        return f"Error generating report: {str(e)}".encode('utf-8')

# Main Application Logic
if st.session_state.page == 'home':
    # HOME PAGE
    st.markdown("""
    <div class="terminal-header">
        <div class="terminal-title">Feedback Forge</div>
        <div class="terminal-subtitle">Transform Play Store Reviews Into Strategic Intelligence</div>
        <div class="creator-tag">dev: ayush_pandey</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">> FEEDBACK_ANALYTICS</div>
        <div class="hero-subtitle">
            Professional review analysis platform with monospace aesthetics and advanced competitive intelligence.
            Built for developers, analysts, and product managers who appreciate clean, terminal-inspired interfaces.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Grid
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    features = [
        {
            "icon": "⚡",
            "title": "DUAL_APP_COMPARISON", 
            "description": "Side-by-side competitive analysis of two applications with detailed metrics and performance benchmarks."
        },
        {
            "icon": "🎯",
            "title": "TERMINAL_ANALYTICS",
            "description": "Monospace interface with professional data visualization and comprehensive sentiment analysis."
        },
        {
            "icon": "🔍",
            "title": "AI_TOPIC_DISCOVERY",
            "description": "Automated identification of key discussion themes, issues, and opportunities in user reviews."
        },
        {
            "icon": "📊",
            "title": "COMPETITIVE_INTELLIGENCE",
            "description": "Advanced market positioning analysis with detailed comparison matrices and strategic insights."
        },
        {
            "icon": "⚙️",
            "title": "CUSTOMIZABLE_PARAMETERS",
            "description": "Flexible configuration options for language, region, sorting methods, and analysis depth."
        },
        {
            "icon": "📄",
            "title": "PROFESSIONAL_REPORTS",
            "description": "Comprehensive PDF reports with AI insights, charts, and executive-level summaries."
        }
    ]
    
    for feature in features:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{feature['icon']}</div>
            <div class="feature-title">{feature['title']}</div>
            <div class="feature-description">{feature['description']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(">> SINGLE_APP_ANALYSIS", type="primary"):
            st.session_state.comparison_mode = False
            navigate_to('analysis')
    
    with col2:
        if st.button(">> COMPETITIVE_COMPARISON", type="primary"):
            st.session_state.comparison_mode = True
            navigate_to('analysis')

elif st.session_state.page == 'analysis':
    # ANALYSIS PAGE
    st.markdown("""
    <div class="terminal-header">
        <div class="terminal-title">> ANALYSIS_MODE</div>
        <div class="terminal-subtitle">Configure parameters and execute comprehensive review analysis</div>
        <div class="creator-tag">mode: """ + ("comparison" if st.session_state.comparison_mode else "single") + """</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation back to home
    if st.button("< RETURN_HOME"):
        navigate_to('home')
    
    # Sidebar Configuration
    st.sidebar.markdown("""
    <div class="control-group">
        <div class="control-header">SYSTEM_CONFIG</div>
    </div>
    """, unsafe_allow_html=True)
    
    # URL Input Section
    if st.session_state.comparison_mode:
        st.markdown("### COMPETITIVE_COMPARISON_MODE")
        st.markdown('<div class="comparison-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="app-input-section">', unsafe_allow_html=True)
            url_a = st.text_area("APPLICATION_A_URL", placeholder="https://play.google.com/store/apps/details?id=...", height=100)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="app-input-section">', unsafe_allow_html=True)
            url_b = st.text_area("APPLICATION_B_URL", placeholder="https://play.google.com/store/apps/details?id=...", height=100)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        url_a = st.text_area("APPLICATION_URL", placeholder="https://play.google.com/store/apps/details?id=...", height=100)
        url_b = None
    
    # Analysis Parameters
    col1, col2 = st.columns(2)
    
    with col1:
        count = st.slider("REVIEWS_PER_APP", 50, 1000, 300, 50)
        language = st.selectbox("LANGUAGE_CODE", ["en", "hi", "es", "fr", "de", "ja"])
    
    with col2:
        country = st.selectbox("REGION_CODE", ["in", "us", "uk", "ca", "de", "jp"])
        sort_by = st.selectbox("SORT_METHOD", ["NEWEST", "MOST_RELEVANT", "RATING"])
    
    # Advanced Options
    st.sidebar.markdown("""
    <div class="control-group">
        <div class="control-header">AI_MODULES</div>
    </div>
    """, unsafe_allow_html=True)
    
    enable_insights = st.sidebar.checkbox("AI_INSIGHTS", value=True)
    enable_topics = st.sidebar.checkbox("TOPIC_ANALYSIS", value=True)
    enable_keywords = st.sidebar.checkbox("KEYWORD_TRACKING", value=True)
    min_rating = st.sidebar.selectbox("MIN_RATING_FILTER", [1, 2, 3, 4, 5], index=0)
    
    # Keywords
    keywords = []
    if enable_keywords:
        keyword_input = st.sidebar.text_input("KEYWORD_LIST", placeholder="performance,bug,excellent,slow")
        if keyword_input:
            keywords = [k.strip().lower() for k in keyword_input.split(",")]
    
    # Execute Analysis
    if st.button(">> EXECUTE_ANALYSIS", type="primary"):
        # Validate inputs
        if not url_a.strip():
            st.error("APPLICATION_A_URL is required")
            st.stop()
        
        if st.session_state.comparison_mode and not url_b.strip():
            st.error("APPLICATION_B_URL is required for comparison mode")
            st.stop()
        
        package_a = extract_package_name(url_a)
        package_b = extract_package_name(url_b) if url_b else None
        
        if not package_a:
            st.error("Invalid APPLICATION_A_URL format")
            st.stop()
        
        if st.session_state.comparison_mode and not package_b:
            st.error("Invalid APPLICATION_B_URL format") 
            st.stop()
        
        # Progress Section
        st.markdown("""
        <div class="progress-panel">
            <div style="color: #58a6ff; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem;">
                >> ANALYSIS_PIPELINE_ACTIVE
            </div>
            <div style="color: #8b949e;">Extracting and processing review data...</div>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_container = st.empty()
        
        # Process Application A
        status_container.markdown(f"""
        <div class="status-item">
            <strong>PROCESSING: {get_app_name(package_a)}</strong><br>
            <span style="color: #8b949e;">Package: {package_a}</span>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            sort_mapping = {
                "NEWEST": Sort.NEWEST,
                "MOST_RELEVANT": Sort.MOST_RELEVANT,
                "RATING": Sort.RATING
            }
            
            result_a, _ = reviews(
                package_a,
                lang=language,
                country=country,
                sort=sort_mapping[sort_by],
                count=count
            )
            
            if result_a:
                df_a = pd.DataFrame(result_a)
                df_a["package"] = package_a
                df_a["app_name"] = get_app_name(package_a)
                
                # Sentiment analysis
                sentiment_results = df_a["content"].apply(analyze_sentiment_advanced)
                df_a["sentiment"] = [r[0] for r in sentiment_results]
                df_a["polarity_score"] = [r[1] for r in sentiment_results]
                df_a["subjectivity_score"] = [r[2] for r in sentiment_results]
                df_a["business_impact"] = [r[3] for r in sentiment_results]
                df_a["at"] = pd.to_datetime(df_a["at"])
                
                # Apply filters
                df_a = df_a[df_a["score"] >= min_rating].copy()
                
            else:
                st.error("Failed to extract reviews for APPLICATION_A")
                st.stop()
                
        except Exception as e:
            st.error(f"Error processing APPLICATION_A: {str(e)}")
            st.stop()
        
        progress_bar.progress(0.5)
        
        # Process Application B (if comparison mode)
        df_b = None
        if st.session_state.comparison_mode:
            status_container.markdown(f"""
            <div class="status-item">
                <strong>PROCESSING: {get_app_name(package_b)}</strong><br>
                <span style="color: #8b949e;">Package: {package_b}</span>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                result_b, _ = reviews(
                    package_b,
                    lang=language,
                    country=country,
                    sort=sort_mapping[sort_by],
                    count=count
                )
                
                if result_b:
                    df_b = pd.DataFrame(result_b)
                    df_b["package"] = package_b
                    df_b["app_name"] = get_app_name(package_b)
                    
                    # Sentiment analysis
                    sentiment_results = df_b["content"].apply(analyze_sentiment_advanced)
                    df_b["sentiment"] = [r[0] for r in sentiment_results]
                    df_b["polarity_score"] = [r[1] for r in sentiment_results]
                    df_b["subjectivity_score"] = [r[2] for r in sentiment_results]
                    df_b["business_impact"] = [r[3] for r in sentiment_results]
                    df_b["at"] = pd.to_datetime(df_b["at"])
                    
                    # Apply filters
                    df_b = df_b[df_b["score"] >= min_rating].copy()
                    
                else:
                    st.error("Failed to extract reviews for APPLICATION_B")
                    st.stop()
                    
            except Exception as e:
                st.error(f"Error processing APPLICATION_B: {str(e)}")
                st.stop()
        
        progress_bar.progress(1.0)
        
        # Clear progress
        status_container.empty()
        progress_bar.empty()
        
        # Generate insights and topics
        insights_a = generate_ai_insights(df_a) if enable_insights else []
        topics_a = perform_topic_analysis(df_a) if enable_topics else {}
        
        insights_b = generate_ai_insights(df_b) if enable_insights and df_b is not None else []
        topics_b = perform_topic_analysis(df_b) if enable_topics and df_b is not None else {}
        
        # Success Message
        st.success(f"ANALYSIS_COMPLETE: {len(df_a):,} reviews processed" + (f" + {len(df_b):,} reviews" if df_b is not None else ""))
        
        # Display Metrics
        if st.session_state.comparison_mode and df_b is not None:
            # Comparison Metrics
            st.markdown('<div class="comparison-grid">', unsafe_allow_html=True)
            
            # App A Metrics
            st.markdown(f"""
            <div class="comparison-card app-a">
                <div style="margin-bottom: 2rem;">
                    <div style="color: #58a6ff; font-size: 1.1rem; font-weight: 700; margin-bottom: 1rem;">
                        {get_app_name(package_a)}
                    </div>
                    <div class="metrics-container">
                        <div class="metric-box">
                            <div class="metric-value">{len(df_a):,}</div>
                            <div class="metric-label">REVIEWS</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-value">{df_a['score'].mean():.1f}</div>
                            <div class="metric-label">AVG_RATING</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-value">{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%</div>
                            <div class="metric-label">POSITIVE</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-value">{df_a['polarity_score'].mean():.2f}</div>
                            <div class="metric-label">SENTIMENT_SCORE</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # App B Metrics  
            st.markdown(f"""
            <div class="comparison-card app-b">
                <div style="margin-bottom: 2rem;">
                    <div style="color: #39d353; font-size: 1.1rem; font-weight: 700; margin-bottom: 1rem;">
                        {get_app_name(package_b)}
                    </div>
                    <div class="metrics-container">
                        <div class="metric-box">
                            <div class="metric-value">{len(df_b):,}</div>
                            <div class="metric-label">REVIEWS</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-value">{df_b['score'].mean():.1f}</div>
                            <div class="metric-label">AVG_RATING</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-value">{(df_b['sentiment'] == 'Positive').mean() * 100:.1f}%</div>
                            <div class="metric-label">POSITIVE</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-value">{df_b['polarity_score'].mean():.2f}</div>
                            <div class="metric-label">SENTIMENT_SCORE</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            # Single App Metrics
            st.markdown(f"""
            <div class="metrics-container">
                <div class="metric-box">
                    <div class="metric-value">{len(df_a):,}</div>
                    <div class="metric-label">TOTAL_REVIEWS</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{df_a['score'].mean():.1f}</div>
                    <div class="metric-label">AVG_RATING</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%</div>
                    <div class="metric-label">POSITIVE_RATE</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{df_a['polarity_score'].mean():.2f}</div>
                    <div class="metric-label">SENTIMENT_SCORE</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{(df_a['sentiment'] == 'Negative').mean() * 100:.1f}%</div>
                    <div class="metric-label">NEGATIVE_RATE</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # AI Insights
        if enable_insights and (insights_a or insights_b):
            st.markdown("""
            <div class="insights-panel">
                <h3 style="color: #f0f6fc; margin-bottom: 1.5rem; font-family: 'Space Mono', monospace;">
                    AI_POWERED_INSIGHTS
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Display insights for both apps
            for insights, app_name in [(insights_a, get_app_name(package_a)), (insights_b, get_app_name(package_b) if package_b else None)]:
                if insights and app_name:
                    st.markdown(f"#### {app_name.upper()}_INSIGHTS")
                    for insight in insights[:3]:
                        css_class = "insight-item positive" if insight['type'] == 'positive' else "insight-item warning"
                        icon = "✓" if insight['type'] == 'positive' else "⚠"
                        st.markdown(f"""
                        <div class="{css_class}">
                            <h5 style="color: #f0f6fc; margin-bottom: 0.5rem;">{icon} {insight['title']}</h5>
                            <p style="color: #8b949e; margin: 0; line-height: 1.5;">{insight['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Charts Section
        st.markdown("""
        <div class="content-panel">
            <div class="panel-header">VISUALIZATION_ANALYTICS</div>
        </div>
        """, unsafe_allow_html=True)
        
        charts = create_terminal_charts(df_a, df_b)
        
        for chart_name, chart in charts.items():
            st.plotly_chart(chart, use_container_width=True)
        
        # Topic Analysis
        if enable_topics and (topics_a or topics_b):
            st.markdown("""
            <div class="content-panel">
                <div class="panel-header">TOPIC_DISCOVERY_ENGINE</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display topics for both apps
            for topics, app_name in [(topics_a, get_app_name(package_a)), (topics_b, get_app_name(package_b) if package_b else None)]:
                if topics and app_name:
                    st.markdown(f"#### {app_name.upper()}_TOPICS")
                    st.markdown('<div class="topic-grid">', unsafe_allow_html=True)
                    
                    for topic_key, topic_data in topics.items():
                        st.markdown(f"""
                        <div class="topic-item">
                            <div class="topic-title">{topic_data['title']}</div>
                            <div class="topic-terms">KEY_TERMS: {', '.join(topic_data['terms'][:3])}</div>
                            <div class="topic-stats">
                                <span class="topic-count">{topic_data['count']} mentions</span>
                                <span class="topic-percentage">{topic_data['percentage']:.1f}%</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Keyword Analysis
        if enable_keywords and keywords:
            st.markdown("""
            <div class="content-panel">
                <div class="panel-header">KEYWORD_INTELLIGENCE</div>
            </div>
            """, unsafe_allow_html=True)
            
            for df, app_name in [(df_a, get_app_name(package_a)), (df_b, get_app_name(package_b) if package_b else None)]:
                if df is not None and not df.empty and app_name:
                    keyword_results = {}
                    for keyword in keywords:
                        count_total = df['content'].str.lower().str.contains(keyword, na=False).sum()
                        keyword_results[keyword] = count_total
                    
                    if any(count > 0 for count in keyword_results.values()):
                        st.markdown(f"#### {app_name.upper()}_KEYWORD_ANALYSIS")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Keyword metrics
                            for keyword, count in keyword_results.items():
                                if count > 0:
                                    percentage = (count / len(df)) * 100
                                    impact = "HIGH" if percentage > 10 else "MEDIUM" if percentage > 5 else "LOW"
                                    st.markdown(f"""
                                    <div class="metric-box" style="text-align: left;">
                                        <div style="color: #58a6ff; font-weight: 700; text-transform: uppercase;">{keyword}</div>
                                        <div style="color: #8b949e;">Mentions: {count} ({percentage:.1f}%)</div>
                                        <div style="color: #39d353; font-size: 0.8rem;">Impact: {impact}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        with col2:
                            # Keyword chart
                            if keyword_results:
                                fig_keywords = px.bar(
                                    x=list(keyword_results.keys()),
                                    y=list(keyword_results.values()),
                                    title=f"{app_name.upper()}_KEYWORD_FREQUENCY",
                                    color=list(keyword_results.values()),
                                    color_continuous_scale='viridis'
                                )
                                
                                fig_keywords.update_layout(
                                    plot_bgcolor='#0d1117',
                                    paper_bgcolor='#0d1117',
                                    font={'color': '#f0f6fc', 'family': 'JetBrains Mono, monospace'},
                                    xaxis_title="KEYWORDS",
                                    yaxis_title="FREQUENCY"
                                )
                                
                                st.plotly_chart(fig_keywords, use_container_width=True)
        
        # Export Section
        st.markdown("""
        <div class="content-panel">
            <div class="panel-header">EXPORT_PROTOCOLS</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="export-container">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="export-option">
                <div class="export-title">COMPREHENSIVE_PDF_REPORT</div>
                <div class="export-desc">AI-generated comprehensive report with insights, charts, and competitive analysis</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate PDF report
            pdf_content = generate_pdf_report(df_a, df_b, insights_a + insights_b if insights_b else insights_a, {**topics_a, **topics_b} if topics_b else topics_a)
            
            st.download_button(
                "DOWNLOAD_PDF_REPORT",
                data=pdf_content,
                file_name=f"ReviewAnalyzer_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                mime="text/html"
            )
        
        with col2:
            st.markdown("""
            <div class="export-option">
                <div class="export-title">DATASET_EXPORT</div>
                <div class="export-desc">Complete review dataset with sentiment analysis and business intelligence</div>
            </div>
            """, unsafe_allow_html=True)
            
            if df_b is not None:
                combined_df = pd.concat([df_a, df_b], ignore_index=True)
                csv_data = combined_df.to_csv(index=False).encode('utf-8')
            else:
                csv_data = df_a.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                "DOWNLOAD_DATASET",
                data=csv_data,
                file_name=f"ReviewData_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        with col3:
            st.markdown("""
            <div class="export-option">
                <div class="export-title">EXECUTIVE_SUMMARY</div>
                <div class="export-desc">High-level metrics and KPIs for stakeholder presentations</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create executive summary
            if df_b is not None:
                summary_data = [{
                    "Application": get_app_name(package_a),
                    "Reviews": len(df_a),
                    "Avg_Rating": round(df_a["score"].mean(), 2),
                    "Positive_Rate": f"{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%",
                    "Sentiment_Score": round(df_a["polarity_score"].mean(), 3)
                }, {
                    "Application": get_app_name(package_b),
                    "Reviews": len(df_b),
                    "Avg_Rating": round(df_b["score"].mean(), 2),
                    "Positive_Rate": f"{(df_b['sentiment'] == 'Positive').mean() * 100:.1f}%",
                    "Sentiment_Score": round(df_b["polarity_score"].mean(), 3)
                }]
            else:
                summary_data = [{
                    "Application": get_app_name(package_a),
                    "Reviews": len(df_a),
                    "Avg_Rating": round(df_a["score"].mean(), 2),
                    "Positive_Rate": f"{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%",
                    "Sentiment_Score": round(df_a["polarity_score"].mean(), 3)
                }]
            
            summary_df = pd.DataFrame(summary_data)
            summary_csv = summary_df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                "DOWNLOAD_SUMMARY",
                data=summary_csv,
                file_name=f"ExecutiveSummary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
