import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import re
from collections import Counter, defaultdict
import json
import base64
from io import BytesIO
import time
import warnings
from functools import lru_cache
import hashlib

# Suppress warnings
warnings.filterwarnings('ignore')

# Advanced Page Configuration
st.set_page_config(
    page_title="ReviewForge Analytics Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "ReviewForge Analytics Pro - Advanced Review Analysis Platform"
    }
)

# Modern CSS Styling with Professional Design
def apply_modern_styling():
    st.markdown("""
    <style>
    /* Import Modern Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* CSS Variables for Theming */
    :root {
        --primary-color: #667eea;
        --primary-dark: #764ba2;
        --secondary-color: #f093fb;
        --accent-color: #4facfe;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --info-color: #3b82f6;
        
        --bg-primary: #0f1419;
        --bg-secondary: #1a202c;
        --bg-card: #2d3748;
        --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --bg-card-gradient: linear-gradient(145deg, #2d3748, #1a202c);
        
        --text-primary: #ffffff;
        --text-secondary: #a0aec0;
        --text-muted: #718096;
        
        --border-color: #4a5568;
        --border-light: #2d3748;
        
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --shadow-glow: 0 0 20px rgba(102, 126, 234, 0.3);
        
        --radius-sm: 4px;
        --radius: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
        
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-fast: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Global Styles */
    .main, .block-container {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        line-height: 1.6;
    }

    .stApp {
        background: var(--bg-primary) !important;
    }

    /* Header Styles */
    .main-header {
        background: var(--bg-card-gradient);
        padding: 2.5rem;
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-xl), var(--shadow-glow);
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--bg-gradient);
    }

    .header-title {
        font-size: 3rem;
        font-weight: 800;
        background: var(--bg-gradient);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .header-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    .developer-credit {
        background: var(--bg-gradient);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: var(--radius-lg);
        font-weight: 600;
        display: inline-block;
        margin-top: 1rem;
        font-size: 0.9rem;
        box-shadow: var(--shadow-lg);
        transition: var(--transition);
    }

    .developer-credit:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-xl);
    }

    /* Card Styles */
    .metric-card, .analysis-card, .insight-card {
        background: var(--bg-card-gradient);
        padding: 2rem;
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
        text-align: center;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--bg-gradient);
        opacity: 0;
        transition: var(--transition);
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl), var(--shadow-glow);
        border-color: var(--primary-color);
    }

    .metric-card:hover::before {
        opacity: 1;
    }

    .metric-value {
        font-size: 2.75rem;
        font-weight: 800;
        background: var(--bg-gradient);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
    }

    .metric-label {
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.8rem;
    }

    /* Sidebar Styles */
    .css-1d391kg, .css-1cypcdb {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color);
    }

    .sidebar-title {
        color: white;
        font-weight: 700;
        font-size: 1.25rem;
        margin-bottom: 1.5rem;
        text-align: center;
        padding: 1.25rem;
        background: var(--bg-gradient);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-lg);
    }

    /* Button Styles */
    .stButton button {
        background: var(--bg-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-lg) !important;
        padding: 0.875rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: var(--transition) !important;
        box-shadow: var(--shadow-lg) !important;
        width: 100% !important;
        text-transform: none !important;
        letter-spacing: 0.01em !important;
    }

    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-xl) !important;
        filter: brightness(1.1) !important;
    }

    .stButton button:active {
        transform: translateY(0) !important;
    }

    /* Input Styles */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        background: var(--bg-card) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: var(--radius-lg) !important;
        padding: 0.875rem !important;
        color: var(--text-primary) !important;
        font-size: 0.95rem !important;
        transition: var(--transition) !important;
    }

    .stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }

    /* Multiselect Styles */
    .stMultiSelect [data-baseweb="select"] {
        background: var(--bg-card) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: var(--radius-lg) !important;
    }

    /* Progress Bar */
    .stProgress .st-bo {
        background: var(--bg-gradient) !important;
        height: 8px !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow) !important;
    }

    /* Alert Styles */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: var(--radius-lg) !important;
        padding: 1.25rem !important;
        font-weight: 500 !important;
        box-shadow: var(--shadow-lg) !important;
    }

    .stSuccess {
        background: var(--success-color) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
    }

    .stWarning {
        background: var(--warning-color) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
    }

    .stError {
        background: var(--error-color) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
    }

    .stInfo {
        background: var(--info-color) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
    }

    /* Chart Container Styles */
    .chart-container {
        background: var(--bg-card-gradient);
        padding: 2rem;
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
        transition: var(--transition);
    }

    .chart-container:hover {
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-color);
    }

    .chart-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
        text-align: center;
    }

    /* Navigation Styles */
    .nav-item {
        background: var(--bg-card);
        padding: 1rem 1.25rem;
        border-radius: var(--radius-lg);
        margin-bottom: 0.75rem;
        cursor: pointer;
        transition: var(--transition);
        border: 2px solid transparent;
        text-align: left;
        font-weight: 500;
        position: relative;
        overflow: hidden;
    }

    .nav-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 0;
        background: var(--bg-gradient);
        transition: var(--transition);
    }

    .nav-item:hover {
        background: var(--bg-card);
        border-color: var(--primary-color);
        transform: translateX(4px);
        box-shadow: var(--shadow-lg);
    }

    .nav-item:hover::before {
        width: 4px;
    }

    .nav-item.active {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-dark);
        box-shadow: var(--shadow-glow);
    }

    /* Table Styles */
    .dataframe {
        background: var(--bg-card) !important;
        border-radius: var(--radius-lg) !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-lg) !important;
        border: 1px solid var(--border-color) !important;
    }

    .dataframe th {
        background: var(--bg-gradient) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1.25rem 1rem !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    .dataframe td {
        padding: 1rem !important;
        border-bottom: 1px solid var(--border-light) !important;
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
    }

    .dataframe tr:hover {
        background-color: rgba(102, 126, 234, 0.05) !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: var(--radius);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--bg-gradient);
        border-radius: var(--radius);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-dark);
    }

    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    @keyframes shimmer {
        0% { background-position: -468px 0; }
        100% { background-position: 468px 0; }
    }

    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    .shimmer {
        animation: shimmer 1.5s ease-in-out infinite;
        background: linear-gradient(to right, transparent 0%, rgba(102, 126, 234, 0.1) 50%, transparent 100%);
        background-size: 468px 100%;
    }

    /* Section Divider */
    .section-divider {
        height: 2px;
        background: var(--bg-gradient);
        margin: 3rem 0;
        border-radius: var(--radius);
        box-shadow: var(--shadow);
    }

    /* Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: var(--radius-lg);
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .status-badge.success {
        background: rgba(16, 185, 129, 0.1);
        color: var(--success-color);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .status-badge.warning {
        background: rgba(245, 158, 11, 0.1);
        color: var(--warning-color);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .status-badge.error {
        background: rgba(239, 68, 68, 0.1);
        color: var(--error-color);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* Feature Card */
    .feature-card {
        background: var(--bg-card-gradient);
        padding: 1.5rem;
        border-radius: var(--radius-xl);
        border: 1px solid var(--border-color);
        transition: var(--transition);
    }

    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-color);
    }

    .feature-icon {
        width: 3rem;
        height: 3rem;
        background: var(--bg-gradient);
        border-radius: var(--radius-lg);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.25rem;
        }
        
        .metric-card {
            padding: 1.5rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .main-header {
            padding: 2rem 1.5rem;
        }
    }

    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stDeployButton {display: none;}
    
    /* Custom Metrics */
    [data-testid="metric-container"] {
        background: var(--bg-card-gradient);
        border: 1px solid var(--border-color);
        padding: 1.5rem;
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-lg);
        transition: var(--transition);
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-color);
    }
    
    [data-testid="metric-container"] > div {
        color: var(--text-primary);
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--primary-color);
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
    }

    /* Plotly Chart Styling */
    .js-plotly-plot .plotly .modebar {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius) !important;
    }
    </style>
    """, unsafe_allow_html=True)

apply_modern_styling()

# Session State Management
def initialize_session_state():
    """Initialize session state with default values"""
    defaults = {
        'current_page': 'dashboard',
        'analyzed_data': None,
        'competitor_data': None,
        'analysis_history': [],
        'user_preferences': {
            'theme': 'dark',
            'auto_refresh': True,
            'export_format': 'csv'
        },
        'ml_models': {},
        'advanced_insights': {},
        'export_data': None,
        'cached_reviews': {},
        'app_info': {},
        'user_authenticated': True,
        'user_role': 'admin',
        'current_app_name': 'Unknown App',
        'competitor_app_name': 'Competitor App',
        'ml_insights': None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# Mock Data Generator for Demo
class MockDataGenerator:
    """Generate realistic mock data for demonstration"""
    
    @staticmethod
    def generate_reviews(count=500):
        """Generate mock review data"""
        np.random.seed(42)
        
        # Sample review content
        positive_reviews = [
            "Excellent app! Love the user interface and smooth performance.",
            "Amazing features and very intuitive design. Highly recommend!",
            "Perfect app for my needs. Works flawlessly on my device.",
            "Outstanding quality and great customer support. Five stars!",
            "Wonderful experience using this app. Very user-friendly.",
            "Great app with fantastic features. Keep up the good work!",
            "Love the new update! Much faster and more responsive now.",
            "This app has exceeded my expectations. Truly remarkable!",
            "Incredible functionality and beautiful design. Well done!",
            "Best app in its category. Couldn't be happier with it."
        ]
        
        negative_reviews = [
            "App crashes frequently and has many bugs. Needs improvement.",
            "Poor performance and confusing interface. Very disappointed.",
            "Doesn't work as advertised. Waste of time and storage space.",
            "Too many ads and the app is very slow. Not recommended.",
            "Terrible user experience. The app freezes constantly.",
            "Bad design and poor functionality. Needs complete overhaul.",
            "App is buggy and unreliable. Can't complete basic tasks.",
            "Worst app I've ever used. Constantly crashing and glitching.",
            "Very poor quality and customer service is non-existent.",
            "Disappointing app with limited features and many issues."
        ]
        
        neutral_reviews = [
            "Decent app with some useful features. Could be better.",
            "Average performance. Some features work well, others don't.",
            "It's okay for basic use. Nothing special but does the job.",
            "Mixed experience. Some parts are good, others need work.",
            "Fair app with room for improvement. Has potential.",
            "Works fine for most things. Some minor issues here and there.",
            "Standard app functionality. Nothing to complain about.",
            "It's alright. Does what it's supposed to do reasonably well.",
            "Mediocre app. Not bad but not great either.",
            "Acceptable quality. Gets the job done with some limitations."
        ]
        
        all_reviews = positive_reviews + negative_reviews + neutral_reviews
        
        data = []
        base_date = datetime.now() - timedelta(days=365)
        
        for i in range(count):
            # Generate review data
            score = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.1, 0.2, 0.35, 0.3])
            
            if score >= 4:
                content = np.random.choice(positive_reviews)
                sentiment = np.random.choice(['Positive', 'Highly Positive'], p=[0.4, 0.6])
                polarity = np.random.uniform(0.3, 1.0)
                emotional_intensity = np.random.uniform(0.5, 2.0)
            elif score <= 2:
                content = np.random.choice(negative_reviews)
                sentiment = np.random.choice(['Negative', 'Highly Negative'], p=[0.5, 0.5])
                polarity = np.random.uniform(-1.0, -0.3)
                emotional_intensity = np.random.uniform(-2.0, -0.5)
            else:
                content = np.random.choice(neutral_reviews)
                sentiment = 'Neutral'
                polarity = np.random.uniform(-0.2, 0.2)
                emotional_intensity = np.random.uniform(-0.3, 0.3)
            
            review_date = base_date + timedelta(days=np.random.randint(0, 365))
            
            data.append({
                'at': review_date,
                'userName': f'User{i+1}',
                'score': score,
                'content': content,
                'sentiment': sentiment,
                'polarity': polarity,
                'subjectivity': np.random.uniform(0.0, 1.0),
                'confidence': np.random.uniform(0.7, 0.95),
                'emotional_intensity': emotional_intensity,
                'aspect_performance': np.random.choice([True, False], p=[0.3, 0.7]),
                'aspect_ui_design': np.random.choice([True, False], p=[0.25, 0.75]),
                'aspect_functionality': np.random.choice([True, False], p=[0.4, 0.6]),
                'aspect_usability': np.random.choice([True, False], p=[0.35, 0.65]),
                'aspect_reliability': np.random.choice([True, False], p=[0.2, 0.8]),
                'keywords': np.random.choice(['great app', 'user friendly', 'needs improvement', 'excellent', 'poor quality'])
            })
        
        return pd.DataFrame(data)

# Initialize mock data generator
mock_generator = MockDataGenerator()

# Advanced Helper Functions
class ReviewAnalyzer:
    def __init__(self):
        self.mock_mode = True  # Enable mock mode for demo
        
    def extract_package_name(self, url):
        """Extract package name from Google Play URL"""
        if not url:
            return None
            
        # For demo purposes, return a valid package name format
        if 'play.google.com' in url or '.' in url:
            if 'id=' in url:
                match = re.search(r'id=([a-zA-Z0-9_.]+)', url)
                if match:
                    return match.group(1)
            else:
                # Assume it's already a package name
                return url.strip()
        return None
    
    def validate_package_name(self, package_name):
        """Validate package name format"""
        if not package_name:
            return False
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)*$'
        return bool(re.match(pattern, package_name)) and len(package_name.split('.')) >= 2
    
    def get_app_name(self, package_name):
        """Extract app name from package name"""
        if not package_name:
            return "Demo App"
        parts = package_name.split('.')
        return parts[-1].replace('_', ' ').title()
    
    def scrape_reviews(self, package_name, count=500, sort_by=None):
        """Mock review scraping with realistic data"""
        if self.mock_mode:
            with st.spinner(f"Generating {count} demo reviews for analysis..."):
                time.sleep(2)  # Simulate API delay
                return mock_generator.generate_reviews(count)
        else:
            # Real implementation would go here
            st.error("Real Google Play scraping requires additional setup. Using demo mode.")
            return mock_generator.generate_reviews(count)
    
    def generate_ml_insights(self, df):
        """Generate mock ML insights"""
        if df.empty:
            return {}
        
        # Mock topic modeling results
        topics = [
            {'topic_id': 1, 'keywords': ['user', 'interface', 'design', 'easy', 'navigation'], 'weight': 0.25},
            {'topic_id': 2, 'keywords': ['performance', 'speed', 'fast', 'responsive', 'smooth'], 'weight': 0.22},
            {'topic_id': 3, 'keywords': ['feature', 'functionality', 'useful', 'tool', 'capability'], 'weight': 0.20},
            {'topic_id': 4, 'keywords': ['bug', 'crash', 'issue', 'problem', 'error'], 'weight': 0.18},
            {'topic_id': 5, 'keywords': ['update', 'improvement', 'better', 'enhance', 'version'], 'weight': 0.15}
        ]
        
        # Mock key phrases
        key_phrases = [
            {'phrase': 'user friendly', 'frequency': 45},
            {'phrase': 'great app', 'frequency': 38},
            {'phrase': 'easy to use', 'frequency': 32},
            {'phrase': 'highly recommend', 'frequency': 28},
            {'phrase': 'works perfectly', 'frequency': 24},
            {'phrase': 'needs improvement', 'frequency': 20},
            {'phrase': 'love this app', 'frequency': 18},
            {'phrase': 'excellent quality', 'frequency': 15},
            {'phrase': 'very helpful', 'frequency': 12},
            {'phrase': 'poor performance', 'frequency': 10}
        ]
        
        return {
            'topics': topics,
            'clusters': list(np.random.randint(0, 3, len(df))),
            'n_clusters': 3,
            'key_phrases': key_phrases,
            'tfidf_features': ['user', 'app', 'great', 'good', 'interface', 'design', 'performance', 'feature', 'easy', 'recommend']
        }
    
    def analyze_trends(self, df):
        """Analyze rating trends over time"""
        if df.empty or 'at' not in df.columns:
            return None
            
        df = df.copy()
        df['date'] = pd.to_datetime(df['at']).dt.date
        df['week'] = pd.to_datetime(df['at']).dt.to_period('W').apply(lambda r: r.start_time)
        
        # Daily trends
        daily_stats = df.groupby('date').agg({
            'score': ['mean', 'count'],
            'polarity': 'mean',
            'emotional_intensity': 'mean'
        }).round(3)
        
        daily_stats.columns = ['avg_rating', 'review_count', 'avg_polarity', 'avg_intensity']
        
        # Weekly trends
        weekly_stats = df.groupby('week').agg({
            'score': ['mean', 'count'],
            'polarity': 'mean',
            'emotional_intensity': 'mean'
        }).round(3)
        
        weekly_stats.columns = ['avg_rating', 'review_count', 'avg_polarity', 'avg_intensity']
        
        return {
            'daily': daily_stats,
            'weekly': weekly_stats
        }

# Initialize analyzer
analyzer = ReviewAnalyzer()

# Caching functions for better performance
@st.cache_data(ttl=3600, show_spinner=False)
def cached_scrape_reviews(package_name, count=500):
    """Cached version of review scraping"""
    return analyzer.scrape_reviews(package_name, count)

@st.cache_data(ttl=3600, show_spinner=False)
def cached_generate_ml_insights(df_hash):
    """Cached version of ML insights generation"""
    # Generate insights based on hash to ensure consistency
    return analyzer.generate_ml_insights(pd.DataFrame())  # Mock implementation

def get_dataframe_hash(df):
    """Generate a hash for dataframe to use as cache key"""
    if df is None or df.empty:
        return "empty"
    return hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()

def create_header():
    """Create modern header with developer credit"""
    st.markdown("""
    <div class="main-header">
        <h1 class="header-title">ReviewForge Analytics Pro</h1>
        <p class="header-subtitle">Advanced AI-Powered Review Analysis Platform</p>
        <div class="developer-credit">
            Developed by Ayush Pandey - Advanced Analytics & Machine Learning
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_navigation():
    """Create modern navigation system"""
    st.sidebar.markdown('<div class="sidebar-title">Navigation Hub</div>', unsafe_allow_html=True)

    pages = {
        'dashboard': '📊 Analytics Dashboard',
        'deep_analysis': '🔬 Deep Analysis Engine',
        'competitor': '⚔️ Competitive Intelligence',
        'ml_insights': '🤖 ML Insights Laboratory',
        'trend_analysis': '📈 Trend Analysis',
        'export_reports': '📄 Export & Reporting',
        'settings': '⚙️ Advanced Settings'
    }

    current_page = st.session_state.current_page

    for page_key, page_name in pages.items():
        if st.sidebar.button(
            page_name, 
            key=f"nav_{page_key}", 
            use_container_width=True,
            type="primary" if page_key == current_page else "secondary"
        ):
            st.session_state.current_page = page_key
            st.rerun()

    # Current page indicator
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div class="feature-card">
        <h3>Current Page</h3>
        <p style="color: #667eea; font-weight: 600;">{pages[current_page]}</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick stats if data is available
    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data
        st.sidebar.markdown("""
        <div class="feature-card">
            <h3>Quick Stats</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Reviews", f"{len(df):,}")
        with col2:
            if 'score' in df.columns:
                st.metric("Avg Rating", f"{df['score'].mean():.1f}")

def create_metrics_dashboard(df):
    """Create comprehensive metrics dashboard"""
    if df.empty:
        return

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.subheader("📊 Key Performance Indicators")

    cols = st.columns(5)

    metrics = [
        ("Average Rating", df['score'].mean() if 'score' in df.columns else 0, "⭐", "1f"),
        ("Total Reviews", len(df), "📝", ","),
        ("Positive Rate", (df['sentiment'].str.contains('Positive', na=False).sum() / len(df)) * 100 if 'sentiment' in df.columns else 0, "😊", "1f%"),
        ("Confidence", df['confidence'].mean() * 100 if 'confidence' in df.columns else 0, "🎯", "1f%"),
        ("Intensity", abs(df['emotional_intensity'].mean()) if 'emotional_intensity' in df.columns else 0, "💪", "2f")
    ]

    for i, (label, value, icon, fmt) in enumerate(metrics):
        with cols[i]:
            if fmt == "," :
                st.metric(f"{icon} {label}", f"{value:,}")
            elif "%" in fmt:
                st.metric(f"{icon} {label}", f"{value:.1f}%")
            elif "f" in fmt:
                precision = int(fmt[0])
                st.metric(f"{icon} {label}", f"{value:.{precision}f}")

def create_advanced_visualizations(df):
    """Create advanced interactive visualizations"""
    if df.empty:
        return

    # Modern color palette
    colors = {
        'primary': '#667eea',
        'secondary': '#764ba2', 
        'accent': '#4facfe',
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444',
        'positive': '#10b981',
        'negative': '#ef4444',
        'neutral': '#6b7280'
    }

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.subheader("📈 Advanced Analytics Visualizations")

    # 1. Sentiment Distribution with enhanced styling
    col1, col2 = st.columns(2)

    with col1:
        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts()

            fig_donut = go.Figure(data=[go.Pie(
                labels=sentiment_counts.index,
                values=sentiment_counts.values,
                hole=0.6,
                marker=dict(
                    colors=[colors['positive'] if 'Positive' in s else 
                           colors['negative'] if 'Negative' in s else colors['neutral'] 
                           for s in sentiment_counts.index],
                    line=dict(color='#1a202c', width=2)
                ),
                textinfo='label+percent+value',
                textfont=dict(size=12, color='white'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])

            fig_donut.update_layout(
                title=dict(
                    text='🎭 Sentiment Distribution Analysis',
                    x=0.5,
                    font=dict(size=18, color='white')
                ),
                annotations=[dict(
                    text=f'<b>Total</b><br>{sentiment_counts.sum():,}',
                    x=0.5, y=0.5,
                    font_size=14,
                    font_color='white',
                    showarrow=False
                )],
                showlegend=True,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )

            st.plotly_chart(fig_donut, use_container_width=True)

    with col2:
        if 'score' in df.columns:
            rating_dist = df['score'].value_counts().sort_index()

            fig_rating = go.Figure()
            fig_rating.add_trace(go.Bar(
                x=[f'{i} ⭐' for i in rating_dist.index],
                y=rating_dist.values,
                marker=dict(
                    color=[colors['error'] if i <= 2 else 
                          colors['warning'] if i == 3 else colors['success'] 
                          for i in rating_dist.index],
                    line=dict(color='#1a202c', width=1)
                ),
                text=rating_dist.values,
                textposition='outside',
                textfont=dict(color='white'),
                hovertemplate='<b>%{x}</b><br>Count: %{y}<br>Percentage: %{customdata:.1f}%<extra></extra>',
                customdata=[(count/rating_dist.sum()*100) for count in rating_dist.values]
            ))

            fig_rating.update_layout(
                title=dict(
                    text='⭐ Rating Distribution',
                    x=0.5,
                    font=dict(size=18, color='white')
                ),
                xaxis=dict(title='Rating', color='white'),
                yaxis=dict(title='Number of Reviews', color='white'),
                showlegend=False,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )

            st.plotly_chart(fig_rating, use_container_width=True)

    # 2. Time-based Analysis
    if 'at' in df.columns:
        st.subheader("⏱️ Temporal Analysis")
        
        df_time = df.copy()
        df_time['date'] = pd.to_datetime(df_time['at']).dt.date
        daily_stats = df_time.groupby('date').agg({
            'score': 'mean',
            'polarity': 'mean'
        }).reset_index()

        fig_time = make_subplots(
            rows=2, cols=1,
            subplot_titles=['Daily Average Rating', 'Daily Sentiment Polarity'],
            vertical_spacing=0.1
        )

        fig_time.add_trace(
            go.Scatter(
                x=daily_stats['date'],
                y=daily_stats['score'],
                mode='lines+markers',
                name='Average Rating',
                line=dict(color=colors['primary'], width=3),
                marker=dict(size=6)
            ),
            row=1, col=1
        )

        fig_time.add_trace(
            go.Scatter(
                x=daily_stats['date'],
                y=daily_stats['polarity'],
                mode='lines+markers',
                name='Sentiment Polarity',
                line=dict(color=colors['accent'], width=3),
                marker=dict(size=6),
                fill='tonexty'
            ),
            row=2, col=1
        )

        fig_time.update_layout(
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )

        fig_time.update_xaxes(color='white')
        fig_time.update_yaxes(color='white')

        st.plotly_chart(fig_time, use_container_width=True)

    # 3. Advanced Aspect Analysis
    aspect_cols = [col for col in df.columns if col.startswith('aspect_')]
    if aspect_cols:
        st.subheader("🎯 Aspect Analysis Overview")

        aspect_data = {}
        for col in aspect_cols:
            aspect_name = col.replace('aspect_', '').replace('_', ' ').title()
            coverage = (df[col].sum() / len(df)) * 100
            aspect_data[aspect_name] = coverage

        # Create radar chart
        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=list(aspect_data.values()),
            theta=list(aspect_data.keys()),
            fill='toself',
            name='Aspect Coverage %',
            line=dict(color=colors['primary'], width=3),
            marker=dict(size=8, color=colors['accent'])
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(aspect_data.values()) * 1.1] if aspect_data.values() else [0, 100],
                    color='white'
                ),
                angularaxis=dict(color='white')
            ),
            title=dict(
                text='🎯 Aspect Coverage Analysis',
                x=0.5,
                font=dict(size=18, color='white')
            ),
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )

        st.plotly_chart(fig_radar, use_container_width=True)

def dashboard_page():
    """Main dashboard page with enhanced UI"""
    create_header()

    # Input section with modern styling
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.subheader("🚀 Application Analysis Configuration")

    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            url_input = st.text_input(
                "📱 Google Play Store URL or Package Name",
                placeholder="https://play.google.com/store/apps/details?id=com.example.app",
                help="Enter the full Google Play Store URL or just the package name"
            )

        with col2:
            review_count = st.selectbox(
                "📊 Reviews to Analyze",
                options=[100, 250, 500, 1000, 2000],
                index=2,
                help="More reviews provide better insights but take longer to process"
            )

        with col3:
            sort_option = st.selectbox(
                "🔄 Sort Reviews By",
                options=["Newest", "Rating", "Helpfulness"],
                help="Choose how to sort the reviews for analysis"
            )

    # Analysis button with enhanced styling
    analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])
    with analyze_col2:
        if st.button("🔬 Analyze Application", type="primary", use_container_width=True):
            if url_input.strip():
                package_name = analyzer.extract_package_name(url_input)

                if package_name or url_input.strip():  # Allow any input for demo
                    with st.spinner("🚀 Performing advanced analysis..."):
                        # Use demo data
                        df = analyzer.scrape_reviews(
                            package_name or "demo.app", 
                            count=review_count
                        )

                        if not df.empty:
                            st.session_state.analyzed_data = df
                            st.session_state.current_app_name = analyzer.get_app_name(package_name or url_input)
                            
                            # Success animation
                            st.balloons()
                            st.success(f"✅ Successfully analyzed {len(df)} reviews for {st.session_state.current_app_name}!")
                        else:
                            st.error("❌ Failed to analyze the application. Please try again.")
                else:
                    st.warning("⚠️ Please enter a valid Google Play Store URL or package name")

    # Display results with enhanced formatting
    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data
        
        # App info header
        st.markdown(f"""
        <div class="feature-card" style="text-align: center; margin: 2rem 0;">
            <div class="feature-icon">📱</div>
            <h2 style="margin-bottom: 0.5rem;">Analysis Results</h2>
            <h3 style="color: #667eea;">{st.session_state.current_app_name}</h3>
            <div class="status-badge success">
                ✅ Analysis Complete - {len(df):,} Reviews Processed
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Metrics dashboard
        create_metrics_dashboard(df)

        # Visualizations
        create_advanced_visualizations(df)

        # Recent reviews table with enhanced styling
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("📋 Recent Reviews Sample")
        
        display_columns = ['at', 'userName', 'score', 'sentiment', 'confidence', 'content']
        available_columns = [col for col in display_columns if col in df.columns]

        if available_columns:
            sample_df = df[available_columns].head(10).copy()
            if 'at' in sample_df.columns:
                sample_df['at'] = pd.to_datetime(sample_df['at']).dt.strftime('%Y-%m-%d')
            if 'content' in sample_df.columns:
                sample_df['content'] = sample_df['content'].str[:80] + '...'
            if 'confidence' in sample_df.columns:
                sample_df['confidence'] = (sample_df['confidence'] * 100).round(1).astype(str) + '%'

            st.dataframe(
                sample_df, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    'score': st.column_config.NumberColumn('Rating', format='⭐ %.0f'),
                    'sentiment': st.column_config.TextColumn('Sentiment'),
                    'confidence': st.column_config.TextColumn('Confidence'),
                }
            )

def deep_analysis_page():
    """Deep analysis page with ML insights"""
    st.markdown("""
    <div class="feature-card" style="text-align: center; margin-bottom: 2rem;">
        <div class="feature-icon">🔬</div>
        <h1>Deep Analysis Engine</h1>
        <p>Advanced analytical tools and machine learning insights</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data

        # Generate ML insights if not cached
        if not st.session_state.ml_insights:
            with st.spinner("🤖 Generating machine learning insights..."):
                time.sleep(1)  # Simulate processing
                ml_insights = analyzer.generate_ml_insights(df)
                st.session_state.ml_insights = ml_insights

        ml_insights = st.session_state.ml_insights

        # Topic Analysis Section
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("🏷️ Topic Modeling Analysis")
        
        if 'topics' in ml_insights and ml_insights['topics']:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                topics_data = []
                for topic in ml_insights['topics']:
                    topics_data.append({
                        'Topic ID': f"Topic {topic['topic_id']}",
                        'Top Keywords': ', '.join(topic['keywords'][:5]),
                        'Relevance': f"{topic['weight']:.1%}",
                        'Weight': topic['weight']
                    })

                topics_df = pd.DataFrame(topics_data)
                st.dataframe(
                    topics_df[['Topic ID', 'Top Keywords', 'Relevance']], 
                    use_container_width=True, 
                    hide_index=True
                )

            with col2:
                # Topic distribution chart
                topic_weights = [topic['weight'] for topic in ml_insights['topics']]
                topic_labels = [f"Topic {topic['topic_id']}" for topic in ml_insights['topics']]

                fig_topics = go.Figure(data=[go.Pie(
                    labels=topic_labels,
                    values=topic_weights,
                    hole=0.4,
                    marker=dict(colors=['#667eea', '#764ba2', '#4facfe', '#10b981', '#f59e0b'])
                )])

                fig_topics.update_layout(
                    title='Topic Distribution',
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    showlegend=True
                )

                st.plotly_chart(fig_topics, use_container_width=True)

        # Key Phrases Analysis
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("🔑 Key Phrases Extraction")
        
        if 'key_phrases' in ml_insights and ml_insights['key_phrases']:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                phrases_data = []
                for phrase_data in ml_insights['key_phrases'][:8]:
                    relevance = 'High' if phrase_data['frequency'] > 20 else 'Medium' if phrase_data['frequency'] > 10 else 'Low'
                    phrases_data.append({
                        'Phrase': phrase_data['phrase'].title(),
                        'Frequency': phrase_data['frequency'],
                        'Relevance': relevance
                    })

                phrases_df = pd.DataFrame(phrases_data)
                st.dataframe(phrases_df, use_container_width=True, hide_index=True)

            with col2:
                # Phrase frequency chart
                phrases = [p['phrase'] for p in ml_insights['key_phrases'][:5]]
                frequencies = [p['frequency'] for p in ml_insights['key_phrases'][:5]]

                fig_phrases = go.Figure(data=[go.Bar(
                    x=frequencies,
                    y=phrases,
                    orientation='h',
                    marker=dict(
                        color=frequencies,
                        colorscale='Viridis',
                        showscale=True
                    )
                )])

                fig_phrases.update_layout(
                    title='Top Phrases by Frequency',
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )

                st.plotly_chart(fig_phrases, use_container_width=True)

        # Statistical Analysis
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("📊 Statistical Analysis Summary")

        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            if 'score' in df.columns:
                st.metric(
                    "📊 Rating Std Dev", 
                    f"{df['score'].std():.2f}",
                    help="Lower values indicate more consistent ratings"
                )

        with stat_col2:
            if 'polarity' in df.columns:
                st.metric(
                    "🎭 Sentiment Range", 
                    f"{df['polarity'].max() - df['polarity'].min():.2f}",
                    help="Range of sentiment scores in the data"
                )

        with stat_col3:
            if 'confidence' in df.columns:
                st.metric(
                    "🎯 Avg Confidence", 
                    f"{df['confidence'].mean():.1%}",
                    help="Average confidence in sentiment analysis"
                )

        with stat_col4:
            unique_users = df['userName'].nunique() if 'userName' in df.columns else len(df)
            st.metric(
                "👥 Unique Reviewers", 
                f"{unique_users:,}",
                help="Number of unique users who left reviews"
            )

    else:
        # Call-to-action when no data
        st.markdown("""
        <div class="feature-card" style="text-align: center; margin: 3rem 0;">
            <div class="feature-icon">📊</div>
            <h3>Ready for Deep Analysis</h3>
            <p>Analyze an application from the Dashboard to unlock advanced ML insights, topic modeling, and statistical analysis.</p>
        </div>
        """, unsafe_allow_html=True)

def competitor_analysis_page():
    """Competitive intelligence page"""
    st.markdown("""
    <div class="feature-card" style="text-align: center; margin-bottom: 2rem;">
        <div class="feature-icon">⚔️</div>
        <h1>Competitive Intelligence</h1>
        <p>Compare your app against competitors with advanced benchmarking</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📱 Primary App Analysis")
        if st.session_state.analyzed_data is not None:
            df_primary = st.session_state.analyzed_data
            
            st.markdown(f"""
            <div class="status-badge success">
                ✅ {st.session_state.current_app_name} Analyzed
            </div>
            """, unsafe_allow_html=True)

            # Primary app metrics
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                if 'score' in df_primary.columns:
                    avg_rating = df_primary['score'].mean()
                    st.metric("⭐ Average Rating", f"{avg_rating:.1f}")

            with metric_col2:
                if 'sentiment' in df_primary.columns:
                    positive_rate = (df_primary['sentiment'].str.contains('Positive', na=False).sum() / len(df_primary)) * 100
                    st.metric("😊 Positive Sentiment", f"{positive_rate:.1f}%")
        else:
            st.markdown("""
            <div class="status-badge warning">
                ⚠️ No Primary App Analyzed Yet
            </div>
            """, unsafe_allow_html=True)
            st.info("📊 Analyze your primary app from the Dashboard first")

    with col2:
        st.markdown("### 🎯 Competitor App")
        competitor_url = st.text_input(
            "🔗 Competitor App URL",
            placeholder="Enter competitor's Google Play URL or package name"
        )

        if st.button("🔬 Analyze Competitor", use_container_width=True):
            if competitor_url:
                package_name = analyzer.extract_package_name(competitor_url) or competitor_url

                with st.spinner("🚀 Analyzing competitor..."):
                    time.sleep(2)  # Simulate analysis
                    competitor_df = analyzer.scrape_reviews(package_name, count=500)

                    if not competitor_df.empty:
                        st.session_state.competitor_data = competitor_df
                        st.session_state.competitor_app_name = analyzer.get_app_name(package_name)
                        st.success("✅ Competitor analyzed successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to analyze competitor")
            else:
                st.warning("⚠️ Please enter a competitor URL")

        if st.session_state.competitor_data is not None:
            st.markdown(f"""
            <div class="status-badge success">
                ✅ {st.session_state.competitor_app_name} Analyzed  
            </div>
            """, unsafe_allow_html=True)

    # Comparative Analysis
    if (st.session_state.analyzed_data is not None and 
        st.session_state.competitor_data is not None):

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("📊 Head-to-Head Comparison")

        df_primary = st.session_state.analyzed_data
        df_competitor = st.session_state.competitor_data

        # Comparison metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            primary_rating = df_primary['score'].mean() if 'score' in df_primary.columns else 0
            competitor_rating = df_competitor['score'].mean() if 'score' in df_competitor.columns else 0

            fig_rating = go.Figure(data=[
                go.Bar(
                    name='Your App',
                    x=['Rating Comparison'],
                    y=[primary_rating],
                    marker_color='#10b981',
                    text=[f'{primary_rating:.1f}'],
                    textposition='outside'
                ),
                go.Bar(
                    name='Competitor',
                    x=['Rating Comparison'],
                    y=[competitor_rating],
                    marker_color='#ef4444',
                    text=[f'{competitor_rating:.1f}'],
                    textposition='outside'
                )
            ])

            fig_rating.update_layout(
                title='⭐ Average Rating Battle',
                barmode='group',
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=True
            )

            st.plotly_chart(fig_rating, use_container_width=True)

        with col2:
            if all('sentiment' in df.columns for df in [df_primary, df_competitor]):
                primary_positive = (df_primary['sentiment'].str.contains('Positive', na=False).sum() / len(df_primary)) * 100
                competitor_positive = (df_competitor['sentiment'].str.contains('Positive', na=False).sum() / len(df_competitor)) * 100

                fig_sentiment = go.Figure(data=[
                    go.Bar(
                        name='Your App',
                        x=['Sentiment Battle'],
                        y=[primary_positive],
                        marker_color='#667eea',
                        text=[f'{primary_positive:.1f}%'],
                        textposition='outside'
                    ),
                    go.Bar(
                        name='Competitor',
                        x=['Sentiment Battle'],
                        y=[competitor_positive],
                        marker_color='#764ba2',
                        text=[f'{competitor_positive:.1f}%'],
                        textposition='outside'
                    )
                ])

                fig_sentiment.update_layout(
                    title='😊 Positive Sentiment Battle',
                    barmode='group',
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    showlegend=True
                )

                st.plotly_chart(fig_sentiment, use_container_width=True)

        with col3:
            volume_data = {
                'Your App': len(df_primary),
                'Competitor': len(df_competitor)
            }

            fig_volume = go.Figure(data=[
                go.Bar(
                    name='Review Volume',
                    x=list(volume_data.keys()),
                    y=list(volume_data.values()),
                    marker_color=['#4facfe', '#f093fb'],
                    text=[f'{v:,}' for v in volume_data.values()],
                    textposition='outside'
                )
            ])

            fig_volume.update_layout(
                title='📊 Review Volume Comparison',
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False
            )

            st.plotly_chart(fig_volume, use_container_width=True)

        # Detailed comparison matrix
        st.subheader("📈 Comprehensive Comparison Matrix")

        primary_name = st.session_state.get('current_app_name', 'Your App')
        competitor_name = st.session_state.get('competitor_app_name', 'Competitor')

        comparison_data = {
            'Metric': [
                'Average Rating',
                'Total Reviews',
                'Positive Sentiment %',
                'Average Confidence',
                'Emotional Intensity',
                'Rating Consistency'
            ],
            primary_name: [
                f"{df_primary['score'].mean():.2f}" if 'score' in df_primary.columns else 'N/A',
                f"{len(df_primary):,}",
                f"{(df_primary['sentiment'].str.contains('Positive', na=False).sum() / len(df_primary)) * 100:.1f}%" if 'sentiment' in df_primary.columns else 'N/A',
                f"{df_primary['confidence'].mean() * 100:.1f}%" if 'confidence' in df_primary.columns else 'N/A',
                f"{abs(df_primary['emotional_intensity'].mean()):.2f}" if 'emotional_intensity' in df_primary.columns else 'N/A',
                f"{df_primary['score'].std():.2f}" if 'score' in df_primary.columns else 'N/A'
            ],
            competitor_name: [
                f"{df_competitor['score'].mean():.2f}" if 'score' in df_competitor.columns else 'N/A',
                f"{len(df_competitor):,}",
                f"{(df_competitor['sentiment'].str.contains('Positive', na=False).sum() / len(df_competitor)) * 100:.1f}%" if 'sentiment' in df_competitor.columns else 'N/A',
                f"{df_competitor['confidence'].mean() * 100:.1f}%" if 'confidence' in df_competitor.columns else 'N/A',
                f"{abs(df_competitor['emotional_intensity'].mean()):.2f}" if 'emotional_intensity' in df_competitor.columns else 'N/A',
                f"{df_competitor['score'].std():.2f}" if 'score' in df_competitor.columns else 'N/A'
            ]
        }

        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

        # Strategic insights
        st.subheader("💡 Strategic Insights & Recommendations")
        
        insights = []
        
        if 'score' in df_primary.columns and 'score' in df_competitor.columns:
            rating_diff = df_primary['score'].mean() - df_competitor['score'].mean()
            if rating_diff > 0.2:
                insights.append("🎯 **Rating Advantage**: Your app has a significant rating advantage. Focus on maintaining this quality edge.")
            elif rating_diff < -0.2:
                insights.append("⚠️ **Rating Gap**: Competitor has higher ratings. Consider quality improvements and bug fixes.")
            else:
                insights.append("⚖️ **Rating Parity**: Ratings are comparable. Differentiate through features and user experience.")

        if len(df_primary) > len(df_competitor) * 1.5:
            insights.append("📈 **Volume Leader**: You have significantly more reviews, indicating higher market penetration.")
        elif len(df_competitor) > len(df_primary) * 1.5:
            insights.append("🚀 **Growth Opportunity**: Competitor has more reviews. Focus on user acquisition and retention.")

        for insight in insights[:3]:  # Show top 3 insights
            st.markdown(f"- {insight}")

def trend_analysis_page():
    """Time series analysis page"""
    st.markdown("""
    <div class="feature-card" style="text-align: center; margin-bottom: 2rem;">
        <div class="feature-icon">📈</div>
        <h1>Trend Analysis</h1>
        <p>Analyze how reviews and ratings change over time</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data
        
        # Generate trend analysis
        trends = analyzer.analyze_trends(df)
        
        if trends:
            st.subheader("📊 Rating Trends Over Time")
            
            # Daily trends chart
            daily_data = trends['daily'].reset_index()
            
            fig_daily = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Daily Average Rating Trend', 'Daily Review Volume'),
                vertical_spacing=0.1
            )

            # Rating trend
            fig_daily.add_trace(
                go.Scatter(
                    x=daily_data['date'],
                    y=daily_data['avg_rating'],
                    mode='lines+markers',
                    name='Daily Rating',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=6),
                    fill='tonexty'
                ),
                row=1, col=1
            )

            # Overall average line
            overall_avg = daily_data['avg_rating'].mean()
            fig_daily.add_hline(
                y=overall_avg,
                line_dash="dash",
                line_color="#ef4444",
                annotation_text=f"Overall Avg: {overall_avg:.1f}",
                row=1, col=1
            )

            # Volume bars
            fig_daily.add_trace(
                go.Bar(
                    x=daily_data['date'],
                    y=daily_data['review_count'],
                    name='Review Volume',
                    marker_color='#4facfe',
                    opacity=0.7
                ),
                row=2, col=1
            )

            fig_daily.update_layout(
                height=600,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False
            )

            fig_daily.update_xaxes(color='white')
            fig_daily.update_yaxes(color='white')

            st.plotly_chart(fig_daily, use_container_width=True)
            
            # Weekly summary
            st.subheader("📅 Weekly Performance Summary")
            
            weekly_data = trends['weekly'].reset_index()
            latest_week = weekly_data.iloc[-1] if len(weekly_data) > 0 else None
            
            if latest_week is not None:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Latest Week Rating", f"{latest_week['avg_rating']:.1f}")
                with col2:
                    st.metric("Weekly Reviews", f"{latest_week['review_count']:,}")
                with col3:
                    st.metric("Sentiment Score", f"{latest_week['avg_polarity']:.2f}")
                with col4:
                    st.metric("Emotional Intensity", f"{latest_week['avg_intensity']:.2f}")

            # Correlation analysis
            if len(daily_data) > 1:
                correlation = daily_data['review_count'].corr(daily_data['avg_rating'])
                
                st.subheader("🔗 Volume vs Rating Correlation")
                st.metric("Correlation Coefficient", f"{correlation:.3f}")
                
                if correlation > 0.3:
                    st.success("📈 Positive correlation: More reviews tend to coincide with higher ratings")
                elif correlation < -0.3:
                    st.warning("📉 Negative correlation: More reviews tend to coincide with lower ratings")
                else:
                    st.info("↔️ Weak correlation: Review volume and rating are not strongly related")

        else:
            st.warning("⚠️ Insufficient temporal data for trend analysis. Need reviews with timestamps.")
    else:
        st.markdown("""
        <div class="feature-card" style="text-align: center; margin: 3rem 0;">
            <div class="feature-icon">📊</div>
            <h3>Ready for Trend Analysis</h3>
            <p>Analyze an application from the Dashboard to unlock time-based insights and rating trends.</p>
        </div>
        """, unsafe_allow_html=True)

def export_reports_page():
    """Export and reporting functionality"""
    st.markdown("""
    <div class="feature-card" style="text-align: center; margin-bottom: 2rem;">
        <div class="feature-icon">📄</div>
        <h1>Export & Reporting</h1>
        <p>Generate comprehensive reports and export your analysis data</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data
        app_name = st.session_state.get('current_app_name', 'Unknown App')

        st.subheader(f"📊 Export Options for {app_name}")

        # Export format selection
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📊 Export as CSV", use_container_width=True):
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV Report",
                    data=csv_data,
                    file_name=f"{app_name.replace(' ', '_')}_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

        with col2:
            if st.button("📈 Export as Excel", use_container_width=True):
                try:
                    excel_buffer = BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        # Main data sheet
                        df.to_excel(writer, sheet_name='Analysis Results', index=False)

                        # Summary sheet
                        if 'sentiment' in df.columns:
                            summary_data = {
                                'Metric': [
                                    'Total Reviews', 
                                    'Average Rating', 
                                    'Positive Sentiment %', 
                                    'Negative Sentiment %',
                                    'Analysis Confidence',
                                    'Report Generated'
                                ],
                                'Value': [
                                    len(df),
                                    f"{df['score'].mean():.2f}" if 'score' in df.columns else 'N/A',
                                    f"{(df['sentiment'].str.contains('Positive', na=False).sum() / len(df)) * 100:.1f}%",
                                    f"{(df['sentiment'].str.contains('Negative', na=False).sum() / len(df)) * 100:.1f}%",
                                    f"{df['confidence'].mean() * 100:.1f}%" if 'confidence' in df.columns else 'N/A',
                                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                ]
                            }
                            summary_df = pd.DataFrame(summary_data)
                            summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)

                    excel_data = excel_buffer.getvalue()
                    st.download_button(
                        label="⬇️ Download Excel Report",
                        data=excel_data,
                        file_name=f"{app_name.replace(' ', '_')}_analysis_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except Exception as e:
                    st.error(f"Error creating Excel file: {str(e)}")

        with col3:
            if st.button("🗂️ Export as JSON", use_container_width=True):
                json_data = df.to_json(orient='records', date_format='iso', indent=2)
                st.download_button(
                    label="⬇️ Download JSON Data",
                    data=json_data,
                    file_name=f"{app_name.replace(' ', '_')}_analysis_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

        # Export customization
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("🎛️ Export Customization")

        export_columns = st.multiselect(
            "Select columns to include in export:",
            options=df.columns.tolist(),
            default=[col for col in ['at', 'userName', 'score', 'sentiment', 'confidence', 'content'] 
                    if col in df.columns]
        )

        if export_columns:
            preview_df = df[export_columns].head(5)
            st.subheader("👁️ Export Preview")
            st.dataframe(preview_df, use_container_width=True, hide_index=True)
            st.info(f"Preview showing first 5 rows. Full export will contain {len(df):,} rows.")

        # Generate comprehensive report
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("📋 Comprehensive Analysis Report")

        if st.button("🚀 Generate Full Report", type="primary"):
            with st.spinner("📊 Generating comprehensive report..."):
                time.sleep(2)  # Simulate report generation
                
                # Calculate statistics
                total_reviews = len(df)
                avg_rating = df['score'].mean() if 'score' in df.columns else 0
                rating_std = df['score'].std() if 'score' in df.columns else 0
                
                positive_pct = (df['sentiment'].str.contains('Positive', na=False).sum() / len(df)) * 100 if 'sentiment' in df.columns else 0
                neutral_pct = (df['sentiment'].str.contains('Neutral', na=False).sum() / len(df)) * 100 if 'sentiment' in df.columns else 0
                negative_pct = (df['sentiment'].str.contains('Negative', na=False).sum() / len(df)) * 100 if 'sentiment' in df.columns else 0
                
                avg_confidence = df['confidence'].mean() * 100 if 'confidence' in df.columns else 0
                avg_intensity = abs(df['emotional_intensity'].mean()) if 'emotional_intensity' in df.columns else 0
                
                most_common_rating = df['score'].mode().iloc[0] if 'score' in df.columns and not df['score'].mode().empty else 'N/A'

                report_content = f"""# {app_name} - Advanced Analysis Report

## Executive Summary
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Platform:** ReviewForge Analytics Pro  
**Developer:** Ayush Pandey

### Key Metrics Overview
- **Total Reviews Analyzed:** {total_reviews:,}
- **Analysis Period:** {df['at'].min() if 'at' in df.columns else 'N/A'} to {df['at'].max() if 'at' in df.columns else 'N/A'}
- **Average Rating:** {avg_rating:.2f}/5.0 (σ = {rating_std:.2f})
- **Most Common Rating:** {most_common_rating} stars
- **Analysis Confidence:** {avg_confidence:.1f}%

### Sentiment Analysis Results
- **Positive Sentiment:** {positive_pct:.1f}%
- **Neutral Sentiment:** {neutral_pct:.1f}%  
- **Negative Sentiment:** {negative_pct:.1f}%
- **Average Emotional Intensity:** {avg_intensity:.2f}

## Strategic Insights

### Strengths
- {'High user satisfaction with consistent ratings' if rating_std < 1.0 else 'Diverse user opinions indicate broad appeal'}
- {'Strong positive sentiment indicates good user experience' if positive_pct > 60 else 'Room for improvement in user satisfaction'}
- {'High analysis confidence ensures reliable insights' if avg_confidence > 80 else 'Moderate confidence levels in analysis'}

### Areas for Improvement
- {'Focus on maintaining current high standards' if avg_rating > 4.0 else 'Consider addressing common user concerns'}
- {'Monitor negative feedback trends' if negative_pct > 20 else 'Continue current positive trajectory'}
- {'Enhance features based on user feedback patterns' if avg_intensity > 1.0 else 'Maintain current feature satisfaction'}

## Recommendations

### Immediate Actions (0-30 days)
1. **User Feedback Analysis**: Deep dive into negative reviews to identify specific pain points
2. **Performance Monitoring**: Track rating trends and sentiment changes
3. **Quality Assurance**: Address any technical issues mentioned in reviews

### Medium-term Strategy (1-3 months)  
1. **Feature Development**: Prioritize features requested by users
2. **User Experience**: Optimize based on sentiment analysis insights
3. **Market Positioning**: Leverage positive feedback for marketing

### Long-term Vision (3+ months)
1. **Competitive Analysis**: Regular benchmarking against competitors
2. **Innovation Pipeline**: Develop next-generation features
3. **Community Building**: Foster positive user relationships

---

**Report generated by ReviewForge Analytics Pro**  
*Advanced Review Analysis Platform by Ayush Pandey*

*This report contains proprietary analysis and should be treated as confidential business intelligence.*
                """

                st.markdown(report_content)

                st.download_button(
                    label="📥 Download Full Report (Markdown)",
                    data=report_content,
                    file_name=f"{app_name.replace(' ', '_')}_comprehensive_report_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
    else:
        st.markdown("""
        <div class="feature-card" style="text-align: center; margin: 3rem 0;">
            <div class="feature-icon">📊</div>
            <h3>Ready to Export</h3>
            <p>Analyze an application from the Dashboard to access export and reporting functionality.</p>
        </div>
        """, unsafe_allow_html=True)

def settings_page():
    """Advanced settings and preferences"""
    st.markdown("""
    <div class="feature-card" style="text-align: center; margin-bottom: 2rem;">
        <div class="feature-icon">⚙️</div>
        <h1>Advanced Settings</h1>
        <p>Customize your analysis preferences and platform configuration</p>
    </div>
    """, unsafe_allow_html=True)

    # Analysis Configuration
    st.subheader("🔧 Analysis Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🎭 Sentiment Analysis Settings")
        sentiment_threshold = st.slider(
            "Sentiment Confidence Threshold", 
            0.0, 1.0, 
            st.session_state.user_preferences.get('sentiment_threshold', 0.6), 
            0.1,
            help="Minimum confidence required for sentiment classification"
        )
        
        enable_aspect_analysis = st.checkbox(
            "Enable Aspect-Based Analysis", 
            value=st.session_state.user_preferences.get('enable_aspect_analysis', True),
            help="Analyze specific aspects like performance, UI, functionality"
        )
        
        enable_emotion_detection = st.checkbox(
            "Enable Emotional Intensity Analysis", 
            value=st.session_state.user_preferences.get('enable_emotion_detection', True),
            help="Measure emotional intensity in reviews"
        )

    with col2:
        st.markdown("#### 🤖 Machine Learning Settings")
        enable_topic_modeling = st.checkbox(
            "Enable Topic Modeling", 
            value=st.session_state.user_preferences.get('enable_topic_modeling', True),
            help="Automatically discover topics in reviews"
        )
        
        topic_count = st.slider(
            "Number of Topics", 
            3, 10, 
            st.session_state.user_preferences.get('topic_count', 5),
            help="Number of topics to extract from reviews"
        )
        
        enable_clustering = st.checkbox(
            "Enable Review Clustering", 
            value=st.session_state.user_preferences.get('enable_clustering', True),
            help="Group similar reviews together"
        )

    # Export & Reporting Settings
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.subheader("📄 Export & Reporting Settings")

    col1, col2 = st.columns(2)

    with col1:
        export_format = st.selectbox(
            "Default Export Format",
            options=["CSV", "Excel", "JSON", "PDF"],
            index=["CSV", "Excel", "JSON", "PDF"].index(st.session_state.user_preferences.get('export_format', 'CSV'))
        )

        include_raw_data = st.checkbox(
            "Include Raw Review Data", 
            value=st.session_state.user_preferences.get('include_raw_data', True)
        )

    with col2:
        include_visualizations = st.checkbox(
            "Include Charts in Reports", 
            value=st.session_state.user_preferences.get('include_visualizations', True)
        )

        auto_refresh = st.checkbox(
            "Auto-refresh Analysis", 
            value=st.session_state.user_preferences.get('auto_refresh', True),
            help="Automatically refresh analysis when data changes"
        )

    # Performance Settings
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.subheader("⚡ Performance & Cache Settings")

    cache_duration = st.slider(
        "Cache Duration (hours)", 
        1, 24, 
        st.session_state.user_preferences.get('cache_duration', 6),
        help="How long to cache analysis results"
    )

    max_reviews = st.select_slider(
        "Maximum Reviews per Analysis",
        options=[100, 250, 500, 1000, 2000, 5000],
        value=st.session_state.user_preferences.get('max_reviews', 1000)
    )

    # Save settings
    if st.button("💾 Save Settings", type="primary"):
        settings = {
            'sentiment_threshold': sentiment_threshold,
            'enable_aspect_analysis': enable_aspect_analysis,
            'enable_emotion_detection': enable_emotion_detection,
            'enable_topic_modeling': enable_topic_modeling,
            'topic_count': topic_count,
            'enable_clustering': enable_clustering,
            'export_format': export_format,
            'include_raw_data': include_raw_data,
            'include_visualizations': include_visualizations,
            'auto_refresh': auto_refresh,
            'cache_duration': cache_duration,
            'max_reviews': max_reviews
        }
        st.session_state.user_preferences = settings
        st.success("✅ Settings saved successfully!")
        time.sleep(1)
        st.balloons()

    # System Information
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.subheader("ℹ️ System Information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.info(f"""
        **Application Version:** 2.0.0 Pro  
        **Developer:** Ayush Pandey  
        **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
        **Platform:** Streamlit {st.__version__ if hasattr(st, '__version__') else 'Latest'}
        """)

    with info_col2:
        st.info(f"""
        **Analysis Engine:** Advanced ML-Powered  
        **Current User:** {st.session_state.user_role.title()}  
        **Session Started:** {datetime.now().strftime('%H:%M:%S')}  
        **Reviews Analyzed:** {len(st.session_state.analyzed_data) if st.session_state.analyzed_data is not None else 0:,}
        """)

    # Advanced Options
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.subheader("🔬 Advanced Options")

    if st.button("🗑️ Clear Cache", help="Clear all cached analysis data"):
        st.cache_data.clear()
        st.success("✅ Cache cleared successfully!")

    if st.button("🔄 Reset to Defaults", help="Reset all settings to default values"):
        st.session_state.user_preferences = {
            'theme': 'dark',
            'auto_refresh': True,
            'export_format': 'CSV'
        }
        st.success("✅ Settings reset to defaults!")
        st.rerun()

# Main application logic
def main():
    """Main application controller"""
    create_navigation()

    # Page routing with enhanced error handling
    page = st.session_state.current_page
    
    try:
        if page == 'dashboard':
            dashboard_page()
        elif page == 'deep_analysis' or page == 'ml_insights':
            deep_analysis_page()
        elif page == 'competitor':
            competitor_analysis_page()
        elif page == 'trend_analysis':
            trend_analysis_page()
        elif page == 'export_reports':
            export_reports_page()
        elif page == 'settings':
            settings_page()
        else:
            st.error(f"Unknown page: {page}")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try refreshing the page or contact support if the issue persists.")

    # Enhanced Footer
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; margin-top: 3rem;">
        <h3 style="color: white; margin-bottom: 1rem;">ReviewForge Analytics Pro</h3>
        <p style="color: rgba(255,255,255,0.9); margin-bottom: 1rem;">Advanced AI-Powered Review Analysis Platform</p>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
            Developed by <strong>Ayush Pandey</strong> | Version 2.0.0 Pro | © 2024
        </p>
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
            <span style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">
                Powered by Advanced Machine Learning & Modern Analytics
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
