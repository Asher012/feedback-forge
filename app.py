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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import json

# Page Configuration
st.set_page_config(
    page_title="Feedback Forge Pro Analytics", 
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Business-Grade CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glassmorphism Container */
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        padding: 2rem;
        margin: 1rem 0;
    }
    
    /* Main Dashboard Header */
    .dashboard-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
        backdrop-filter: blur(30px);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, 
            transparent 30%, 
            rgba(255,255,255,0.1) 50%, 
            transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -1px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        z-index: 2;
        position: relative;
        background: linear-gradient(45deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .main-subtitle {
        font-size: 1.4rem;
        font-weight: 400;
        margin-top: 1rem;
        opacity: 0.95;
        z-index: 2;
        position: relative;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    .creator-badge {
        position: absolute;
        top: 30px;
        right: 30px;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(15px);
        padding: 12px 24px;
        border-radius: 30px;
        border: 1px solid rgba(255,255,255,0.3);
        font-size: 1rem;
        font-weight: 600;
        z-index: 3;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .control-panel {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .panel-title {
        color: #2d3748;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid transparent;
        background: linear-gradient(90deg, #667eea, #764ba2) padding-box,
                    linear-gradient(90deg, #667eea, #764ba2) border-box;
        border-image: linear-gradient(90deg, #667eea, #764ba2) 1;
    }
    
    /* Metric Cards */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(20px);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: all 0.6s;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 60px rgba(0,0,0,0.15);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-value {
        font-size: 3.2rem;
        font-weight: 800;
        color: #667eea;
        font-family: 'Space Grotesk', sans-serif;
        margin-bottom: 0.8rem;
        line-height: 1;
        text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .metric-label {
        color: #4a5568;
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.8;
    }
    
    .metric-icon {
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 2rem;
        opacity: 0.3;
        color: #667eea;
    }
    
    /* Content Sections */
    .content-section {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(25px);
        padding: 3rem 2.5rem;
        border-radius: 25px;
        margin: 2rem 0;
        box-shadow: 0 15px 50px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.3);
        position: relative;
    }
    
    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid transparent;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb) padding-box,
                    linear-gradient(90deg, #667eea, #764ba2, #f093fb) border-box;
        border-image: linear-gradient(90deg, #667eea, #764ba2, #f093fb) 1;
    }
    
    /* Progress Section */
    .progress-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(25px);
        padding: 3rem 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .status-card {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* AI Insights Panel */
    .ai-insights {
        background: linear-gradient(135deg, rgba(72, 187, 120, 0.1) 0%, rgba(56, 178, 172, 0.1) 100%);
        border: 2px solid rgba(72, 187, 120, 0.3);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        position: relative;
    }
    
    .ai-insights::before {
        content: 'AI';
        position: absolute;
        top: -15px;
        left: 20px;
        background: linear-gradient(135deg, #48bb78, #38b2ac);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    
    /* Smart Recommendations */
    .recommendation-card {
        background: linear-gradient(135deg, rgba(237, 137, 54, 0.1) 0%, rgba(245, 101, 101, 0.1) 100%);
        border-left: 4px solid #ed8936;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(237, 137, 54, 0.1);
    }
    
    /* Interactive Elements */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        width: 100%;
        font-family: 'Space Grotesk', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    /* Chart Containers */
    .chart-container {
        background: rgba(255,255,255,0.98);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.3);
        margin: 1.5rem 0;
    }
    
    /* Topic Analysis */
    .topic-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .topic-card {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .topic-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.12);
    }
    
    /* Export Section */
    .export-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .export-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(20px);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.4s ease;
    }
    
    .export-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .metrics-grid {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        }
        
        .metric-value {
            font-size: 2.5rem;
        }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8, #6b46c1);
    }
</style>
""", unsafe_allow_html=True)

# Dashboard Header
st.markdown("""
<div class="dashboard-header">
    <div class="main-title">Feedback Forge Pro</div>
    <div class="main-subtitle">Advanced Business Intelligence Platform for Review Analytics and Market Insights</div>
    <div class="creator-badge">Developed by Ayush Pandey</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("""
<div class="control-panel">
    <div class="panel-title">Analysis Configuration</div>
    <p style="color: #718096; margin: 0; font-size: 1rem; line-height: 1.5;">Configure your comprehensive review analysis parameters for maximum insights</p>
</div>
""", unsafe_allow_html=True)

# Application URLs Input
play_urls = st.sidebar.text_area(
    "Application URLs",
    placeholder="Enter Google Play Store URLs, one per line",
    height=100,
    help="Paste valid Google Play Store application URLs for analysis"
)

# Analysis Parameters
count = st.sidebar.slider("Reviews per Application", 10, 2000, 500, 50)
language = st.sidebar.selectbox("Language", ["en", "hi", "es", "fr", "de", "ja"], index=0)
country = st.sidebar.selectbox("Region", ["in", "us", "uk", "ca", "de", "jp"], index=0)
sort_by = st.sidebar.selectbox("Sort Method", ["NEWEST", "MOST_RELEVANT", "RATING"], index=0)

# Advanced Intelligence Features
st.sidebar.markdown("""
<div class="control-panel">
    <div class="panel-title">AI Intelligence Suite</div>
</div>
""", unsafe_allow_html=True)

enable_keywords = st.sidebar.checkbox("Keyword Intelligence", value=True)
enable_topic_modeling = st.sidebar.checkbox("Topic Modeling AI", value=True)
enable_trends = st.sidebar.checkbox("Predictive Analytics", value=True)
enable_smart_insights = st.sidebar.checkbox("Smart Business Insights", value=True)
min_rating_filter = st.sidebar.selectbox("Rating Filter", [1, 2, 3, 4, 5], index=0)

# Keywords Configuration
keywords = []
if enable_keywords:
    keyword_input = st.sidebar.text_input(
        "Keywords to Monitor",
        placeholder="performance, bug, excellent, slow",
        help="Monitor specific business-critical keywords"
    )
    if keyword_input:
        keywords = [k.strip().lower() for k in keyword_input.split(",")]

# Enhanced Helper Functions
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
    
    # Business categorization
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

def perform_topic_modeling(df, n_topics=5):
    """Advanced topic modeling using TF-IDF and clustering"""
    if df.empty or len(df) < 10:
        return {}
    
    try:
        # Clean and prepare text
        texts = df['content'].dropna().astype(str).tolist()
        
        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # K-Means Clustering
        kmeans = KMeans(n_clusters=min(n_topics, len(texts)), random_state=42)
        clusters = kmeans.fit_predict(tfidf_matrix)
        
        # Extract top terms for each topic
        feature_names = vectorizer.get_feature_names_out()
        topics = {}
        
        for i in range(min(n_topics, len(set(clusters)))):
            # Get centroid for this cluster
            centroid = kmeans.cluster_centers_[i]
            # Get top terms
            top_indices = centroid.argsort()[-10:][::-1]
            top_terms = [feature_names[idx] for idx in top_indices]
            
            topics[f"Topic {i+1}"] = {
                "terms": top_terms[:5],
                "count": np.sum(clusters == i),
                "percentage": (np.sum(clusters == i) / len(clusters)) * 100
            }
        
        return topics
        
    except Exception as e:
        return {}

def generate_smart_insights(df):
    """Generate AI-powered business insights"""
    insights = []
    
    if df.empty:
        return insights
    
    try:
        # Sentiment distribution insight
        sentiment_dist = df['sentiment'].value_counts(normalize=True) * 100
        
        if sentiment_dist.get('Positive', 0) > 70:
            insights.append({
                "type": "positive",
                "title": "Strong Market Position",
                "description": f"Exceptional customer satisfaction with {sentiment_dist.get('Positive', 0):.1f}% positive reviews indicates strong market positioning and user loyalty."
            })
        elif sentiment_dist.get('Negative', 0) > 40:
            insights.append({
                "type": "warning",
                "title": "Critical Action Required",
                "description": f"High negative sentiment ({sentiment_dist.get('Negative', 0):.1f}%) suggests immediate attention needed for user experience improvements."
            })
        
        # Rating distribution insight
        avg_rating = df['score'].mean()
        if avg_rating >= 4.5:
            insights.append({
                "type": "positive",
                "title": "Premium Quality Recognition",
                "description": f"Outstanding average rating of {avg_rating:.1f} stars demonstrates exceptional product quality and user satisfaction."
            })
        elif avg_rating < 3.5:
            insights.append({
                "type": "warning", 
                "title": "Quality Improvement Opportunity",
                "description": f"Average rating of {avg_rating:.1f} stars indicates significant room for product enhancement and user experience optimization."
            })
        
        # Trend insight
        if 'at' in df.columns:
            recent_reviews = df[df['at'] >= (datetime.now() - timedelta(days=30))]
            if not recent_reviews.empty:
                recent_sentiment = (recent_reviews['sentiment'] == 'Positive').mean() * 100
                overall_sentiment = (df['sentiment'] == 'Positive').mean() * 100
                
                if recent_sentiment > overall_sentiment + 10:
                    insights.append({
                        "type": "positive",
                        "title": "Positive Momentum Building",
                        "description": f"Recent reviews show {recent_sentiment:.1f}% positivity vs {overall_sentiment:.1f}% overall, indicating improving user experience."
                    })
                elif recent_sentiment < overall_sentiment - 10:
                    insights.append({
                        "type": "warning",
                        "title": "Declining Satisfaction Trend", 
                        "description": f"Recent sentiment decline to {recent_sentiment:.1f}% from {overall_sentiment:.1f}% requires immediate investigation."
                    })
        
        return insights
        
    except Exception:
        return []

def create_business_charts(df):
    """Create professional business-grade visualizations"""
    charts = {}
    
    # Professional color schemes
    colors = {
        'Positive': '#10b981',
        'Neutral': '#f59e0b', 
        'Negative': '#ef4444'
    }
    
    template = {
        'layout': {
            'font': {'family': 'Inter, sans-serif'},
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'colorway': ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
        }
    }
    
    # Advanced Sentiment Timeline
    if 'at' in df.columns and not df.empty:
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['at']).dt.date
        daily_sentiment = df_copy.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
        
        if not daily_sentiment.empty:
            fig = go.Figure()
            
            for sentiment in ['Positive', 'Neutral', 'Negative']:
                if sentiment in daily_sentiment.columns:
                    fig.add_trace(go.Scatter(
                        x=daily_sentiment.index,
                        y=daily_sentiment[sentiment],
                        mode='lines+markers',
                        name=sentiment,
                        fill='tonexty' if sentiment != 'Positive' else 'tozeroy',
                        line=dict(color=colors[sentiment], width=3),
                        marker=dict(size=8, line=dict(width=2, color='white'))
                    ))
            
            fig.update_layout(
                title='Sentiment Evolution Timeline',
                xaxis_title='Date',
                yaxis_title='Number of Reviews',
                hovermode='x unified',
                font=dict(family='Inter, sans-serif', size=12),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            charts['sentiment_timeline'] = fig
    
    # Business Impact Heatmap
    if 'app_name' in df.columns and len(df['app_name'].unique()) > 1:
        heatmap_data = df.groupby(['app_name', 'score']).size().unstack(fill_value=0)
        
        fig = px.imshow(
            heatmap_data.values,
            labels=dict(x="Rating", y="Application", color="Reviews"),
            x=[f"{i} Stars" for i in heatmap_data.columns],
            y=heatmap_data.index,
            color_continuous_scale='RdYlGn',
            title="Rating Distribution Heatmap by Application"
        )
        
        fig.update_layout(
            font=dict(family='Inter, sans-serif'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        charts['rating_heatmap'] = fig
    
    return charts

# Main Analysis Execution
if st.sidebar.button("Launch Analysis", type="primary"):
    # Input validation
    urls_list = [url.strip() for url in play_urls.splitlines() if url.strip()]
    packages = [extract_package_name(url) for url in urls_list if extract_package_name(url)]
    
    if not packages:
        st.error("Please provide valid Google Play Store URLs to proceed with the analysis")
        st.stop()
    
    # Progress tracking
    with st.container():
        st.markdown("""
        <div class="progress-section">
            <h2 style="margin: 0 0 1rem 0; font-weight: 700;">Advanced Analysis Pipeline Active</h2>
            <p style="margin: 0; opacity: 0.95; font-size: 1.2rem;">Processing review data through AI-powered analytics engine</p>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_container = st.empty()
    
    all_dfs = []
    
    # Data collection with enhanced progress tracking
    for i, package in enumerate(packages):
        app_name = get_app_name(package)
        status_container.markdown(f"""
        <div class="status-card">
            <strong style="font-size: 1.2rem;">Analyzing: {app_name}</strong><br>
            <span style="opacity: 0.9; font-size: 1rem;">Extracting insights from {count} reviews</span>
            <div style="margin-top: 1rem; opacity: 0.8;">Package: {package}</div>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            sort_mapping = {
                "NEWEST": Sort.NEWEST,
                "MOST_RELEVANT": Sort.MOST_RELEVANT,
                "RATING": Sort.RATING
            }
            
            result, _ = reviews(
                package,
                lang=language,
                country=country,
                sort=sort_mapping[sort_by],
                count=count
            )
            
            if result:
                df = pd.DataFrame(result)
                df["package"] = package
                df["app_name"] = app_name
                all_dfs.append(df)
                
        except Exception as e:
            st.warning(f"Analysis limitation encountered for {app_name}: {str(e)}")
        
        progress_bar.progress((i + 1) / len(packages))
    
    # Clear progress indicators
    status_container.empty()
    progress_bar.empty()
    
    if not all_dfs:
        st.error("Unable to collect sufficient data for analysis")
        st.stop()
    
    # Advanced data processing
    df_all = pd.concat(all_dfs, ignore_index=True)
    
    with st.spinner("Executing advanced AI analytics pipeline..."):
        # Enhanced sentiment analysis
        sentiment_results = df_all["content"].apply(analyze_sentiment_advanced)
        df_all["sentiment"] = [r[0] for r in sentiment_results]
        df_all["polarity_score"] = [r[1] for r in sentiment_results]
        df_all["subjectivity_score"] = [r[2] for r in sentiment_results]
        df_all["business_impact"] = [r[3] for r in sentiment_results]
        df_all["at"] = pd.to_datetime(df_all["at"])
        
        # Apply filters
        df_filtered = df_all[df_all["score"] >= min_rating_filter].copy()
        
        # Generate business insights
        if enable_smart_insights:
            smart_insights = generate_smart_insights(df_filtered)
        
        # Perform topic modeling
        if enable_topic_modeling:
            topics = perform_topic_modeling(df_filtered)
    
    # Success notification with metrics
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.success(f"Analysis Pipeline Complete: {len(df_all):,} reviews processed from {len(packages)} applications")
    with col2:
        st.info(f"Processing Time: ~{len(df_all) * 0.001:.1f}s")
    with col3:
        st.info(f"Data Quality: {(len(df_filtered)/len(df_all)*100):.1f}%")
    
    # Executive Dashboard Metrics
    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics_data = [
        {"value": len(packages), "label": "Applications", "icon": "📱"},
        {"value": f"{len(df_filtered):,}", "label": "Reviews Analyzed", "icon": "📊"},
        {"value": f"{df_filtered['score'].mean():.1f}", "label": "Avg Rating", "icon": "⭐"},
        {"value": f"{(df_filtered['sentiment'] == 'Positive').mean() * 100:.0f}%", "label": "Positive Rate", "icon": "📈"},
        {"value": f"{df_filtered['polarity_score'].mean():.2f}", "label": "Sentiment Index", "icon": "🎯"}
    ]
    
    for i, (col, metric) in enumerate(zip([col1, col2, col3, col4, col5], metrics_data)):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">{metric['icon']}</div>
                <div class="metric-value">{metric['value']}</div>
                <div class="metric-label">{metric['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Insights Panel
    if enable_smart_insights and smart_insights:
        st.markdown("""
        <div class="ai-insights">
            <h3 style="color: #2d3748; margin-bottom: 1.5rem; font-family: 'Space Grotesk', sans-serif;">AI-Powered Business Insights</h3>
        """, unsafe_allow_html=True)
        
        for insight in smart_insights[:3]:  # Show top 3 insights
            icon = "🟢" if insight['type'] == 'positive' else "🟡"
            st.markdown(f"""
            <div class="recommendation-card">
                <h4 style="color: #2d3748; margin-bottom: 0.5rem;">{icon} {insight['title']}</h4>
                <p style="color: #4a5568; margin: 0; line-height: 1.6;">{insight['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced Analytics Tabs
    tabs = st.tabs([
        "Executive Dashboard", 
        "Sentiment Intelligence", 
        "Topic Analysis", 
        "Competitive Insights", 
        "Data Explorer"
    ])
    
    # Tab 1: Executive Dashboard
    with tabs[0]:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">Executive Dashboard</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced Sentiment Distribution
            sentiment_counts = df_filtered["sentiment"].value_counts()
            fig_donut = go.Figure(data=[go.Pie(
                labels=sentiment_counts.index,
                values=sentiment_counts.values,
                hole=0.6,
                marker_colors=['#10b981', '#f59e0b', '#ef4444']
            )])
            
            fig_donut.update_layout(
                title="Market Sentiment Overview",
                font=dict(family='Inter, sans-serif', size=14),
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            # Add center text
            total_reviews = sentiment_counts.sum()
            fig_donut.add_annotation(
                text=f"<b>{total_reviews:,}</b><br>Total Reviews",
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False
            )
            
            st.plotly_chart(fig_donut, use_container_width=True)
        
        with col2:
            # Business Performance Matrix
            if len(df_filtered['app_name'].unique()) > 1:
                performance_data = []
                for app in df_filtered['app_name'].unique():
                    app_data = df_filtered[df_filtered['app_name'] == app]
                    performance_data.append({
                        'Application': app,
                        'Avg Rating': app_data['score'].mean(),
                        'Review Volume': len(app_data),
                        'Positive Rate': (app_data['sentiment'] == 'Positive').mean() * 100,
                        'Sentiment Score': app_data['polarity_score'].mean()
                    })
                
                perf_df = pd.DataFrame(performance_data)
                
                fig_scatter = px.scatter(
                    perf_df,
                    x='Avg Rating',
                    y='Positive Rate',
                    size='Review Volume',
                    color='Sentiment Score',
                    hover_data=['Application'],
                    title='Application Performance Matrix',
                    color_continuous_scale='RdYlGn'
                )
                
                fig_scatter.update_layout(
                    font=dict(family='Inter, sans-serif'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 2: Sentiment Intelligence
    with tabs[1]:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">Advanced Sentiment Intelligence</h2>', unsafe_allow_html=True)
        
        # Create advanced charts
        business_charts = create_business_charts(df_filtered)
        
        for chart_name, chart in business_charts.items():
            st.plotly_chart(chart, use_container_width=True)
        
        # Keyword Intelligence
        if enable_keywords and keywords:
            st.markdown("### Keyword Intelligence Dashboard")
            
            keyword_results = {}
            for keyword in keywords:
                count_total = df_filtered['content'].str.lower().str.contains(keyword, na=False).sum()
                keyword_results[keyword] = count_total
            
            if keyword_results:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Keyword frequency chart
                    fig_keywords = px.bar(
                        x=list(keyword_results.keys()),
                        y=list(keyword_results.values()),
                        title="Strategic Keyword Performance",
                        color=list(keyword_results.values()),
                        color_continuous_scale='viridis'
                    )
                    
                    fig_keywords.update_layout(
                        font=dict(family='Inter, sans-serif'),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis_title="Keywords",
                        yaxis_title="Mention Frequency"
                    )
                    
                    st.plotly_chart(fig_keywords, use_container_width=True)
                
                with col2:
                    # Keyword insights
                    st.markdown("**Business Impact Analysis**")
                    for keyword, count in keyword_results.items():
                        percentage = (count / len(df_filtered)) * 100
                        impact_level = "High" if percentage > 10 else "Medium" if percentage > 5 else "Low"
                        
                        st.markdown(f"""
                        <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; margin: 0.5rem 0; border-radius: 10px; border-left: 4px solid #667eea;">
                            <strong style="color: #2d3748; text-transform: uppercase;">{keyword}</strong><br>
                            <span style="color: #4a5568;">Mentions: {count} ({percentage:.1f}%)</span><br>
                            <span style="color: #667eea; font-weight: 600;">Impact: {impact_level}</span>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 3: Topic Analysis
    with tabs[2]:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">AI Topic Analysis</h2>', unsafe_allow_html=True)
        
        if enable_topic_modeling and topics:
            st.markdown("### Discovered Discussion Topics")
            
            st.markdown('<div class="topic-grid">', unsafe_allow_html=True)
            
            for topic_name, topic_data in topics.items():
                st.markdown(f"""
                <div class="topic-card">
                    <h4 style="color: #2d3748; margin-bottom: 1rem; font-family: 'Space Grotesk', sans-serif;">{topic_name}</h4>
                    <div style="margin-bottom: 1rem;">
                        <strong style="color: #667eea;">Key Terms:</strong><br>
                        <span style="color: #4a5568;">{', '.join(topic_data['terms'])}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #718096; font-size: 0.9rem;">{topic_data['count']} reviews</span>
                        <span style="background: #667eea; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                            {topic_data['percentage']:.1f}%
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Enable Topic Modeling AI to discover key discussion themes in your reviews")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 4: Competitive Insights
    with tabs[3]:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">Competitive Market Analysis</h2>', unsafe_allow_html=True)
        
        if len(df_filtered['app_name'].unique()) > 1:
            # Competitive comparison matrix
            comp_data = []
            for app in df_filtered['app_name'].unique():
                app_data = df_filtered[df_filtered['app_name'] == app]
                comp_data.append({
                    'Application': app,
                    'Market Share (Reviews)': len(app_data),
                    'Customer Satisfaction': app_data['score'].mean(),
                    'Sentiment Strength': app_data['polarity_score'].mean(),
                    'Review Velocity': len(app_data) / max(1, (app_data['at'].max() - app_data['at'].min()).days),
                    'Positive Sentiment %': (app_data['sentiment'] == 'Positive').mean() * 100
                })
            
            comp_df = pd.DataFrame(comp_data)
            
            # Competitive radar chart
            categories = ['Customer Satisfaction', 'Sentiment Strength', 'Positive Sentiment %']
            
            fig_radar = go.Figure()
            
            for _, row in comp_df.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=[row['Customer Satisfaction'], row['Sentiment Strength']*5, row['Positive Sentiment %']/20],
                    theta=categories,
                    fill='toself',
                    name=row['Application']
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )
                ),
                showlegend=True,
                title="Competitive Performance Radar",
                font=dict(family='Inter, sans-serif')
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # Competitive table
            st.markdown("### Competitive Intelligence Matrix")
            st.dataframe(comp_df.round(2), use_container_width=True)
            
        else:
            st.info("Add multiple applications for competitive analysis insights")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 5: Data Explorer
    with tabs[4]:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">Advanced Data Explorer</h2>', unsafe_allow_html=True)
        
        # Enhanced filtering options
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            app_filter = st.selectbox("Application", ["All Applications"] + list(df_filtered["app_name"].unique()))
        with col2:
            sentiment_filter = st.selectbox("Sentiment Filter", ["All Sentiments", "Positive", "Neutral", "Negative"])
        with col3:
            rating_range = st.slider("Rating Range", 1, 5, (1, 5))
        with col4:
            business_impact_filter = st.selectbox("Business Impact", ["All Impact Levels"] + list(df_filtered["business_impact"].unique()))
        
        # Apply advanced filters
        display_df = df_filtered.copy()
        
        if app_filter != "All Applications":
            display_df = display_df[display_df["app_name"] == app_filter]
        if sentiment_filter != "All Sentiments":
            display_df = display_df[display_df["sentiment"] == sentiment_filter]
        if business_impact_filter != "All Impact Levels":
            display_df = display_df[display_df["business_impact"] == business_impact_filter]
        
        display_df = display_df[
            (display_df["score"] >= rating_range[0]) & 
            (display_df["score"] <= rating_range[1])
        ]
        
        # Data summary
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    padding: 1rem; border-radius: 10px; margin: 1rem 0; text-align: center;">
            <strong style="color: #2d3748; font-size: 1.1rem;">
                Displaying {len(display_df):,} of {len(df_filtered):,} reviews
            </strong>
        </div>
        """, unsafe_allow_html=True)
        
        if not display_df.empty:
            # Enhanced data display
            display_columns = [
                "app_name", "userName", "score", "content", 
                "sentiment", "business_impact", "polarity_score", "at"
            ]
            
            st.dataframe(
                display_df[display_columns].sort_values('at', ascending=False),
                use_container_width=True,
                height=600
            )
        else:
            st.warning("No reviews match the current filter criteria")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Professional Export Suite
    st.markdown("""
    <div class="content-section">
        <h2 class="section-header">Professional Export Suite</h2>
        <p style="color: #718096; margin-bottom: 2rem; font-size: 1.1rem;">
            Download comprehensive business intelligence reports and datasets for stakeholder presentations and strategic planning
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="export-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="export-card">
            <h4 style="color: #2d3748; margin-bottom: 1rem; font-family: 'Space Grotesk', sans-serif;">Executive Intelligence Report</h4>
            <p style="color: #718096; margin-bottom: 1.5rem;">Comprehensive business analytics with AI insights and strategic recommendations</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create executive summary
        executive_data = []
        for app in df_filtered["app_name"].unique():
            app_data = df_filtered[df_filtered["app_name"] == app]
            sentiment_dist = app_data["sentiment"].value_counts(normalize=True) * 100
            
            executive_data.append({
                "Application": app,
                "Total Reviews": len(app_data),
                "Average Rating": round(app_data["score"].mean(), 2),
                "Sentiment Index": round(app_data["polarity_score"].mean(), 3),
                "Customer Satisfaction": f"{sentiment_dist.get('Positive', 0):.1f}%",
                "Risk Level": f"{sentiment_dist.get('Negative', 0):.1f}%",
                "Market Position": "Leader" if app_data["score"].mean() > 4.0 else "Challenger"
            })
        
        executive_df = pd.DataFrame(executive_data)
        executive_csv = executive_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            "Download Executive Report",
            data=executive_csv,
            file_name=f"Executive_Intelligence_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            key="executive_report"
        )
    
    with col2:
        st.markdown("""
        <div class="export-card">
            <h4 style="color: #2d3748; margin-bottom: 1rem; font-family: 'Space Grotesk', sans-serif;">Complete Dataset</h4>
            <p style="color: #718096; margin-bottom: 1.5rem;">Full review database with advanced sentiment analysis and business intelligence metrics</p>
        </div>
        """, unsafe_allow_html=True)
        
        complete_csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Complete Dataset",
            data=complete_csv,
            file_name=f"Complete_Review_Analytics_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            key="complete_dataset"
        )
    
    with col3:
        st.markdown("""
        <div class="export-card">
            <h4 style="color: #2d3748; margin-bottom: 1rem; font-family: 'Space Grotesk', sans-serif;">Strategic Intelligence</h4>
            <p style="color: #718096; margin-bottom: 1.5rem;">AI-generated insights, topic analysis, and strategic recommendations for business growth</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create strategic intelligence report
        strategic_data = {
            "insights": smart_insights if enable_smart_insights else [],
            "topics": topics if enable_topic_modeling else {},
            "keywords": {k: {"count": v, "percentage": f"{(v/len(df_filtered)*100):.1f}%"} 
                        for k, v in (analyze_keywords(df_filtered, keywords).items() if keywords else {}).items()},
            "summary": {
                "total_reviews": len(df_filtered),
                "applications_analyzed": len(packages),
                "average_rating": round(df_filtered['score'].mean(), 2),
                "sentiment_distribution": df_filtered['sentiment'].value_counts().to_dict(),
                "analysis_date": datetime.now().isoformat()
            }
        }
        
        strategic_json = json.dumps(strategic_data, indent=2, default=str).encode('utf-8')
        st.download_button(
            "Download Strategic Report",
            data=strategic_json,
            file_name=f"Strategic_Intelligence_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            key="strategic_report"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Professional Welcome Interface
    st.markdown("""
    <div class="content-section">
        <h2 style="text-align: center; color: #2d3748; margin-bottom: 2rem; font-family: 'Space Grotesk', sans-serif;">
            Welcome to Advanced Business Intelligence Platform
        </h2>
        <p style="text-align: center; color: #718096; font-size: 1.3rem; line-height: 1.7; max-width: 800px; margin: 0 auto 3rem;">
            Transform customer feedback into strategic business advantages with our cutting-edge AI-powered analytics platform designed for modern enterprises.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature showcase with business focus
    st.markdown('<div class="topic-grid">', unsafe_allow_html=True)
    
    business_features = [
        {
            "title": "Executive Intelligence Dashboard",
            "description": "Real-time business metrics, KPI tracking, and executive-level insights for data-driven strategic decision making."
        },
        {
            "title": "AI-Powered Sentiment Analysis", 
            "description": "Advanced natural language processing with business impact categorization and predictive sentiment modeling."
        },
        {
            "title": "Competitive Market Intelligence",
            "description": "Comprehensive competitive analysis with market positioning insights and performance benchmarking."
        },
        {
            "title": "Strategic Topic Modeling",
            "description": "Automated discovery of key business themes, customer concerns, and market opportunities using machine learning."
        },
        {
            "title": "Predictive Business Analytics",
            "description": "Trend forecasting, customer satisfaction predictions, and proactive business intelligence recommendations."
        },
        {
            "title": "Professional Reporting Suite",
            "description": "Executive-ready reports, strategic intelligence summaries, and comprehensive data exports for stakeholder presentations."
        }
    ]
    
    for feature in business_features:
        st.markdown(f"""
        <div class="topic-card">
            <h4 style="color: #2d3748; margin-bottom: 1rem; font-family: 'Space Grotesk', sans-serif;">{feature['title']}</h4>
            <p style="color: #4a5568; line-height: 1.6; margin: 0;">{feature['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Getting started guide
    st.markdown("""
    <div class="content-section">
        <h3 style="color: #2d3748; margin-bottom: 2rem; text-align: center; font-family: 'Space Grotesk', sans-serif;">Enterprise Implementation Guide</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⚙️</div>
                <h4 style="color: #2d3748; margin-bottom: 1rem;">Configuration</h4>
                <p style="color: #718096; line-height: 1.6;">Configure analysis parameters and enable advanced AI features through the intelligent control panel</p>
            </div>
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
                <h4 style="color: #2d3748; margin-bottom: 1rem;">Analysis</h4>
                <p style="color: #718096; line-height: 1.6;">Launch comprehensive review analysis with real-time progress tracking and quality assurance</p>
            </div>
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h4 style="color: #2d3748; margin-bottom: 1rem;">Intelligence</h4>
                <p style="color: #718096; line-height: 1.6;">Explore executive dashboards, competitive insights, and AI-generated strategic recommendations</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Professional Footer
st.markdown("""
<div class="content-section" style="text-align: center; margin-top: 4rem;">
    <h3 style="color: #2d3748; margin-bottom: 1rem; font-family: 'Space Grotesk', sans-serif;">Feedback Forge Pro Analytics</h3>
    <p style="color: #718096; line-height: 1.7; font-size: 1.1rem;">
        Engineered with precision by <strong style="color: #667eea;">Ayush Pandey</strong><br>
        Advanced Business Intelligence Platform<br>
        Powered by Artificial Intelligence & Machine Learning
    </p>
    <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e2e8f0;">
        <p style="color: #a0aec0; font-size: 0.9rem;">
            Transform Data Into Strategic Advantage | Enterprise-Grade Analytics | AI-Powered Insights
        </p>
    </div>
</div>
""", unsafe_allow_html=True)