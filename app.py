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
import time

# Page Configuration
st.set_page_config(
    page_title="Feedback Forge", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Medium-Inspired CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=GT+Planar:wght@400;500;600;700&family=Source+Serif+Pro:wght@400;600;700&display=swap');
    
    /* Global Styles - Medium Inspired */
    .stApp {
        background: #ffffff;
        color: #242424;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }
    
    /* Hide Streamlit Elements */
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stMainBlockContainer {padding-top: 0;}
    
    /* Navigation Header */
    .main-nav {
        background: #ffffff;
        border-bottom: 1px solid #e6e6e6;
        padding: 16px 0;
        position: sticky;
        top: 0;
        z-index: 100;
        margin-bottom: 40px;
    }
    
    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .brand {
        font-family: 'Source Serif Pro', serif;
        font-size: 32px;
        font-weight: 700;
        color: #1a8917;
        text-decoration: none;
        letter-spacing: -0.5px;
    }
    
    .nav-links {
        display: flex;
        gap: 32px;
        align-items: center;
    }
    
    .nav-link {
        color: #242424;
        text-decoration: none;
        font-size: 16px;
        font-weight: 400;
        transition: color 0.2s ease;
        cursor: pointer;
    }
    
    .nav-link:hover {
        color: #1a8917;
    }
    
    .nav-link.active {
        color: #1a8917;
        font-weight: 500;
    }
    
    /* Hero Section */
    .hero-section {
        max-width: 800px;
        margin: 80px auto 120px;
        text-align: center;
        padding: 0 24px;
    }
    
    .hero-title {
        font-family: 'Source Serif Pro', serif;
        font-size: 56px;
        font-weight: 700;
        color: #242424;
        line-height: 1.1;
        margin-bottom: 24px;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 22px;
        color: #6b6b6b;
        line-height: 1.4;
        margin-bottom: 48px;
        font-weight: 400;
    }
    
    /* Button Styles */
    .primary-button {
        background: #1a8917;
        color: white;
        border: none;
        border-radius: 99999px;
        padding: 14px 28px;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        display: inline-block;
        margin: 8px;
    }
    
    .primary-button:hover {
        background: #156f13;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(26, 137, 23, 0.3);
    }
    
    .secondary-button {
        background: transparent;
        color: #1a8917;
        border: 1px solid #1a8917;
        border-radius: 99999px;
        padding: 14px 28px;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        display: inline-block;
        margin: 8px;
    }
    
    .secondary-button:hover {
        background: #1a8917;
        color: white;
        transform: translateY(-1px);
    }
    
    /* Content Container */
    .content-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 24px;
    }
    
    .section {
        margin-bottom: 80px;
    }
    
    .section-title {
        font-family: 'Source Serif Pro', serif;
        font-size: 36px;
        font-weight: 600;
        color: #242424;
        margin-bottom: 16px;
        text-align: center;
    }
    
    .section-subtitle {
        font-size: 18px;
        color: #6b6b6b;
        text-align: center;
        margin-bottom: 48px;
        line-height: 1.5;
    }
    
    /* Feature Cards */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
        gap: 32px;
        margin: 64px 0;
    }
    
    .feature-card {
        background: #ffffff;
        border: 1px solid #e6e6e6;
        border-radius: 8px;
        padding: 32px;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .feature-card:hover {
        border-color: #1a8917;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    .feature-title {
        font-family: 'Source Serif Pro', serif;
        font-size: 24px;
        font-weight: 600;
        color: #242424;
        margin-bottom: 12px;
    }
    
    .feature-description {
        color: #6b6b6b;
        line-height: 1.6;
        font-size: 16px;
    }
    
    /* Form Styles */
    .form-section {
        background: #f9f9f9;
        border-radius: 12px;
        padding: 48px;
        margin: 48px 0;
        border: 1px solid #e6e6e6;
    }
    
    .form-title {
        font-family: 'Source Serif Pro', serif;
        font-size: 28px;
        font-weight: 600;
        color: #242424;
        margin-bottom: 24px;
        text-align: center;
    }
    
    /* Metrics Display */
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 24px;
        margin: 48px 0;
    }
    
    .metric-card {
        background: #ffffff;
        border: 1px solid #e6e6e6;
        border-radius: 8px;
        padding: 24px;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        border-color: #1a8917;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    }
    
    .metric-value {
        font-family: 'Source Serif Pro', serif;
        font-size: 32px;
        font-weight: 700;
        color: #1a8917;
        margin-bottom: 8px;
    }
    
    .metric-label {
        color: #6b6b6b;
        font-size: 14px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Results Section */
    .results-container {
        background: #ffffff;
        border: 1px solid #e6e6e6;
        border-radius: 12px;
        padding: 32px;
        margin: 32px 0;
    }
    
    .results-header {
        font-family: 'Source Serif Pro', serif;
        font-size: 24px;
        font-weight: 600;
        color: #242424;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid #e6e6e6;
    }
    
    /* Review Cards */
    .review-card {
        background: #ffffff;
        border: 1px solid #e6e6e6;
        border-radius: 8px;
        padding: 24px;
        margin: 16px 0;
        transition: all 0.2s ease;
    }
    
    .review-card:hover {
        border-color: #1a8917;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .review-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    
    .review-author {
        font-weight: 500;
        color: #242424;
    }
    
    .review-rating {
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .star {
        color: #f59e0b;
        font-size: 16px;
    }
    
    .review-content {
        color: #242424;
        line-height: 1.6;
        margin-bottom: 12px;
    }
    
    .review-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 14px;
        color: #6b6b6b;
    }
    
    .sentiment-tag {
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .sentiment-positive {
        background: #dcfce7;
        color: #166534;
    }
    
    .sentiment-negative {
        background: #fef2f2;
        color: #dc2626;
    }
    
    .sentiment-neutral {
        background: #f3f4f6;
        color: #374151;
    }
    
    /* Insights Section */
    .insights-container {
        background: #f0f9ff;
        border: 1px solid #0ea5e9;
        border-radius: 12px;
        padding: 32px;
        margin: 32px 0;
    }
    
    .insight-item {
        background: #ffffff;
        border-radius: 8px;
        padding: 20px;
        margin: 16px 0;
        border-left: 4px solid #1a8917;
    }
    
    .insight-item.warning {
        border-left-color: #f59e0b;
    }
    
    .insight-title {
        font-weight: 600;
        color: #242424;
        margin-bottom: 8px;
    }
    
    .insight-description {
        color: #6b6b6b;
        line-height: 1.5;
    }
    
    /* About Page Styles */
    .about-hero {
        max-width: 800px;
        margin: 60px auto;
        text-align: center;
        padding: 0 24px;
    }
    
    .about-content {
        max-width: 700px;
        margin: 0 auto;
        padding: 0 24px;
    }
    
    .about-section {
        margin-bottom: 48px;
    }
    
    .about-section h2 {
        font-family: 'Source Serif Pro', serif;
        font-size: 28px;
        font-weight: 600;
        color: #242424;
        margin-bottom: 16px;
    }
    
    .about-section p {
        color: #242424;
        line-height: 1.7;
        font-size: 18px;
        margin-bottom: 16px;
    }
    
    /* Footer */
    .footer {
        background: #f9f9f9;
        border-top: 1px solid #e6e6e6;
        padding: 48px 0;
        margin-top: 80px;
        text-align: center;
    }
    
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 24px;
    }
    
    .footer-brand {
        font-family: 'Source Serif Pro', serif;
        font-size: 24px;
        font-weight: 600;
        color: #1a8917;
        margin-bottom: 16px;
    }
    
    .footer-text {
        color: #6b6b6b;
        font-size: 16px;
        line-height: 1.5;
    }
    
    /* Developer Credit */
    .developer-credit {
        background: linear-gradient(135deg, #1a8917 0%, #0ea5e9 100%);
        color: white;
        padding: 16px;
        border-radius: 8px;
        margin-top: 32px;
        text-align: center;
        font-weight: 500;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 40px;
        }
        
        .hero-subtitle {
            font-size: 18px;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .nav-container {
            padding: 0 16px;
        }
        
        .form-section {
            padding: 32px 24px;
        }
    }
    
    /* Custom Streamlit Button Override */
    .stButton > button {
        background: #1a8917 !important;
        color: white !important;
        border: none !important;
        border-radius: 99999px !important;
        padding: 14px 28px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        height: auto !important;
        width: auto !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #156f13 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(26, 137, 23, 0.3) !important;
    }
    
    /* Hide Streamlit specific elements */
    .stSelectbox > label,
    .stSlider > label,
    .stTextArea > label,
    .stTextInput > label {
        font-weight: 500 !important;
        color: #242424 !important;
        margin-bottom: 8px !important;
    }
    
    /* Analysis Results Improvements */
    .result-highlight {
        background: linear-gradient(135deg, #1a8917 0%, #0ea5e9 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        margin: 24px 0;
        text-align: center;
    }
    
    .result-highlight h3 {
        margin: 0;
        font-size: 22px;
        font-weight: 600;
    }
    
    .result-highlight p {
        margin: 8px 0 0;
        font-size: 18px;
    }
    
    /* Keyword Highlights */
    .keyword-pill {
        display: inline-block;
        background: #e6f7ff;
        color: #0ea5e9;
        padding: 4px 12px;
        border-radius: 16px;
        margin: 4px;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .loading-pulse {
        animation: pulse 1.5s infinite;
        text-align: center;
        color: #1a8917;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None

# Navigation
def show_navigation():
    st.markdown(f"""
    <div class="main-nav">
        <div class="nav-container">
            <div class="brand">Feedback Forge</div>
            <div class="nav-links">
                <span class="nav-link {'active' if st.session_state.page == 'home' else ''}" 
                      onclick="window.navigateTo('home')">Home</span>
                <span class="nav-link {'active' if st.session_state.page == 'about' else ''}" 
                      onclick="window.navigateTo('about')">About</span>
                <span class="nav-link {'active' if st.session_state.page == 'analysis' else ''}" 
                      onclick="window.navigateTo('analysis')">Analysis</span>
            </div>
        </div>
    </div>
    
    <script>
    function navigateTo(page) {{
        // This will be handled by the Streamlit buttons
        if (page === 'home') {{
            document.querySelector('button[key="nav_home"]').click();
        }} else if (page === 'about') {{
            document.querySelector('button[key="nav_about"]').click();
        }} else if (page === 'analysis') {{
            document.querySelector('button[key="nav_analysis"]').click();
        }}
    }}
    window.navigateTo = navigateTo;
    </script>
    """, unsafe_allow_html=True)

# Hidden navigation buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Home", key="nav_home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()
with col2:
    if st.button("About", key="nav_about", use_container_width=True):
        st.session_state.page = 'about'
        st.rerun()
with col3:
    if st.button("Analysis", key="nav_analysis", use_container_width=True):
        st.session_state.page = 'analysis'
        st.rerun()

# Helper Functions
def extract_package_name(url):
    if "id=" in url:
        return url.split("id=")[1].split("&")[0].strip()
    return None

def analyze_sentiment_advanced(text):
    if pd.isna(text) or text.strip() == "":
        return "Neutral", 0.0, 0.0, "Unknown"
    
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.3:
        return "Positive", polarity, subjectivity, "Highly Positive"
    elif polarity > 0.1:
        return "Positive", polarity, subjectivity, "Moderately Positive"
    elif polarity < -0.3:
        return "Negative", polarity, subjectivity, "Highly Negative"
    elif polarity < -0.1:
        return "Negative", polarity, subjectivity, "Moderately Negative"
    else:
        return "Neutral", polarity, subjectivity, "Neutral"

def get_app_name(package_name):
    parts = package_name.split('.')
    return parts[-1].replace('_', ' ').title() if parts else package_name

def generate_insights(df):
    insights = []
    if df.empty:
        return insights
    
    try:
        sentiment_dist = df['sentiment'].value_counts(normalize=True) * 100
        avg_rating = df['score'].mean()
        total_reviews = len(df)
        
        positive_rate = sentiment_dist.get('Positive', 0)
        negative_rate = sentiment_dist.get('Negative', 0)
        neutral_rate = sentiment_dist.get('Neutral', 0)
        
        # Generate more comprehensive insights
        if positive_rate > 75 and avg_rating > 4.0:
            insights.append({
                "type": "positive",
                "title": "Excellent User Satisfaction",
                "description": f"Your app shows outstanding performance with {positive_rate:.1f}% positive reviews and a {avg_rating:.1f} star average rating. Users are clearly delighted with your app."
            })
        elif positive_rate > 60:
            insights.append({
                "type": "positive",
                "title": "Strong User Satisfaction",
                "description": f"Your app is performing well with {positive_rate:.1f}% positive reviews. Users appreciate your app's features and functionality."
            })
        
        if negative_rate > 35:
            insights.append({
                "type": "warning",
                "title": "Significant Improvement Needed",
                "description": f"With {negative_rate:.1f}% negative feedback, there are clear opportunities to enhance user experience. Focus on addressing the most common complaints."
            })
        elif negative_rate > 20:
            insights.append({
                "type": "warning",
                "title": "Areas for Improvement",
                "description": f"With {negative_rate:.1f}% negative feedback, there are some areas that need attention to improve user satisfaction."
            })
        
        if total_reviews > 1000:
            insights.append({
                "type": "positive",
                "title": "Exceptional User Engagement",
                "description": f"Your app has generated {total_reviews:,} reviews, indicating exceptional user engagement and strong market presence."
            })
        elif total_reviews > 500:
            insights.append({
                "type": "positive",
                "title": "Strong User Engagement",
                "description": f"Your app has generated {total_reviews:,} reviews, indicating solid user engagement and market presence."
            })
        
        rating_std = df['score'].std()
        if rating_std < 0.8:
            insights.append({
                "type": "positive",
                "title": "Consistent User Experience",
                "description": f"Your ratings show low variance ({rating_std:.2f}), suggesting a consistent user experience across different user types."
            })
        else:
            insights.append({
                "type": "warning",
                "title": "Inconsistent User Experience",
                "description": f"Your ratings show high variance ({rating_std:.2f}), suggesting inconsistent experiences that may need addressing."
            })
            
        # Check for recent trends
        if 'at' in df.columns:
            df['date'] = pd.to_datetime(df['at'])
            recent_reviews = df[df['date'] > (datetime.now() - timedelta(days=30))]
            if len(recent_reviews) > 0:
                recent_positive = (recent_reviews['sentiment'] == 'Positive').mean() * 100
                if recent_positive > (positive_rate + 10):
                    insights.append({
                        "type": "positive",
                        "title": "Improving Trend",
                        "description": f"Recent reviews show improvement with {recent_positive:.1f}% positive feedback, compared to your overall {positive_rate:.1f}%."
                    })
                elif recent_positive < (positive_rate - 10):
                    insights.append({
                        "type": "warning",
                        "title": "Declining Trend",
                        "description": f"Recent reviews show a decline with only {recent_positive:.1f}% positive feedback, compared to your overall {positive_rate:.1f}%."
                    })
        
        return insights[:5]
        
    except Exception as e:
        return [{
            "type": "neutral",
            "title": "Analysis Incomplete",
            "description": f"Could not generate all insights due to an error: {str(e)}"
        }]

def extract_keywords(text_series, n=10):
    all_text = ' '.join([str(text) for text in text_series if pd.notna(text)])
    words = re.findall(r'\b[a-zA-Z]{4,}\b', all_text.lower())
    word_counts = Counter(words)
    # Remove common stop words
    stop_words = {'this', 'that', 'with', 'have', 'from', 'they', 'what', 'when', 'were', 'your', 'just', 'like', 'than', 'because', 'very', 'much', 'more', 'some', 'will', 'about', 'their', 'should', 'would', 'could'}
    filtered_words = {word: count for word, count in word_counts.items() if word not in stop_words}
    return dict(Counter(filtered_words).most_common(n))

def create_charts(df_a, df_b=None):
    charts = {}
    
    # Clean color scheme
    colors = {
        'Positive': '#1a8917',
        'Neutral': '#f59e0b', 
        'Negative': '#dc2626'
    }
    
    template = {
        'layout': {
            'plot_bgcolor': '#ffffff',
            'paper_bgcolor': '#ffffff',
            'font': {'color': '#242424', 'family': 'system-ui, sans-serif'},
            'colorway': ['#1a8917', '#0ea5e9', '#dc2626', '#f59e0b', '#8b5cf6']
        }
    }
    
    if df_b is not None and not df_b.empty:
        # Comparison chart
        sentiment_a = df_a['sentiment'].value_counts(normalize=True) * 100
        sentiment_b = df_b['sentiment'].value_counts(normalize=True) * 100
        
        fig = go.Figure()
        
        sentiments = ['Positive', 'Neutral', 'Negative']
        x_pos = [0.8, 1.8, 2.8]
        x_pos_b = [1.2, 2.2, 3.2]
        
        fig.add_trace(go.Bar(
            name='First App',
            x=x_pos,
            y=[sentiment_a.get(s, 0) for s in sentiments],
            marker_color='#1a8917',
            width=0.35
        ))
        
        fig.add_trace(go.Bar(
            name='Second App',
            x=x_pos_b,
            y=[sentiment_b.get(s, 0) for s in sentiments],
            marker_color='#0ea5e9',
            width=0.35
        ))
        
        fig.update_layout(
            title='Sentiment Comparison',
            xaxis_title='Sentiment Categories',
            yaxis_title='Percentage of Reviews',
            xaxis=dict(tickvals=[1, 2, 3], ticktext=sentiments),
            template=template,
            showlegend=True,
            barmode='group'
        )
        
        charts['comparison'] = fig
        
        # Rating comparison
        fig_rating = go.Figure()
        fig_rating.add_trace(go.Box(
            y=df_a['score'],
            name='First App',
            marker_color='#1a8917'
        ))
        fig_rating.add_trace(go.Box(
            y=df_b['score'],
            name='Second App',
            marker_color='#0ea5e9'
        ))
        fig_rating.update_layout(
            title='Rating Distribution Comparison',
            yaxis_title='Rating (1-5 stars)',
            template=template
        )
        charts['rating_comparison'] = fig_rating
    
    else:
        # Single app chart
        sentiment_counts = df_a['sentiment'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=0.4,
            marker=dict(colors=[colors.get(label, '#6b6b6b') for label in sentiment_counts.index]),
            textinfo='label+percent',
            textfont=dict(size=14, color='#242424')
        )])
        
        fig.update_layout(
            title="Sentiment Distribution",
            template=template,
            annotations=[dict(text=f'Total<br>{sentiment_counts.sum()}', x=0.5, y=0.5, font_size=16, showarrow=False)]
        )
        
        charts['sentiment'] = fig
        
        # Rating distribution
        rating_counts = df_a['score'].value_counts().sort_index()
        fig_rating = go.Figure(data=[go.Bar(
            x=rating_counts.index.astype(str),
            y=rating_counts.values,
            marker_color='#1a8917'
        )])
        fig_rating.update_layout(
            title="Rating Distribution",
            xaxis_title="Rating",
            yaxis_title="Number of Reviews",
            template=template
        )
        charts['rating_dist'] = fig_rating
        
        # Time series of reviews
        if 'at' in df_a.columns:
            df_a['date'] = pd.to_datetime(df_a['at'])
            daily_reviews = df_a.groupby(df_a['date'].dt.date).size()
            fig_time = go.Figure(data=[go.Scatter(
                x=daily_reviews.index,
                y=daily_reviews.values,
                mode='lines+markers',
                line=dict(color='#1a8917', width=2),
                marker=dict(size=4)
            )])
            fig_time.update_layout(
                title="Reviews Over Time",
                xaxis_title="Date",
                yaxis_title="Number of Reviews",
                template=template
            )
            charts['reviews_over_time'] = fig_time
    
    return charts

def display_review_cards(df, max_reviews=10):
    if 'at' in df.columns:
        df_sorted = df.sort_values('at', ascending=False).head(max_reviews)
    else:
        df_sorted = df.head(max_reviews)
    
    for _, review in df_sorted.iterrows():
        sentiment = review.get('sentiment', 'Neutral')
        badge_class = f"sentiment-{sentiment.lower()}"
        
        rating = review.get('score', 0)
        stars = "★" * int(rating) + "☆" * (5 - int(rating))
        
        if 'at' in review and pd.notna(review['at']):
            date_str = pd.to_datetime(review['at']).strftime('%B %d, %Y')
        else:
            date_str = "Date not available"
        
        content = str(review.get('content', 'No content available'))
        if len(content) > 400:
            content = content[:400] + "..."
        
        st.markdown(f"""
        <div class="review-card">
            <div class="review-header">
                <div class="review-author">{review.get('userName', 'Anonymous User')}</div>
                <div class="review-rating">
                    <span class="star">{stars}</span>
                    <span>{rating}/5</span>
                </div>
            </div>
            <div class="review-content">{content}</div>
            <div class="review-meta">
                <div>{date_str}</div>
                <div class="sentiment-tag {badge_class}">{sentiment}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Show Navigation
show_navigation()

# HOME PAGE
if st.session_state.page == 'home':
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Transform App Reviews Into Actionable Insights</h1>
        <p class="hero-subtitle">
            Discover what your users really think with advanced sentiment analysis, 
            competitive benchmarking, and detailed review intelligence.
        </p>
        <div>
            <button class="primary-button" onclick="window.navigateTo('analysis')">Start Analysis</button>
            <button class="secondary-button" onclick="window.navigateTo('about')">Learn More</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <div class="content-container">
        <div class="section">
            <h2 class="section-title">Everything You Need to Understand Your Users</h2>
            <p class="section-subtitle">
                Our platform combines artificial intelligence with intuitive design to help you 
                make data-driven decisions about your app's future.
            </p>
            
            <div class="features-grid">
                <div class="feature-card">
                    <h3 class="feature-title">Smart Sentiment Analysis</h3>
                    <p class="feature-description">
                        Our advanced algorithms analyze thousands of reviews to understand exactly how users feel about your app. 
                        Get detailed breakdowns of positive, negative, and neutral feedback with confidence scores.
                    </p>
                </div>
                
                <div class="feature-card">
                    <h3 class="feature-title">Competitive Intelligence</h3>
                    <p class="feature-description">
                        Compare your app directly with competitors. See how you stack up in user satisfaction, 
                        feature preferences, and market positioning to identify opportunities for growth.
                    </p>
                </div>
                
                <div class="feature-card">
                    <h3 class="feature-title">Topic Discovery</h3>
                    <p class="feature-description">
                        Automatically identify the most important themes in user feedback. Discover what features 
                        users love, what frustrates them, and what they're asking for next.
                    </p>
                </div>
                
                <div class="feature-card">
                    <h3 class="feature-title">Individual Review Reading</h3>
                    <p class="feature-description">
                        Dive deep into individual user experiences. Read complete reviews with context, 
                        ratings, and sentiment classification to understand the full story behind the data.
                    </p>
                </div>
                
                <div class="feature-card">
                    <h3 class="feature-title">Professional Reports</h3>
                    <p class="feature-description">
                        Generate comprehensive reports perfect for sharing with your team or stakeholders. 
                        Include charts, insights, and recommendations in a clean, professional format.
                    </p>
                </div>
                
                <div class="feature-card">
                    <h3 class="feature-title">Real-Time Analysis</h3>
                    <p class="feature-description">
                        Get instant results as soon as you submit your app's link. Our system processes 
                        reviews in real-time, so you always have the most current insights available.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ABOUT PAGE
elif st.session_state.page == 'about':
    st.markdown("""
    <div class="about-hero">
        <h1 class="hero-title">About Feedback Forge</h1>
        <p class="hero-subtitle">
            We help app developers and product managers make better decisions 
            by understanding what their users really think.
        </p>
    </div>
    
    <div class="about-content">
        <div class="about-section">
            <h2>Our Mission</h2>
            <p>
                In today's competitive app landscape, user feedback is more valuable than ever. 
                But with thousands of reviews across different platforms, it's nearly impossible 
                to manually analyze what users are actually saying about your product.
            </p>
            <p>
                That's where Feedback Forge comes in. We've built a platform that automatically 
                processes app store reviews, identifies key themes, and presents actionable insights 
                in a way that's easy to understand and act upon.
            </p>
        </div>
        
        <div class="about-section">
            <h2>How It Works</h2>
            <p>
                Our system uses advanced natural language processing to understand the context 
                and emotion behind each review. We don't just count positive and negative words – 
                we understand the nuance of human language and can identify specific issues, 
                feature requests, and areas of praise.
            </p>
            <p>
                The process is simple: you provide a link to your app on the Google Play Store, 
                and we handle the rest. Within minutes, you'll have a comprehensive analysis 
                of user sentiment, key topics, and competitive positioning.
            </p>
        </div>
        
        <div class="about-section">
            <h2>Why We Built This</h2>
            <p>
                As developers ourselves, we understand the challenge of staying connected with 
                your users as your app grows. Reading every review becomes impossible, but 
                missing important feedback can be costly.
            </p>
            <p>
                We wanted to create a tool that scales with your success – something that can 
                process thousands of reviews as easily as dozens, while still preserving the 
                human insight that makes user feedback so valuable.
            </p>
        </div>
        
        <div class="about-section">
            <h2>Our Approach</h2>
            <p>
                We believe in making complex data simple and actionable. Our reports focus on 
                the insights that matter most: what's working well, what needs improvement, 
                and how you compare to your competition.
            </p>
            <p>
                Every analysis includes both high-level trends and specific examples, so you 
                can see the big picture while still understanding individual user experiences. 
                We also provide recommendations based on patterns we've identified across 
                thousands of successful apps.
            </p>
        </div>
        
        <div class="about-section">
            <h2>Get Started Today</h2>
            <p>
                Ready to understand what your users really think? Our analysis takes just a 
                few minutes and provides insights that typically take weeks to gather manually.
            </p>
            <p>
                Whether you're launching a new feature, responding to user complaints, or 
                planning your product roadmap, Feedback Forge gives you the data you need 
                to make confident decisions.
            </p>
        </div>
        
        <div class="developer-credit">
            <h3>Developed by Ayush Pandey</h3>
            <p>Feedback Forge was created with passion for helping developers understand their users better.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ANALYSIS PAGE
elif st.session_state.page == 'analysis':
    st.markdown("""
    <div class="content-container">
        <div class="section">
            <h1 class="section-title">App Review Analysis</h1>
            <p class="section-subtitle">
                Enter your app's Google Play Store URL to get detailed insights about user sentiment and feedback themes.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Analysis Form
    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        
        # Mode Selection
        st.markdown('<h2 class="form-title">Choose Analysis Type</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Single App Analysis", type="primary", key="single_btn", use_container_width=True):
                st.session_state.comparison_mode = False
                st.rerun()
        
        with col2:
            if st.button("Compare Two Apps", type="secondary", key="compare_btn", use_container_width=True):
                st.session_state.comparison_mode = True
                st.rerun()
        
        st.markdown("---")
        
        # URL Input
        if st.session_state.comparison_mode:
            st.markdown("### App Comparison")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**First App**")
                url_a = st.text_input("Google Play Store URL", placeholder="https://play.google.com/store/apps/details?id=com.example.app", key="url_a")
            
            with col2:
                st.markdown("**Second App**")
                url_b = st.text_input("Google Play Store URL", placeholder="https://play.google.com/store/apps/details?id=com.example.app", key="url_b")
        else:
            st.markdown("### App Analysis")
            url_a = st.text_input("Google Play Store URL", placeholder="https://play.google.com/store/apps/details?id=com.example.app", key="url_a_single")
            url_b = None
        
        # Analysis Parameters
        st.markdown("### Analysis Settings")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            count = st.slider("Number of Reviews", 50, 1000, 300, 50, key="review_count")
        with col2:
            language = st.selectbox("Language", ["en", "hi", "es", "fr", "de", "ja"], key="language_select")
        with col3:
            sort_by = st.selectbox("Sort By", ["NEWEST", "MOST_RELEVANT", "RATING"], key="sort_select")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Start Analysis Button
        if st.button("Start Analysis", type="primary", key="start_analysis", use_container_width=True):
            if not url_a.strip():
                st.error("Please enter at least one app URL to begin analysis.")
                st.stop()
            
            if st.session_state.comparison_mode and not url_b.strip():
                st.error("Please enter both app URLs for comparison analysis.")
                st.stop()
            
            package_a = extract_package_name(url_a)
            package_b = extract_package_name(url_b) if st.session_state.comparison_mode and url_b else None
            
            if not package_a:
                st.error("Please enter a valid Google Play Store URL.")
                st.stop()
            
            if st.session_state.comparison_mode and not package_b:
                st.error("Please enter valid Google Play Store URLs for both apps.")
                st.stop()
            
            # Progress indicator
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                sort_mapping = {"NEWEST": Sort.NEWEST, "MOST_RELEVANT": Sort.MOST_RELEVANT, "RATING": Sort.RATING}
                
                # Process first app
                status_text.markdown('<p class="loading-pulse">Analyzing app reviews...</p>', unsafe_allow_html=True)
                result_a, continuation_token = reviews(
                    package_a, 
                    lang=language, 
                    country="us", 
                    sort=sort_mapping[sort_by], 
                    count=count
                )
                
                if result_a:
                    df_a = pd.DataFrame(result_a)
                    df_a["package"] = package_a
                    df_a["app_name"] = get_app_name(package_a)
                    
                    # Analyze sentiment with progress
                    status_text.markdown('<p class="loading-pulse">Analyzing sentiment...</p>', unsafe_allow_html=True)
                    sentiment_results = df_a["content"].apply(analyze_sentiment_advanced)
                    df_a["sentiment"] = [r[0] for r in sentiment_results]
                    df_a["polarity_score"] = [r[1] for r in sentiment_results]
                    df_a["subjectivity_score"] = [r[2] for r in sentiment_results]
                    df_a["business_impact"] = [r[3] for r in sentiment_results]
                    df_a["at"] = pd.to_datetime(df_a["at"])
                else:
                    st.error("Could not retrieve reviews for the first app. Please check the URL.")
                    st.stop()
                
                progress_bar.progress(0.5)
                
                # Process second app if needed
                df_b = None
                if st.session_state.comparison_mode and package_b:
                    status_text.markdown('<p class="loading-pulse">Analyzing second app...</p>', unsafe_allow_html=True)
                    result_b, _ = reviews(
                        package_b, 
                        lang=language, 
                        country="us", 
                        sort=sort_mapping[sort_by], 
                        count=count
                    )
                    
                    if result_b:
                        df_b = pd.DataFrame(result_b)
                        df_b["package"] = package_b
                        df_b["app_name"] = get_app_name(package_b)
                        
                        sentiment_results = df_b["content"].apply(analyze_sentiment_advanced)
                        df_b["sentiment"] = [r[0] for r in sentiment_results]
                        df_b["polarity_score"] = [r[1] for r in sentiment_results]
                        df_b["subjectivity_score"] = [r[2] for r in sentiment_results]
                        df_b["business_impact"] = [r[3] for r in sentiment_results]
                        df_b["at"] = pd.to_datetime(df_b["at"])
                    else:
                        st.error("Could not retrieve reviews for the second app. Please check the URL.")
                        st.stop()
                
                progress_bar.progress(1.0)
                status_text.markdown('<p class="loading-pulse">Analysis complete! Generating report...</p>', unsafe_allow_html=True)
                
                # Store data in session state
                st.session_state.analysis_data = {
                    'df_a': df_a,
                    'df_b': df_b,
                    'package_a': package_a,
                    'package_b': package_b
                }
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                st.rerun()
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                progress_bar.empty()
                status_text.empty()
    
    # Display results if analysis is complete
    if st.session_state.analysis_data:
        data = st.session_state.analysis_data
        df_a = data['df_a']
        df_b = data['df_b']
        package_a = data['package_a']
        package_b = data['package_b']
        
        # Display Results
        st.success(f"Successfully analyzed {len(df_a):,} reviews" + (f" and {len(df_b):,} reviews" if df_b is not None else ""))
        
        # Metrics Section
        if st.session_state.comparison_mode and df_b is not None:
            st.markdown("## Comparison Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"### {get_app_name(package_a)}")
                st.markdown(f"""
                <div class="metrics-row">
                    <div class="metric-card">
                        <div class="metric-value">{len(df_a):,}</div>
                        <div class="metric-label">Reviews</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{df_a['score'].mean():.1f}</div>
                        <div class="metric-label">Avg Rating</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%</div>
                        <div class="metric-label">Positive</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"### {get_app_name(package_b)}")
                st.markdown(f"""
                <div class="metrics-row">
                    <div class="metric-card">
                        <div class="metric-value">{len(df_b):,}</div>
                        <div class="metric-label">Reviews</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{df_b['score'].mean():.1f}</div>
                        <div class="metric-label">Avg Rating</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{(df_b['sentiment'] == 'Positive').mean() * 100:.1f}%</div>
                        <div class="metric-label">Positive</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.markdown("## Analysis Results")
            st.markdown(f"""
            <div class="metrics-row">
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
                    <div class="metric-label">Positive Reviews</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{df_a['polarity_score'].mean():.2f}</div>
                    <div class="metric-label">Sentiment Score</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Highlight key metrics
            positive_rate = (df_a['sentiment'] == 'Positive').mean() * 100
            if positive_rate > 70:
                st.markdown(f"""
                <div class="result-highlight">
                    <h3>Excellent User Satisfaction! 🎉</h3>
                    <p>Your app has {positive_rate:.1f}% positive reviews, indicating strong user satisfaction.</p>
                </div>
                """, unsafe_allow_html=True)
            elif positive_rate > 50:
                st.markdown(f"""
                <div class="result-highlight">
                    <h3>Good User Satisfaction 👍</h3>
                    <p>Your app has {positive_rate:.1f}% positive reviews, with room for improvement.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-highlight">
                    <h3>Needs Improvement ⚠️</h3>
                    <p>Your app has only {positive_rate:.1f}% positive reviews. Consider addressing user feedback.</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Charts
        charts = create_charts(df_a, df_b)
        for chart_name, chart in charts.items():
            st.plotly_chart(chart, use_container_width=True)
        
        # Keyword analysis
        if not st.session_state.comparison_mode:
            st.markdown("## Top Keywords in Reviews")
            keywords = extract_keywords(df_a['content'])
            keyword_html = " ".join([f'<span class="keyword-pill">{word} ({count})</span>' for word, count in keywords.items()])
            st.markdown(f'<div style="margin: 20px 0;">{keyword_html}</div>', unsafe_allow_html=True)
        
        # Insights
        insights_a = generate_insights(df_a)
        if insights_a:
            st.markdown(f"""
            <div class="insights-container">
                <h2 class="results-header">Key Insights for {get_app_name(package_a)}</h2>
            """, unsafe_allow_html=True)
            
            for insight in insights_a:
                css_class = 'insight-item' if insight['type'] == 'positive' else 'insight-item warning'
                st.markdown(f"""
                <div class="{css_class}">
                    <div class="insight-title">{insight['title']}</div>
                    <div class="insight-description">{insight['description']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        if df_b is not None:
            insights_b = generate_insights(df_b)
            if insights_b:
                st.markdown(f"""
                <div class="insights-container">
                    <h2 class="results-header">Key Insights for {get_app_name(package_b)}</h2>
                """, unsafe_allow_html=True)
                
                for insight in insights_b:
                    css_class = 'insight-item' if insight['type'] == 'positive' else 'insight-item warning'
                    st.markdown(f"""
                    <div class="{css_class}">
                        <div class="insight-title">{insight['title']}</div>
                        <div class="insight-description">{insight['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Individual Reviews
        st.markdown(f"""
        <div class="results-container">
            <h2 class="results-header">Recent Reviews for {get_app_name(package_a)}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        display_review_cards(df_a, 10)
        
        if df_b is not None:
            st.markdown(f"""
            <div class="results-container">
                <h2 class="results-header">Recent Reviews for {get_app_name(package_b)}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            display_review_cards(df_b, 10)
        
        # Export Options
        st.markdown("## Export Results")
        col1, col2 = st.columns(2)
        
        with col1:
            if df_b is not None:
                combined_df = pd.concat([df_a, df_b], ignore_index=True)
                csv_data = combined_df.to_csv(index=False).encode('utf-8')
            else:
                csv_data = df_a.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                "Download Complete Data (CSV)",
                data=csv_data,
                file_name=f"feedback_forge_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Create summary data
            if df_b is not None:
                summary_data = [{
                    "App": get_app_name(package_a),
                    "Reviews": len(df_a),
                    "Avg_Rating": round(df_a["score"].mean(), 2),
                    "Positive_Percent": f"{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%"
                }, {
                    "App": get_app_name(package_b),
                    "Reviews": len(df_b),
                    "Avg_Rating": round(df_b["score"].mean(), 2),
                    "Positive_Percent": f"{(df_b['sentiment'] == 'Positive').mean() * 100:.1f}%"
                }]
            else:
                summary_data = [{
                    "App": get_app_name(package_a),
                    "Reviews": len(df_a),
                    "Avg_Rating": round(df_a["score"].mean(), 2),
                    "Positive_Percent": f"{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%"
                }]
            
            summary_df = pd.DataFrame(summary_data)
            summary_csv = summary_df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                "Download Summary (CSV)",
                data=summary_csv,
                file_name=f"feedback_forge_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# Footer with developer credit
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <div class="footer-brand">Feedback Forge</div>
        <p class="footer-text">
            Transform app reviews into actionable insights with advanced sentiment analysis and competitive intelligence.
        </p>
        <p class="footer-text">
            Developed by Ayush Pandey • Built with care for developers and product managers who want to understand their users better.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
