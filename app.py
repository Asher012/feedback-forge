import streamlit as st
import pandas as pd
from google_play_scraper import Sort, reviews
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re

# Page Configuration
st.set_page_config(
    page_title="Feedback Forge", 
    page_icon="🔨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0d5aa7;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🔨 Feedback Forge</h1>
    <p>Multi-App Review & Sentiment Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("## 🔧 Configuration")
st.sidebar.markdown("---")

# Input Section
play_urls = st.sidebar.text_area(
    "📱 Enter Google Play Store URLs:",
    placeholder="""https://play.google.com/store/apps/details?id=in.workindia.nileshdungarwal.workindiaandroid
https://play.google.com/store/apps/details?id=com.example.app""",
    height=120,
    help="Paste one URL per line"
)

count = st.sidebar.slider(
    "📊 Reviews per app:", 
    min_value=10, 
    max_value=500, 
    value=100, 
    step=10,
    help="Number of reviews to fetch from each app"
)

# Advanced Options
st.sidebar.markdown("### Advanced Options")
language = st.sidebar.selectbox("🌍 Language:", ["en", "hi", "es", "fr"], index=0)
country = st.sidebar.selectbox("🏳️ Country:", ["in", "us", "uk", "ca"], index=0)
sort_by = st.sidebar.selectbox("📈 Sort by:", ["NEWEST", "MOST_RELEVANT", "RATING"], index=0)

# Helper Functions
def extract_package_name(url):
    """Extract package name from Google Play URL"""
    if "id=" in url:
        package = url.split("id=")[1].split("&")[0]
        return package.strip()
    return None

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob"""
    if pd.isna(text) or text.strip() == "":
        return "Neutral", 0
    
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        return "Positive", polarity
    elif polarity < -0.1:
        return "Negative", polarity
    else:
        return "Neutral", polarity

def get_app_name(package_name):
    """Extract a readable app name from package"""
    # Simple extraction - you can enhance this
    parts = package_name.split('.')
    if len(parts) > 0:
        return parts[-1].replace('_', ' ').title()
    return package_name

# Main Analysis Button
if st.sidebar.button("🚀 Start Analysis", type="primary"):
    # Validate URLs
    urls_list = [url.strip() for url in play_urls.splitlines() if url.strip()]
    packages = []
    
    for url in urls_list:
        pkg = extract_package_name(url)
        if pkg:
            packages.append(pkg)
    
    if not packages:
        st.error("❌ Please enter valid Google Play Store URLs")
        st.stop()
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    all_dfs = []
    
    # Scrape reviews for each package
    for i, package in enumerate(packages):
        status_text.text(f"🔍 Scraping reviews for {get_app_name(package)}...")
        
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
            st.warning(f"⚠️ Could not fetch reviews for {package}: {str(e)}")
        
        progress_bar.progress((i + 1) / len(packages))
    
    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()
    
    if not all_dfs:
        st.error("❌ No reviews were successfully fetched")
        st.stop()
    
    # Combine all dataframes
    df_all = pd.concat(all_dfs, ignore_index=True)
    
    # Perform sentiment analysis
    with st.spinner("🧠 Analyzing sentiment..."):
        sentiment_results = df_all["content"].apply(analyze_sentiment)
        df_all["sentiment"] = [result[0] for result in sentiment_results]
        df_all["sentiment_score"] = [result[1] for result in sentiment_results]
        df_all["at"] = pd.to_datetime(df_all["at"])
    
    st.success(f"✅ Analysis complete! Processed {len(df_all)} reviews from {len(packages)} app(s)")
    
    # Display Results
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📱 Apps Analyzed", len(packages))
    
    with col2:
        st.metric("📝 Total Reviews", len(df_all))
    
    with col3:
        avg_rating = df_all["score"].mean()
        st.metric("⭐ Average Rating", f"{avg_rating:.1f}")
    
    with col4:
        positive_percentage = (df_all["sentiment"] == "Positive").mean() * 100
        st.metric("😊 Positive Sentiment", f"{positive_percentage:.1f}%")
    
    # Sentiment Distribution Chart
    st.markdown("### 🎯 Overall Sentiment Distribution")
    
    sentiment_counts = df_all["sentiment"].value_counts()
    fig_pie = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title="Sentiment Distribution",
        color_discrete_map={
            "Positive": "#2ecc71",
            "Neutral": "#f39c12", 
            "Negative": "#e74c3c"
        }
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # App-wise Comparison
    st.markdown("### 📱 App-wise Analysis")
    
    # Create app-wise sentiment breakdown
    app_sentiment = df_all.groupby(["app_name", "sentiment"]).size().unstack(fill_value=0)
    
    fig_bar = px.bar(
        app_sentiment.reset_index(),
        x="app_name",
        y=["Positive", "Neutral", "Negative"],
        title="Sentiment Distribution by App",
        labels={"value": "Number of Reviews", "app_name": "App Name"},
        color_discrete_map={
            "Positive": "#2ecc71",
            "Neutral": "#f39c12",
            "Negative": "#e74c3c"
        }
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Rating Distribution
    st.markdown("### ⭐ Rating Distribution")
    
    fig_hist = px.histogram(
        df_all,
        x="score",
        color="sentiment",
        title="Rating Distribution with Sentiment",
        labels={"score": "Star Rating", "count": "Number of Reviews"},
        color_discrete_map={
            "Positive": "#2ecc71",
            "Neutral": "#f39c12",
            "Negative": "#e74c3c"
        }
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Timeline Analysis
    st.markdown("### 📅 Review Timeline")
    
    df_all["date"] = df_all["at"].dt.date
    timeline_data = df_all.groupby(["date", "sentiment"]).size().unstack(fill_value=0)
    
    fig_timeline = px.line(
        timeline_data.reset_index(),
        x="date",
        y=["Positive", "Neutral", "Negative"],
        title="Sentiment Trends Over Time",
        labels={"value": "Number of Reviews", "date": "Date"}
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Detailed Data Table
    st.markdown("### 📋 Detailed Review Data")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        app_filter = st.selectbox("Filter by App:", ["All"] + list(df_all["app_name"].unique()))
    with col2:
        sentiment_filter = st.selectbox("Filter by Sentiment:", ["All", "Positive", "Neutral", "Negative"])
    with col3:
        min_rating = st.selectbox("Minimum Rating:", [1, 2, 3, 4, 5], index=0)
    
    # Apply filters
    filtered_df = df_all.copy()
    if app_filter != "All":
        filtered_df = filtered_df[filtered_df["app_name"] == app_filter]
    if sentiment_filter != "All":
        filtered_df = filtered_df[filtered_df["sentiment"] == sentiment_filter]
    filtered_df = filtered_df[filtered_df["score"] >= min_rating]
    
    # Display filtered data
    display_columns = ["app_name", "userName", "score", "content", "sentiment", "sentiment_score", "at"]
    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        height=400
    )
    
    # Download Options
    st.markdown("### 📥 Download Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Full dataset download
        csv_full = df_all.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Download Complete Dataset",
            data=csv_full,
            file_name=f"FeedbackForge_Complete_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Summary report download
        summary_data = {
            "App Name": [],
            "Total Reviews": [],
            "Average Rating": [],
            "Positive %": [],
            "Neutral %": [],
            "Negative %": []
        }
        
        for app in df_all["app_name"].unique():
            app_data = df_all[df_all["app_name"] == app]
            sentiment_dist = app_data["sentiment"].value_counts(normalize=True) * 100
            
            summary_data["App Name"].append(app)
            summary_data["Total Reviews"].append(len(app_data))
            summary_data["Average Rating"].append(app_data["score"].mean())
            summary_data["Positive %"].append(sentiment_dist.get("Positive", 0))
            summary_data["Neutral %"].append(sentiment_dist.get("Neutral", 0))
            summary_data["Negative %"].append(sentiment_dist.get("Negative", 0))
        
        summary_df = pd.DataFrame(summary_data)
        csv_summary = summary_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📈 Download Summary Report",
            data=csv_summary,
            file_name=f"FeedbackForge_Summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

else:
    # Welcome message when no analysis is running
    st.markdown("""
    ## Welcome to Feedback Forge! 🔨
    
    **Your comprehensive review analysis platform**
    
    ### How to use:
    1. **📱 Add URLs**: Paste Google Play Store app URLs in the sidebar
    2. **⚙️ Configure**: Set the number of reviews and other options
    3. **🚀 Analyze**: Click "Start Analysis" to begin
    4. **📊 Explore**: View interactive charts and insights
    5. **📥 Download**: Export your data and reports
    
    ### Features:
    - ✅ Multi-app comparison
    - ✅ Real-time sentiment analysis
    - ✅ Interactive visualizations
    - ✅ Detailed data filtering
    - ✅ Export capabilities
    - ✅ Timeline analysis
    
    ### Sample URLs to try:
    ```
    https://play.google.com/store/apps/details?id=in.workindia.nileshdungarwal.workindiaandroid
    https://play.google.com/store/apps/details?id=com.whatsapp
    ```
    
    ---
    
    **Built with ❤️ for data-driven insights**
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    Made with 💪 by <strong>Feedback Forge</strong> | 
    Powered by Streamlit | 
    Data from Google Play Store
</div>
""", unsafe_allow_html=True)