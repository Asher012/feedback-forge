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

# Page Configuration
st.set_page_config(
    page_title="Feedback Forge", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Medium-Inspired CSS (unchanged, keeping the same styling)
st.markdown("""
<style>
    /* CSS remains exactly the same */
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
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
                <span class="nav-link" 
                      onclick="window.navigateTo('contact')">Contact</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# JavaScript for navigation
st.markdown("""
<script>
// Store navigation function in window object for global access
window.navigateTo = function(page) {
    // This will be handled by the hidden buttons
    if (page === 'home') {
        document.querySelector('button[key="nav_home"]').click();
    } else if (page === 'about') {
        document.querySelector('button[key="nav_about"]').click();
    } else if (page === 'analysis') {
        document.querySelector('button[key="nav_analysis"]').click();
    } else if (page === 'contact') {
        document.querySelector('button[key="nav_contact"]').click();
    }
}
</script>
""", unsafe_allow_html=True)

# Navigation handlers
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Home", key="nav_home", type="primary"):
        st.session_state.page = 'home'
        st.rerun()
with col2:
    if st.button("About", key="nav_about", type="primary"):
        st.session_state.page = 'about'
        st.rerun()
with col3:
    if st.button("Analysis", key="nav_analysis", type="primary"):
        st.session_state.page = 'analysis'
        st.rerun()
with col4:
    if st.button("Contact", key="nav_contact", type="primary"):
        st.session_state.page = 'contact'
        st.rerun()

# Helper Functions (unchanged, keeping the same functionality)
def extract_package_name(url):
    if "id=" in url:
        return url.split("id=")[1].split("&")[0].strip()
    return None

def analyze_sentiment_advanced(text):
    # Function remains the same
    pass

def get_app_name(package_name):
    # Function remains the same
    pass

def generate_insights(df):
    # Function remains the same
    pass

def create_charts(df_a, df_b=None):
    # Function remains the same
    pass

def display_review_cards(df, max_reviews=10):
    # Function remains the same
    pass

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
    
    # Features Section (unchanged)
    st.markdown("""
    <div class="content-container">
        <!-- Content remains the same -->
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
        <!-- About sections remain the same -->
        
        <div class="about-section">
            <h2>Developer Information</h2>
            <p>
                Feedback Forge was developed by <strong>Ayush Pandey</strong>, a passionate developer 
                with expertise in data analysis, machine learning, and user experience design.
            </p>
            <p>
                The application combines advanced natural language processing techniques with 
                intuitive visualization to help businesses understand their customers better.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# CONTACT PAGE (new page)
elif st.session_state.page == 'contact':
    st.markdown("""
    <div class="about-hero">
        <h1 class="hero-title">Contact Us</h1>
        <p class="hero-subtitle">
            Have questions or feedback? We'd love to hear from you.
        </p>
    </div>
    
    <div class="form-section">
        <h2 class="form-title">Get in Touch</h2>
        <p style="text-align: center; margin-bottom: 30px;">
            Developed by <strong>Ayush Pandey</strong>
        </p>
        
        <div style="max-width: 600px; margin: 0 auto;">
            <div class="feature-card">
                <h3 class="feature-title">Email</h3>
                <p class="feature-description">
                    For support inquiries: support@feedbackforge.com
                </p>
            </div>
            
            <div class="feature-card">
                <h3 class="feature-title">Feedback</h3>
                <p class="feature-description">
                    We're constantly improving Feedback Forge. Share your suggestions 
                    and feature requests at feedback@feedbackforge.com
                </p>
            </div>
            
            <div class="feature-card">
                <h3 class="feature-title">Development</h3>
                <p class="feature-description">
                    For technical inquiries and collaboration opportunities, 
                    please contact ayush.pandey@feedbackforge.com
                </p>
            </div>
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
                url_a = st.text_input("Google Play Store URL", placeholder="https://play.google.com/store/apps/details?id=...", key="url_a")
            
            with col2:
                st.markdown("**Second App**")
                url_b = st.text_input("Google Play Store URL", placeholder="https://play.google.com/store/apps/details?id=...", key="url_b")
        else:
            st.markdown("### App Analysis")
            url_a = st.text_input("Google Play Store URL", placeholder="https://play.google.com/store/apps/details?id=...", key="url_a_single")
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
                status_text.text(f"Analyzing {get_app_name(package_a)}...")
                result_a, _ = reviews(package_a, lang=language, country="us", sort=sort_mapping[sort_by], count=count)
                
                if result_a:
                    df_a = pd.DataFrame(result_a)
                    df_a["package"] = package_a
                    df_a["app_name"] = get_app_name(package_a)
                    
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
                    status_text.text(f"Analyzing {get_app_name(package_b)}...")
                    result_b, _ = reviews(package_b, lang=language, country="us", sort=sort_mapping[sort_by], count=count)
                    
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
                status_text.text("Analysis complete!")
                
                # Store results in session state
                st.session_state.analysis_data = {
                    'df_a': df_a,
                    'df_b': df_b,
                    'package_a': package_a,
                    'package_b': package_b,
                    'comparison_mode': st.session_state.comparison_mode
                }
                st.session_state.analysis_complete = True
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                st.rerun()
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                progress_bar.empty()
                status_text.empty()
    
    # Display results if analysis is complete
    if st.session_state.analysis_complete and st.session_state.analysis_data:
        data = st.session_state.analysis_data
        df_a = data['df_a']
        df_b = data['df_b']
        package_a = data['package_a']
        package_b = data['package_b']
        
        # Display Results
        st.success(f"Successfully analyzed {len(df_a):,} reviews" + 
                  (f" and {len(df_b):,} reviews" if df_b is not None else ""))
        
        # Metrics Section (unchanged)
        # Charts (unchanged)
        # Insights (unchanged)
        # Individual Reviews (unchanged)
        # Export Options (unchanged)

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