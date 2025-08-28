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

# Medium-Inspired CSS (unchanged)
st.markdown("""
<style>
    /* Your existing CSS remains exactly the same */
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False

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
    // Function to handle navigation
    window.navigateTo = function(page) {{
        // This will trigger a Streamlit button click
        if (page === 'home') {{
            document.querySelector('button[key="nav_home"]').click();
        }} else if (page === 'about') {{
            document.querySelector('button[key="nav_about"]').click();
        }} else if (page === 'analysis') {{
            document.querySelector('button[key="nav_analysis"]').click();
        }}
    }}
    </script>
    """, unsafe_allow_html=True)

# Hidden buttons for navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Home", key="nav_home", type="primary", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()
with col2:
    if st.button("About", key="nav_about", type="primary", use_container_width=True):
        st.session_state.page = 'about'
        st.rerun()
with col3:
    if st.button("Analysis", key="nav_analysis", type="primary", use_container_width=True):
        st.session_state.page = 'analysis'
        st.rerun()

# Helper Functions (unchanged)
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
        
        if positive_rate > 75 and avg_rating > 4.0:
            insights.append({
                "type": "positive",
                "title": "Strong User Satisfaction",
                "description": f"Your app shows excellent performance with {positive_rate:.1f}% positive reviews and a {avg_rating:.1f} star average rating. Users are clearly happy with the experience you're providing."
            })
        elif negative_rate > 35:
            insights.append({
                "type": "warning",
                "title": "Areas for Improvement",
                "description": f"With {negative_rate:.1f}% negative feedback, there are opportunities to enhance user experience. Consider reviewing common complaints to identify improvement areas."
            })
        
        if total_reviews > 500:
            insights.append({
                "type": "positive",
                "title": "Strong User Engagement",
                "description": f"Your app has generated {total_reviews:,} reviews, indicating strong user engagement and market presence. This level of feedback provides valuable insights for growth."
            })
        
        rating_std = df['score'].std()
        if rating_std < 0.8:
            insights.append({
                "type": "positive",
                "title": "Consistent User Experience",
                "description": f"Your ratings show low variance ({rating_std:.2f}), suggesting a consistent user experience across different user types and usage patterns."
            })
        
        return insights[:4]
        
    except Exception:
        return []

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
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
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
                
                # Charts
                charts = create_charts(df_a, df_b)
                for chart_name, chart in charts.items():
                    st.plotly_chart(chart, use_container_width=True)
                
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
                        mime="text/csv"
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
                        mime="text/csv"
                    )
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                progress_bar.empty()
                status_text.empty()

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