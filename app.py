import streamlit as st
import pandas as pd
from google_play_scraper import Sort, reviews, app
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re
from collections import Counter
import numpy as np
import json
from urllib.parse import urlparse, parse_qs

# Page Configuration
st.set_page_config(
    page_title="Feedback Forge",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Medium-inspired design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Header Styles */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2E7D32;
        text-align: center;
        margin: 2rem 0;
    }
    
    /* Navigation Styles */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .nav-item {
        padding: 0.5rem 1rem;
        cursor: pointer;
        border-radius: 20px;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .nav-item:hover {
        background-color: #f5f5f5;
    }
    
    .nav-item.active {
        background-color: #2E7D32;
        color: white;
    }
    
    /* Card Styles */
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #2E7D32;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        color: #666;
        line-height: 1.6;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        margin: 2rem 0;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    /* Input Section */
    .input-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    /* Analysis Results */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2E7D32;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Button Styles */
    .stButton button {
        background-color: #2E7D32;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #1B5E20;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None

# Helper Functions
def extract_app_id_from_url(url):
    """Extract app ID from Google Play Store URL"""
    try:
        if 'play.google.com' in url:
            if 'id=' in url:
                return url.split('id=')[1].split('&')[0]
            else:
                # Handle different URL formats
                parts = url.split('/')
                if 'details' in parts:
                    idx = parts.index('details')
                    if idx + 1 < len(parts):
                        return parts[idx + 1].split('?')[0]
        return None
    except:
        return None

def get_sentiment_color(sentiment):
    """Return color based on sentiment"""
    if sentiment > 0.1:
        return '#4CAF50'  # Green for positive
    elif sentiment < -0.1:
        return '#F44336'  # Red for negative
    else:
        return '#FF9800'  # Orange for neutral

def analyze_reviews(app_id, count=500):
    """Analyze app reviews"""
    try:
        # Fetch app details
        app_details = app(app_id)
        
        # Fetch reviews
        result, continuation_token = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=count
        )
        
        if not result:
            return None, "No reviews found"
        
        # Convert to DataFrame
        df = pd.DataFrame(result)
        
        # Sentiment Analysis
        sentiments = []
        for review_text in df['content']:
            if review_text:
                blob = TextBlob(str(review_text))
                sentiments.append(blob.sentiment.polarity)
            else:
                sentiments.append(0)
        
        df['sentiment'] = sentiments
        df['sentiment_label'] = df['sentiment'].apply(
            lambda x: 'Positive' if x > 0.1 else ('Negative' if x < -0.1 else 'Neutral')
        )
        
        # Theme extraction
        all_text = ' '.join(df['content'].dropna().astype(str))
        words = re.findall(r'\b[a-zA-Z]{3,}\b', all_text.lower())
        
        # Filter out common words
        stop_words = {'the', 'and', 'app', 'this', 'that', 'with', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'use', 'man', 'new', 'now', 'old', 'see', 'him', 'two', 'how', 'its', 'who', 'oil', 'sit', 'set'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        
        word_freq = Counter(filtered_words)
        top_themes = dict(word_freq.most_common(10))
        
        analysis_results = {
            'app_details': app_details,
            'reviews_df': df,
            'total_reviews': len(df),
            'avg_rating': df['score'].mean(),
            'avg_sentiment': np.mean(sentiments),
            'sentiment_distribution': df['sentiment_label'].value_counts().to_dict(),
            'rating_distribution': df['score'].value_counts().sort_index().to_dict(),
            'top_themes': top_themes,
            'recent_reviews': df.head(10)
        }
        
        return analysis_results, None
        
    except Exception as e:
        return None, f"Error analyzing reviews: {str(e)}"

# Navigation
def show_navigation():
    st.markdown("""
    <div class="nav-container">
        <div class="nav-item {}" onclick="window.location.reload()">🏠 Home</div>
        <div class="nav-item">📋 About</div>
        <div class="nav-item">📊 Analysis</div>
    </div>
    """.format('active' if st.session_state.page == 'home' else ''), unsafe_allow_html=True)

# Home Page
def show_home_page():
    st.markdown('<h1 class="main-header">📊 Feedback Forge</h1>', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h2 class="hero-title">App Review Analysis Made Simple</h2>
        <p class="hero-subtitle">Discover what your users really think with advanced sentiment analysis and feedback intelligence.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### 🔗 Enter Your App's Google Play Store URL")
    
    app_url = st.text_input(
        "App URL",
        placeholder="https://play.google.com/store/apps/details?id=com.example.app",
        help="Paste your app's Google Play Store URL here"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button("🔍 Analyze Reviews", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis Logic
    if analyze_button and app_url:
        app_id = extract_app_id_from_url(app_url)
        
        if not app_id:
            st.error("❌ Invalid Google Play Store URL. Please check the format.")
            return
        
        with st.spinner("🔄 Analyzing reviews... This may take a few minutes."):
            analysis_results, error = analyze_reviews(app_id)
            
            if error:
                st.error(f"❌ {error}")
                return
            
            st.session_state.analysis_data = analysis_results
            show_analysis_results(analysis_results)
    
    elif st.session_state.analysis_data:
        show_analysis_results(st.session_state.analysis_data)
    
    else:
        # Features Section
        st.markdown("## ✨ Key Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">🎯 Sentiment Analysis</div>
                <div class="feature-description">Advanced AI algorithms analyze user emotions and satisfaction levels in reviews.</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">🔍 Theme Detection</div>
                <div class="feature-description">Automatically identify key topics and issues mentioned in user feedback.</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">📈 Visual Analytics</div>
                <div class="feature-description">Interactive charts and graphs to visualize review patterns and trends.</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">⚡ Real-time Processing</div>
                <div class="feature-description">Get instant insights from thousands of reviews in just minutes.</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">📊 Comprehensive Reports</div>
                <div class="feature-description">Detailed analytics with actionable insights and recommendations.</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">🎨 Beautiful Interface</div>
                <div class="feature-description">Clean, intuitive design that makes complex data easy to understand.</div>
            </div>
            """, unsafe_allow_html=True)

def show_analysis_results(results):
    """Display comprehensive analysis results"""
    st.markdown("## 📊 Analysis Results")
    
    # App Info
    app_info = results['app_details']
    st.markdown(f"### 📱 {app_info['title']}")
    st.markdown(f"**Developer:** {app_info['developer']}")
    st.markdown(f"**Category:** {app_info['genre']}")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['total_reviews']}</div>
            <div class="metric-label">Total Reviews Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['avg_rating']:.1f}</div>
            <div class="metric-label">Average Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        sentiment_score = results['avg_sentiment']
        sentiment_text = "Positive" if sentiment_score > 0.1 else ("Negative" if sentiment_score < -0.1 else "Neutral")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {get_sentiment_color(sentiment_score)}">{sentiment_text}</div>
            <div class="metric-label">Overall Sentiment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        positive_pct = (results['sentiment_distribution'].get('Positive', 0) / results['total_reviews']) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{positive_pct:.1f}%</div>
            <div class="metric-label">Positive Reviews</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment Distribution
        sentiment_data = results['sentiment_distribution']
        fig_sentiment = px.pie(
            values=list(sentiment_data.values()),
            names=list(sentiment_data.keys()),
            title="📈 Sentiment Distribution",
            color_discrete_map={'Positive': '#4CAF50', 'Negative': '#F44336', 'Neutral': '#FF9800'}
        )
        fig_sentiment.update_layout(showlegend=True)
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    with col2:
        # Rating Distribution
        rating_data = results['rating_distribution']
        fig_rating = px.bar(
            x=list(rating_data.keys()),
            y=list(rating_data.values()),
            title="⭐ Rating Distribution",
            labels={'x': 'Rating', 'y': 'Number of Reviews'}
        )
        fig_rating.update_traces(marker_color='#2E7D32')
        st.plotly_chart(fig_rating, use_container_width=True)
    
    # Top Themes
    st.markdown("### 🔍 Top Themes in Reviews")
    themes_data = results['top_themes']
    fig_themes = px.bar(
        x=list(themes_data.values()),
        y=list(themes_data.keys()),
        orientation='h',
        title="Most Mentioned Topics"
    )
    fig_themes.update_traces(marker_color='#2E7D32')
    fig_themes.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_themes, use_container_width=True)
    
    # Recent Reviews Sample
    st.markdown("### 💬 Recent Reviews Sample")
    recent_reviews = results['recent_reviews']
    
    for idx, review in recent_reviews.iterrows():
        sentiment_color = get_sentiment_color(review['sentiment'])
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {sentiment_color};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong>Rating: {'⭐' * review['score']}</strong>
                <span style="color: {sentiment_color}; font-weight: bold;">
                    {review['sentiment_label']}
                </span>
            </div>
            <p style="margin: 0; color: #333;">{review['content'][:300]}{'...' if len(str(review['content'])) > 300 else ''}</p>
        </div>
        """, unsafe_allow_html=True)

# Main App Logic
def main():
    show_navigation()
    
    if st.session_state.page == 'home':
        show_home_page()

if __name__ == "__main__":
    main()
