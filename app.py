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
    page_title="TerminalAnalyzer Pro", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: #f8fafc;
        color: #334155;
        font-family: 'Inter', sans-serif;
    }
    
    .header-container {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        border-radius: 12px;
        padding: 30px 40px;
        margin: 20px 0;
        color: white;
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -20px;
        right: -20px;
        width: 120px;
        height: 120px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 10px 0 5px 0;
    }
    
    .app-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 15px;
    }
    
    .creator-badge {
        position: absolute;
        bottom: 20px;
        right: 30px;
        background: rgba(255, 255, 255, 0.2);
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Enhanced Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(79, 70, 229, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
    }
    
    /* Content Sections */
    .content-section {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #4f46e5;
    }
    
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    /* Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin: 25px 0;
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #4f46e5;
        margin-bottom: 8px;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Review Cards */
    .review-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
    }
    
    .review-card:hover {
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
    }
    
    .review-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .review-user {
        color: #1e293b;
        font-weight: 600;
    }
    
    .review-rating {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .star-rating {
        color: #f59e0b;
        font-size: 1.1rem;
    }
    
    .review-content {
        color: #475569;
        line-height: 1.6;
        margin: 15px 0;
    }
    
    .review-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px solid #f1f5f9;
    }
    
    .sentiment-badge {
        padding: 5px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .sentiment-positive {
        background: #dcfce7;
        color: #16a34a;
    }
    
    .sentiment-negative {
        background: #fee2e2;
        color: #dc2626;
    }
    
    .sentiment-neutral {
        background: #fef3c7;
        color: #d97706;
    }
    
    /* AI Insights */
    .ai-insights {
        background: linear-gradient(135deg, #e0e7ff 0%, #ede9fe 100%);
        border-radius: 12px;
        padding: 30px;
        margin: 25px 0;
        position: relative;
    }
    
    .insight-item {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .insight-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
    }
    
    .insight-item.warning {
        border-left: 4px solid #ef4444;
    }
    
    .insight-item.positive {
        border-left: 4px solid #10b981;
    }
    
    /* Export Cards */
    .export-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin: 25px 0;
    }
    
    .export-card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
    }
    
    .export-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
    }
    
    .export-title {
        color: #4f46e5;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 12px;
    }
    
    .export-desc {
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    /* Progress Section */
    .progress-section {
        background: white;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
    }
    
    .status-card {
        background: #f8fafc;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }
    
    /* Loading Spinner */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(79, 70, 229, 0.3);
        border-top: 3px solid #4f46e5;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 10px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Input Styling */
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        padding: 12px;
    }
    
    .stTextArea textarea:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1);
    }
    
    /* Selectbox Styling */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px;
    }
    
    /* Slider Styling */
    .stSlider div[data-baseweb="slider"] {
        color: #4f46e5;
    }
    
    /* Checkbox Styling */
    .stCheckbox label {
        font-weight: 500;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #4f46e5;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c7d2fe;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a5b4fc;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2rem;
        }
        
        .metrics-grid {
            grid-template-columns: 1fr;
        }
        
        .metric-value {
            font-size: 1.8rem;
        }
        
        .export-container {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False

# Helper Functions (remain the same as in the original code)
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
    
    if polarity > 0.4:
        return "Positive", polarity, subjectivity, "Highly Positive"
    elif polarity > 0.2:
        return "Positive", polarity, subjectivity, "Moderately Positive"
    elif polarity > 0.0:
        return "Positive", polarity, subjectivity, "Slightly Positive"
    elif polarity < -0.4:
        return "Negative", polarity, subjectivity, "Highly Negative"
    elif polarity < -0.2:
        return "Negative", polarity, subjectivity, "Moderately Negative"
    elif polarity < 0.0:
        return "Negative", polarity, subjectivity, "Slightly Negative"
    else:
        return "Neutral", polarity, subjectivity, "Neutral"

def get_app_name(package_name):
    parts = package_name.split('.')
    return parts[-1].replace('_', ' ').title() if parts else package_name

def generate_advanced_ai_insights(df):
    insights = []
    if df.empty:
        return insights
    
    try:
        sentiment_dist = df['sentiment'].value_counts(normalize=True) * 100
        avg_rating = df['score'].mean()
        total_reviews = len(df)
        
        positive_rate = sentiment_dist.get('Positive', 0)
        negative_rate = sentiment_dist.get('Negative', 0)
        
        # Advanced market analysis
        if positive_rate > 80 and avg_rating > 4.5:
            insights.append({
                "type": "positive",
                "title": "MARKET LEADER STATUS",
                "description": f"Exceptional performance with {positive_rate:.1f}% positive sentiment and {avg_rating:.1f}/5 rating indicates dominant market position and outstanding user satisfaction."
            })
        elif positive_rate > 60 and avg_rating > 4.0:
            insights.append({
                "type": "positive", 
                "title": "STRONG COMPETITIVE POSITION",
                "description": f"Above-average performance with {positive_rate:.1f}% positive sentiment demonstrates strong competitive positioning in the market segment."
            })
        elif negative_rate > 40:
            insights.append({
                "type": "warning",
                "title": "URGENT INTERVENTION REQUIRED",
                "description": f"Critical alert: {negative_rate:.1f}% negative sentiment requires immediate strategic intervention and comprehensive user experience overhaul."
            })
        
        # Review volume insights
        if total_reviews > 1000:
            insights.append({
                "type": "positive",
                "title": "HIGH MARKET PENETRATION",
                "description": f"Substantial user engagement with {total_reviews:,} reviews indicates strong market penetration and highly active user community."
            })
        elif total_reviews < 100:
            insights.append({
                "type": "warning",
                "title": "LIMITED MARKET VISIBILITY",
                "description": f"Low review volume ({total_reviews} reviews) suggests limited market visibility or early market entry phase. Consider enhancing marketing strategies."
            })
        
        # Rating consistency analysis
        rating_std = df['score'].std()
        if rating_std < 0.5:
            insights.append({
                "type": "positive",
                "title": "CONSISTENT USER EXPERIENCE",
                "description": f"Low rating variance ({rating_std:.2f}) indicates highly consistent user experience across diverse user segments and use cases."
            })
        elif rating_std > 1.5:
            insights.append({
                "type": "warning",
                "title": "INCONSISTENT USER EXPERIENCE",
                "description": f"High rating variance ({rating_std:.2f}) suggests inconsistent user experience. Investigate user journey pain points and feature disparities."
            })
        
        # Sentiment polarity insights
        avg_polarity = df['polarity_score'].mean()
        if avg_polarity > 0.3:
            insights.append({
                "type": "positive",
                "title": "STRONG EMOTIONAL CONNECTION",
                "description": f"High sentiment polarity ({avg_polarity:.2f}) indicates strong positive emotional connection and user advocacy potential."
            })
        elif avg_polarity < -0.2:
            insights.append({
                "type": "warning",
                "title": "NEGATIVE USER SENTIMENT TREND",
                "description": f"Negative sentiment polarity ({avg_polarity:.2f}) suggests underlying user frustration. Focus on addressing core experience issues."
            })
        
        return insights[:6]
        
    except Exception:
        return []

def perform_enhanced_topic_analysis(df):
    if df.empty or len(df) < 10:
        return {}
    
    try:
        all_text = ' '.join(df['content'].dropna().astype(str).tolist())
        
        stop_words = set([
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
            'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his',
            'its', 'our', 'their', 'app', 'application', 'good', 'bad', 'very', 'much', 'more',
            'most', 'get', 'go', 'come', 'like', 'just', 'time', 'way', 'work', 'use', 'make',
            'see', 'know', 'really', 'great', 'nice', 'think', 'want', 'need', 'can', 'cant'
        ])
        
        words = re.findall(r'\b[a-zA-Z]{4,}\b', all_text.lower())
        words = [word for word in words if word not in stop_words and len(word) > 3]
        word_counts = Counter(words)
        top_words = word_counts.most_common(100)
        
        topics = {
            "performance": {
                "title": "PERFORMANCE OPTIMIZATION",
                "keywords": ['performance', 'speed', 'fast', 'slow', 'quick', 'lag', 'freeze', 'loading', 'responsive', 'smooth'],
                "terms": [],
                "count": 0
            },
            "user_interface": {
                "title": "USER INTERFACE DESIGN",
                "keywords": ['interface', 'design', 'layout', 'navigation', 'menu', 'button', 'screen', 'display', 'visual', 'theme'],
                "terms": [],
                "count": 0
            },
            "functionality": {
                "title": "FEATURE FUNCTIONALITY", 
                "keywords": ['feature', 'function', 'option', 'setting', 'tool', 'capability', 'functionality', 'working'],
                "terms": [],
                "count": 0
            },
            "reliability": {
                "title": "RELIABILITY STABILITY",
                "keywords": ['crash', 'bug', 'error', 'issue', 'problem', 'glitch', 'fail', 'broken', 'stable', 'reliable'],
                "terms": [],
                "count": 0
            },
            "usability": {
                "title": "USER EXPERIENCE",
                "keywords": ['easy', 'difficult', 'simple', 'complex', 'user', 'experience', 'friendly', 'intuitive', 'confusing'],
                "terms": [],
                "count": 0
            }
        }
        
        for word, count in top_words:
            for topic_key, topic_data in topics.items():
                if any(keyword in word or word in keyword for keyword in topic_data['keywords']):
                    topic_data['terms'].append(word)
                    topic_data['count'] += count
        
        total_categorized = sum(topic_data['count'] for topic_data in topics.values())
        clean_topics = {}
        
        for topic_key, topic_data in topics.items():
            if topic_data['count'] > 0 and topic_data['terms']:
                topic_data['percentage'] = (topic_data['count'] / total_categorized) * 100 if total_categorized > 0 else 0
                topic_data['terms'] = list(set(topic_data['terms']))[:8]
                clean_topics[topic_key] = topic_data
        
        return clean_topics
        
    except Exception:
        return {}

def create_enhanced_charts(df_a, df_b=None):
    charts = {}
    
    template = {
        'layout': {
            'plot_bgcolor': 'rgba(255, 255, 255, 1)',
            'paper_bgcolor': 'rgba(255, 255, 255, 1)',
            'font': {'color': '#334155', 'family': 'Inter, sans-serif'},
            'colorway': ['#4f46e5', '#8b5cf6', '#ec4899', '#f59e0b', '#ef4444']
        }
    }
    
    if df_b is not None and not df_b.empty:
        # Comparative analysis
        sentiment_a = df_a['sentiment'].value_counts(normalize=True) * 100
        sentiment_b = df_b['sentiment'].value_counts(normalize=True) * 100
        
        fig_comparison = go.Figure()
        
        sentiments = ['Positive', 'Neutral', 'Negative']
        x_pos = [0.8, 1.8, 2.8]
        x_pos_b = [1.2, 2.2, 3.2]
        
        fig_comparison.add_trace(go.Bar(
            name='Application A',
            x=x_pos,
            y=[sentiment_a.get(s, 0) for s in sentiments],
            marker_color='#4f46e5',
            width=0.35
        ))
        
        fig_comparison.add_trace(go.Bar(
            name='Application B',
            x=x_pos_b,
            y=[sentiment_b.get(s, 0) for s in sentiments],
            marker_color='#8b5cf6',
            width=0.35
        ))
        
        fig_comparison.update_layout(
            title='COMPETITIVE SENTIMENT ANALYSIS',
            xaxis_title='SENTIMENT CATEGORIES',
            yaxis_title='PERCENTAGE DISTRIBUTION',
            xaxis=dict(tickvals=[1, 2, 3], ticktext=sentiments),
            template=template,
            showlegend=True,
            barmode='group'
        )
        
        charts['comparison_sentiment'] = fig_comparison
        
        # Rating radar comparison
        rating_data_a = []
        rating_data_b = []
        categories = []
        
        for rating in range(1, 6):
            count_a = (df_a['score'] == rating).sum()
            count_b = (df_b['score'] == rating).sum()
            rating_data_a.append(count_a)
            rating_data_b.append(count_b)
            categories.append(f'{rating} Star')
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=rating_data_a,
            theta=categories,
            fill='toself',
            name='Application A',
            line_color='#4f46e5'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=rating_data_b,
            theta=categories,
            fill='toself',
            name='Application B',
            line_color='#8b5cf6'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(max(rating_data_a), max(rating_data_b)) + 10])
            ),
            showlegend=True,
            title="RATING DISTRIBUTION RADAR",
            template=template
        )
        
        charts['comparison_radar'] = fig_radar
    
    else:
        # Single app enhanced charts
        if not df_a.empty:
            sentiment_counts = df_a['sentiment'].value_counts()
            colors_map = {'Positive': '#10b981', 'Neutral': '#f59e0b', 'Negative': '#ef4444'}
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=sentiment_counts.index,
                values=sentiment_counts.values,
                hole=0.6,
                marker=dict(colors=[colors_map.get(label, '#94a3b8') for label in sentiment_counts.index]),
                textinfo='label+percent',
                textfont=dict(size=16, color='#334155')
            )])
            
            fig_pie.update_layout(
                title="SENTIMENT DISTRIBUTION ANALYSIS",
                template=template,
                annotations=[dict(text=f'Total<br>{sentiment_counts.sum()}', x=0.5, y=0.5, font_size=18, showarrow=False)]
            )
            
            charts['sentiment_pie'] = fig_pie
            
            # Enhanced timeline
            if 'at' in df_a.columns:
                df_copy = df_a.copy()
                df_copy['date'] = pd.to_datetime(df_copy['at']).dt.date
                daily_sentiment = df_copy.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
                
                if not daily_sentiment.empty:
                    fig_timeline = go.Figure()
                    
                    for sentiment in ['Positive', 'Neutral', 'Negative']:
                        if sentiment in daily_sentiment.columns:
                            fig_timeline.add_trace(go.Scatter(
                                x=daily_sentiment.index,
                                y=daily_sentiment[sentiment],
                                mode='lines+markers',
                                name=f'{sentiment} Reviews',
                                line=dict(color=colors_map.get(sentiment, '#94a3b8'), width=3),
                                marker=dict(size=8)
                            ))
                    
                    fig_timeline.update_layout(
                        title='SENTIMENT EVOLUTION TIMELINE',
                        xaxis_title='DATE RANGE',
                        yaxis_title='REVIEW COUNT',
                        template=template,
                        hovermode='x unified'
                    )
                    
                    charts['sentiment_timeline'] = fig_timeline
    
    return charts

def generate_professional_pdf(df_a, df_b=None, insights=None, topics=None):
    try:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>TerminalAnalyzer Pro - Professional Report</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
                
                body {{
                    font-family: 'Inter', sans-serif;
                    background: #f8fafc;
                    color: #334155;
                    margin: 0;
                    padding: 40px;
                    line-height: 1.6;
                }}
                
                .header {{
                    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                    border-radius: 12px;
                    padding: 40px;
                    text-align: center;
                    margin-bottom: 40px;
                    color: white;
                }}
                
                .logo {{
                    font-size: 36px;
                    font-weight: 700;
                    margin-bottom: 15px;
                }}
                
                .report-title {{
                    font-size: 24px;
                    margin-bottom: 15px;
                }}
                
                .report-meta {{
                    opacity: 0.9;
                    font-size: 14px;
                }}
                
                .section {{
                    background: white;
                    border-radius: 12px;
                    padding: 30px;
                    margin-bottom: 30px;
                    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
                }}
                
                .section-title {{
                    font-size: 20px;
                    font-weight: 600;
                    color: #1e293b;
                    margin-bottom: 25px;
                    padding-bottom: 10px;
                    border-bottom: 1px solid #e2e8f0;
                }}
                
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 25px 0;
                }}
                
                .metric-card {{
                    background: #f8fafc;
                    border-radius: 10px;
                    padding: 20px;
                    text-align: center;
                }}
                
                .metric-value {{
                    font-size: 28px;
                    font-weight: 700;
                    color: #4f46e5;
                    margin-bottom: 8px;
                }}
                
                .metric-label {{
                    color: #64748b;
                    font-size: 14px;
                }}
                
                .insight {{
                    background: #f1f5f9;
                    padding: 20px;
                    margin: 15px 0;
                    border-radius: 10px;
                }}
                
                .insight.warning {{
                    border-left: 4px solid #ef4444;
                }}
                
                .insight.positive {{
                    border-left: 4px solid #10b981;
                }}
                
                .insight-title {{
                    font-weight: 600;
                    font-size: 16px;
                    margin-bottom: 10px;
                }}
                
                .insight-desc {{
                    color: #475569;
                    font-size: 14px;
                    line-height: 1.6;
                }}
                
                .comparison-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 25px 0;
                }}
                
                .comparison-table th,
                .comparison-table td {{
                    border: 1px solid #e2e8f0;
                    padding: 15px;
                    text-align: center;
                }}
                
                .comparison-table th {{
                    background: #f1f5f9;
                    color: #4f46e5;
                    font-weight: 600;
                }}
                
                .comparison-table td {{
                    background: white;
                }}
                
                .app-a {{ color: #4f46e5; }}
                .app-b {{ color: #8b5cf6; }}
                
                .topic-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin: 25px 0;
                }}
                
                .topic-card {{
                    background: #f8fafc;
                    border-radius: 10px;
                    padding: 20px;
                }}
                
                .topic-title {{
                    color: #4f46e5;
                    font-weight: 600;
                    font-size: 16px;
                    margin-bottom: 15px;
                }}
                
                .topic-terms {{
                    color: #64748b;
                    font-size: 14px;
                    line-height: 1.5;
                }}
                
                .footer {{
                    text-align: center;
                    padding: 40px;
                    border-top: 1px solid #e2e8f0;
                    margin-top: 40px;
                    color: #64748b;
                }}
                
                .brand {{
                    color: #4f46e5;
                    font-weight: 700;
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">TERMINALANALYZER PRO</div>
                <div class="report-title">Professional Intelligence Report</div>
                <div class="report-meta">
                    Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')} | 
                    Advanced AI Analytics Platform
                </div>
            </div>
        """
        
        # Executive Summary
        html_content += f"""
        <div class="section">
            <div class="section-title">Executive Summary</div>
            <div class="metrics-grid">
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
                    <div class="metric-label">Positive Sentiment</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{df_a['polarity_score'].mean():.2f}</div>
                    <div class="metric-label">Sentiment Score</div>
                </div>
            </div>
        </div>
        """
        
        # Competitive Analysis
        if df_b is not None and not df_b.empty:
            html_content += f"""
            <div class="section">
                <div class="section-title">Competitive Analysis</div>
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th class="app-a">Application A</th>
                            <th class="app-b">Application B</th>
                            <th>Winner</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Total Reviews</td>
                            <td class="app-a">{len(df_a):,}</td>
                            <td class="app-b">{len(df_b):,}</td>
                            <td>{'App A' if len(df_a) > len(df_b) else 'App B' if len(df_b) > len(df_a) else 'Tie'}</td>
                        </tr>
                        <tr>
                            <td>Average Rating</td>
                            <td class="app-a">{df_a['score'].mean():.2f}</td>
                            <td class="app-b">{df_b['score'].mean():.2f}</td>
                            <td>{'App A' if df_a['score'].mean() > df_b['score'].mean() else 'App B' if df_b['score'].mean() > df_a['score'].mean() else 'Tie'}</td>
                        </tr>
                        <tr>
                            <td>Positive Sentiment</td>
                            <td class="app-a">{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%</td>
                            <td class="app-b">{(df_b['sentiment'] == 'Positive').mean() * 100:.1f}%</td>
                            <td>{'App A' if (df_a['sentiment'] == 'Positive').mean() > (df_b['sentiment'] == 'Positive').mean() else 'App B' if (df_b['sentiment'] == 'Positive').mean() > (df_a['sentiment'] == 'Positive').mean() else 'Tie'}</td>
                        </tr>
                        <tr>
                            <td>Sentiment Score</td>
                            <td class="app-a">{df_a['polarity_score'].mean():.3f}</td>
                            <td class="app-b">{df_b['polarity_score'].mean():.3f}</td>
                            <td>{'App A' if df_a['polarity_score'].mean() > df_b['polarity_score'].mean() else 'App B' if df_b['polarity_score'].mean() > df_a['polarity_score'].mean() else 'Tie'}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """
        
        # AI Insights
        if insights and len(insights) > 0:
            html_content += '<div class="section"><div class="section-title">AI Strategic Insights</div>'
            
            for insight in insights[:5]:
                css_class = 'insight positive' if insight['type'] == 'positive' else 'insight warning'
                html_content += f"""
                <div class="{css_class}">
                    <div class="insight-title">{insight['title']}</div>
                    <div class="insight-desc">{insight['description']}</div>
                </div>
                """
            
            html_content += '</div>'
        
        # Topic Analysis
        if topics and len(topics) > 0:
            html_content += '<div class="section"><div class="section-title">Topic Analysis</div>'
            html_content += '<div class="topic-grid">'
            
            for topic_key, topic_data in topics.items():
                html_content += f"""
                <div class="topic-card">
                    <div class="topic-title">{topic_data['title']}</div>
                    <div class="topic-terms">
                        <strong>Key Terms:</strong><br>
                        {', '.join(topic_data['terms'][:5])}
                    </div>
                    <div style="margin-top: 15px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #64748b;">{topic_data['count']} mentions</span>
                        <span style="background: #4f46e5; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">{topic_data['percentage']:.1f}%</span>
                    </div>
                </div>
                """
            
            html_content += '</div></div>'
        
        # Footer
        html_content += f"""
            <div class="footer">
                <div class="brand">TERMINALANALYZER PRO</div>
                <div>Professional Review Intelligence Platform | Created by Ayush Pandey</div>
                <div>Advanced AI Analytics & Business Intelligence Solutions</div>
                <div style="margin-top: 20px; font-size: 14px;">
                    This report contains proprietary analysis and should be treated as confidential business intelligence.
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content.encode('utf-8')
        
    except Exception as e:
        return f"Error generating report: {str(e)}".encode('utf-8')

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

def display_review_cards(df, title, max_reviews=10):
    st.markdown(f"""
    <div class="content-section">
        <div class="section-header">{title}</div>
    </div>
    """, unsafe_allow_html=True)
    
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
            date_str = "Unknown date"
        
        content = str(review.get('content', 'No content available'))
        if len(content) > 400:
            content = content[:400] + "..."
        
        st.markdown(f"""
        <div class="review-card">
            <div class="review-header">
                <div class="review-user">{review.get('userName', 'Anonymous User')}</div>
                <div class="review-rating">
                    <span class="star-rating">{stars}</span>
                    <span style="margin-left: 10px; color: #64748b; font-weight: 600;">{rating}/5</span>
                </div>
            </div>
            <div class="review-content">{content}</div>
            <div class="review-meta">
                <div style="color: #94a3b8;">{date_str}</div>
                <div class="sentiment-badge {badge_class}">{sentiment}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# HOME PAGE
if st.session_state.page == 'home':
    st.markdown("""
    <div class="header-container">
        <div class="app-title">TerminalAnalyzer Pro</div>
        <div class="app-subtitle">Advanced Professional Review Intelligence Platform</div>
        <div class="creator-badge">developed by ayush_pandey</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-section" style="text-align: center;">
        <div class="section-header">WELCOME TO ADVANCED ANALYTICS</div>
        <p style="color: #64748b; font-size: 1.1rem; line-height: 1.8; margin-bottom: 40px; max-width: 800px; margin-left: auto; margin-right: auto;">
            Professional-grade review analysis platform with advanced AI intelligence, 
            comprehensive competitive analysis, and modern interface design.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-section" style="text-align: center; min-height: 250px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 3.5rem; margin-bottom: 25px; color: #4f46e5;">📱</div>
            <div class="section-header">SINGLE APPLICATION ANALYSIS</div>
            <p style="color: #64748b; margin-bottom: 35px; line-height: 1.6;">
                Comprehensive deep-dive analysis of individual applications with advanced AI insights, 
                topic discovery, and professional reporting capabilities.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("INITIATE SINGLE ANALYSIS", type="primary"):
            st.session_state.comparison_mode = False
            navigate_to('analysis')
    
    with col2:
        st.markdown("""
        <div class="content-section" style="text-align: center; min-height: 250px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 3.5rem; margin-bottom: 25px; color: #8b5cf6;">📊</div>
            <div class="section-header">COMPETITIVE COMPARISON</div>
            <p style="color: #64748b; margin-bottom: 35px; line-height: 1.6;">
                Head-to-head competitive analysis with side-by-side metrics, 
                comparative visualizations, and strategic intelligence reports.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("LAUNCH COMPETITIVE MODE", type="primary"):
            st.session_state.comparison_mode = True
            navigate_to('analysis')

# ANALYSIS PAGE
elif st.session_state.page == 'analysis':
    mode_text = "COMPETITIVE COMPARISON MODE" if st.session_state.comparison_mode else "SINGLE APPLICATION ANALYSIS"
    st.markdown(f"""
    <div class="header-container">
        <div class="app-title">ANALYSIS DASHBOARD</div>
        <div class="app-subtitle">{mode_text} ACTIVE</div>
        <div class="creator-badge">mode: {'competitive' if st.session_state.comparison_mode else 'single'}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("◀ RETURN TO HOME", type="secondary"):
        navigate_to('home')
    
    # URL Configuration
    if st.session_state.comparison_mode:
        st.markdown("### COMPETITIVE ANALYSIS CONFIGURATION")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; border-left: 4px solid #4f46e5;">
                <div style="color: #4f46e5; font-weight: 600; font-size: 1rem; margin-bottom: 10px;">
                    APPLICATION A TARGET
                </div>
            </div>
            """, unsafe_allow_html=True)
            url_a = st.text_area("Primary Application URL", placeholder="https://play.google.com/store/apps/details?id=...", height=100)
        
        with col2:
            st.markdown("""
            <div style="background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; border-left: 4px solid #8b5cf6;">
                <div style="color: #8b5cf6; font-weight: 600; font-size: 1rem; margin-bottom: 10px;">
                    APPLICATION B COMPETITOR
                </div>
            </div>
            """, unsafe_allow_html=True)
            url_b = st.text_area("Competitor Application URL", placeholder="https://play.google.com/store/apps/details?id=...", height=100)
    else:
        st.markdown("### SINGLE APPLICATION ANALYSIS")
        url_a = st.text_area("Application URL", placeholder="https://play.google.com/store/apps/details?id=...", height=100)
        url_b = None
    
    # Parameters
    st.markdown("### ANALYSIS PARAMETERS")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        count = st.slider("Reviews per App", 50, 2000, 500, 50)
    with col2:
        language = st.selectbox("Language", ["en", "hi", "es", "fr", "de", "ja"])
    with col3:
        country = st.selectbox("Region", ["in", "us", "uk", "ca", "de", "jp"])
    with col4:
        sort_by = st.selectbox("Sort Method", ["NEWEST", "MOST_RELEVANT", "RATING"])
    
    # Advanced Options
    with st.expander("ADVANCED CONFIGURATION", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            enable_insights = st.checkbox("AI Intelligence Module", value=True)
            enable_topics = st.checkbox("Topic Discovery Engine", value=True)
        with col2:
            min_rating = st.selectbox("Minimum Rating Filter", [1, 2, 3, 4, 5])
            max_reviews_display = st.slider("Reviews to Display", 5, 50, 15)
        with col3:
            enable_keywords = st.checkbox("Keyword Tracking", value=True)
    
    keywords = []
    if enable_keywords:
        keyword_input = st.text_input("Keywords to Track", placeholder="performance, bug, excellent, slow, crash")
        if keyword_input:
            keywords = [k.strip().lower() for k in keyword_input.split(",")]
    
    # Execute Analysis
    if st.button("EXECUTE COMPREHENSIVE ANALYSIS", type="primary"):
        # Validation
        if not url_a.strip():
            st.error("PRIMARY APPLICATION URL IS REQUIRED")
            st.stop()
        
        if st.session_state.comparison_mode and not url_b.strip():
            st.error("COMPETITOR APPLICATION URL IS REQUIRED")
            st.stop()
        
        package_a = extract_package_name(url_a)
        package_b = extract_package_name(url_b) if url_b else None
        
        if not package_a:
            st.error("INVALID URL FORMAT FOR PRIMARY APPLICATION")
            st.stop()
        
        if st.session_state.comparison_mode and not package_b:
            st.error("INVALID URL FORMAT FOR COMPETITOR APPLICATION")
            st.stop()
        
        # Progress Section
        st.markdown("""
        <div class="progress-section">
            <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 15px;">
                <span class="loading-spinner"></span>
                ANALYSIS PIPELINE EXECUTING
            </div>
            <div style="color: #64748b; font-size: 1rem;">
                Processing review data through advanced AI algorithms...
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_container = st.empty()
        
        # Process applications
        try:
            sort_mapping = {"NEWEST": Sort.NEWEST, "MOST_RELEVANT": Sort.MOST_RELEVANT, "RATING": Sort.RATING}
            
            # Process App A
            status_container.markdown(f"""
            <div class="status-card">
                <strong style="color: #4f46e5; font-size: 1.1rem;">PROCESSING: {get_app_name(package_a)}</strong><br>
                <div style="color: #64748b; margin-top: 8px;">Extracting {count:,} reviews and performing sentiment analysis...</div>
            </div>
            """, unsafe_allow_html=True)
            
            result_a, _ = reviews(package_a, lang=language, country=country, sort=sort_mapping[sort_by], count=count)
            
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
                df_a = df_a[df_a["score"] >= min_rating].copy()
            else:
                st.error("FAILED TO EXTRACT REVIEWS FOR PRIMARY APPLICATION")
                st.stop()
            
            progress_bar.progress(0.5)
            
            # Process App B if needed
            df_b = None
            if st.session_state.comparison_mode:
                status_container.markdown(f"""
                <div class="status-card">
                    <strong style="color: #8b5cf6; font-size: 1.1rem;">PROCESSING: {get_app_name(package_b)}</strong><br>
                    <div style="color: #64748b; margin-top: 8px;">Extracting {count:,} reviews and performing competitive analysis...</div>
                </div>
                """, unsafe_allow_html=True)
                
                result_b, _ = reviews(package_b, lang=language, country=country, sort=sort_mapping[sort_by], count=count)
                
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
                    df_b = df_b[df_b["score"] >= min_rating].copy()
                else:
                    st.error("FAILED TO EXTRACT REVIEWS FOR COMPETITOR APPLICATION")
                    st.stop()
            
            progress_bar.progress(0.8)
            
            # Generate insights
            status_container.markdown("""
            <div class="status-card">
                <strong style="color: #ec4899; font-size: 1.1rem;">GENERATING AI INTELLIGENCE</strong><br>
                <div style="color: #64748b; margin-top: 8px;">Processing advanced insights and topic discovery...</div>
            </div>
            """, unsafe_allow_html=True)
            
            insights_a = generate_advanced_ai_insights(df_a) if enable_insights else []
            topics_a = perform_enhanced_topic_analysis(df_a) if enable_topics else {}
            insights_b = generate_advanced_ai_insights(df_b) if enable_insights and df_b is not None else []
            topics_b = perform_enhanced_topic_analysis(df_b) if enable_topics and df_b is not None else {}
            
            progress_bar.progress(1.0)
            
        except Exception as e:
            st.error(f"PROCESSING ERROR: {str(e)}")
            st.stop()
        
        # Clear progress
        status_container.empty()
        progress_bar.empty()
        
        # Success
        total_reviews = len(df_a) + (len(df_b) if df_b is not None else 0)
        st.success(f"ANALYSIS COMPLETED: {total_reviews:,} reviews processed with advanced AI intelligence")
        
        # Display Metrics
        if st.session_state.comparison_mode and df_b is not None:
            st.markdown("## COMPETITIVE METRICS DASHBOARD")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 25px; margin-bottom: 25px; border-left: 4px solid #4f46e5;">
                    <div style="color: #4f46e5; font-size: 1.2rem; font-weight: 600; margin-bottom: 25px; text-align: center;">
                        {get_app_name(package_a).upper()}
                    </div>
                    <div class="metrics-grid" style="grid-template-columns: 1fr 1fr;">
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
                        <div class="metric-card">
                            <div class="metric-value">{df_a['polarity_score'].mean():.2f}</div>
                            <div class="metric-label">Sentiment</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 25px; margin-bottom: 25px; border-left: 4px solid #8b5cf6;">
                    <div style="color: #8b5cf6; font-size: 1.2rem; font-weight: 600; margin-bottom: 25px; text-align: center;">
                        {get_app_name(package_b).upper()}
                    </div>
                    <div class="metrics-grid" style="grid-template-columns: 1fr 1fr;">
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
                        <div class="metric-card">
                            <div class="metric-value">{df_b['polarity_score'].mean():.2f}</div>
                            <div class="metric-label">Sentiment</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.markdown("## COMPREHENSIVE METRICS OVERVIEW")
            st.markdown(f"""
            <div class="metrics-grid">
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
                    <div class="metric-label">Positive Rate</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{df_a['polarity_score'].mean():.2f}</div>
                    <div class="metric-label">Sentiment Score</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{(df_a['sentiment'] == 'Negative').mean() * 100:.1f}%</div>
                    <div class="metric-label">Negative Rate</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{df_a['subjectivity_score'].mean():.2f}</div>
                    <div class="metric-label">Subjectivity</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # AI Insights
        if enable_insights and (insights_a or insights_b):
            st.markdown("""
            <div class="ai-insights">
                <h2 style="color: #4f46e5; margin-bottom: 30px;">
                    ADVANCED AI STRATEGIC INTELLIGENCE
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.comparison_mode and insights_b:
                col1, col2 = st.columns(2)
                
                with col1:
                    if insights_a:
                        st.markdown(f"### {get_app_name(package_a).upper()} INSIGHTS")
                        for insight in insights_a[:4]:
                            css_class = "insight-item positive" if insight['type'] == 'positive' else "insight-item warning"
                            icon = "✓" if insight['type'] == 'positive' else "⚠"
                            st.markdown(f"""
                            <div class="{css_class}">
                                <h5 style="color: #4f46e5; margin-bottom: 12px; font-size: 1.1rem;">{icon} {insight['title']}</h5>
                                <p style="color: #475569; margin: 0; line-height: 1.6;">{insight['description']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                with col2:
                    if insights_b:
                        st.markdown(f"### {get_app_name(package_b).upper()} INSIGHTS")
                        for insight in insights_b[:4]:
                            css_class = "insight-item positive" if insight['type'] == 'positive' else "insight-item warning"
                            icon = "✓" if insight['type'] == 'positive' else "⚠"
                            st.markdown(f"""
                            <div class="{css_class}">
                                <h5 style="color: #8b5cf6; margin-bottom: 12px; font-size: 1.1rem;">{icon} {insight['title']}</h5>
                                <p style="color: #475569; margin: 0; line-height: 1.6;">{insight['description']}</p>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                for insight in insights_a[:5]:
                    css_class = "insight-item positive" if insight['type'] == 'positive' else "insight-item warning"
                    icon = "✓" if insight['type'] == 'positive' else "⚠"
                    st.markdown(f"""
                    <div class="{css_class}">
                        <h5 style="color: #4f46e5; margin-bottom: 12px; font-size: 1.1rem;">{icon} {insight['title']}</h5>
                        <p style="color: #475569; margin: 0; line-height: 1.6;">{insight['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Enhanced Visualizations
        st.markdown("""
        <div class="content-section">
            <div class="section-header">ADVANCED VISUALIZATION ANALYTICS</div>
        </div>
        """, unsafe_allow_html=True)
        
        charts = create_enhanced_charts(df_a, df_b)
        for chart_name, chart in charts.items():
            st.plotly_chart(chart, use_container_width=True)
        
        # Individual Reviews
        st.markdown("""
        <div class="content-section">
            <div class="section-header">INDIVIDUAL REVIEW ANALYSIS</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.comparison_mode and df_b is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                display_review_cards(df_a, f"{get_app_name(package_a).upper()} REVIEWS", max_reviews_display)
            
            with col2:
                display_review_cards(df_b, f"{get_app_name(package_b).upper()} REVIEWS", max_reviews_display)
        else:
            display_review_cards(df_a, f"{get_app_name(package_a).upper()} REVIEWS", max_reviews_display)
        
        # Export Section
        st.markdown("""
        <div class="content-section">
            <div class="section-header">PROFESSIONAL EXPORT SUITE</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="export-container">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="export-card">
                <div class="export-title">COMPREHENSIVE INTELLIGENCE REPORT</div>
                <div class="export-desc">
                    Professional HTML report with AI insights, competitive analysis, 
                    topic discovery, and executive summary with branded presentation.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            all_insights = insights_a + (insights_b if insights_b else [])
            all_topics = {**topics_a, **(topics_b if topics_b else {})}
            report_content = generate_professional_pdf(df_a, df_b, all_insights, all_topics)
            
            st.download_button(
                "DOWNLOAD PROFESSIONAL REPORT",
                data=report_content,
                file_name=f"TerminalAnalyzer_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                mime="text/html",
                type="primary"
            )
        
        with col2:
            st.markdown("""
            <div class="export-card">
                <div class="export-title">COMPLETE DATASET EXPORT</div>
                <div class="export-desc">
                    Full review database with enhanced sentiment analysis, 
                    business intelligence metrics, and processed data points.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if df_b is not None:
                combined_df = pd.concat([df_a, df_b], ignore_index=True)
                csv_data = combined_df.to_csv(index=False).encode('utf-8')
            else:
                csv_data = df_a.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                "DOWNLOAD COMPLETE DATASET",
                data=csv_data,
                file_name=f"TerminalAnalyzer_Dataset_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        with col3:
            st.markdown("""
            <div class="export-card">
                <div class="export-title">EXECUTIVE SUMMARY</div>
                <div class="export-desc">
                    High-level strategic metrics and KPIs formatted for 
                    executive presentations and stakeholder briefings.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if df_b is not None:
                summary_data = [{
                    "Application": get_app_name(package_a),
                    "Total_Reviews": len(df_a),
                    "Average_Rating": round(df_a["score"].mean(), 2),
                    "Positive_Rate_Percent": f"{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%",
                    "Sentiment_Score": round(df_a["polarity_score"].mean(), 3),
                    "Market_Position": "Leader" if df_a["score"].mean() > df_b["score"].mean() else "Challenger"
                }, {
                    "Application": get_app_name(package_b),
                    "Total_Reviews": len(df_b),
                    "Average_Rating": round(df_b["score"].mean(), 2),
                    "Positive_Rate_Percent": f"{(df_b['sentiment'] == 'Positive').mean() * 100:.1f}%",
                    "Sentiment_Score": round(df_b["polarity_score"].mean(), 3),
                    "Market_Position": "Leader" if df_b["score"].mean() > df_a["score"].mean() else "Challenger"
                }]
            else:
                avg_rating = df_a["score"].mean()
                positive_rate = (df_a['sentiment'] == 'Positive').mean() * 100
                market_position = "Leader" if avg_rating > 4.0 and positive_rate > 70 else "Strong" if avg_rating > 3.5 and positive_rate > 50 else "Developing"
                
                summary_data = [{
                    "Application": get_app_name(package_a),
                    "Total_Reviews": len(df_a),
                    "Average_Rating": round(avg_rating, 2),
                    "Positive_Rate_Percent": f"{positive_rate:.1f}%",
                    "Sentiment_Score": round(df_a["polarity_score"].mean(), 3),
                    "Market_Position": market_position
                }]
            
            summary_df = pd.DataFrame(summary_data)
            summary_csv = summary_df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                "DOWNLOAD EXECUTIVE SUMMARY",
                data=summary_csv,
                file_name=f"TerminalAnalyzer_Summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

# Professional Footer
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 40px; margin-top: 50px; 
           border-top: 1px solid #e2e8f0; background: white;">
    <div style="color: #4f46e5; font-size: 1.1rem; font-weight: 600; margin-bottom: 15px;">
        TERMINALANALYZER PRO v3.0
    </div>
    <div style="margin-bottom: 15px;">
        Professional Review Intelligence Platform | Created by <strong style="color: #4f46e5;">Ayush Pandey</strong>
    </div>
    <div style="font-size: 0.9rem; color: #94a3b8; line-height: 1.6;">
        Advanced AI Analytics • Modern Interface • Professional Intelligence<br>
        Transform Review Data Into Strategic Business Advantage
    </div>
</div>
""", unsafe_allow_html=True)
