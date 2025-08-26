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
    page_title="Feedback Forge X1", 
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Retro-Futuristic CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    .retro-header {
        background: linear-gradient(90deg, #0f3460, #16537e, #00ff88);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: #ffffff;
        margin-bottom: 2rem;
        border: 2px solid #00ff88;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .cyber-title {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        text-shadow: 0 0 20px #00ff88;
        margin: 0;
        letter-spacing: 3px;
    }
    
    .cyber-subtitle {
        font-size: 1.2rem;
        color: #64ffda;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    .creator-tag {
        position: absolute;
        bottom: 10px;
        right: 20px;
        background: rgba(0, 255, 136, 0.1);
        padding: 5px 15px;
        border-radius: 20px;
        border: 1px solid #00ff88;
        font-size: 0.9rem;
        color: #00ff88;
    }
    
    .terminal-box {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #00ff88;
        font-family: 'Courier New', monospace;
        box-shadow: inset 0 0 20px rgba(0, 255, 136, 0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16537e);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #00ff88;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 255, 136, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00ff88;
        font-family: 'Orbitron', monospace;
    }
    
    .metric-label {
        color: #64ffda;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #00ff88, #64ffda);
        color: #000;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        font-family: 'Orbitron', monospace;
        text-transform: uppercase;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
    }
    
    .analysis-section {
        background: rgba(0, 255, 136, 0.05);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #00ff88;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .feature-highlight {
        background: linear-gradient(45deg, rgba(100, 255, 218, 0.1), rgba(0, 255, 136, 0.1));
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #00ff88;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="retro-header">
    <div class="cyber-title">⚡ FEEDBACK FORGE X1 ⚡</div>
    <div class="cyber-subtitle">Advanced Multi-Platform Review Intelligence System</div>
    <div class="creator-tag">Created by Ayush Pandey</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem; background: linear-gradient(45deg, #0f3460, #16537e); border-radius: 10px; margin-bottom: 1rem;">
    <h2 style="color: #00ff88; font-family: 'Orbitron', monospace;">⚙️ CONTROL PANEL</h2>
    <p style="color: #64ffda; font-size: 0.9rem;">Configure Analysis Parameters</p>
</div>
""", unsafe_allow_html=True)

# Input Section
play_urls = st.sidebar.text_area(
    "📱 TARGET APP URLs:",
    placeholder="""https://play.google.com/store/apps/details?id=in.workindia.nileshdungarwal.workindiaandroid
https://play.google.com/store/apps/details?id=com.whatsapp""",
    height=120,
    help="Enter Google Play Store URLs (one per line)"
)

count = st.sidebar.slider(
    "📊 REVIEWS PER APP:", 
    min_value=10, 
    max_value=1000, 
    value=200, 
    step=25,
    help="Number of reviews to analyze from each app"
)

# Advanced Options
st.sidebar.markdown("### 🔬 ADVANCED PARAMETERS")
language = st.sidebar.selectbox("🌍 LANGUAGE:", ["en", "hi", "es", "fr", "de", "ja"], index=0)
country = st.sidebar.selectbox("🏳️ REGION:", ["in", "us", "uk", "ca", "de", "jp"], index=0)
sort_by = st.sidebar.selectbox("📈 SORT BY:", ["NEWEST", "MOST_RELEVANT", "RATING"], index=0)

# New Advanced Features
st.sidebar.markdown("### 🚀 INTELLIGENCE FEATURES")
enable_keywords = st.sidebar.checkbox("🔍 Keyword Analysis", value=True)
if WORDCLOUD_AVAILABLE:
    enable_wordcloud = st.sidebar.checkbox("☁️ Word Cloud Generation", value=True)
else:
    enable_wordcloud = False
    st.sidebar.info("📝 Word Cloud requires additional packages")

enable_trends = st.sidebar.checkbox("📈 Trend Analysis", value=True)
min_rating_filter = st.sidebar.selectbox("⭐ MINIMUM RATING:", [1, 2, 3, 4, 5], index=0)

# Keywords input
keywords = []
if enable_keywords:
    keyword_input = st.sidebar.text_input(
        "🎯 TARGET KEYWORDS:",
        placeholder="bug, crash, slow, good, excellent",
        help="Comma-separated keywords to highlight"
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
    """Advanced sentiment analysis with confidence scores"""
    if pd.isna(text) or text.strip() == "":
        return "Neutral", 0, 0
    
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.2:
        return "Positive", polarity, subjectivity
    elif polarity < -0.2:
        return "Negative", polarity, subjectivity
    else:
        return "Neutral", polarity, subjectivity

def get_app_name(package_name):
    """Extract readable app name from package"""
    parts = package_name.split('.')
    if len(parts) > 0:
        return parts[-1].replace('_', ' ').title()
    return package_name

def analyze_keywords(df, keywords):
    """Analyze keyword frequency in reviews"""
    if not keywords or df.empty:
        return {}
    
    keyword_counts = {}
    for keyword in keywords:
        count = df['content'].str.lower().str.contains(keyword, na=False).sum()
        keyword_counts[keyword] = count
    
    return keyword_counts

def generate_wordcloud(text_data):
    """Generate word cloud from text data"""
    if not WORDCLOUD_AVAILABLE or not text_data:
        return None
    
    text = " ".join(text_data)
    if len(text.strip()) == 0:
        return None
        
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='#0d1117',
        colormap='plasma',
        max_words=100
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    return fig

def create_advanced_charts(df):
    """Create advanced visualization charts"""
    charts = {}
    
    # Sentiment over time
    if 'at' in df.columns and not df.empty:
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['at']).dt.date
        daily_sentiment = df_copy.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
        
        if not daily_sentiment.empty:
            fig = px.area(
                daily_sentiment.reset_index(),
                x='date',
                y=[col for col in ['Positive', 'Neutral', 'Negative'] if col in daily_sentiment.columns],
                title="Sentiment Trends Over Time",
                color_discrete_map={
                    'Positive': '#00ff88',
                    'Neutral': '#64ffda',
                    'Negative': '#ff6b6b'
                }
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#00ff88'
            )
            charts['sentiment_timeline'] = fig
    
    return charts

# Main Analysis Button
if st.sidebar.button("🚀 INITIATE ANALYSIS", type="primary"):
    # Validate URLs
    urls_list = [url.strip() for url in play_urls.splitlines() if url.strip()]
    packages = []
    
    for url in urls_list:
        pkg = extract_package_name(url)
        if pkg:
            packages.append(pkg)
    
    if not packages:
        st.error("❌ **SYSTEM ERROR**: No valid Google Play Store URLs detected")
        st.stop()
    
    # Create progress container
    progress_container = st.container()
    with progress_container:
        st.markdown("""
        <div class="terminal-box">
            <div style="color: #00ff88;">⚡ FEEDBACK FORGE X1 - ANALYSIS INITIATED ⚡</div>
            <div style="color: #64ffda; margin-top: 0.5rem;">Scanning target applications...</div>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    all_dfs = []
    
    # Scrape reviews for each package
    for i, package in enumerate(packages):
        status_text.markdown(f"""
        <div class="terminal-box">
            <div style="color: #64ffda;">🔍 EXTRACTING DATA FROM: {get_app_name(package)}</div>
            <div style="color: #00ff88;">Package: {package}</div>
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
            st.warning(f"⚠️ **DATA EXTRACTION WARNING**: Could not process {package}: {str(e)}")
        
        progress_bar.progress((i + 1) / len(packages))
    
    # Clear progress indicators
    progress_container.empty()
    
    if not all_dfs:
        st.error("❌ **CRITICAL ERROR**: No review data successfully extracted")
        st.stop()
    
    # Combine all dataframes
    df_all = pd.concat(all_dfs, ignore_index=True)
    
    # Perform advanced sentiment analysis
    with st.spinner("🧠 **ADVANCED AI ANALYSIS IN PROGRESS...**"):
        sentiment_results = df_all["content"].apply(analyze_sentiment_advanced)
        df_all["sentiment"] = [result[0] for result in sentiment_results]
        df_all["polarity_score"] = [result[1] for result in sentiment_results]
        df_all["subjectivity_score"] = [result[2] for result in sentiment_results]
        df_all["at"] = pd.to_datetime(df_all["at"])
        
        # Filter by minimum rating
        df_filtered = df_all[df_all["score"] >= min_rating_filter].copy()
    
    st.markdown(f"""
    <div class="terminal-box">
        <div style="color: #00ff88; font-size: 1.2rem;">✅ ANALYSIS COMPLETE - INTELLIGENCE EXTRACTED</div>
        <div style="color: #64ffda;">Reviews Processed: {len(df_all)}</div>
        <div style="color: #64ffda;">Apps Analyzed: {len(packages)}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different analysis views
    if enable_wordcloud and WORDCLOUD_AVAILABLE:
        tabs = st.tabs(["📊 OVERVIEW", "🧠 INTELLIGENCE", "☁️ WORD CLOUD", "🔍 DETAILED DATA", "📈 ADVANCED ANALYTICS"])
    else:
        tabs = st.tabs(["📊 OVERVIEW", "🧠 INTELLIGENCE", "🔍 DETAILED DATA", "📈 ADVANCED ANALYTICS"])
        enable_wordcloud = False
    
    # Tab 1: Overview
    with tabs[0]:
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.markdown("## 📊 SYSTEM OVERVIEW")
        
        # Key Metrics in a grid
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{len(packages)}</div>
                <div class="metric-label">APPS ANALYZED</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{len(df_filtered):,}</div>
                <div class="metric-label">REVIEWS PROCESSED</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_rating = df_filtered["score"].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{avg_rating:.1f}⭐</div>
                <div class="metric-label">AVG RATING</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            positive_pct = (df_filtered["sentiment"] == "Positive").mean() * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{positive_pct:.1f}%</div>
                <div class="metric-label">POSITIVE SENTIMENT</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            avg_polarity = df_filtered["polarity_score"].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{avg_polarity:.2f}</div>
                <div class="metric-label">POLARITY SCORE</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sentiment Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 SENTIMENT DISTRIBUTION")
            sentiment_counts = df_filtered["sentiment"].value_counts()
            fig_pie = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="Sentiment Breakdown",
                color_discrete_map={
                    "Positive": "#00ff88",
                    "Neutral": "#64ffda", 
                    "Negative": "#ff6b6b"
                }
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#00ff88'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("### 📱 APP COMPARISON")
            app_sentiment = df_filtered.groupby(["app_name", "sentiment"]).size().unstack(fill_value=0)
            fig_bar = px.bar(
                app_sentiment.reset_index(),
                x="app_name",
                y=[col for col in ["Positive", "Neutral", "Negative"] if col in app_sentiment.columns],
                title="Sentiment by Application",
                color_discrete_map={
                    "Positive": "#00ff88",
                    "Neutral": "#64ffda",
                    "Negative": "#ff6b6b"
                }
            )
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#00ff88'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Tab 2: Intelligence Analysis
    with tabs[1]:
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.markdown("## 🧠 ADVANCED INTELLIGENCE")
        
        # Keyword Analysis
        if enable_keywords and keywords:
            st.markdown("### 🎯 KEYWORD INTELLIGENCE")
            keyword_results = analyze_keywords(df_filtered, keywords)
            
            if keyword_results:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📊 KEYWORD FREQUENCY")
                    for keyword, count in keyword_results.items():
                        percentage = (count / len(df_filtered)) * 100
                        st.markdown(f"""
                        <div class="feature-highlight">
                            <strong style="color: #00ff88;">{keyword.upper()}</strong><br>
                            <span style="color: #64ffda;">Mentions: {count} ({percentage:.1f}%)</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    if keyword_results:
                        fig_keywords = px.bar(
                            x=list(keyword_results.keys()),
                            y=list(keyword_results.values()),
                            title="Keyword Frequency Analysis",
                            color=list(keyword_results.values()),
                            color_continuous_scale="viridis"
                        )
                        fig_keywords.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#00ff88'
                        )
                        st.plotly_chart(fig_keywords, use_container_width=True)
        
        # Advanced Charts
        if enable_trends:
            st.markdown("### 📈 TREND INTELLIGENCE")
            advanced_charts = create_advanced_charts(df_filtered)
            
            for chart_name, chart in advanced_charts.items():
                st.plotly_chart(chart, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 3: Word Cloud (only if available)
    if enable_wordcloud and WORDCLOUD_AVAILABLE:
        with tabs[2]:
            st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
            st.markdown("## ☁️ WORD CLOUD ANALYSIS")
            
            # Generate word clouds for different sentiments
            sentiments = ["Positive", "Negative", "Neutral"]
            cols = st.columns(len(sentiments))
            
            for i, sentiment in enumerate(sentiments):
                with cols[i]:
                    st.markdown(f"### {sentiment} Reviews")
                    sentiment_reviews = df_filtered[df_filtered["sentiment"] == sentiment]["content"].tolist()
                    
                    if sentiment_reviews:
                        wordcloud_fig = generate_wordcloud(sentiment_reviews)
                        if wordcloud_fig:
                            st.pyplot(wordcloud_fig)
                    else:
                        st.info(f"No {sentiment.lower()} reviews found")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 4: Detailed Data
    tab_idx = 3 if enable_wordcloud and WORDCLOUD_AVAILABLE else 2
    with tabs[tab_idx]:
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.markdown("## 🔍 DETAILED DATA ANALYSIS")
        
        # Advanced filters
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            app_filter = st.selectbox("📱 Filter by App:", ["All"] + list(df_filtered["app_name"].unique()))
        with col2:
            sentiment_filter = st.selectbox("😊 Filter by Sentiment:", ["All", "Positive", "Neutral", "Negative"])
        with col3:
            rating_filter = st.selectbox("⭐ Filter by Rating:", ["All"] + list(sorted(df_filtered["score"].unique(), reverse=True)))
        with col4:
            date_filter = st.selectbox("📅 Time Period:", ["All Time", "Last 30 Days", "Last 7 Days"])
        
        # Apply filters
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
        
        st.markdown(f"**Showing {len(display_df):,} of {len(df_filtered):,} reviews**")
        
        # Display data
        if not display_df.empty:
            display_columns = ["app_name", "userName", "score", "content", "sentiment", "polarity_score", "at"]
            st.dataframe(
                display_df[display_columns],
                use_container_width=True,
                height=500
            )
        else:
            st.warning("No reviews match the selected filters")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 5: Advanced Analytics
    tab_idx_adv = 4 if enable_wordcloud and WORDCLOUD_AVAILABLE else 3
    with tabs[tab_idx_adv]:
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.markdown("## 📈 ADVANCED ANALYTICS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 SENTIMENT vs RATING CORRELATION")
            fig_scatter = px.scatter(
                df_filtered,
                x="score",
                y="polarity_score",
                color="sentiment",
                size="subjectivity_score",
                title="Sentiment Score vs Star Rating",
                color_discrete_map={
                    "Positive": "#00ff88",
                    "Neutral": "#64ffda",
                    "Negative": "#ff6b6b"
                }
            )
            fig_scatter.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#00ff88'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            st.markdown("### 📅 REVIEW VOLUME OVER TIME")
            if not df_filtered.empty:
                df_filtered_copy = df_filtered.copy()
                df_filtered_copy['date'] = df_filtered_copy['at'].dt.date
                daily_counts = df_filtered_copy.groupby('date').size().reset_index(name='count')
                
                fig_volume = px.line(
                    daily_counts,
                    x='date',
                    y='count',
                    title="Daily Review Volume",
                    markers=True
                )
                fig_volume.update_traces(line_color='#00ff88')
                fig_volume.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#00ff88'
                )
                st.plotly_chart(fig_volume, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Download Section
    st.markdown("""
    <div class="terminal-box">
        <div style="color: #00ff88; font-size: 1.2rem;">📥 DATA EXPORT PROTOCOLS</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 EXPORT COMPLETE DATASET",
            data=csv_data,
            file_name=f"FeedbackForge_Complete_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Summary report
        summary_data = []
        for app in df_filtered["app_name"].unique():
            app_data = df_filtered[df_filtered["app_name"] == app]
            sentiment_dist = app_data["sentiment"].value_counts(normalize=True) * 100
            
            summary_data.append({
                "App Name": app,
                "Total Reviews": len(app_data),
                "Average Rating": app_data["score"].mean(),
                "Average Polarity": app_data["polarity_score"].mean(),
                "Positive %": sentiment_dist.get("Positive", 0),
                "Neutral %": sentiment_dist.get("Neutral", 0),
                "Negative %": sentiment_dist.get("Negative", 0)
            })
        
        summary_df = pd.DataFrame(summary_data)
        csv_summary = summary_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📈 EXPORT INTELLIGENCE REPORT",
            data=csv_summary,
            file_name=f"FeedbackForge_Intelligence_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col3:
        # Keywords analysis export
        if enable_keywords and keywords and 'keyword_results' in locals():
            keyword_df = pd.DataFrame(list(keyword_results.items()), columns=["Keyword", "Frequency"])
            keyword_csv = keyword_df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="🎯 EXPORT KEYWORD ANALYSIS",
                data=keyword_csv,
                file_name=f"FeedbackForge_Keywords_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

else:
    # Welcome Interface
    st.markdown("""
    <div class="analysis-section">
        <h2 style="color: #00ff88; font-family: 'Orbitron', monospace; text-align: center;">
            ⚡ WELCOME TO FEEDBACK FORGE X1 ⚡
        </h2>
        <p style="color: #64ffda; text-align: center; font-size: 1.1rem; margin-bottom: 2rem;">
            Advanced Multi-Platform Review Intelligence System
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-highlight">
            <h3 style="color: #00ff88;">🚀 SYSTEM CAPABILITIES</h3>
            <ul style="color: #64ffda;">
                <li>✅ Multi-App Comparative Analysis</li>
                <li>✅ Advanced AI Sentiment Intelligence</li>
                <li>✅ Real-time Keyword Tracking</li>
                <li>✅ Interactive Data Visualization</li>
                <li>✅ Word Cloud Generation</li>
                <li>✅ Trend Analysis & Forecasting</li>
                <li>✅ Export & Reporting Protocols</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-highlight">
            <h3 style="color: #00ff88;">📋 OPERATION MANUAL</h3>
            <ol style="color: #64ffda;">
                <li><strong>Configure Parameters:</strong> Set URLs and analysis options in control panel</li>
                <li><strong>Initiate Scan:</strong> Click "INITIATE ANALYSIS" to begin extraction</li>
                <li><strong>Intelligence Review:</strong> Explore results in organized tabs</li>
                <li><strong>Export Data:</strong> Download reports in various formats</li>
                <li><strong>Iterate:</strong> Refine parameters for deeper insights</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="terminal-box">
        <div style="text-align: center;">
            <div style="color: #00ff88; font-size: 1.3rem; font-family: 'Orbitron', monospace;">SAMPLE TARGET APPLICATIONS</div>
            <div style="color: #64ffda; margin-top: 1rem;">
                https://play.google.com/store/apps/details?id=in.workindia.nileshdungarwal.workindiaandroid<br>
                https://play.google.com/store/apps/details?id=com.whatsapp<br>
                https://play.google.com/store/apps/details?id=com.instagram.android
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; color: #64ffda; padding: 2rem; margin-top: 3rem; border-top: 1px solid #00ff88;'>
    <div style='font-family: "Orbitron", monospace; font-size: 1.1rem; color: #00ff88; margin-bottom: 0.5rem;'>
        ⚡ FEEDBACK FORGE X1 ⚡
    </div>
    <div style='font-size: 0.9rem;'>
        Created with 💚 by <strong style="color: #00ff88;">Ayush Pandey</strong> | 
        Advanced Review Intelligence Platform | 
        Powered by AI & Data Science
    </div>
</div>
""", unsafe_allow_html=True)