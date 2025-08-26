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
