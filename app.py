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
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Source+Sans+Pro:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Source Sans Pro', sans-serif;
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .app-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .app-subtitle {
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    .creator-info {
        position: absolute;
        top: 15px;
        right: 20px;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding: 6px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    .sidebar-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .sidebar-title {
        color: #1e293b;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Metrics Cards */
    .metrics-container {
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
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
        border-color: #667eea;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e293b;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    /* Content Sections */
    .content-section {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    .section-header {
        color: #1e293b;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.4rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #667eea;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 60px;
        height: 2px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    .stButton>button:active {
        transform: translateY(0px);
    }
    
    /* Progress and Status */
    .progress-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .status-message {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        font-weight: 500;
    }
    
    /* Chart Containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    
    .chart-title {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Download Section */
    .download-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 16px;
        margin: 2rem 0;
        border: 1px solid #cbd5e1;
    }
    
    .download-title {
        color: #1e293b;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-top: 3rem;
    }
    
    .footer-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .footer-text {
        opacity: 0.8;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f8fafc;
        border-radius: 12px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 500;
        padding: 12px 24px;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    /* Form Elements */
    .stSelectbox > div > div {
        background: white;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stTextArea > div > div > textarea {
        background: white;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 0.9rem;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Welcome Screen */
    .welcome-container {
        background: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        margin: 2rem 0;
    }
    
    .welcome-title {
        color: #1e293b;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
        border-color: #667eea;
    }
    
    .feature-title {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    .feature-description {
        color: #64748b;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2rem;
        }
        
        .metrics-container {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }
        
        .metric-card {
            padding: 1.5rem 1rem;
        }
        
        .metric-value {
            font-size: 1.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <div class="app-title">Feedback Forge Analytics</div>
    <div class="app-subtitle">Professional Review Intelligence & Data Analytics Platform</div>
    <div class="creator-info">Developed by Ayush Pandey</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("""
<div class="sidebar-section">
    <div class="sidebar-title">Configuration Panel</div>
    <p style="color: #64748b; font-size: 0.9rem; margin: 0;">Set up your analysis parameters</p>
</div>
""", unsafe_allow_html=True)

# URL Input Section
play_urls = st.sidebar.text_area(
    "Application URLs",
    placeholder="https://play.google.com/store/apps/details?id=com.example.app1\nhttps://play.google.com/store/apps/details?id=com.example.app2",
    height=120,
    help="Enter Google Play Store URLs, one per line"
)

review_count = st.sidebar.slider(
    "Reviews per Application", 
    min_value=10, 
    max_value=1000, 
    value=200, 
    step=25,
    help="Number of reviews to analyze from each application"
)

# Advanced Configuration
st.sidebar.markdown("""
<div class="sidebar-section">
    <div class="sidebar-title">Advanced Settings</div>
</div>
""", unsafe_allow_html=True)

language = st.sidebar.selectbox("Language", ["en", "hi", "es", "fr", "de", "ja"], index=0)
country = st.sidebar.selectbox("Country", ["in", "us", "uk", "ca", "de", "jp"], index=0)
sort_method = st.sidebar.selectbox("Sort Method", ["NEWEST", "MOST_RELEVANT", "RATING"], index=0)

# Analysis Features
st.sidebar.markdown("""
<div class="sidebar-section">
    <div class="sidebar-title">Analysis Features</div>
</div>
""", unsafe_allow_html=True)

enable_keyword_analysis = st.sidebar.checkbox("Keyword Analysis", value=True)
enable_wordcloud_generation = st.sidebar.checkbox("Word Cloud Generation", value=WORDCLOUD_AVAILABLE)
enable_trend_analysis = st.sidebar.checkbox("Trend Analysis", value=True)
minimum_rating_filter = st.sidebar.selectbox("Minimum Rating Filter", [1, 2, 3, 4, 5], index=0)

# Keyword Configuration
target_keywords = []
if enable_keyword_analysis:
    keyword_input = st.sidebar.text_input(
        "Target Keywords",
        placeholder="performance, bug, crash, excellent, good",
        help="Enter comma-separated keywords for analysis"
    )
    if keyword_input:
        target_keywords = [keyword.strip().lower() for keyword in keyword_input.split(",")]

# Core Functions
def extract_app_package(url):
    """Extract application package from Play Store URL"""
    if "id=" in url:
        package_id = url.split("id=")[1].split("&")[0]
        return package_id.strip()
    return None

def perform_sentiment_analysis(text_content):
    """Perform comprehensive sentiment analysis"""
    if pd.isna(text_content) or not text_content.strip():
        return "Neutral", 0.0, 0.0
    
    sentiment_blob = TextBlob(str(text_content))
    polarity_score = sentiment_blob.sentiment.polarity
    subjectivity_score = sentiment_blob.sentiment.subjectivity
    
    if polarity_score > 0.15:
        sentiment_category = "Positive"
    elif polarity_score < -0.15:
        sentiment_category = "Negative"
    else:
        sentiment_category = "Neutral"
    
    return sentiment_category, polarity_score, subjectivity_score

def extract_app_name(package_identifier):
    """Extract readable application name from package"""
    components = package_identifier.split('.')
    if components:
        return components[-1].replace('_', ' ').title()
    return package_identifier

def analyze_keyword_frequency(dataframe, keyword_list):
    """Analyze frequency of target keywords in reviews"""
    if not keyword_list or dataframe.empty:
        return {}
    
    frequency_results = {}
    for keyword in keyword_list:
        matches = dataframe['content'].str.lower().str.contains(keyword, na=False).sum()
        frequency_results[keyword] = matches
    
    return frequency_results

def generate_word_cloud_visualization(text_data_list):
    """Generate professional word cloud visualization"""
    if not WORDCLOUD_AVAILABLE or not text_data_list:
        return None
    
    combined_text = " ".join(text_data_list)
    if not combined_text.strip():
        return None
        
    word_cloud = WordCloud(
        width=1200, 
        height=600, 
        background_color='white',
        colormap='viridis',
        max_words=150,
        relative_scaling=0.5,
        min_font_size=10
    ).generate(combined_text)
    
    figure, axis = plt.subplots(figsize=(15, 7.5))
    figure.patch.set_facecolor('white')
    axis.imshow(word_cloud, interpolation='bilinear')
    axis.axis('off')
    
    return figure

def create_professional_visualizations(analysis_dataframe):
    """Create professional data visualizations"""
    visualization_charts = {}
    
    # Professional color palette
    color_scheme = {
        'Positive': '#10B981',    # Emerald
        'Neutral': '#F59E0B',     # Amber
        'Negative': '#EF4444'     # Red
    }
    
    # Sentiment timeline analysis
    if 'at' in analysis_dataframe.columns and not analysis_dataframe.empty:
        timeline_df = analysis_dataframe.copy()
        timeline_df['review_date'] = pd.to_datetime(timeline_df['at']).dt.date
        daily_sentiment_data = timeline_df.groupby(['review_date', 'sentiment']).size().unstack(fill_value=0)
        
        if not daily_sentiment_data.empty:
            sentiment_timeline_chart = px.area(
                daily_sentiment_data.reset_index(),
                x='review_date',
                y=[col for col in ['Positive', 'Neutral', 'Negative'] if col in daily_sentiment_data.columns],
                title="Sentiment Analysis Timeline",
                color_discrete_map=color_scheme,
                template='plotly_white'
            )
            sentiment_timeline_chart.update_layout(
                font=dict(family="Source Sans Pro, sans-serif"),
                title_font_size=16,
                title_x=0.5,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            visualization_charts['sentiment_timeline'] = sentiment_timeline_chart
    
    return visualization_charts

# Main Analysis Execution
if st.sidebar.button("Execute Analysis", type="primary"):
    # Input Validation
    url_list = [url.strip() for url in play_urls.splitlines() if url.strip()]
    valid_packages = []
    
    for url in url_list:
        package = extract_app_package(url)
        if package:
            valid_packages.append(package)
    
    if not valid_packages:
        st.error("Please provide valid Google Play Store URLs for analysis")
        st.stop()
    
    # Analysis Progress Display
    with st.container():
        st.markdown("""
        <div class="progress-container">
            <h2 style="margin: 0 0 1rem 0;">Analysis in Progress</h2>
            <p style="margin: 0; opacity: 0.9;">Processing application data and performing sentiment analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        analysis_progress = st.progress(0)
        status_display = st.empty()
    
    collected_dataframes = []
    
    # Data Collection Process
    for index, package in enumerate(valid_packages):
        status_display.markdown(f"""
        <div class="status-message">
            <strong>Processing Application: {extract_app_name(package)}</strong><br>
            <small>Package Identifier: {package}</small>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            sorting_options = {
                "NEWEST": Sort.NEWEST,
                "MOST_RELEVANT": Sort.MOST_RELEVANT,
                "RATING": Sort.RATING
            }
            
            review_data, _ = reviews(
                package,
                lang=language,
                country=country,
                sort=sorting_options[sort_method],
                count=review_count
            )
            
            if review_data:
                app_dataframe = pd.DataFrame(review_data)
                app_dataframe["package_id"] = package
                app_dataframe["application_name"] = extract_app_name(package)
                collected_dataframes.append(app_dataframe)
                
        except Exception as error:
            st.warning(f"Unable to process {package}: {str(error)}")
        
        analysis_progress.progress((index + 1) / len(valid_packages))
    
    # Clear progress indicators
    status_display.empty()
    analysis_progress.empty()
    
    if not collected_dataframes:
        st.error("No review data was successfully collected for analysis")
        st.stop()
    
    # Data Processing and Analysis
    complete_dataset = pd.concat(collected_dataframes, ignore_index=True)
    
    with st.spinner("Performing comprehensive sentiment analysis..."):
        # Apply sentiment analysis
        sentiment_analysis_results = complete_dataset["content"].apply(perform_sentiment_analysis)
        complete_dataset["sentiment_category"] = [result[0] for result in sentiment_analysis_results]
        complete_dataset["polarity_score"] = [result[1] for result in sentiment_analysis_results]
        complete_dataset["subjectivity_score"] = [result[2] for result in sentiment_analysis_results]
        complete_dataset["review_timestamp"] = pd.to_datetime(complete_dataset["at"])
        
        # Apply rating filter
        filtered_dataset = complete_dataset[complete_dataset["score"] >= minimum_rating_filter].copy()
    
    # Success Notification
    st.success(f"Analysis completed successfully! Processed {len(complete_dataset):,} reviews from {len(valid_packages)} application(s)")
    
    # Key Performance Metrics
    st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
    
    metrics_data = {
        "Applications": len(valid_packages),
        "Total Reviews": len(filtered_dataset),
        "Average Rating": filtered_dataset["score"].mean(),
        "Positive Sentiment": (filtered_dataset["sentiment_category"] == "Positive").mean() * 100,
        "Average Polarity": filtered_dataset["polarity_score"].mean()
    }
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics_data['Applications']}</div>
            <div class="metric-label">Applications</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics_data['Total Reviews']:,}</div>
            <div class="metric-label">Reviews</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics_data['Average Rating']:.1f}</div>
            <div class="metric-label">Avg Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics_data['Positive Sentiment']:.0f}%</div>
            <div class="metric-label">Positive</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics_data['Average Polarity']:.2f}</div>
            <div class="metric-label">Polarity</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis Tabs
    if enable_wordcloud_generation and WORDCLOUD_AVAILABLE:
        tab_names = ["Overview", "Intelligence", "Word Clouds", "Data Analysis", "Advanced Analytics"]
    else:
        tab_names = ["Overview", "Intelligence", "Data Analysis", "Advanced Analytics"]
        enable_wordcloud_generation = False
    
    analysis_tabs = st.tabs(tab_names)
    
    # Overview Tab
    with analysis_tabs[0]:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">Analysis Overview</h2>', unsafe_allow_html=True)
        
        overview_col1, overview_col2 = st.columns(2)
        
        with overview_col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Sentiment Distribution Analysis</div>', unsafe_allow_html=True)
            
            sentiment_distribution = filtered_dataset["sentiment_category"].value_counts()
            sentiment_pie_chart = px.pie(
                values=sentiment_distribution.values,
                names=sentiment_distribution.index,
                color_discrete_map={
                    "Positive": "#10B981",
                    "Neutral": "#F59E0B", 
                    "Negative": "#EF4444"
                },
                template='plotly_white'
            )
            sentiment_pie_chart.update_layout(
                font=dict(family="Source Sans Pro, sans-serif"),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
            )
            st.plotly_chart(sentiment_pie_chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with overview_col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Application Comparison</div>', unsafe_allow_html=True)
            
            app_sentiment_comparison = filtered_dataset.groupby(["application_name", "sentiment_category"]).size().unstack(fill_value=0)
            app_comparison_chart = px.bar(
                app_sentiment_comparison.reset_index(),
                x="application_name",
                y=[col for col in ["Positive", "Neutral", "Negative"] if col in app_sentiment_comparison.columns],
                color_discrete_map={
                    "Positive": "#10B981",
                    "Neutral": "#F59E0B",
                    "Negative": "#EF4444"
                },
                template='plotly_white'
            )
            app_comparison_chart.update_layout(
                font=dict(family="Source Sans Pro, sans-serif"),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(app_comparison_chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Intelligence Tab
    with analysis_tabs[1]:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">Intelligence Analysis</h2>', unsafe_allow_html=True)
        
        # Keyword Analysis Section
        if enable_keyword_analysis and target_keywords:
            st.markdown("### Keyword Intelligence")
            keyword_analysis_results = analyze_keyword_frequency(filtered_dataset, target_keywords)
            
            if keyword_analysis_results:
                intelligence_col1, intelligence_col2 = st.columns(2)
                
                with intelligence_col1:
                    st.markdown("#### Keyword Frequency Analysis")
                    for keyword, frequency in keyword_analysis_results.items():
                        percentage = (frequency / len(filtered_dataset)) * 100
                        st.metric(
                            label=keyword.title(),
                            value=f"{frequency} mentions",
                            delta=f"{percentage:.1f}% coverage"
                        )
                
                with intelligence_col2:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.markdown('<div class="chart-title">Keyword Frequency Distribution</div>', unsafe_allow_html=True)
                    
                    keyword_chart = px.bar(
                        x=list(keyword_analysis_results.keys()),
                        y=list(keyword_analysis_results.values()),
                        color=list(keyword_analysis_results.values()),
                        color_continuous_scale="Viridis",
                        template='plotly_white'
                    )
                    keyword_chart.update_layout(
                        font=dict(family="Source Sans Pro, sans-serif"),
                        showlegend=False
                    )
                    st.plotly_chart(keyword_chart, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Trend Analysis Section
        if enable_trend_analysis:
            st.markdown("### Trend Analysis")
            professional_charts = create_professional_visualizations(filtered_dataset)
            
            for chart_name, chart_object in professional_charts.items():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(chart_object, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Word Cloud Tab
    if enable_wordcloud_generation and WORDCLOUD_AVAILABLE:
        with analysis_tabs[2]:
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            st.markdown('<h2 class="section-header">Word Cloud Analysis</h2>', unsafe_allow_html=True)
            
            sentiment_categories = ["Positive", "Negative", "Neutral"]
            wordcloud_columns = st.columns(len(sentiment_categories))
            
            for idx, sentiment in enumerate(sentiment_categories):
                with wordcloud_columns[idx]:
                    st.markdown(f"### {sentiment} Reviews")
                    sentiment_specific_reviews = filtered_dataset[filtered_dataset["sentiment_category"] == sentiment]["content"].tolist()
                    
                    if sentiment_specific_reviews:
                        wordcloud_visualization = generate_word_cloud_visualization(sentiment_specific_reviews)
                        if wordcloud_visualization:
                            st.pyplot(wordcloud_visualization, use_container_width=True)
                        else:
                            st.info(f"Unable to generate word cloud for {sentiment.lower()} reviews")
                    else:
                        st.info(f"No {sentiment.lower()} reviews available for visualization")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Analysis Tab
    tab_data_index = 3 if enable_wordcloud_generation and WORDCLOUD_AVAILABLE else 2
    with analysis_tabs[tab_data_index]:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">Detailed Data Analysis</h2>', unsafe_allow_html=True)
        
        # Advanced Filtering Options
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        
        with filter_col1:
            application_filter = st.selectbox("Application Filter", ["All Applications"] + list(filtered_dataset["application_name"].unique()))
        
        with filter_col2:
            sentiment_filter = st.selectbox("Sentiment Filter", ["All Sentiments", "Positive", "Neutral", "Negative"])
        
        with filter_col3:
            rating_range_filter = st.selectbox("Rating Filter", ["All Ratings"] + [str(rating) for rating in sorted(filtered_dataset["score"].unique(), reverse=True)])
        
        with filter_col4:
            time_period_filter = st.selectbox("Time Period", ["All Time", "Last 30 Days", "Last 7 Days", "Last 24 Hours"])
        
        # Apply comprehensive filters
        display_dataset = filtered_dataset.copy()
        
        if application_filter != "All Applications":
            display_dataset = display_dataset[display_dataset["application_name"] == application_filter]
        
        if sentiment_filter != "All Sentiments":
            display_dataset = display_dataset[display_dataset["sentiment_category"] == sentiment_filter]
        
        if rating_range_filter != "All Ratings":
            display_dataset = display_dataset[display_dataset["score"] == int(rating_range_filter)]
        
        # Time-based filtering
        if time_period_filter == "Last 30 Days":
            cutoff_timestamp = datetime.now() - timedelta(days=30)
            display_dataset = display_dataset[display_dataset["review_timestamp"] >= cutoff_timestamp]
        elif time_period_filter == "Last 7 Days":
            cutoff_timestamp = datetime.now() - timedelta(days=7)
            display_dataset = display_dataset[display_dataset["review_timestamp"] >= cutoff_timestamp]
        elif time_period_filter == "Last 24 Hours":
            cutoff_timestamp = datetime.now() - timedelta(days=1)
            display_dataset = display_dataset[display_dataset["review_timestamp"] >= cutoff_timestamp]
        
        st.info(f"Displaying {len(display_dataset):,} reviews out of {len(filtered_dataset):,} total reviews")
        
        # Display filtered data
        if not display_dataset.empty:
            display_columns = ["application_name", "userName", "score", "content", "sentiment_category", "polarity_score", "review_timestamp"]
            st.dataframe(
                display_dataset[display_columns],
                use_container_width=True,
                height=500
            )
        else:
            st.warning("No reviews match the current filter criteria")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced Analytics Tab
    tab_analytics_index = 4 if enable_wordcloud_generation and WORDCLOUD_AVAILABLE else 3
    with analysis_tabs[tab_analytics_index]:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">Advanced Analytics</h2>', unsafe_allow_html=True)
        
        analytics_col1, analytics_col2 = st.columns(2)
        
        with analytics_col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Sentiment Score vs Rating Correlation</div>', unsafe_allow_html=True)
            
            correlation_scatter = px.scatter(
                filtered_dataset,
                x="score",
                y="polarity_score",
                color="sentiment_category",
                size="subjectivity_score",
                hover_data=["application_name"],
                color_discrete_map={
                    "Positive": "#10B981",
                    "Neutral": "#F59E0B",
                    "Negative": "#EF4444"
                },
                template='plotly_white'
            )
            correlation_scatter.update_layout(
                font=dict(family="Source Sans Pro, sans-serif"),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(correlation_scatter, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with analytics_col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Review Volume Analysis</div>', unsafe_allow_html=True)
            
            if not filtered_dataset.empty:
                volume_dataset = filtered_dataset.copy()
                volume_dataset['analysis_date'] = volume_dataset['review_timestamp'].dt.date
                daily_volume_data = volume_dataset.groupby('analysis_date').size().reset_index(name='review_count')
                
                volume_line_chart = px.line(
                    daily_volume_data,
                    x='analysis_date',
                    y='review_count',
                    markers=True,
                    template='plotly_white'
                )
                volume_line_chart.update_traces(line_color='#667eea', marker_color='#667eea')
                volume_line_chart.update_layout(
                    font=dict(family="Source Sans Pro, sans-serif")
                )
                st.plotly_chart(volume_line_chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Export Section
    st.markdown("""
    <div class="download-section">
        <div class="download-title">Export Analysis Results</div>
        <p style="text-align: center; color: #64748b; margin-bottom: 2rem;">Download your comprehensive analysis in multiple formats</p>
    </div>
    """, unsafe_allow_html=True)
    
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        complete_dataset_csv = filtered_dataset.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Complete Dataset",
            data=complete_dataset_csv,
            file_name=f"FeedbackForge_Complete_Analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with export_col2:
        # Generate executive summary
        executive_summary_data = []
        for app_name in filtered_dataset["application_name"].unique():
            app_specific_data = filtered_dataset[filtered_dataset["application_name"] == app_name]
            sentiment_distribution = app_specific_data["sentiment_category"].value_counts(normalize=True) * 100
            
            executive_summary_data.append({
                "Application": app_name,
                "Total Reviews": len(app_specific_data),
                "Average Rating": round(app_specific_data["score"].mean(), 2),
                "Average Polarity": round(app_specific_data["polarity_score"].mean(), 3),
                "Positive Percentage": round(sentiment_distribution.get("Positive", 0), 1),
                "Neutral Percentage": round(sentiment_distribution.get("Neutral", 0), 1),
                "Negative Percentage": round(sentiment_distribution.get("Negative", 0), 1)
            })
        
        executive_summary_dataframe = pd.DataFrame(executive_summary_data)
        executive_summary_csv = executive_summary_dataframe.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Executive Summary",
            data=executive_summary_csv,
            file_name=f"FeedbackForge_Executive_Summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with export_col3:
        if enable_keyword_analysis and target_keywords and 'keyword_analysis_results' in locals():
            keyword_analysis_dataframe = pd.DataFrame(
                list(keyword_analysis_results.items()), 
                columns=["Keyword", "Frequency"]
            )
            keyword_analysis_csv = keyword_analysis_dataframe.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="Keyword Analysis",
                data=keyword_analysis_csv,
                file_name=f"FeedbackForge_Keyword_Analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

else:
    # Welcome Interface
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-title">Welcome to Feedback Forge Analytics</div>
        <div class="welcome-subtitle">
            Transform application reviews into actionable business intelligence with our comprehensive analytics platform
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Showcase
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    platform_features = [
        {
            "title": "Multi-Application Analysis",
            "description": "Simultaneously analyze reviews from multiple applications with comprehensive comparative insights and performance metrics."
        },
        {
            "title": "Advanced Sentiment Intelligence",
            "description": "Sophisticated natural language processing algorithms provide detailed sentiment analysis with polarity and subjectivity scoring."
        },
        {
            "title": "Keyword Tracking & Analysis",
            "description": "Monitor specific keywords and phrases to identify trends, feature requests, and critical issues across your applications."
        },
        {
            "title": "Interactive Data Visualizations",
            "description": "Professional-grade charts and graphs that make complex data insights accessible and actionable for stakeholders."
        },
        {
            "title": "Comprehensive Word Clouds",
            "description": "Visual representations of the most frequently mentioned terms and concepts in your application reviews."
        },
        {
            "title": "Trend Analysis & Forecasting",
            "description": "Track sentiment evolution over time to measure the impact of updates, releases, and market changes."
        }
    ]
    
    feature_columns = st.columns(3)
    for index, feature in enumerate(platform_features):
        with feature_columns[index % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-title">{feature['title']}</div>
                <div class="feature-description">{feature['description']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Usage Instructions
    st.markdown("""
    <div class="content-section">
        <h3 style="color: #1e293b; margin-bottom: 1.5rem;">Getting Started with Analysis</h3>
        <div style="color: #64748b; line-height: 1.8;">
            <ol style="padding-left: 1.5rem;">
                <li><strong>Application URLs:</strong> Enter Google Play Store URLs in the configuration panel sidebar</li>
                <li><strong>Analysis Parameters:</strong> Configure language, country, and sorting preferences</li>
                <li><strong>Feature Selection:</strong> Enable keyword analysis, word cloud generation, and trend analysis</li>
                <li><strong>Execute Analysis:</strong> Click the analysis button to begin comprehensive data processing</li>
                <li><strong>Explore Results:</strong> Navigate through different analysis tabs to discover insights</li>
                <li><strong>Export Data:</strong> Download complete datasets and executive summaries</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Professional Footer
st.markdown("""
<div class="footer">
    <div class="footer-title">Feedback Forge Analytics</div>
    <div class="footer-text">
        Professional Review Intelligence & Data Analytics Platform<br>
        Developed with expertise by <strong>Ayush Pandey</strong><br>
        Powered by Advanced Machine Learning & Data Science
    </div>
</div>
""", unsafe_allow_html=True)