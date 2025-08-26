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
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

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
    
    .main-container {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 50%, #16213e 100%);
        color: #00ff88;
        font-family: 'Rajdhani', sans-serif;
    }
    
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
    
    .retro-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: sweep 3s infinite;
    }
    
    @keyframes sweep {
        0% { left: -100%; }
        100% { left: 100%; }
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
