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
import time
from PIL import Image
import base64
import io

try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="Feedback Forge Analytics Pro", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS Styling with Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom Header */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
        animation: slideInDown 0.8s ease-out;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    }

    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .app-title {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
        text-shadow: 0 4px 8px rgba(0,0,0,0.2);
        background: linear-gradient(45deg, #fff, #e3f2fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .app-subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        margin-top: 0.5rem;
        opacity: 0.9;
        letter-spacing: 0.5px;
    }

    .logo-container {
        position: absolute;
        top: 20px;
        right: 30px;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255,255,255,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    /* Animated Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        animation: slideInLeft 0.6s ease-out;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }

    .feature-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.9));
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
    }

    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }

    .feature-description {
        color: #5a6c7d;
        line-height: 1.6;
        font-weight: 400;
    }

    /* Sample URLs Section */
    .sample-urls {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        color: white;
        animation: slideInLeft 1s ease-out;
    }

    .url-item {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .url-item:hover {
        background: rgba(255,255,255,0.2);
        transform: translateX(10px);
    }

    /* Custom Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(20px);
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }

    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border-radius: 10px;
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
    }

    /* Animation Classes */
    .animate-slide {
        animation: slideInLeft 0.8s ease-out;
    }

    .animate-fade {
        animation: fadeInUp 1s ease-out;
    }

    /* Chart Container */
    .chart-container {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        animation: fadeInUp 0.8s ease-out;
    }

    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Color Palettes for Professional Charts
SENTIMENT_COLORS = {
    'Positive': '#10B981',  # Emerald Green
    'Negative': '#EF4444',  # Red
    'Neutral': '#F59E0B'    # Amber
}

CHART_COLORS = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']

def create_animated_header():
    """Create animated header with logo space"""
    st.markdown("""
    <div class="main-header">
        <div class="logo-container" id="logo-space">
            📊
        </div>
        <h1 class="app-title">Feedback Forge Analytics Pro</h1>
        <p class="app-subtitle">Advanced Multi-Application Sentiment Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)

def create_sample_urls_section():
    """Create attractive sample URLs section"""
    st.markdown("""
    <div class="sample-urls">
        <h2 style="margin-bottom: 1rem; font-size: 1.8rem; font-weight: 700;">
            🎯 Sample Application URLs
        </h2>
        <p style="opacity: 0.9; margin-bottom: 1.5rem;">
            Use these sample URLs to test the platform capabilities:
        </p>

        <div class="url-item">
            <strong>📱 WorkIndia</strong><br>
            <code>https://play.google.com/store/apps/details?id=in.workindia.nileshdungarwal.workindiaandroid</code>
        </div>

        <div class="url-item">
            <strong>💬 WhatsApp</strong><br>
            <code>https://play.google.com/store/apps/details?id=com.whatsapp</code>
        </div>

        <div class="url-item">
            <strong>📷 Instagram</strong><br>
            <code>https://play.google.com/store/apps/details?id=com.instagram.android</code>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_features_showcase():
    """Create animated features showcase"""
    st.markdown('<div class="animate-fade">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3 class="feature-title">Multi-Application Analysis</h3>
            <p class="feature-description">
                Simultaneously analyze and compare sentiment across multiple applications with comprehensive statistical insights and trend identification.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">Intelligent Keyword Tracking</h3>
            <p class="feature-description">
                Monitor specific terms, phrases, and topics within reviews to identify emerging trends, feature requests, and critical issues.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">☁️</div>
            <h3 class="feature-title">Word Cloud Generation</h3>
            <p class="feature-description">
                Create visually appealing word clouds that highlight the most frequently mentioned terms in positive, negative, and neutral reviews.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3 class="feature-title">Advanced AI Sentiment Analysis</h3>
            <p class="feature-description">
                Utilize cutting-edge natural language processing algorithms to accurately determine user sentiment, polarity, and subjectivity scores.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">Professional Data Visualization</h3>
            <p class="feature-description">
                Generate publication-ready charts, graphs, and visualizations that clearly communicate insights to stakeholders and decision-makers.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3 class="feature-title">Comprehensive Analytics Dashboard</h3>
            <p class="feature-description">
                Access detailed statistical analysis, correlation studies, and trend forecasting to make data-driven business decisions.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def logo_upload_section():
    """Handle logo upload functionality"""
    with st.sidebar:
        st.markdown("### 🎨 Brand Customization")
        uploaded_logo = st.file_uploader(
            "Upload Your Logo", 
            type=["png", "jpg", "jpeg", "svg"],
            help="Upload your company logo (recommended: 200x200px)"
        )

        if uploaded_logo:
            # Display logo in sidebar
            try:
                logo_image = Image.open(uploaded_logo)
                st.image(logo_image, caption="Your Logo", use_column_width=True)

                # Convert to base64 for header injection
                buffered = io.BytesIO()
                logo_image.save(buffered, format="PNG")
                logo_b64 = base64.b64encode(buffered.getvalue()).decode()

                # Inject logo into header
                st.markdown(f"""
                <script>
                document.getElementById('logo-space').innerHTML = '<img src="data:image/png;base64,{logo_b64}" style="width:100%; height:100%; object-fit:cover; border-radius:50%;">';
                </script>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error loading logo: {e}")

def extract_app_package(url):
    """Extract package ID from Google Play URL"""
    match = re.search(r'id=([^&]+)', url)
    return match.group(1) if match else None

def perform_sentiment_analysis(text_content):
    """Enhanced sentiment analysis with polarity and subjectivity"""
    blob = TextBlob(text_content)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.1:
        sentiment = 'Positive'
    elif polarity < -0.1:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return {
        'sentiment': sentiment,
        'polarity': polarity,
        'subjectivity': subjectivity,
        'confidence': abs(polarity)
    }

def fetch_app_reviews(package_id, review_count=500):
    """Fetch reviews with error handling and progress tracking"""
    try:
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("🔍 Fetching reviews...")
        progress_bar.progress(25)

        # Fetch reviews
        result, continuation_token = reviews(
            package_id,
            lang='en',
            country='us',
            sort=Sort.MOST_RELEVANT,
            count=review_count,
            filter_score_with=None
        )

        progress_bar.progress(75)
        status_text.text("📊 Processing data...")

        if not result:
            st.error("No reviews found for this app.")
            return None

        # Convert to DataFrame
        df = pd.DataFrame(result)

        progress_bar.progress(100)
        status_text.text("✅ Reviews loaded successfully!")
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()

        return df

    except Exception as e:
        st.error(f"Error fetching reviews: {str(e)}")
        return None

def create_professional_charts(df, app_name):
    """Create professional charts with proper colors"""

    # Sentiment Analysis
    sentiment_results = []
    for content in df['content']:
        if pd.notna(content):
            result = perform_sentiment_analysis(str(content))
            sentiment_results.append(result)

    sentiment_df = pd.DataFrame(sentiment_results)

    # 1. Sentiment Distribution Pie Chart
    sentiment_counts = sentiment_df['sentiment'].value_counts()

    fig_pie = go.Figure(data=[go.Pie(
        labels=sentiment_counts.index,
        values=sentiment_counts.values,
        hole=0.4,
        marker_colors=[SENTIMENT_COLORS[label] for label in sentiment_counts.index],
        textinfo='label+percent',
        textfont_size=14,
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])

    fig_pie.update_layout(
        title=f"📊 Sentiment Distribution - {app_name}",
        title_font_size=20,
        title_x=0.5,
        font=dict(family="Inter", size=12),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=80, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # 2. Rating Distribution Bar Chart
    rating_counts = df['score'].value_counts().sort_index()

    fig_bar = go.Figure(data=[go.Bar(
        x=rating_counts.index,
        y=rating_counts.values,
        marker_color=CHART_COLORS[0],
        text=rating_counts.values,
        textposition='auto',
        hovertemplate='<b>Rating: %{x} stars</b><br>Count: %{y}<extra></extra>'
    )])

    fig_bar.update_layout(
        title=f"⭐ Rating Distribution - {app_name}",
        title_font_size=20,
        title_x=0.5,
        xaxis_title="Rating (Stars)",
        yaxis_title="Number of Reviews",
        font=dict(family="Inter", size=12),
        margin=dict(t=80, b=60, l=60, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
    )

    # 3. Polarity vs Subjectivity Scatter Plot
    fig_scatter = go.Figure(data=go.Scatter(
        x=sentiment_df['polarity'],
        y=sentiment_df['subjectivity'],
        mode='markers',
        marker=dict(
            size=8,
            color=sentiment_df['sentiment'].map(SENTIMENT_COLORS),
            opacity=0.7,
            line=dict(width=1, color='white')
        ),
        text=sentiment_df['sentiment'],
        hovertemplate='<b>Sentiment: %{text}</b><br>Polarity: %{x:.2f}<br>Subjectivity: %{y:.2f}<extra></extra>'
    ))

    fig_scatter.update_layout(
        title=f"🎯 Sentiment Analysis Scatter Plot - {app_name}",
        title_font_size=20,
        title_x=0.5,
        xaxis_title="Polarity (Negative ← → Positive)",
        yaxis_title="Subjectivity (Objective ← → Subjective)",
        font=dict(family="Inter", size=12),
        margin=dict(t=80, b=60, l=80, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=True, zerolinecolor='rgba(0,0,0,0.3)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
    )

    return fig_pie, fig_bar, fig_scatter, sentiment_df

def create_word_cloud(df, sentiment_filter=None):
    """Create word cloud for specific sentiment"""
    if not WORDCLOUD_AVAILABLE:
        st.warning("WordCloud library not available. Install it using: pip install wordcloud")
        return None

    # Filter reviews by sentiment if specified
    if sentiment_filter:
        # You would filter based on sentiment analysis results here
        text_data = ' '.join([str(content) for content in df['content'] if pd.notna(content)])
    else:
        text_data = ' '.join([str(content) for content in df['content'] if pd.notna(content)])

    if not text_data.strip():
        return None

    # Create word cloud
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        colormap='viridis',
        max_words=100,
        relative_scaling=0.5,
        random_state=42
    ).generate(text_data)

    # Convert to image for Streamlit
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    return fig

def create_metrics_cards(df, sentiment_df):
    """Create animated metrics cards"""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; font-size: 2.5rem;">📱</h3>
            <h2 style="margin:0.5rem 0; font-size: 2rem;">{len(df):,}</h2>
            <p style="margin:0; opacity:0.8;">Total Reviews</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        avg_rating = df['score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; font-size: 2.5rem;">⭐</h3>
            <h2 style="margin:0.5rem 0; font-size: 2rem;">{avg_rating:.1f}</h2>
            <p style="margin:0; opacity:0.8;">Average Rating</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        positive_pct = (sentiment_df['sentiment'] == 'Positive').mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; font-size: 2.5rem;">😊</h3>
            <h2 style="margin:0.5rem 0; font-size: 2rem;">{positive_pct:.1f}%</h2>
            <p style="margin:0; opacity:0.8;">Positive Sentiment</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        avg_polarity = sentiment_df['polarity'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; font-size: 2.5rem;">🎯</h3>
            <h2 style="margin:0.5rem 0; font-size: 2rem;">{avg_polarity:.2f}</h2>
            <p style="margin:0; opacity:0.8;">Avg Polarity</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""

    # Create animated header
    create_animated_header()

    # Logo upload in sidebar
    logo_upload_section()

    # Navigation
    with st.sidebar:
        st.markdown("### 🚀 Navigation")
        page = st.selectbox(
            "Choose Analysis Type",
            ["🏠 Home", "📱 Single App Analysis", "🔄 Multi-App Comparison", "🔍 Advanced Analytics"]
        )

    if page == "🏠 Home":
        # Show sample URLs
        create_sample_urls_section()

        # Show features
        st.markdown('<div class="animate-fade">', unsafe_allow_html=True)
        st.markdown("## 🎯 Platform Capabilities")
        create_features_showcase()
        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "📱 Single App Analysis":
        st.markdown('<div class="animate-slide">', unsafe_allow_html=True)

        # App input
        with st.container():
            st.markdown("### 📱 Single Application Analysis")

            col1, col2 = st.columns([3, 1])
            with col1:
                app_url = st.text_input(
                    "Google Play Store URL",
                    placeholder="https://play.google.com/store/apps/details?id=com.example.app",
                    help="Enter the complete Google Play Store URL"
                )

            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                analyze_btn = st.button("🔍 Analyze App", use_container_width=True)

        if analyze_btn and app_url:
            package_id = extract_app_package(app_url)

            if package_id:
                app_name = package_id.split('.')[-1].title()

                # Fetch reviews
                df = fetch_app_reviews(package_id)

                if df is not None:
                    # Create charts
                    fig_pie, fig_bar, fig_scatter, sentiment_df = create_professional_charts(df, app_name)

                    # Show metrics
                    create_metrics_cards(df, sentiment_df)

                    # Show charts in tabs
                    tab1, tab2, tab3, tab4 = st.tabs(["📊 Sentiment Overview", "⭐ Ratings", "🎯 Analysis", "☁️ Word Cloud"])

                    with tab1:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        st.plotly_chart(fig_pie, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with tab2:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        st.plotly_chart(fig_bar, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with tab3:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        st.plotly_chart(fig_scatter, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with tab4:
                        if WORDCLOUD_AVAILABLE:
                            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                            wc_fig = create_word_cloud(df)
                            if wc_fig:
                                st.pyplot(wc_fig)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.info("Install wordcloud library for word cloud generation")

        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "🔄 Multi-App Comparison":
        st.markdown('<div class="animate-slide">', unsafe_allow_html=True)
        st.markdown("### 🔄 Multi-Application Comparison")

        st.info("🚀 Multi-app comparison feature coming soon! This will allow you to compare sentiment across multiple applications simultaneously.")

        # Placeholder for multi-app comparison
        urls_text = st.text_area(
            "Enter multiple Google Play URLs (one per line)",
            height=150,
            placeholder="https://play.google.com/store/apps/details?id=com.app1\nhttps://play.google.com/store/apps/details?id=com.app2\nhttps://play.google.com/store/apps/details?id=com.app3"
        )

        if st.button("🔄 Compare Apps"):
            st.success("Multi-app comparison will be implemented here!")

        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "🔍 Advanced Analytics":
        st.markdown('<div class="animate-slide">', unsafe_allow_html=True)
        st.markdown("### 🔍 Advanced Analytics Dashboard")

        st.info("📊 Advanced analytics features including keyword tracking, trend analysis, and correlation studies coming soon!")
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.7);">
        <p>💡 Built with Streamlit • 🚀 Powered by Advanced AI • 📊 Professional Analytics</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
