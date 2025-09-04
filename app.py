import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from google_play_scraper import Sort, reviews
from datetime import datetime, timedelta
from collections import Counter
import time

# NLTK imports for text analysis
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# --- NLTK Data Download ---
# Helper function to download NLTK data safely
def download_nltk_data():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        st.info("Pehli baar setup ke liye 'stopwords' download kiya ja raha hai...")
        nltk.download('stopwords')
    try:
        nltk.data.find('sentiment/vader_lexicon.zip/vader_lexicon/vader_lexicon.txt')
    except LookupError:
        st.info("Pehli baar setup ke liye 'vader_lexicon' download kiya ja raha hai...")
        nltk.download('vader_lexicon')

# Download data at the start
download_nltk_data()

# --- Page Configuration ---
st.set_page_config(
    page_title="ReviewForge Pro | AI Review Analysis",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Modern UI/UX ---
st.markdown("""
<style>
    /* Main App Font and Colors */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    :root {
        --primary-color: #6c5ce7;
        --secondary-color: #a29bfe;
        --background-color: #1a1a2e;
        --card-bg-color: #24243e;
        --text-color: #e0e0e0;
        --subtle-text-color: #a0a0b0;
        --success-color: #00b894;
        --danger-color: #ff7675;
        --neutral-color: #fdcb6e;
    }
    body {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    .stApp {
        background-color: var(--background-color);
    }

    /* Sidebar Styling */
    .st-emotion-cache-16txtl3 {
        background-color: var(--card-bg-color);
        border-right: 1px solid #3a3a5a;
    }
    .st-emotion-cache-16txtl3 h1 {
        color: var(--primary-color);
        font-weight: 700;
    }

    /* Main Content Styling */
    .st-emotion-cache-z5fcl4 {
        width: 100%;
        padding: 2rem 3rem;
    }
    h1, h2, h3 {
        color: var(--text-color);
    }

    /* Custom Button Styling */
    .stButton > button {
        border: 2px solid var(--primary-color);
        background-color: transparent;
        color: var(--primary-color);
        padding: 12px 28px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: var(--primary-color);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.4);
    }
    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.5) !important;
    }

    /* Metric Cards Styling */
    .metric-card {
        background-color: var(--card-bg-color);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #3a3a5a;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        border-color: var(--primary-color);
    }
    .metric-card h3 {
        color: var(--subtle-text-color);
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .metric-card p {
        font-size: 2.25rem;
        font-weight: 700;
        color: var(--text-color);
        margin: 0;
    }

    /* Container/Card Styling */
    .st-emotion-cache-r421ms {
        background-color: var(--card-bg-color);
        border: 1px solid #3a3a5a;
        border-radius: 15px;
        padding: 1.5rem;
    }

    /* Expander/Accordion Styling */
    .st-expander {
        background-color: transparent !important;
        border: 1px solid #3a3a5a;
        border-radius: 10px;
    }
    .st-expander header {
        font-weight: 600;
        color: var(--secondary-color);
    }
    
    /* Hide Streamlit default elements */
    .st-emotion-cache-h4xjwg, .st-emotion-cache-1uihe3n {
        display: none;
    }
    footer {
        visibility: hidden;
    }
    .st-emotion-cache-cio0dv {
      visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# --- Caching Functions ---
@st.cache_data(ttl=3600, show_spinner="Aapke liye reviews laaye ja rahe hain...")
def get_all_reviews(app_id, review_count):
    """Google Play Store se reviews fetch karta hai."""
    result, continuation_token = reviews(
        app_id,
        lang='en',
        country='us',
        sort=Sort.NEWEST,
        count=review_count,
        filter_score_with=None
    )
    if not result:
        st.error("Is App ID ke liye koi review nahi mila. Kripya App ID check karein.")
        return pd.DataFrame()
    return pd.DataFrame(result)

@st.cache_data(show_spinner="Sentiment ka vishleshan kiya ja raha hai...")
def analyze_sentiment(df):
    """Review text ke aadhar par sentiment ka vishleshan karta hai."""
    if 'content' not in df.columns:
        return df

    sia = SentimentIntensityAnalyzer()
    
    def get_sentiment(text):
        if not isinstance(text, str):
            return "Neutral"
        score = sia.polarity_scores(text)['compound']
        if score > 0.05:
            return "Positive"
        elif score < -0.05:
            return "Negative"
        else:
            return "Neutral"

    df['sentiment_by_text'] = df['content'].apply(get_sentiment)
    return df

@st.cache_data(show_spinner="Mukhya vishayon (topics) ko nikala ja raha hai...")
def extract_topics(_df, num_topics=5, num_words=4):
    """LDA ka upyog karke pramukh vishayon ko nikalta hai."""
    if 'content' not in _df.columns:
        return [], "Content column not found."
    
    # Preprocessing
    stop_words = stopwords.words('english')
    # Use only non-empty documents
    documents = _df['content'].dropna().astype(str).tolist()
    if not documents:
        return [], "Koi valid review text vishleshan ke liye nahi hai."

    vectorizer = TfidfVectorizer(stop_words=stop_words, max_df=0.9, min_df=5, ngram_range=(1,2))
    try:
        X = vectorizer.fit_transform(documents)
    except ValueError:
        return [], "Text data process karne ke liye paryapt nahi hai. Kam se kam 5 alag-alag shabdon wale reviews chahiye."

    if X.shape[0] < num_topics:
        return [], f"Topics ki sankhya ({num_topics}) reviews ki sankhya ({X.shape[0]}) se kam honi chahiye."

    # LDA Model
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(X)

    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-num_words - 1:-1]]
        topics.append(top_words)
    
    # Assign topic to each review
    topic_distribution = lda.transform(X)
    _df['topic_id'] = np.argmax(topic_distribution, axis=1)

    return topics, _df

# --- UI Helper Functions ---
def render_metric(label, value, color="var(--text-color)"):
    """Ek single metric card render karta hai."""
    st.markdown(f"""
    <div class="metric-card">
        <h3>{label}</h3>
        <p style="color:{color};">{value}</p>
    </div>
    """, unsafe_allow_html=True)

def render_chart_container(title, description):
    """Chart ke liye ek styled container banata hai."""
    st.markdown(f"### {title}")
    st.caption(description)

# --- Main Application Pages ---

def dashboard_page():
    """Dashboard Page - Mukhya insights aur review list dikhata hai."""
    st.title("📊 Review Analysis Dashboard")
    st.markdown("---")

    if 'df_reviews' not in st.session_state or st.session_state.df_reviews.empty:
        st.info("Kripya vishleshan shuru karne ke liye sidebar se ek App ID enter karein.")
        return

    df = st.session_state.df_reviews

    # --- Sidebar Filters ---
    st.sidebar.header("Filter Reviews")
    
    # Rating Filter
    selected_ratings = st.sidebar.multiselect(
        "Star Rating se Filter Karein",
        options=sorted(df['score'].unique()),
        default=sorted(df['score'].unique())
    )

    # Date Range Filter
    min_date = df['at'].min().date()
    max_date = df['at'].max().date()
    date_range = st.sidebar.date_input(
        "Date Range se Filter Karein",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Aap kin dates ke beech ke reviews dekhna chahte hain."
    )
    
    # Apply filters
    start_date, end_date = date_range if len(date_range) == 2 else (min_date, max_date)
    filtered_df = df[
        (df['score'].isin(selected_ratings)) &
        (df['at'].dt.date >= start_date) &
        (df['at'].dt.date <= end_date)
    ]

    if filtered_df.empty:
        st.warning("Aapke chune gaye filters ke anusaar koi review nahi mila.")
        return

    # --- Key Metrics ---
    st.markdown("### 📈 Mukhya Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric("Kul Reviews", f"{filtered_df.shape[0]:,}")
    with col2:
        render_metric("Average Rating", f"{filtered_df['score'].mean():.2f} ⭐")
    with col3:
        pos_count = filtered_df[filtered_df['sentiment_by_text'] == 'Positive'].shape[0]
        render_metric("Positive Reviews", f"{pos_count:,}", "var(--success-color)")
    with col4:
        neg_count = filtered_df[filtered_df['sentiment_by_text'] == 'Negative'].shape[0]
        render_metric("Negative Reviews", f"{neg_count:,}", "var(--danger-color)")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Visualizations ---
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            render_chart_container(
                "Sentiment ka Vitaran (Review Text ke Aadhar par)",
                "Yeh chart dikhata hai ki kitne pratishat reviews positive, negative, ya neutral hain."
            )
            sentiment_counts = filtered_df['sentiment_by_text'].value_counts()
            fig = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                hole=0.4,
                color=sentiment_counts.index,
                color_discrete_map={'Positive':'#00b894', 'Negative':'#ff7675', 'Neutral':'#fdcb6e'}
            )
            fig.update_layout(
                legend_title_text='Sentiment',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='var(--text-color)'
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        with st.container(border=True):
            render_chart_container(
                "Rating ka Vitaran",
                "Yeh chart har star rating (1 se 5) ke liye reviews ki sankhya dikhata hai."
            )
            rating_counts = filtered_df['score'].value_counts().sort_index()
            fig = px.bar(
                x=rating_counts.index,
                y=rating_counts.values,
                labels={'x': 'Star Rating', 'y': 'Reviews ki Sankhya'},
                text_auto=True
            )
            fig.update_traces(marker_color='#a29bfe', textfont_size=12, textposition='outside')
            fig.update_layout(
                xaxis_title="Star Rating",
                yaxis_title="Reviews ki Sankhya",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='var(--text-color)',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
    # --- Recent Reviews Table ---
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 💬 Sabhi Reviews")
        st.caption(f"Yahan {filtered_df.shape[0]} reviews dikhaye ja rahe hain. Aap sidebar se filter kar sakte hain.")
        
        # Display DataFrame
        display_df = filtered_df[['at', 'userName', 'score', 'content', 'sentiment_by_text']].rename(columns={
            'at': 'Date', 'userName': 'User', 'score': 'Rating', 'content': 'Review Text', 'sentiment_by_text': 'Text Sentiment'
        })
        st.dataframe(display_df, use_container_width=True, height=400)


def deep_analysis_page():
    """Deep Analysis Page - Topic modeling aur keywords dikhata hai."""
    st.title("🔬 Gehrai se Vishleshan Engine")
    st.markdown("---")

    with st.expander("ℹ️ Yeh Engine Kaise Kaam Karta Hai?", expanded=False):
        st.markdown("""
        Yeh engine aapke app ke reviews ko samajhne ke liye **Machine Learning** ka upyog karta hai.

        - **Kaise Kaam Karta Hai?**
            1.  **Text Safai:** Reviews se aam shabdon (jaise 'is', 'the', 'a') ko hata diya jaata hai.
            2.  **Topic Modeling (LDA):** Ek advanced algorithm (Latent Dirichlet Allocation) ka istemal karke, engine reviews ke andar chhupe hue mukhya 'vishayon' ya 'themes' ko pehchanta hai. Jaise, ek vishay 'bugs' aur 'crashes' ke baare mein ho sakta hai, aur doosra 'UI' aur 'design' ke baare mein.
            3.  **Keyword Extraction:** Har vishay ke liye, engine sabse mahatvapurna keywords nikalta hai jo us vishay ko represent karte hain.

        - **Isse Kya Pata Chalta Hai?**
            Aapko turant pata chal jaata hai ki users aapke app ke kin features ke baare mein sabse zyada baat kar rahe hain, kya samasyayein hain, aur kya sudhar ke avsar hain, bina hazaron reviews padhe.
        """)

    if 'df_reviews' not in st.session_state or st.session_state.df_reviews.empty:
        st.info("Kripya vishleshan shuru karne ke liye sidebar se ek App ID enter karein.")
        return

    # --- Advanced Settings in Sidebar ---
    st.sidebar.header("Advanced Settings")
    st.sidebar.markdown("In settings ko badalne se vishleshan ke results par asar padega.")
    
    num_topics = st.sidebar.slider(
        "Topics ki Sankhya Chunein", 
        min_value=2, 
        max_value=10, 
        value=5, 
        step=1,
        help="Aap kitne alag-alag vishay/theme reviews se nikalna chahte hain? 4-6 ek accha starting point hai."
    )
    
    num_words = st.sidebar.slider(
        "Har Topic ke liye Keywords ki Sankhya", 
        min_value=3, 
        max_value=8, 
        value=5, 
        step=1,
        help="Har vishay ko represent karne ke liye kitne mukhya shabd dikhaye jaayein."
    )
    
    # --- Run Topic Modeling ---
    topics, df_with_topics = extract_topics(st.session_state.df_reviews, num_topics, num_words)

    if not topics:
        st.error(f"Topics nahi nikale ja sake. Sambhavit karan: {df_with_topics}") # df_with_topics will contain error message
        return

    st.session_state.df_reviews = df_with_topics # Update dataframe with topic ids

    st.markdown(f"### 💡 Mukhya {len(topics)} Topics Jo Reviews Mein Paaye Gaye")
    st.caption("Har card ek mukhya vishay, usse jude keywords aur udaharan review dikhata hai.")
    
    cols = st.columns(3)
    for i, topic_words in enumerate(topics):
        col = cols[i % 3]
        with col:
            with st.container(border=True):
                st.markdown(f"**Topic #{i+1}:**")
                
                # Display keywords
                keywords_html = " ".join([f"<span style='background-color: #3a3a5a; color: #a29bfe; padding: 4px 8px; border-radius: 5px; margin: 2px; display: inline-block;'>{word}</span>" for word in topic_words])
                st.markdown(keywords_html, unsafe_allow_html=True)
                st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                
                # Show sample reviews for this topic
                sample_reviews = st.session_state.df_reviews[st.session_state.df_reviews['topic_id'] == i].head(2)
                for _, row in sample_reviews.iterrows():
                    sentiment_color = "var(--success-color)" if row['sentiment_by_text'] == 'Positive' else ("var(--danger-color)" if row['sentiment_by_text'] == 'Negative' else "var(--neutral-color)")
                    st.markdown(f"<small style='color: {sentiment_color};'>❝ {row['content'][:100]}... ❞</small>", unsafe_allow_html=True)


# --- Main Application Logic ---
def main():
    st.sidebar.image("https://i.imgur.com/8W1gOEZ.png", width=100)
    st.sidebar.title("ReviewForge Pro")
    
    # --- Input Section ---
    st.sidebar.markdown("---")
    app_id = st.sidebar.text_input(
        "App ID Daalein", 
        placeholder="com.google.android.apps.maps",
        help="Play Store URL se App ID copy karein. Udaharan: 'com.google.android.apps.maps'"
    )
    review_count = st.sidebar.slider(
        "Kitne Reviews Analyze Karne Hain?", 
        min_value=100, 
        max_value=5000, 
        value=1000, 
        step=100,
        help="Zyada reviews behtar insights dete hain, lekin vishleshan mein adhik samay lag sakta hai."
    )

    if st.sidebar.button("Analyze Karein"):
        if app_id:
            with st.spinner("Analysis in progress... Kripya pratiksha karein..."):
                df = get_all_reviews(app_id, review_count)
                if not df.empty:
                    df_analyzed = analyze_sentiment(df)
                    st.session_state.df_reviews = df_analyzed
                    st.session_state.app_id = app_id
                    st.success(f"{app_id} ke liye {len(df_analyzed)} reviews ka vishleshan safaltapoorvak kiya gaya!")
                    time.sleep(1) # For user to see success message
        else:
            st.sidebar.warning("Kripya ek App ID daalein.")
    
    st.sidebar.markdown("---")
    # --- Navigation ---
    page = st.sidebar.radio(
        "Navigation",
        ["📊 Dashboard", "🔬 Gehrai se Vishleshan"],
        key='page'
    )
    
    if page == "📊 Dashboard":
        dashboard_page()
    elif page == "🔬 Gehrai se Vishleshan":
        deep_analysis_page()
        
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("Developed with ❤️ by Ayush Pandey | Version 3.0")


if __name__ == "__main__":
    main()
