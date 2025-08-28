import streamlit as st
import pandas as pd
from google_play_scraper import Sort, reviews
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from collections import Counter
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="Feedback Forge",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom Styling (Medium-Inspired) ---
st.markdown("""
<style>
    /* Base Layout */
    .stApp {
        background: #fff;
        color: #242424;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }

    /* Hide Default Streamlit Elements */
    .stDeployButton, header[data-testid="stHeader"] {display: none;}
    .stMainBlockContainer {padding-top: 0;}

    /* Navigation */
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
        margin: auto;
        padding: 0 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .brand {
        font-family: 'Source Serif Pro', serif;
        font-size: 28px;
        font-weight: 700;
        color: #1a8917;
        text-decoration: none;
    }
    .nav-links {
        display: flex;
        gap: 24px;
    }
    .nav-link {
        color: #242424;
        text-decoration: none;
        font-size: 16px;
        cursor: pointer;
    }
    .nav-link:hover, .nav-link.active {color: #1a8917;}

    /* Hero */
    .hero-section {
        max-width: 800px;
        margin: 80px auto;
        text-align: center;
        padding: 0 24px;
    }
    .hero-title {
        font-family: 'Source Serif Pro', serif;
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 16px;
    }
    .hero-subtitle {
        font-size: 20px;
        color: #6b6b6b;
        margin-bottom: 32px;
    }

    /* Buttons */
    .primary-button {
        background: #1a8917;
        color: white;
        border: none;
        border-radius: 9999px;
        padding: 14px 28px;
        font-size: 16px;
        cursor: pointer;
        transition: 0.2s;
        margin: 8px;
    }
    .primary-button:hover {background: #156f13; transform: translateY(-2px);}
    .secondary-button {
        background: transparent;
        color: #1a8917;
        border: 1px solid #1a8917;
        border-radius: 9999px;
        padding: 14px 28px;
        font-size: 16px;
        cursor: pointer;
        transition: 0.2s;
        margin: 8px;
    }
    .secondary-button:hover {background: #1a8917; color: white;}

    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {font-size: 36px;}
        .hero-subtitle {font-size: 18px;}
    }
</style>
""", unsafe_allow_html=True)

# --- Navigation State ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate(page):
    st.session_state.page = page
    st.rerun()

# --- Navigation ---
st.markdown(f"""
<div class="main-nav">
    <div class="nav-container">
        <div class="brand">Feedback Forge</div>
        <div class="nav-links">
            <span class="nav-link {'active' if st.session_state.page == 'home' else ''}" onclick="navigate('home')">Home</span>
            <span class="nav-link {'active' if st.session_state.page == 'about' else ''}" onclick="navigate('about')">About</span>
            <span class="nav-link {'active' if st.session_state.page == 'analysis' else ''}" onclick="navigate('analysis')">Analysis</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Home Page ---
if st.session_state.page == 'home':
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Transform App Reviews Into Insights</h1>
        <p class="hero-subtitle">
            Discover what users really think with AI-powered sentiment analysis and review intelligence.
        </p>
        <div>
            <button class="primary-button" onclick="document.querySelector('[data-testid=\\"stButton\\"] button').click()">Start Analysis</button>
            <button class="secondary-button" onclick="navigate('about')">Learn More</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("", key="start_hidden"):
        navigate("analysis")

# --- About Page ---
elif st.session_state.page == 'about':
    st.write("## About Feedback Forge")
    st.write("""
    Feedback Forge helps app developers and product managers make better decisions by understanding
    what their users really think.
    """)

# --- Analysis Page ---
elif st.session_state.page == 'analysis':
    st.write("## App Review Analysis")
    st.write("Upload your app link or select your analysis preferences.")
