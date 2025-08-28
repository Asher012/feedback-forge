import streamlit as st
import pandas as pd
from google_play_scraper import Sort, reviews
from textblob import TextBlob
import plotly.graph_objects as go
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Feedback Forge",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS: Medium-inspired clean style + nav bar
st.markdown("""
<style>
    /* General styles */
    .stApp { background: #fff; color: #242424; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;}
    /* Navigation bar */
    .nav-container {
        display: flex; padding: 16px 24px; justify-content: flex-end; border-bottom: 1px solid #e6e6e6; background-color: #fff;
        position: sticky; top: 0; z-index: 999;
    }
    .nav-button {
        font-size: 16px; font-weight: 500; color: #242424; background: none; border: none; cursor: pointer;
        padding: 8px 16px; border-radius: 6px; transition: 0.2s ease; margin-left: 16px;
    }
    .nav-button:hover {
        color: #1a8917; background-color: #f8f9fa;
    }
    .nav-button-active {
        color: #1a8917; font-weight: 600; background-color: #f0fff4;
    }
    .nav-brand {
        font-weight: 700; font-size: 28px; color: #1a8917; margin-right: auto; cursor: pointer;
    }
    /* Buttons style */
    button[kind="primary"] {
        background-color: #1a8917 !important;
        color: white !important;
        border-radius: 9999px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
    }
    button[kind="primary"]:hover {
        background-color: #156f13 !important;
    }
</style>
""", unsafe_allow_html=True)

# Session state navigation helper
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False

def navigate_to(page):
    st.session_state.page = page
    st.experimental_rerun()

# Navigation bar with buttons and active highlight
def show_navigation():
    col1, col2, col3, col4 = st.columns([2,1,1,1])
    with col1:
        if st.button("Feedback Forge", key="nav_brand"):
            navigate_to('home')
    with col2:
        if st.button("Home", key="nav_home"):
            navigate_to('home')
    with col3:
        if st.button("About", key="nav_about"):
            navigate_to('about')
    with col4:
        if st.button("Analysis", key="nav_analysis"):
            navigate_to('analysis')

show_navigation()

# Helper functions
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

# Home page
if st.session_state.page == 'home':
    st.markdown("""
    <div style="max-width:800px; margin:auto; text-align:center; padding:40px 24px;">
        <h1 style="font-family: 'Source Serif Pro', serif; font-size: 56px; font-weight: 700; color:#242424; margin-bottom:24px;">Transform App Reviews Into Actionable Insights</h1>
        <p style="font-size: 22px; color: #6b6b6b; line-height: 1.4; margin-bottom: 48px;">Discover what your users really think with advanced sentiment analysis, competitive benchmarking, and detailed review intelligence.</p>
        <div style="display:flex; gap:24px; justify-content:center;">
            <button onclick="window.parent.document.querySelector('button[kind=&quot;primary&quot;]').click();" style="background:#1a8917; color:#fff; border:none; border-radius:9999px; padding:14px 28px; font-weight:600; font-size:16px; cursor:pointer;">Start Analysis</button>
            <button onclick="window.parent.document.querySelector('button[key=&quot;navigate_about&quot;]').click();" style="background:none; color:#1a8917; border:1px solid #1a8917; border-radius:9999px; padding:14px 28px; font-weight:600; font-size:16px; cursor:pointer;">Learn More</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# About page
elif st.session_state.page == 'about':
    st.markdown("""
    <div style="max-width:700px; margin: 60px auto; padding:0 24px;">
        <h1 style="font-family: 'Source Serif Pro', serif; font-size: 48px; font-weight: 700; color:#242424; margin-bottom:24px;">About Feedback Forge</h1>
        <p style="font-size:18px; color:#242424; line-height:1.7; margin-bottom:16px;">
            We help app developers and product managers make better decisions by understanding what their users really think.
        </p>
        <h2 style="font-family: 'Source Serif Pro', serif; font-size:28px; font-weight:600; color:#242424; margin-bottom:16px;">Our Mission</h2>
        <p>In today's competitive app landscape, user feedback is more valuable than ever. But with thousands of reviews across different platforms, it's nearly impossible to manually analyze what users are actually saying about your product.</p>
        <p>That's where Feedback Forge comes in. We've built a platform that automatically processes app store reviews, identifies key themes, and presents actionable insights in a way that's easy to understand and act upon.</p>
        <h2 style="font-family: 'Source Serif Pro', serif; font-size:28px; font-weight:600; color:#242424; margin-bottom:16px;">How It Works</h2>
        <p>Our system uses advanced natural language processing to understand the context and emotion behind each review. We don't just count positive and negative words – we understand the nuance of human language and can identify specific issues, feature requests, and areas of praise.</p>
        <p>The process is simple: you provide a link to your app on the Google Play Store, and we handle the rest. Within minutes, you'll have a comprehensive analysis of user sentiment, key topics, and competitive positioning.</p>
    </div>
    """, unsafe_allow_html=True)

# Analysis page
elif st.session_state.page == 'analysis':
    st.markdown("""
    <div style="max-width:800px; margin:auto; padding:24px;">
        <h1 style="font-family: 'Source Serif Pro', serif; font-size:36px; font-weight:600; margin-bottom:20px; color:#242424;">App Review Analysis</h1>
        <p style="font-size:18px; color:#6b6b6b; margin-bottom:40px;">Enter your app's Google Play Store URL to get detailed insights about user sentiment and feedback themes.</p>
    </div>
    """, unsafe_allow_html=True)

    url = st.text_area("Google Play Store URL", height=100, placeholder="https://play.google.com/store/apps/details?id=...", key="app_url")
    
    count = st.slider("Number of Reviews", min_value=50, max_value=1000, value=300, step=50)
    language = st.selectbox("Language", ["en", "hi", "es", "fr", "de", "ja"])
    sort_by = st.selectbox("Sort By", ["NEWEST", "MOST_RELEVANT", "RATING"])
    
    if st.button("Start Analysis", key="start_analysis"):
        package_name = extract_package_name(url)
        if not package_name:
            st.error("Please enter a valid Google Play Store app URL.")
            st.stop()
        
        st.info(f"Fetching reviews for {get_app_name(package_name)}...")
        sort_mapping = {"NEWEST": Sort.NEWEST, "MOST_RELEVANT": Sort.MOST_RELEVANT, "RATING": Sort.RATING}
        
        try:
            result, _ = reviews(package_name, lang=language, country="us", sort=sort_mapping[sort_by], count=count)
            if result:
                df = pd.DataFrame(result)
                df["sentiments"] = df["content"].apply(lambda t: analyze_sentiment_advanced(t)[0])
                st.write(df.head())
                # Add more detailed analysis charts and info here
            else:
                st.error("No reviews retrieved.")
        except Exception as e:
            st.error(f"Error fetching reviews: {e}")

# Footer
st.markdown("""
<div style="text-align:center; padding:24px; font-size:14px; color:#6b6b6b;">
    Built by Ayush Pandeywith care for developers and product managers who want to understand their users better.<br>
</div>
""", unsafe_allow_html=True)
