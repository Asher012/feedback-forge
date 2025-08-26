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
