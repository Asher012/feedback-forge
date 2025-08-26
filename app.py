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
try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="Feedback Forge Analytics", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.05)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.05)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.03)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .app-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2);
        z-index: 2;
        position: relative;
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        margin-top: 0.8rem;
        opacity: 0.95;
        z-index: 2;
        position: relative;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .creator-badge {
        position: absolute;
        top: 25px;
        right: 25px;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding: 10px 20px;
        border-radius: 25px;
        border: 1px solid rgba(255,255,255,0.2);
        font-size: 0.95rem;
        font-weight: 500;
        z-index: 3;
        color: white;
    }
    
    .sidebar .sidebar-content {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 10px;
    }
    
    .control-section {
        background: white;
        padding: 1.8rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
    }
    
    .section-header {
        color: #2d3748;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.15);
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: 700;
        color: #667eea;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .metric-label {
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .content-container {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
    }
    
    .tab-container {
        background: white;
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.06);
        overflow: hidden;
        margin: 1.5rem 0;
    }
    
    .progress-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .status-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .download-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .download-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
        transition: all 0.3s ease;
    }
    
    .download-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.15);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        width: 100%;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    .welcome-container {
        background: white;
        padding: 4rem 3rem;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 15px 50px rgba(0,0,0,0.08);
        margin: 2rem 0;
        border: 1px solid #e1e5e9;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.06);
        border: 1px solid #e1e5e9;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.12);
        border-color: #667eea;
    }
    
    .feature-title {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .feature-description {
        color: #718096;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .footer-section {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 4rem;
        box-shadow: 0 15px 50px rgba(45, 55, 72, 0.3);
    }
    
    .stats-highlight {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8, #6b46c1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="app-title">Feedback Forge Analytics</div>
    <div class="app-subtitle">Advanced Review Intelligence Platform for Data-Driven Insights</div>
    <div class="creator-badge">Created by Ayush Pandey</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("""
<div class="control-section">
    <div class="section-header">Analysis Configuration</div>
    <p style="color: #718096; margin: 0; font-size: 0.9rem;">Set up your review analysis parameters</p>
</div>
""", unsafe_allow_html=True)

# Input Section
play_urls = st.sidebar.text_area(
    "Application URLs",
    placeholder="""https://play.google.com/store/apps/details?id=in.workindia.nileshdungarwal.workindiaandroid
https://play.google.com/store/apps/details?id=com.whatsapp""",
    height=120,
    help="Enter Google Play Store URLs, one per line"
)

count = st.sidebar.slider(
    "Reviews per Application", 
    min_value=10, 
    max_value=1000, 
    value=200, 
    step=25,
    help="Number of reviews to analyze from each application"
)

# Advanced Configuration
st.sidebar.markdown("""
<div class="control-section">
    <div class="section-header">Advanced Settings</div>
</div>
""", unsafe_allow_html=True)

language = st.sidebar.selectbox("Language", ["en", "hi", "es", "fr", "de", "ja"], index=0)
country = st.sidebar.selectbox("Region", ["in", "us", "uk", "ca", "de", "jp"], index=0)
sort_by = st.sidebar.selectbox("Sort Method", ["NEWEST", "MOST_RELEVANT", "RATING"], index=0)

# Intelligence Features
st.sidebar.markdown("""
<div class="control-section">
    <div class="section-header">AI Intelligence</div>
</div>
""", unsafe_allow_html=True)

enable_keywords = st.sidebar.checkbox("Enable Keyword Analysis", value=True)
if WORDCLOUD_AVAILABLE:
    enable_wordcloud = st.sidebar.checkbox("Generate Word Clouds", value=True)
else:
    enable_wordcloud = False
    st.sidebar.info("Install wordcloud package for visual text analysis")

enable_trends = st.sidebar.checkbox("Enable Trend Analysis", value=True)
min_rating_filter = st.sidebar.selectbox("Minimum Rating Filter", [1, 2, 3, 4, 5], index=0)

# Keywords input
keywords = []
if enable_keywords:
    keyword_input = st.sidebar.text_input(
        "Keywords to Track",
        placeholder="bug, crash, slow, good, excellent",
        help="Comma-separated keywords for frequency analysis"
    )
    if keyword_input:
        keywords = [k.strip().lower() for k in keyword_input.split(",")]

# Helper Functions
def extract_package_name(url):
    """Extract package name from Google Play URL"""
    if "id=" in url:
        package = url.split("id=")[1].split("&")[0]
        return package.strip()
    return None

def analyze_sentiment_advanced(text):
    """Advanced sentiment analysis with polarity and subjectivity scores"""
    if pd.isna(text) or text.strip() == "":
        return "Neutral", 0.0, 0.0
    
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.15:
        return "Positive", polarity, subjectivity
    elif polarity < -0.15:
        return "Negative", polarity, subjectivity
    else:
        return "Neutral", polarity, subjectivity

def get_app_name(package_name):
    """Extract readable app name from package identifier"""
    parts = package_name.split('.')
    if len(parts) > 0:
        return parts[-1].replace('_', ' ').title()
    return package_name

def analyze_keywords(df, keywords):
    """Analyze keyword frequency in review content"""
    if not keywords or df.empty:
        return {}
    
    keyword_counts = {}
    for keyword in keywords:
        count = df['content'].str.lower().str.contains(keyword, na=False).sum()
        keyword_counts[keyword] = count
    
    return keyword_counts

def generate_wordcloud(text_data, sentiment=""):
    """Generate professional word cloud visualization"""
    if not WORDCLOUD_AVAILABLE or not text_data:
        return None
    
    text = " ".join(text_data)
    if len(text.strip()) == 0:
        return None
    
    # Color schemes based on sentiment
    color_schemes = {
        "Positive": "Greens",
        "Negative": "Reds", 
        "Neutral": "Blues",
        "": "viridis"
    }
    
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        colormap=color_schemes.get(sentiment, "viridis"),
        max_words=80,
        relative_scaling=0.5,
        max_font_size=60
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    
    return fig

def create_professional_charts(df):
    """Create professional-grade visualization charts"""
    charts = {}
    
    # Professional color palette
    colors = {
        'Positive': '#48bb78',
        'Neutral': '#ed8936', 
        'Negative': '#f56565'
    }
    
    template = "plotly_white"
    
    # Sentiment timeline analysis
    if 'at' in df.columns and not df.empty:
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['at']).dt.date
        daily_sentiment = df_copy.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
        
        if not daily_sentiment.empty:
            fig = px.area(
                daily_sentiment.reset_index(),
                x='date',
                y=[col for col in ['Positive', 'Neutral', 'Negative'] if col in daily_sentiment.columns],
                title="Sentiment Trends Analysis",
                color_discrete_map=colors,
                template=template
            )
            fig.update_layout(
                font_family='Inter',
                title_font_size=18,
                title_font_color='#2d3748',
                hovermode='x unified'
            )
            charts['sentiment_timeline'] = fig
    
    return charts

# Main Analysis Button
if st.sidebar.button("Start Analysis", type="primary"):
    # URL Validation
    urls_list = [url.strip() for url in play_urls.splitlines() if url.strip()]
    packages = []
    
    for url in urls_list:
        pkg = extract_package_name(url)
        if pkg:
            packages.append(pkg)
    
    if not packages:
        st.error("Please enter valid Google Play Store URLs to begin analysis")
        st.stop()
    
    # Progress Section
    with st.container():
        st.markdown("""
        <div class="progress-section">
            <h2 style="margin: 0 0 1rem 0; font-weight: 600;">Analysis in Progress</h2>
            <p style="margin: 0; opacity: 0.9; font-size: 1.1rem;">Processing review data and performing sentiment analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    all_dfs = []
    
    # Data Collection Process
    for i, package in enumerate(packages):
        status_text.markdown(f"""
        <div class="status-card">
            <strong style="font-size: 1.1rem;">Processing: {get_app_name(package)}</strong><br>
            <span style="opacity: 0.8; font-size: 0.9rem;">Package: {package}</span>
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
                df["app_name"] = get_app_name(package)
                all_dfs.append(df)
                
        except Exception as e:
            st.warning(f"Unable to process {package}: {str(e)}")
        
        progress_bar.progress((i + 1) / len(packages))
    
    # Clear progress indicators
    status_text.empty()
    progress_bar.empty()
    
    if not all_dfs:
        st.error("No review data was successfully collected")
        st.stop()
    
    # Data Processing and Analysis
    df_all = pd.concat(all_dfs, ignore_index=True)
    
    with st.spinner("Performing advanced sentiment analysis..."):
        sentiment_results = df_all["content"].apply(analyze_sentiment_advanced)
        df_all["sentiment"] = [result[0] for result in sentiment_results]
        df_all["polarity_score"] = [result[1] for result in sentiment_results]
        df_all["subjectivity_score"] = [result[2] for result in sentiment_results]
        df_all["at"] = pd.to_datetime(df_all["at"])
        
        # Apply rating filter
        df_filtered = df_all[df_all["score"] >= min_rating_filter].copy()
    
    # Success notification
    st.success(f"Analysis completed successfully! Processed {len(df_all):,} reviews from {len(packages)} application(s)")
    
    # Key Performance Metrics
    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(packages)}</div>
            <div class="metric-label">Applications</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df_filtered):,}</div>
            <div class="metric-label">Reviews</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_rating = df_filtered["score"].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_rating:.1f}</div>
            <div class="metric-label">Average Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        positive_pct = (df_filtered["sentiment"] == "Positive").mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{positive_pct:.0f}%</div>
            <div class="metric-label">Positive Sentiment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        avg_polarity = df_filtered["polarity_score"].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_polarity:.2f}</div>
            <div class="metric-label">Sentiment Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis Tabs
    if enable_wordcloud and WORDCLOUD_AVAILABLE:
        tabs = st.tabs(["Overview", "Intelligence", "Word Analysis", "Data Explorer", "Advanced Analytics"])
    else:
        tabs = st.tabs(["Overview", "Intelligence", "Data Explorer", "Advanced Analytics"])
        enable_wordcloud = False
    
    # Overview Tab
    with tabs[0]:
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sentiment Distribution Analysis")
            sentiment_counts = df_filtered["sentiment"].value_counts()
            fig_pie = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="Overall Sentiment Breakdown",
                color_discrete_map={
                    "Positive": "#48bb78",
                    "Neutral": "#ed8936", 
                    "Negative": "#f56565"
                },
                template="plotly_white"
            )
            fig_pie.update_layout(
                font_family='Inter',
                title_font_size=16,
                title_font_color='#2d3748'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("Application Comparison")
            app_sentiment = df_filtered.groupby(["app_name", "sentiment"]).size().unstack(fill_value=0)
            fig_bar = px.bar(
                app_sentiment.reset_index(),
                x="app_name",
                y=[col for col in ["Positive", "Neutral", "Negative"] if col in app_sentiment.columns],
                title="Sentiment Distribution by Application",
                color_discrete_map={
                    "Positive": "#48bb78",
                    "Neutral": "#ed8936",
                    "Negative": "#f56565"
                },
                template="plotly_white"
            )
            fig_bar.update_layout(
                font_family='Inter',
                title_font_size=16,
                title_font_color='#2d3748',
                xaxis_title="Application",
                yaxis_title="Number of Reviews"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Rating Analysis
        st.subheader("Rating Distribution Analysis")
        fig_hist = px.histogram(
            df_filtered,
            x="score",
            color="sentiment",
            title="Rating Distribution with Sentiment Analysis",
            labels={"score": "Star Rating", "count": "Number of Reviews"},
            color_discrete_map={
                "Positive": "#48bb78",
                "Neutral": "#ed8936",
                "Negative": "#f56565"
            },
            template="plotly_white",
            nbins=5
        )
        fig_hist.update_layout(
            font_family='Inter',
            title_font_size=16,
            title_font_color='#2d3748'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Intelligence Tab
    with tabs[1]:
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        # Keyword Analysis
        if enable_keywords and keywords:
            st.subheader("Keyword Intelligence Analysis")
            keyword_results = analyze_keywords(df_filtered, keywords)
            
            if keyword_results:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Keyword Frequency Results**")
                    for keyword, count in keyword_results.items():
                        percentage = (count / len(df_filtered)) * 100
                        st.markdown(f"""
                        <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #667eea;">
                            <strong style="color: #2d3748;">{keyword.upper()}</strong><br>
                            <span style="color: #718096;">Mentions: {count} ({percentage:.1f}% of reviews)</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    if keyword_results:
                        fig_keywords = px.bar(
                            x=list(keyword_results.keys()),
                            y=list(keyword_results.values()),
                            title="Keyword Frequency Analysis",
                            color=list(keyword_results.values()),
                            color_continuous_scale="Blues",
                            template="plotly_white"
                        )
                        fig_keywords.update_layout(
                            font_family='Inter',
                            title_font_size=16,
                            title_font_color='#2d3748',
                            xaxis_title="Keywords",
                            yaxis_title="Frequency"
                        )
                        st.plotly_chart(fig_keywords, use_container_width=True)
        
        # Trend Analysis
        if enable_trends:
            st.subheader("Trend Intelligence")
            advanced_charts = create_professional_charts(df_filtered)
            
            for chart_name, chart in advanced_charts.items():
                st.plotly_chart(chart, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Word Cloud Tab
    if enable_wordcloud and WORDCLOUD_AVAILABLE:
        with tabs[2]:
            st.markdown('<div class="content-container">', unsafe_allow_html=True)
            st.subheader("Word Cloud Visualization Analysis")
            
            sentiments = ["Positive", "Negative", "Neutral"]
            cols = st.columns(len(sentiments))
            
            for i, sentiment in enumerate(sentiments):
                with cols[i]:
                    st.write(f"**{sentiment} Reviews Word Cloud**")
                    sentiment_reviews = df_filtered[df_filtered["sentiment"] == sentiment]["content"].tolist()
                    
                    if sentiment_reviews:
                        wordcloud_fig = generate_wordcloud(sentiment_reviews, sentiment)
                        if wordcloud_fig:
                            st.pyplot(wordcloud_fig)
                        else:
                            st.info(f"Insufficient data for {sentiment.lower()} word cloud")
                    else:
                        st.info(f"No {sentiment.lower()} reviews found")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Explorer Tab
    tab_idx = 3 if enable_wordcloud and WORDCLOUD_AVAILABLE else 2
    with tabs[tab_idx]:
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.subheader("Data Explorer")
        
        # Advanced Filters
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            app_filter = st.selectbox("Application Filter", ["All"] + list(df_filtered["app_name"].unique()))
        with col2:
            sentiment_filter = st.selectbox("Sentiment Filter", ["All", "Positive", "Neutral", "Negative"])
        with col3:
            rating_filter = st.selectbox("Rating Filter", ["All"] + list(sorted(df_filtered["score"].unique(), reverse=True)))
        with col4:
            date_filter = st.selectbox("Time Period", ["All Time", "Last 30 Days", "Last 7 Days"])
        
        # Apply Filters
        display_df = df_filtered.copy()
        if app_filter != "All":
            display_df = display_df[display_df["app_name"] == app_filter]
        if sentiment_filter != "All":
            display_df = display_df[display_df["sentiment"] == sentiment_filter]
        if rating_filter != "All":
            display_df = display_df[display_df["score"] == int(rating_filter)]
        
        if date_filter == "Last 30 Days":
            cutoff_date = datetime.now() - timedelta(days=30)
            display_df = display_df[display_df["at"] >= cutoff_date]
        elif date_filter == "Last 7 Days":
            cutoff_date = datetime.now() - timedelta(days=7)
            display_df = display_df[display_df["at"] >= cutoff_date]
        
        st.markdown(f'<div class="stats-highlight">Displaying {len(display_df):,} of {len(df_filtered):,} reviews</div>', unsafe_allow_html=True)
        
        if not display_df.empty:
            display_columns = ["app_name", "userName", "score", "content", "sentiment", "polarity_score", "at"]
            st.dataframe(
                display_df[display_columns],
                use_container_width=True,
                height=500
            )
        else:
            st.warning("No reviews match the selected filter criteria")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced Analytics Tab
    tab_idx_adv = 4 if enable_wordcloud and WORDCLOUD_AVAILABLE else 3
    with tabs[tab_idx_adv]:
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.subheader("Advanced Analytics Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Sentiment vs Rating Correlation**")
            fig_scatter = px.scatter(
                df_filtered,
                x="score",
                y="polarity_score",
                color="sentiment",
                size="subjectivity_score",
                title="Sentiment Polarity vs Star Rating Analysis",
                color_discrete_map={
                    "Positive": "#48bb78",
                    "Neutral": "#ed8936",
                    "Negative": "#f56565"
                },
                template="plotly_white"
            )
            fig_scatter.update_layout(
                font_family='Inter',
                title_font_size=16,
                title_font_color='#2d3748',
                xaxis_title="Star Rating",
                yaxis_title="Sentiment Polarity"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            st.write("**Review Volume Analysis**")
            if not df_filtered.empty:
                df_filtered_copy = df_filtered.copy()
                df_filtered_copy['date'] = df_filtered_copy['at'].dt.date
                daily_counts = df_filtered_copy.groupby('date').size().reset_index(name='count')
                
                fig_volume = px.line(
                    daily_counts,
                    x='date',
                    y='count',
                    title="Daily Review Volume Trends",
                    markers=True,
                    template="plotly_white"
                )
                fig_volume.update_traces(line_color='#667eea')
                fig_volume.update_layout(
                    font_family='Inter',
                    title_font_size=16,
                    title_font_color='#2d3748',
                    xaxis_title="Date",
                    yaxis_title="Number of Reviews"
                )
                st.plotly_chart(fig_volume, use_container_width=True)
        
        # Statistical Summary
        st.write("**Statistical Summary**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Standard Deviation (Rating)", f"{df_filtered['score'].std():.2f}")
            st.metric("Median Rating", f"{df_filtered['score'].median():.1f}")
        
        with col2:
            st.metric("Sentiment Variance", f"{df_filtered['polarity_score'].var():.3f}")
            st.metric("Most Active Day", df_filtered['at'].dt.date.mode()[0] if not df_filtered.empty else "N/A")
        
        with col3:
            highest_rated_app = df_filtered.groupby('app_name')['score'].mean().idxmax()
            st.metric("Highest Rated App", highest_rated_app)
            most_reviewed_app = df_filtered['app_name'].mode()[0] if not df_filtered.empty else "N/A"
            st.metric("Most Reviewed App", most_reviewed_app)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Export Section
    st.markdown('<div class="download-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="download-card">
            <h4 style="color: #2d3748; margin-bottom: 1rem;">Complete Dataset</h4>
            <p style="color: #718096; font-size: 0.9rem;">Full review data with sentiment analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Complete Dataset",
            data=csv_data,
            file_name=f"FeedbackForge_Complete_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col2:
        st.markdown("""
        <div class="download-card">
            <h4 style="color: #2d3748; margin-bottom: 1rem;">Executive Summary</h4>
            <p style="color: #718096; font-size: 0.9rem;">Key metrics and insights summary</p>
        </div>
        """, unsafe_allow_html=True)
        
        summary_data = []
        for app in df_filtered["app_name"].unique():
            app_data = df_filtered[df_filtered["app_name"] == app]
            sentiment_dist = app_data["sentiment"].value_counts(normalize=True) * 100
            
            summary_data.append({
                "Application": app,
                "Total Reviews": len(app_data),
                "Average Rating": round(app_data["score"].mean(), 2),
                "Average Sentiment": round(app_data["polarity_score"].mean(), 3),
                "Positive Percentage": round(sentiment_dist.get("Positive", 0), 1),
                "Neutral Percentage": round(sentiment_dist.get("Neutral", 0), 1),
                "Negative Percentage": round(sentiment_dist.get("Negative", 0), 1)
            })
        
        summary_df = pd.DataFrame(summary_data)
        csv_summary = summary_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download Executive Summary",
            data=csv_summary,
            file_name=f"FeedbackForge_Executive_Summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col3:
        st.markdown("""
        <div class="download-card">
            <h4 style="color: #2d3748; margin-bottom: 1rem;">Keyword Analysis</h4>
            <p style="color: #718096; font-size: 0.9rem;">Keyword frequency and trends</p>
        </div>
        """, unsafe_allow_html=True)
        
        if enable_keywords and keywords and 'keyword_results' in locals():
            keyword_df = pd.DataFrame([
                {"Keyword": keyword, "Frequency": count, "Percentage": f"{(count/len(df_filtered)*100):.1f}%"}
                for keyword, count in keyword_results.items()
            ])
            keyword_csv = keyword_df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="Download Keyword Analysis",
                data=keyword_csv,
                file_name=f"FeedbackForge_Keywords_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Enable keyword analysis to download this report")
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Welcome Interface
    st.markdown("""
    <div class="welcome-container">
        <h2 style="color: #2d3748; margin-bottom: 1.5rem; font-family: 'Poppins', sans-serif;">
            Welcome to Feedback Forge Analytics
        </h2>
        <p style="color: #718096; font-size: 1.2rem; margin-bottom: 2rem; line-height: 1.6;">
            Transform application reviews into actionable business insights with advanced AI-powered sentiment analysis and comprehensive data visualization.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Showcase
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    features = [
        {
            "title": "Multi-Application Analysis",
            "description": "Simultaneously analyze and compare sentiment across multiple applications with comprehensive statistical insights and trend identification."
        },
        {
            "title": "Advanced AI Sentiment Analysis", 
            "description": "Utilize cutting-edge natural language processing algorithms to accurately determine user sentiment, polarity, and subjectivity scores."
        },
        {
            "title": "Intelligent Keyword Tracking",
            "description": "Monitor specific terms, phrases, and topics within reviews to identify emerging trends, feature requests, and critical issues."
        },
        {
            "title": "Professional Data Visualization",
            "description": "Generate publication-ready charts, graphs, and visualizations that clearly communicate insights to stakeholders and decision-makers."
        },
        {
            "title": "Word Cloud Generation",
            "description": "Create visually appealing word clouds that highlight the most frequently mentioned terms in positive, negative, and neutral reviews."
        },
        {
            "title": "Comprehensive Analytics Dashboard",
            "description": "Access detailed statistical analysis, correlation studies, and trend forecasting to make data-driven business decisions."
        }
    ]
    
    cols = st.columns(2)
    for i, feature in enumerate(features):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-title">{feature['title']}</div>
                <div class="feature-description">{feature['description']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Getting Started Guide
    st.markdown("""
    <div class="content-container">
        <h3 style="color: #2d3748; margin-bottom: 1.5rem; font-family: 'Poppins', sans-serif;">Getting Started Guide</h3>
        <div style="color: #718096; line-height: 1.8;">
            <p><strong style="color: #2d3748;">Step 1:</strong> Configure your analysis parameters in the sidebar by entering Google Play Store application URLs</p>
            <p><strong style="color: #2d3748;">Step 2:</strong> Adjust advanced settings including language, region, sorting method, and review quantity</p>
            <p><strong style="color: #2d3748;">Step 3:</strong> Enable AI intelligence features such as keyword analysis and word cloud generation</p>
            <p><strong style="color: #2d3748;">Step 4:</strong> Initiate the analysis process and monitor progress through the intelligent processing pipeline</p>
            <p><strong style="color: #2d3748;">Step 5:</strong> Explore comprehensive results through organized tabs featuring overview, intelligence, and advanced analytics</p>
            <p><strong style="color: #2d3748;">Step 6:</strong> Export your findings in multiple formats for presentations, reports, and further analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample URLs
    st.markdown("""
    <div class="content-container">
        <h3 style="color: #2d3748; margin-bottom: 1rem; font-family: 'Poppins', sans-serif;">Sample Application URLs</h3>
        <p style="color: #718096; margin-bottom: 1rem;">Use these sample URLs to test the platform capabilities:</p>
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #667eea;">
            <code style="color: #2d3748; font-family: monospace;">
                https://play.google.com/store/apps/details?id=in.workindia.nileshdungarwal.workindiaandroid<br>
                https://play.google.com/store/apps/details?id=com.whatsapp<br>
                https://play.google.com/store/apps/details?id=com.instagram.android
            </code>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-section">
    <h3 style="margin-bottom: 1rem; font-family: 'Poppins', sans-serif;">Feedback Forge Analytics</h3>
    <p style="opacity: 0.9; line-height: 1.6; max-width: 600px; margin: 0 auto;">
        Developed with precision and innovation by <strong>Ayush Pandey</strong><br>
        Advanced Review Intelligence Platform<br>
        Powered by Artificial Intelligence, Machine Learning, and Data Science
    </p>
</div>
""", unsafe_allow_html=True)
