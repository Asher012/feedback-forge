# 🔨 Feedback Forge

**Multi-App Review & Sentiment Intelligence Platform**

A powerful web application that scrapes and analyzes reviews from multiple Google Play Store apps, providing comprehensive sentiment analysis and interactive visualizations.

## 🚀 Features

- **Multi-App Analysis**: Compare reviews across multiple apps simultaneously
- **Real-time Sentiment Analysis**: Advanced sentiment scoring using TextBlob
- **Interactive Visualizations**: Beautiful charts and graphs powered by Plotly
- **Detailed Filtering**: Filter data by app, sentiment, rating, and more
- **Export Capabilities**: Download complete datasets and summary reports
- **Timeline Analysis**: Track sentiment trends over time
- **Professional UI**: Clean, responsive interface with custom styling

## 📊 What You Get

### Analysis Features:
- ✅ **Sentiment Distribution**: Pie charts showing positive/neutral/negative breakdown
- ✅ **App Comparison**: Side-by-side sentiment analysis across apps
- ✅ **Rating Analysis**: Histogram showing rating distribution with sentiment overlay
- ✅ **Timeline Trends**: Track how sentiment changes over time
- ✅ **Key Metrics**: Total reviews, average ratings, sentiment percentages

### Data Export:
- 📊 **Complete Dataset**: Full review data with sentiment scores
- 📈 **Summary Reports**: App-wise analysis summary
- 📅 **Filtered Views**: Export filtered data based on your criteria

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Data Scraping**: google-play-scraper
- **Sentiment Analysis**: TextBlob
- **Visualizations**: Plotly
- **Data Processing**: Pandas

## 🚀 Quick Start

### Method 1: Deploy on Streamlit Cloud (Recommended)

1. **Fork this repository** to your GitHub account

2. **Visit [Streamlit Cloud](https://share.streamlit.io/)**

3. **Create New App**:
   - Select your forked repository
   - Branch: `main`
   - Main file path: `app.py`

4. **Deploy** - Your app will be live in minutes!

### Method 2: Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/feedback-forge.git
   cd feedback-forge
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open browser** at `http://localhost:8501`

## 📱 How to Use

### Step 1: Add App URLs
In the sidebar, paste Google Play Store URLs (one per line):
```
https://play.google.com/store/apps/details?id=xyz
https://play.google.com/store/apps/details?id=com.whatsapp
```

### Step 2: Configure Settings
- Set number of reviews per app (10-500)
- Choose language and country
- Select sorting preference

### Step 3: Start Analysis
Click "🚀 Start Analysis" and watch the magic happen!

### Step 4: Explore Results
- View interactive charts and metrics
- Filter data by various criteria
- Download reports in CSV format

## 📈 Sample Use Cases

### For Businesses:
- **Competitor Analysis**: Compare your app's sentiment vs competitors
- **Market Research**: Understand user feedback across app categories  
- **Product Strategy**: Identify common pain points and opportunities

### For Developers:
- **App Optimization**: Track sentiment changes after updates
- **User Feedback**: Analyze what users love and hate
- **Market Positioning**: See how you stack against similar apps

### For Researchers:
- **Sentiment Trends**: Study how app reviews correlate with ratings
- **User Behavior**: Understand review patterns across different apps
- **Market Analysis**: Analyze mobile app ecosystem trends

## 🔧 Configuration Options

The app supports several configuration options:

- **Languages**: English, Hindi, Spanish, French
- **Countries**: India, US, UK, Canada
- **Sorting**: Newest, Most Relevant, Rating
- **Review Count**: 10 to 500 reviews per app

## 📁 Project Structure

```
feedback-forge/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .streamlit/
    └── config.toml       # Streamlit configuration (optional)
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

## 📋 Roadmap

### Upcoming Features:
- [ ] **Multi-Platform Support**: Add Apple App Store, Amazon, etc.
- [ ] **Advanced Analytics**: Keyword extraction, topic modeling
- [ ] **API Integration**: RESTful API for programmatic access
- [ ] **Scheduling**: Automated periodic analysis
- [ ] **Email Reports**: Automated report delivery
- [ ] **Team Collaboration**: User accounts and shared dashboards

## ⚠️ Important Notes

### Rate Limiting
- Be respectful of Google Play Store's servers
- The app includes reasonable delays between requests
- Consider the ethical implications of data scraping

### Data Privacy
- No user data is stored on servers
- All processing happens in your browser session
- Downloaded data is your responsibility to handle securely

### Terms of Use
- This tool is for educational and research purposes
- Ensure compliance with Google Play Store's Terms of Service
- Use responsibly and ethically

## 🐛 Known Issues & Troubleshooting

### Common Issues:
1. **"No reviews found"**: App may have restricted access or incorrect URL
2. **Slow performance**: Large review counts take longer to process
3. **Memory errors**: Reduce review count if experiencing issues

### Solutions:
- Verify app URLs are correct and public
- Start with smaller review counts (50-100)
- Check internet connection for scraping issues

## 📞 Support

If you encounter any issues or have questions:

1. **Check the [Issues](https://github.com/your-username/feedback-forge/issues)** page
2. **Create a new issue** if your problem isn't already reported
3. **Include details**: Error messages, steps to reproduce, browser info

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit Team**: For the amazing web app framework
- **google-play-scraper**: For the excellent scraping library
- **TextBlob**: For sentiment analysis capabilities
- **Plotly**: For beautiful interactive visualizations

---

**Made with ❤️ for data-driven insights**

*Transform reviews into actionable intelligence with Feedback Forge!*
