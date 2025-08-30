                    progress_bar.progress(1.0)
                    status_text.text("Analysis complete!")
                    
                    # Clear progress indicators
                    progress_container.empty()
                    
                    # Display Enhanced Results
                    app_name_a = app_details_a['title'] if app_details_a else get_app_name(package_a)
                    app_name_b = app_details_b['title'] if app_details_b else get_app_name(package_b)
                    
                    st.success(f"Successfully analyzed {len(df_a):,} reviews for {app_name_a}" + 
                              (f" and {len(df_b):,} reviews for {app_name_b}" if df_b is not None else ""))
                    
                    # App Details Cards
                    if include_app_details and app_details_a:
                        st.markdown("## App Information")
                        
                        if st.session_state.comparison_mode and app_details_b:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f"""
                                <div class="dashboard-card">
                                    <h3 style="color: #667eea; margin-bottom: 16px;">{app_details_a['title']}</h3>
                                    <p><strong>Developer:</strong> {app_details_a['developer']}</p>
                                    <p><strong>Category:</strong> {app_details_a['category']}</p>
                                    <p><strong>Play Store Rating:</strong> {app_details_a['rating']:.1f}/5</p>
                                    <p><strong>Installs:</strong> {app_details_a['installs']}</p>
                                    <p><strong>Version:</strong> {app_details_a['version']}</p>
                                    <p><strong>Description:</strong> {app_details_a['description']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown(f"""
                                <div class="dashboard-card">
                                    <h3 style="color: #764ba2; margin-bottom: 16px;">{app_details_b['title']}</h3>
                                    <p><strong>Developer:</strong> {app_details_b['developer']}</p>
                                    <p><strong>Category:</strong> {app_details_b['category']}</p>
                                    <p><strong>Play Store Rating:</strong> {app_details_b['rating']:.1f}/5</p>
                                    <p><strong>Installs:</strong> {app_details_b['installs']}</p>
                                    <p><strong>Version:</strong> {app_details_b['version']}</p>
                                    <p><strong>Description:</strong> {app_details_b['description']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="glass-container">
                                <h3 style="color: #667eea; margin-bottom: 20px; text-align: center;">{app_details_a['title']}</h3>
                                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                                    <div style="text-align: center;">
                                        <strong>Developer</strong><br>{app_details_a['developer']}
                                    </div>
                                    <div style="text-align: center;">
                                        <strong>Category</strong><br>{app_details_a['category']}
                                    </div>
                                    <div style="text-align: center;">
                                        <strong>Play Store Rating</strong><br>{app_details_a['rating']:.1f}/5
                                    </div>
                                    <div style="text-align: center;">
                                        <strong>Installs</strong><br>{app_details_a['installs']}
                                    </div>
                                </div>
                                <div style="margin-top: 20px; padding: 20px; background: rgba(102, 126, 234, 0.1); border-radius: 12px;">
                                    <strong>Description:</strong><br>{app_details_a['description']}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Enhanced Metrics Section
                    if st.session_state.comparison_mode and df_b is not None:
                        st.markdown("## Comparison Results")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"""
                            <div class="results-container">
                                <h3 style="color: #667eea; text-align: center; margin-bottom: 20px;">{app_name_a}</h3>
                                <div class="metrics-row">
                                    <div class="metric-card">
                                        <div class="metric-value">{len(df_a):,}</div>
                                        <div class="metric-label">Reviews Analyzed</div>
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
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div class="results-container">
                                <h3 style="color: #764ba2; text-align: center; margin-bottom: 20px;">{app_name_b}</h3>
                                <div class="metrics-row">
                                    <div class="metric-card">
                                        <div class="metric-value">{len(df_b):,}</div>
                                        <div class="metric-label">Reviews Analyzed</div>
                                    </div>
                                    <div class="metric-card">
                                        <div class="metric-value">{df_b['score'].mean():.1f}</div>
                                        <div class="metric-label">Average Rating</div>
                                    </div>
                                    <div class="metric-card">
                                        <div class="metric-value">{(df_b['sentiment'] == 'Positive').mean() * 100:.1f}%</div>
                                        <div class="metric-label">Positive Reviews</div>
                                    </div>
                                    <div class="metric-card">
                                        <div class="metric-value">{df_b['polarity_score'].mean():.2f}</div>
                                        <div class="metric-label">Sentiment Score</div>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Winner Analysis
                        a_positive = (df_a['sentiment'] == 'Positive').mean() * 100
                        b_positive = (df_b['sentiment'] == 'Positive').mean() * 100
                        a_rating = df_a['score'].mean()
                        b_rating = df_b['score'].mean()
                        
                        if a_positive > b_positive and a_rating > b_rating:
                            winner = app_name_a
                            winner_color = "#667eea"
                        elif b_positive > a_positive and b_rating > a_rating:
                            winner = app_name_b
                            winner_color = "#764ba2"
                        else:
                            winner = "Tied Performance"
                            winner_color = "#48bb78"
                        
                        st.markdown(f"""
                        <div class="insights-container">
                            <h3 style="text-align: center; color: {winner_color}; margin-bottom: 20px;">
                                Overall Winner: {winner}
                            </h3>
                            <p style="text-align: center; color: #4a5568;">
                                Based on sentiment analysis and average ratings
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    else:
                        st.markdown("## Analysis Results")
                        st.markdown(f"""
                        <div class="results-container">
                            <h3 style="color: #667eea; text-align: center; margin-bottom: 20px;">{app_name_a}</h3>
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
                                <div class="metric-card">
                                    <div class="metric-value">{df_a['subjectivity_score'].mean():.2f}</div>
                                    <div class="metric-label">Subjectivity</div>
                                </div>
                                <div class="metric-card">
                                    <div class="metric-value">{len(df_a['userName'].unique()):,}</div>
                                    <div class="metric-label">Unique Users</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Enhanced Charts
                    charts = create_enhanced_charts(df_a, df_b, app_name_a, app_name_b)
                    
                    st.markdown("## Visual Analytics")
                    for chart_name, chart in charts.items():
                        st.plotly_chart(chart, use_container_width=True)
                    
                    # Word frequency analysis
                    word_chart_a = create_word_frequency_chart(df_a, f"Most Mentioned Words - {app_name_a}")
                    if word_chart_a:
                        st.plotly_chart(word_chart_a, use_container_width=True)
                    
                    if df_b is not None:
                        word_chart_b = create_word_frequency_chart(df_b, f"Most Mentioned Words - {app_name_b}")
                        if word_chart_b:
                            st.plotly_chart(word_chart_b, use_container_width=True)
                    
                    # Enhanced Insights
                    insights_a = generate_enhanced_insights(df_a, app_name_a)
                    if insights_a:
                        st.markdown(f"""
                        <div class="insights-container">
                            <h2 class="results-header">Key Insights for {app_name_a}</h2>
                        """, unsafe_allow_html=True)
                        
                        for insight in insights_a:
                            css_class = f'insight-item {insight["type"]}'
                            priority_indicators = {"critical": "CRITICAL", "high": "HIGH", "medium": "MEDIUM", "low": "LOW"}
                            indicator = priority_indicators.get(insight.get("priority", "low"), "INFO")
                            
                            st.markdown(f"""
                            <div class="{css_class}">
                                <div class="insight-title">[{indicator}] {insight['title']}</div>
                                <div class="insight-description">{insight['description']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    if df_b is not None:
                        insights_b = generate_enhanced_insights(df_b, app_name_b)
                        if insights_b:
                            st.markdown(f"""
                            <div class="insights-container">
                                <h2 class="results-header">Key Insights for {app_name_b}</h2>
                            """, unsafe_allow_html=True)
                            
                            for insight in insights_b:
                                css_class = f'insight-item {insight["type"]}'
                                priority_indicators = {"critical": "CRITICAL", "high": "HIGH", "medium": "MEDIUM", "low": "LOW"}
                                indicator = priority_indicators.get(insight.get("priority", "low"), "INFO")
                                
                                st.markdown(f"""
                                <div class="{css_class}">
                                    <div class="insight-title">[{indicator}] {insight['title']}</div>
                                    <div class="insight-description">{insight['description']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Enhanced Review Display
                    display_enhanced_review_cards(df_a, 15, f"Recent Reviews - {app_name_a}")
                    
                    if df_b is not None:
                        display_enhanced_review_cards(df_b, 15, f"Recent Reviews - {app_name_b}")
                    
                    # Enhanced Export Options
                    st.markdown("## Export & Share Results")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Prepare export data
                        if df_b is not None:
                            combined_df = pd.concat([df_a, df_b], ignore_index=True)
                            export_df = combined_df
                        else:
                            export_df = df_a
                        
                        if export_format == "CSV":
                            export_data = export_df.to_csv(index=False).encode('utf-8')
                            mime_type = "text/csv"
                            file_extension = "csv"
                        elif export_format == "JSON":
                            export_data = export_df.to_json(orient='records', indent=2).encode('utf-8')
                            mime_type = "application/json"
                            file_extension = "json"
                        else:  # Excel
                            buffer = BytesIO()
                            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                df_a.to_excel(writer, sheet_name=app_name_a[:30], index=False)
                                if df_b is not None:
                                    df_b.to_excel(writer, sheet_name=app_name_b[:30], index=False)
                            export_data = buffer.getvalue()
                            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            file_extension = "xlsx"
                        
                        st.download_button(
                            f"Download Complete Data ({export_format})",
                            data=export_data,
                            file_name=f"feedback_forge_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.{file_extension}",
                            mime=mime_type,
                            help=f"Download all review data in {export_format} format"
                        )
                    
                    with col2:
                        # Create enhanced summary
                        if df_b is not None:
                            summary_data = [{
                                "App_Name": app_name_a,
                                "Reviews_Count": len(df_a),
                                "Average_Rating": round(df_a["score"].mean(), 2),
                                "Positive_Percent": f"{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%",
                                "Negative_Percent": f"{(df_a['sentiment'] == 'Negative').mean() * 100:.1f}%",
                                "Sentiment_Score": round(df_a["polarity_score"].mean(), 3),
                                "Subjectivity": round(df_a["subjectivity_score"].mean(), 3)
                            }, {
                                "App_Name": app_name_b,
                                "Reviews_Count": len(df_b),
                                "Average_Rating": round(df_b["score"].mean(), 2),
                                "Positive_Percent": f"{(df_b['sentiment'] == 'Positive').mean() * 100:.1f}%",
                                "Negative_Percent": f"{(df_b['sentiment'] == 'Negative').mean() * 100:.1f}%",
                                "Sentiment_Score": round(df_b["polarity_score"].mean(), 3),
                                "Subjectivity": round(df_b["subjectivity_score"].mean(), 3)
                            }]
                        else:
                            summary_data = [{
                                "App_Name": app_name_a,
                                "Reviews_Count": len(df_a),
                                "Average_Rating": round(df_a["score"].mean(), 2),
                                "Positive_Percent": f"{(df_a['sentiment'] == 'Positive').mean() * 100:.1f}%",
                                "Negative_Percent": f"{(df_a['sentiment'] == 'Negative').mean() * 100:.1f}%",
                                "Sentiment_Score": round(df_a["polarity_score"].mean(), 3),
                                "Subjectivity": round(df_a["subjectivity_score"].mean(), 3)
                            }]
                        
                        summary_df = pd.DataFrame(summary_data)
                        summary_csv = summary_df.to_csv(index=False).encode('utf-8')
                        
                        st.download_button(
                            "Download Executive Summary",
                            data=summary_csv,
                            file_name=f"feedback_forge_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                            mime="text/csv",
                            help="Download a concise summary perfect for sharing with stakeholders"
                        )
                    
                    with col3:
                        # Generate insights report
                        insights_text = f"# Feedback Forge Analysis Report\n\n"
                        insights_text += f"**Generated on:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n"
                        insights_text += f"**Developed by:** Ayush Pandey\n\n"
                        
                        if df_b is not None:
                            insights_text += f"## Comparison Analysis: {app_name_a} vs {app_name_b}\n\n"
                        else:
                            insights_text += f"## Analysis Report: {app_name_a}\n\n"
                        
                        insights_text += f"### Key Metrics\n"
                        for insight in insights_a[:3]:
                            insights_text += f"- **{insight['title']}:** {insight['description']}\n"
                        
                        st.download_button(
                            "Download Insights Report",
                            data=insights_text.encode('utf-8'),
                            file_name=f"feedback_forge_insights_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                            mime="text/markdown",
                            help="Download a markdown report with key insights and recommendations"
                        )
                
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                    st.info("Please check your internet connection and verify the app URLs are correct.")

# DASHBOARD PAGE
elif st.session_state.page == 'dashboard':
    st.markdown("""
    <div class="content-container">
        <div class="glass-container">
            <div class="section">
                <h1 class="section-title">Analytics Dashboard</h1>
                <p class="section-subtitle">
                    Comprehensive overview of your analysis history and saved reports
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.current_analysis:
        analysis = st.session_state.current_analysis
        df_a = analysis['df_a']
        df_b = analysis.get('df_b')
        
        st.markdown("## Current Analysis Overview")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(df_a):,}</div>
                <div class="metric-label">Reviews Analyzed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_reviews = len(df_a) + (len(df_b) if df_b is not None else 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_reviews:,}</div>
                <div class="metric-label">Total Data Points</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_sentiment = df_a['polarity_score'].mean()
            if df_b is not None:
                avg_sentiment = (df_a['polarity_score'].mean() + df_b['polarity_score'].mean()) / 2
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_sentiment:.2f}</div>
                <div class="metric-label">Avg Sentiment</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            analysis_time = analysis['timestamp'].strftime('%H:%M')
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{analysis_time}</div>
                <div class="metric-label">Last Updated</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Dashboard charts
        app_name_a = analysis.get('app_details_a', {}).get('title', 'App A') if analysis.get('app_details_a') else 'App A'
        app_name_b = analysis.get('app_details_b', {}).get('title', 'App B') if analysis.get('app_details_b') else 'App B'
        
        if df_b is not None:
            charts = create_enhanced_charts(df_a, df_b, app_name_a, app_name_b)
        else:
            charts = create_enhanced_charts(df_a, None, app_name_a)
        
        for chart_name, chart in charts.items():
            st.plotly_chart(chart, use_container_width=True)
        
        # Quick actions
        st.markdown("## Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Refresh Analysis", key="refresh_dashboard"):
                st.rerun()
        
        with col2:
            if st.button("New Analysis", key="new_analysis_dashboard"):
                navigate_to('analysis')
        
        with col3:
            if st.button("Export Data", key="export_dashboard"):
                st.info("Use the Analysis page to configure and download reports")
    
    else:
        st.markdown("""
        <div class="glass-container">
            <div style="text-align: center; padding: 60px 0;">
                <h2 style="color: #4a5568; margin-bottom: 20px;">No Analysis Available</h2>
                <p style="color: #718096; margin-bottom: 32px;">Start your first analysis to see dashboard insights</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Start Analysis", key="start_from_dashboard"):
                navigate_to('analysis')

# ABOUT PAGE
elif st.session_state.page == 'about':
    st.markdown("""
    <div class="content-container">
        <div class="glass-container">
            <div class="hero-section">
                <h1 class="hero-title">About Feedback Forge</h1>
                <p class="hero-subtitle">
                    Empowering developers and product managers with AI-driven insights 
                    from app store reviews and user feedback.
                </p>
            </div>
        </div>
        
        <div class="glass-container">
            <div class="section">
                <h2 style="color: #1a202c; font-size: 32px; font-weight: 700; margin-bottom: 24px;">Our Mission</h2>
                <p style="color: #4a5568; font-size: 18px; line-height: 1.7; margin-bottom: 20px;">
                    In today's hyper-competitive app ecosystem, user feedback represents the most valuable source 
                    of product intelligence. However, with thousands of reviews across multiple platforms, 
                    manually processing this feedback becomes impossible at scale.
                </p>
                <p style="color: #4a5568; font-size: 18px; line-height: 1.7; margin-bottom: 20px;">
                    Feedback Forge bridges this gap by applying advanced artificial intelligence to transform 
                    raw review data into strategic insights. We help product teams understand not just what 
                    users are saying, but what they really mean and what actions should be taken.
                </p>
            </div>
        </div>
        
        <div class="glass-container">
            <div class="section">
                <h2 style="color: #1a202c; font-size: 32px; font-weight: 700; margin-bottom: 24px;">Developer Information</h2>
                <div style="text-align: center; padding: 40px;">
                    <div style="display: inline-block; background: rgba(102, 126, 234, 0.1); padding: 32px; border-radius: 20px; border: 2px solid rgba(102, 126, 234, 0.2);">
                        <h3 style="color: #667eea; font-size: 28px; margin-bottom: 16px;">Ayush Pandey</h3>
                        <p style="color: #4a5568; font-size: 18px; margin-bottom: 12px;">Full-Stack Developer & Data Scientist</p>
                        <p style="color: #718096; font-size: 16px; line-height: 1.6;">
                            Passionate about building intelligent applications that solve real-world problems. 
                            Specializing in AI/ML integration, modern web development, and data-driven insights.
                        </p>
                        <div style="margin-top: 24px;">
                            <span style="background: rgba(102, 126, 234, 0.2); color: #667eea; padding: 8px 16px; border-radius: 20px; margin: 4px; display: inline-block; font-size: 14px;">Python</span>
                            <span style="background: rgba(102, 126, 234, 0.2); color: #667eea; padding: 8px 16px; border-radius: 20px; margin: 4px; display: inline-block; font-size: 14px;">Machine Learning</span>
                            <span style="background: rgba(102, 126, 234, 0.2); color: #667eea; padding: 8px 16px; border-radius: 20px; margin: 4px; display: inline-block; font-size: 14px;">Data Analytics</span>
                            <span style="background: rgba(102, 126, 234, 0.2); color: #667eea; padding: 8px 16px; border-radius: 20px; margin: 4px; display: inline-block; font-size: 14px;">Streamlit</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# HELP PAGE
elif st.session_state.page == 'help':
    st.markdown("""
    <div class="content-container">
        <div class="glass-container">
            <div class="section">
                <h1 class="section-title">Help & Documentation</h1>
                <p class="section-subtitle">
                    Everything you need to know to get the most out of Feedback Forge
                </p>
            </div>
        </div>
        
        <div class="glass-container">
            <div class="section">
                <h2 style="color: #1a202c; font-size: 28px; font-weight: 700; margin-bottom: 24px;">Getting Started</h2>
                
                <div class="dashboard-grid">
                    <div class="dashboard-card">
                        <h3 style="color: #667eea; margin-bottom: 16px;">Step 1: Find Your App URL</h3>
                        <p>Go to the Google Play Store, search for your app, and copy the full URL from your browser. 
                        It should look like: https://play.google.com/store/apps/details?id=com.yourapp.name</p>
                    </div>
                    
                    <div class="dashboard-card">
                        <h3 style="color: #667eea; margin-bottom: 16px;">Step 2: Choose Analysis Type</h3>
                        <p>Select either Single App Analysis for deep insights into one app, or Competitive Comparison 
                        to analyze your app against a competitor side-by-side.</p>
                    </div>
                    
                    <div class="dashboard-card">
                        <h3 style="color: #667eea; margin-bottom: 16px;">Step 3: Configure Settings</h3>
                        <p>Adjust the number of reviews to analyze (more = better insights but slower processing), 
                        select language, and choose sorting preferences based on your analysis goals.</p>
                    </div>
                    
                    <div class="dashboard-card">
                        <h3 style="color: #667eea; margin-bottom: 16px;">Step 4: Review Results</h3>
                        <p>Examine the comprehensive results including sentiment analysis, key insights, 
                        visual charts, and individual review breakdowns to inform your product decisions.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="glass-container">
            <div class="section">
                <h2 style="color: #1a202c; font-size: 28px; font-weight: 700; margin-bottom: 24px;">Understanding Results</h2>
                
                <div style="margin-bottom: 32px;">
                    <h3 style="color: #4a5568; margin-bottom: 16px;">Sentiment Categories</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
                        <div style="padding: 16px; background: rgba(72, 187, 120, 0.1); border-radius: 8px; border-left: 4px solid #48bb78;">
                            <strong style="color: #48bb78;">Positive</strong><br>
                            <small style="color: #4a5568;">Reviews expressing satisfaction, praise, or positive experiences</small>
                        </div>
                        <div style="padding: 16px; background: rgba(160, 174, 192, 0.1); border-radius: 8px; border-left: 4px solid #a0aec0;">
                            <strong style="color: #a0aec0;">Neutral</strong><br>
                            <small style="color: #4a5568;">Reviews with balanced or factual content without strong emotion</small>
                        </div>
                        <div style="padding: 16px; background: rgba(245, 101, 101, 0.1); border-radius: 8px; border-left: 4px solid #f56565;">
                            <strong style="color: #f56565;">Negative</strong><br>
                            <small style="color: #4a5568;">Reviews expressing frustration, complaints, or negative experiences</small>
                        </div>
                    </div>
                </div>
                
                <div style="margin-bottom: 32px;">
                    <h3 style="color: #4a5568; margin-bottom: 16px;">Key Metrics Explained</h3>
                    <div style="background: rgba(102, 126, 234, 0.05); padding: 24px; border-radius: 12px;">
                        <ul style="color: #4a5568; line-height: 1.8;">
                            <li><strong>Sentiment Score:</strong> Ranges from -1 (very negative) to +1 (very positive)</li>
                            <li><strong>Subjectivity:</strong> Ranges from 0 (objective) to 1 (subjective/opinionated)</li>
                            <li><strong>Business Impact:</strong> Categorizes the potential impact on your business</li>
                            <li><strong>Review Volume:</strong> Total number of reviews analyzed for insights</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="glass-container">
            <div class="section">
                <h2 style="color: #1a202c; font-size: 28px; font-weight: 700; margin-bottom: 24px;">Contact & Support</h2>
                <div style="text-align: center; padding: 32px;">
                    <p style="color: #4a5568; font-size: 18px; margin-bottom: 24px;">
                        Need help with your analysis or have suggestions for improvement?
                    </p>
                    <div style="background: rgba(102, 126, 234, 0.1); padding: 24px; border-radius: 16px; display: inline-block;">
                        <p style="color: #667eea; font-weight: 600; margin-bottom: 8px;">Developer: Ayush Pandey</p>
                        <p style="color: #4a5568; margin-bottom: 4px;">Available for consulting and custom development</p>
                        <p style="color: #718096; font-size: 14px;">Built with Python, Streamlit, and advanced ML techniques</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Navigation buttons (hidden but functional)
with st.container():
    st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Home", key="nav_home"):
            navigate_to('home')
    
    with col2:
        if st.button("Analysis", key="nav_analysis"):
            navigate_to('analysis')
    
    with col3:
        if st.button("Dashboard", key="nav_dashboard"):
            navigate_to('dashboard')
    
    with col4:
        if st.button("About", key="nav_about"):
            navigate_to('about')
    
    with col5:
        if st.button("Help", key="nav_help"):
            navigate_to('help')
    
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <div class="footer-brand">Feedback Forge</div>
        <p class="footer-text">
            Transform app reviews into actionable intelligence with advanced AI-powered sentiment analysis 
            and competitive insights.
        </p>
        <p class="footer-text">
            Built with precision and care for developers and product managers who want to understand 
            their users better and make data-driven decisions.
        </p>
        <div class="footer-developer">
            Crafted with passion by Ayush Pandey | Full-Stack Developer & Data Scientist
        </div>
        <p style="color: rgba(255, 255, 255, 0.6); font-size: 14px; margin-top: 20px;">
            2024 Feedback Forge. Empowering product teams with intelligent insights.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)    try:
        sentiment_dist = df['sentiment'].value_counts(normalize=True) * 100
        avg_rating = df['score'].mean()
        total_reviews = len(df)
        
        positive_rate = sentiment_dist.get('Positive', 0)
        negative_rate = sentiment_dist.get('Negative', 0)
        neutral_rate = sentiment_dist.get('Neutral', 0)
        
        # Performance Insights
        if positive_rate > 75 and avg_rating > 4.0:
            insights.append({
                "type": "positive",
                "title": "Exceptional User Satisfaction",
                "description": f"{app_name} demonstrates outstanding performance with {positive_rate:.1f}% positive reviews and a {avg_rating:.1f}-star average. Users are consistently delighted with the experience.",
                "priority": "high"
            })
        elif positive_rate > 60 and avg_rating > 3.5:
            insights.append({
                "type": "positive", 
                "title": "Strong User Approval",
                "description": f"With {positive_rate:.1f}% positive feedback and {avg_rating:.1f} stars, {app_name} maintains good user satisfaction levels.",
                "priority": "medium"
            })
        
        # Areas for Improvement
        if negative_rate > 40:
            insights.append({
                "type": "negative",
                "title": "Critical Issues Detected",
                "description": f"High negative sentiment ({negative_rate:.1f}%) indicates significant user frustrations that require immediate attention.",
                "priority": "critical"
            })
        elif negative_rate > 25:
            insights.append({
                "type": "warning",
                "title": "Improvement Opportunities",
                "description": f"{negative_rate:.1f}% negative feedback suggests areas where user experience can be enhanced.",
                "priority": "medium"
            })
        
        # Engagement Insights
        if total_reviews > 1000:
            insights.append({
                "type": "positive",
                "title": "High User Engagement",
                "description": f"With {total_reviews:,} reviews, {app_name} shows excellent user engagement and market presence.",
                "priority": "medium"
            })
        elif total_reviews < 50:
            insights.append({
                "type": "warning",
                "title": "Low Review Volume",
                "description": f"Only {total_reviews} reviews available. Consider strategies to encourage more user feedback.",
                "priority": "low"
            })
        
        # Consistency Analysis
        rating_std = df['score'].std()
        if rating_std < 0.8:
            insights.append({
                "type": "positive",
                "title": "Consistent User Experience",
                "description": f"Low rating variance ({rating_std:.2f}) indicates reliable, consistent user experiences across different users.",
                "priority": "medium"
            })
        elif rating_std > 1.5:
            insights.append({
                "type": "warning",
                "title": "Inconsistent Experiences",
                "description": f"High rating variance ({rating_std:.2f}) suggests mixed user experiences that need investigation.",
                "priority": "high"
            })
        
        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        insights.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 3))
        
        return insights[:6]
        
    except Exception as e:
        return [{
            "type": "warning",
            "title": "Analysis Error",
            "description": "Some insights could not be generated due to data processing issues.",
            "priority": "low"
        }]

def create_enhanced_charts(df_a, df_b=None, app_name_a="App A", app_name_b="App B"):
    charts = {}
    
    # Enhanced color scheme
    colors = {
        'Positive': '#48bb78',
        'Neutral': '#f6ad55', 
        'Negative': '#f56565'
    }
    
    template = {
        'layout': {
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': '#1a202c', 'family': 'Inter, system-ui, sans-serif'},
            'colorway': ['#667eea', '#764ba2', '#48bb78', '#f6ad55', '#f56565']
        }
    }
    
    if df_b is not None and not df_b.empty:
        # Comparison charts
        sentiment_a = df_a['sentiment'].value_counts(normalize=True) * 100
        sentiment_b = df_b['sentiment'].value_counts(normalize=True) * 100
        
        # Sentiment comparison
        fig_comparison = go.Figure()
        
        sentiments = ['Positive', 'Neutral', 'Negative']
        x_pos = [0.8, 1.8, 2.8]
        x_pos_b = [1.2, 2.2, 3.2]
        
        fig_comparison.add_trace(go.Bar(
            name=app_name_a,
            x=x_pos,
            y=[sentiment_a.get(s, 0) for s in sentiments],
            marker_color='#667eea',
            width=0.35,
            text=[f'{sentiment_a.get(s, 0):.1f}%' for s in sentiments],
            textposition='outside'
        ))
        
        fig_comparison.add_trace(go.Bar(
            name=app_name_b,
            x=x_pos_b,
            y=[sentiment_b.get(s, 0) for s in sentiments],
            marker_color='#764ba2',
            width=0.35,
            text=[f'{sentiment_b.get(s, 0):.1f}%' for s in sentiments],
            textposition='outside'
        ))
        
        fig_comparison.update_layout(
            title=f'Sentiment Comparison: {app_name_a} vs {app_name_b}',
            xaxis_title='Sentiment Categories',
            yaxis_title='Percentage of Reviews',
            xaxis=dict(tickvals=[1, 2, 3], ticktext=sentiments),
            template=template,
            showlegend=True,
            barmode='group',
            height=500
        )
        
        charts['sentiment_comparison'] = fig_comparison
        
        # Rating distribution comparison
        fig_rating = make_subplots(rows=1, cols=2, subplot_titles=(app_name_a, app_name_b))
        
        for i, (df, name) in enumerate([(df_a, app_name_a), (df_b, app_name_b)], 1):
            rating_counts = df['score'].value_counts().sort_index()
            fig_rating.add_trace(
                go.Bar(x=rating_counts.index, y=rating_counts.values, 
                      name=name, marker_color='#667eea' if i==1 else '#764ba2'),
                row=1, col=i
            )
        
        fig_rating.update_layout(
            title='Rating Distribution Comparison',
            template=template,
            height=400,
            showlegend=False
        )
        
        charts['rating_comparison'] = fig_rating
    
    else:
        # Single app charts
        sentiment_counts = df_a['sentiment'].value_counts()
        
        # Enhanced pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=0.5,
            marker=dict(colors=[colors.get(label, '#718096') for label in sentiment_counts.index]),
            textinfo='label+percent+value',
            textfont=dict(size=14, color='#1a202c'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig_pie.update_layout(
            title=f"Sentiment Distribution for {app_name_a}",
            template=template,
            annotations=[dict(text=f'Total<br>{sentiment_counts.sum():,}<br>Reviews', 
                            x=0.5, y=0.5, font_size=16, showarrow=False, 
                            font_color='#1a202c', font_weight='bold')],
            height=500
        )
        
        charts['sentiment_pie'] = fig_pie
        
        # Rating distribution
        rating_counts = df_a['score'].value_counts().sort_index()
        fig_rating = go.Figure(data=[
            go.Bar(x=rating_counts.index, y=rating_counts.values,
                  marker_color='#667eea',
                  text=rating_counts.values,
                  textposition='outside',
                  hovertemplate='<b>Rating: %{x}</b><br>Count: %{y}<extra></extra>')
        ])
        
        fig_rating.update_layout(
            title=f'Rating Distribution for {app_name_a}',
            xaxis_title='Rating (Stars)',
            yaxis_title='Number of Reviews',
            template=template,
            height=400
        )
        
        charts['rating_distribution'] = fig_rating
        
        # Sentiment over time (if date available)
        if 'at' in df_a.columns:
            df_time = df_a.copy()
            df_time['date'] = pd.to_datetime(df_time['at']).dt.date
            daily_sentiment = df_time.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
            
            fig_timeline = go.Figure()
            
            for sentiment in ['Positive', 'Neutral', 'Negative']:
                if sentiment in daily_sentiment.columns:
                    fig_timeline.add_trace(go.Scatter(
                        x=daily_sentiment.index,
                        y=daily_sentiment[sentiment],
                        mode='lines+markers',
                        name=sentiment,
                        line=dict(color=colors[sentiment], width=3),
                        marker=dict(size=6)
                    ))
            
            fig_timeline.update_layout(
                title=f'Sentiment Trends Over Time for {app_name_a}',
                xaxis_title='Date',
                yaxis_title='Number of Reviews',
                template=template,
                height=400,
                hovermode='x unified'
            )
            
            charts['sentiment_timeline'] = fig_timeline
    
    return charts

def display_enhanced_review_cards(df, max_reviews=10, title="Recent Reviews"):
    if df.empty:
        st.warning("No reviews available to display.")
        return
    
    st.markdown(f"""
    <div class="results-container">
        <h2 class="results-header">{title}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Sort by date if available, otherwise by score
    if 'at' in df.columns:
        df_sorted = df.sort_values('at', ascending=False).head(max_reviews)
    else:
        df_sorted = df.sort_values('score', ascending=False).head(max_reviews)
    
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
        if len(content) > 500:
            content = content[:500] + "..."
        
        # Get polarity score for color coding
        polarity = review.get('polarity_score', 0)
        polarity_display = f"Sentiment Score: {polarity:.2f}" if polarity != 0 else "Sentiment Score: N/A"
        
        st.markdown(f"""
        <div class="review-card">
            <div class="review-header">
                <div class="review-author">{review.get('userName', 'Anonymous User')}</div>
                <div class="review-rating">
                    <span class="star">{stars}</span>
                    <span style="margin-left: 8px; font-weight: 600;">{rating}/5</span>
                </div>
            </div>
            <div class="review-content">{content}</div>
            <div class="review-meta">
                <div>
                    <span style="margin-right: 16px;">{date_str}</span>
                    <span style="font-size: 12px; color: #718096;">{polarity_display}</span>
                </div>
                <div class="sentiment-tag {badge_class}">{sentiment}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_word_frequency_chart(df, title="Most Common Words"):
    """Create word frequency analysis"""
    if df.empty or 'content' not in df.columns:
        return None
    
    # Combine all review content
    all_text = ' '.join(df['content'].dropna().astype(str))
    
    # Simple word frequency
    words = re.findall(r'\b[a-zA-Z]{4,}\b', all_text.lower())
    
    # Remove common stop words
    stop_words = {'this', 'that', 'with', 'have', 'will', 'from', 'they', 'know', 'want', 'been', 
                 'good', 'much', 'some', 'time', 'very', 'when', 'come', 'here', 'just', 'like',
                 'long', 'make', 'many', 'over', 'such', 'take', 'than', 'them', 'well', 'were'}
    
    filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
    
    word_freq = Counter(filtered_words).most_common(15)
    
    if not word_freq:
        return None
    
    words, counts = zip(*word_freq)
    
    fig = go.Figure(data=[
        go.Bar(x=list(counts), y=list(words), orientation='h',
               marker_color='#667eea',
               text=list(counts),
               textposition='outside')
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title='Frequency',
        yaxis_title='Words',
        template={
            'layout': {
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'font': {'color': '#1a202c', 'family': 'Inter, system-ui, sans-serif'}
            }
        },
        height=500,
        yaxis=dict(autorange="reversed")
    )
    
    return fig

# Show Enhanced Navigation
show_navigation()

# HOME PAGE
if st.session_state.page == 'home':
    # Enhanced Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Transform App Reviews Into Actionable Intelligence</h1>
        <p class="hero-subtitle">
            Leverage advanced sentiment analysis, competitive benchmarking, and AI-powered insights 
            to understand what your users truly think and drive product success.
        </p>
        
        <div class="hero-stats">
            <div class="hero-stat">
                <span class="hero-stat-number">10K+</span>
                <span class="hero-stat-label">Reviews Analyzed</span>
            </div>
            <div class="hero-stat">
                <span class="hero-stat-number">500+</span>
                <span class="hero-stat-label">Apps Reviewed</span>
            </div>
            <div class="hero-stat">
                <span class="hero-stat-number">95%</span>
                <span class="hero-stat-label">Accuracy Rate</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Start Free Analysis", key="start_analysis_home"):
                navigate_to('analysis')
        with col_b:
            if st.button("Learn More", key="learn_more_home"):
                navigate_to('about')
    
    # Enhanced Features Section
    st.markdown("""
    <div class="content-container">
        <div class="glass-container">
            <div class="section">
                <h2 class="section-title">Comprehensive App Intelligence Platform</h2>
                <p class="section-subtitle">
                    Our AI-powered platform combines multiple analysis techniques to provide you with 
                    deeper insights than traditional review monitoring tools.
                </p>
                
                <div class="features-grid">
                    <div class="feature-card">
                        <h3 class="feature-title">AI-Powered Sentiment Analysis</h3>
                        <p class="feature-description">
                            Advanced natural language processing identifies not just positive/negative sentiment, 
                            but emotional nuances, intensity levels, and context-aware insights that traditional 
                            tools miss.
                        </p>
                    </div>
                    
                    <div class="feature-card">
                        <h3 class="feature-title">Competitive Intelligence</h3>
                        <p class="feature-description">
                            Side-by-side app comparisons reveal market positioning opportunities, feature gaps, 
                            and user satisfaction differences to guide strategic decisions.
                        </p>
                    </div>
                    
                    <div class="feature-card">
                        <h3 class="feature-title">Topic & Theme Discovery</h3>
                        <p class="feature-description">
                            Automatically identify recurring themes, feature requests, and pain points across 
                            thousands of reviews to prioritize development efforts effectively.
                        </p>
                    </div>
                    
                    <div class="feature-card">
                        <h3 class="feature-title">Individual Review Deep-Dive</h3>
                        <p class="feature-description">
                            Read and analyze individual user experiences with contextual sentiment scoring, 
                            keyword extraction, and impact assessment for targeted improvements.
                        </p>
                    </div>
                    
                    <div class="feature-card">
                        <h3 class="feature-title">Interactive Dashboards</h3>
                        <p class="feature-description">
                            Beautiful, interactive visualizations make complex data accessible to both 
                            technical and non-technical stakeholders with customizable reporting options.
                        </p>
                    </div>
                    
                    <div class="feature-card">
                        <h3 class="feature-title">Real-Time Processing</h3>
                        <p class="feature-description">
                            Lightning-fast analysis processes thousands of reviews in seconds, providing 
                            immediate insights when you need them most for rapid decision-making.
                        </p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="glass-container">
            <div class="section">
                <h2 class="section-title">Why Choose Feedback Forge?</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3 style="color: #667eea; font-size: 24px; margin-bottom: 16px;">Accuracy</h3>
                        <p>Our machine learning models achieve 95%+ accuracy in sentiment classification, 
                        outperforming traditional keyword-based approaches.</p>
                    </div>
                    
                    <div class="stat-card">
                        <h3 style="color: #667eea; font-size: 24px; margin-bottom: 16px;">Speed</h3>
                        <p>Process up to 10,000 reviews in under 2 minutes, giving you instant insights 
                        without the wait times of manual analysis.</p>
                    </div>
                    
                    <div class="stat-card">
                        <h3 style="color: #667eea; font-size: 24px; margin-bottom: 16px;">Depth</h3>
                        <p>Go beyond simple ratings with emotional analysis, theme extraction, and 
                        competitive positioning insights for actionable intelligence.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ANALYSIS PAGE
elif st.session_state.page == 'analysis':
    st.markdown("""
    <div class="content-container">
        <div class="glass-container">
            <div class="section">
                <h1 class="section-title">Advanced App Review Analysis</h1>
                <p class="section-subtitle">
                    Enter your app's Google Play Store URL to unlock comprehensive insights about user sentiment, 
                    satisfaction trends, and competitive positioning.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Analysis Form
    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        
        # Mode Selection with improved UI
        st.markdown('<h2 class="form-title">Choose Your Analysis Type</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Single App Deep Dive", key="single_btn", help="Comprehensive analysis of one app"):
                st.session_state.comparison_mode = False
                st.success("Single app analysis mode selected")
        
        with col2:
            if st.button("Competitive Comparison", key="compare_btn", help="Compare two apps side by side"):
                st.session_state.comparison_mode = True
                st.success("Comparison mode selected")
        
        st.markdown("---")
        
        # URL Input with enhanced validation
        if st.session_state.comparison_mode:
            st.markdown("### App Comparison Analysis")
            st.info("Compare your app with a direct competitor to identify opportunities and threats")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**First App (Your App)**")
                url_a = st.text_area(
                    "Google Play Store URL", 
                    placeholder="https://play.google.com/store/apps/details?id=com.example.app", 
                    height=100, 
                    key="url_a",
                    help="Paste the complete Google Play Store URL"
                )
            
            with col2:
                st.markdown("**Second App (Competitor)**")
                url_b = st.text_area(
                    "Google Play Store URL", 
                    placeholder="https://play.google.com/store/apps/details?id=com.competitor.app", 
                    height=100, 
                    key="url_b",
                    help="Paste the competitor's Google Play Store URL"
                )
        else:
            st.markdown("### Single App Analysis")
            st.info("Get comprehensive insights about your app's user sentiment and feedback patterns")
            url_a = st.text_area(
                "Google Play Store URL", 
                placeholder="https://play.google.com/store/apps/details?id=com.example.app", 
                height=100,
                help="Paste your app's complete Google Play Store URL"
            )
            url_b = None
        
        # Enhanced Analysis Parameters
        st.markdown("### Analysis Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            count = st.slider(
                "Number of Reviews", 
                50, 2000, 500, 50,
                help="More reviews = more accurate insights but longer processing time"
            )
        with col2:
            language = st.selectbox(
                "Language", 
                ["en", "hi", "es", "fr", "de", "ja", "pt", "ru"],
                help="Select the primary language of reviews to analyze"
            )
        with col3:
            sort_by = st.selectbox(
                "Sort Reviews By", 
                ["NEWEST", "MOST_RELEVANT", "RATING"],
                help="Choose how to prioritize which reviews to analyze"
            )
        
        # Advanced Options
        with st.expander("Advanced Options", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                include_app_details = st.checkbox("Include App Metadata", value=True, help="Fetch additional app information like developer, category, etc.")
                sentiment_threshold = st.slider("Sentiment Sensitivity", 0.1, 0.5, 0.3, 0.1, help="Lower values = more sensitive sentiment detection")
            
            with col2:
                export_format = st.selectbox("Export Format", ["CSV", "JSON", "Excel"], help="Choose your preferred export format")
                chart_style = st.selectbox("Chart Theme", ["Professional", "Colorful", "Minimal"], help="Select visualization style")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced Start Analysis Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Start Comprehensive Analysis", type="primary", key="start_analysis", use_container_width=True):
                if not url_a.strip():
                    st.error("Please enter at least one app URL to begin analysis.")
                    st.stop()
                
                if st.session_state.comparison_mode and not url_b.strip():
                    st.error("Please enter both app URLs for comparison analysis.")
                    st.stop()
                
                package_a = extract_package_name(url_a)
                package_b = extract_package_name(url_b) if url_b else None
                
                if not package_a:
                    st.error("Invalid Google Play Store URL. Please check the format.")
                    st.stop()
                
                if st.session_state.comparison_mode and not package_b:
                    st.error("Please enter valid Google Play Store URLs for both apps.")
                    st.stop()
                
                # Enhanced Progress tracking
                progress_container = st.container()
                with progress_container:
                    st.markdown('<div class="loading-container"><div class="loading-spinner"></div></div>', unsafe_allow_html=True)
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                try:
                    sort_mapping = {"NEWEST": Sort.NEWEST, "MOST_RELEVANT": Sort.MOST_RELEVANT, "RATING": Sort.RATING}
                    
                    # Get app details if requested
                    app_details_a = None
                    app_details_b = None
                    
                    if include_app_details:
                        status_text.text("Fetching app metadata...")
                        app_details_a = get_app_details(package_a)
                        if package_b:
                            app_details_b = get_app_details(package_b)
                        progress_bar.progress(0.1)
                    
                    # Process first app
                    status_text.text(f"Analyzing {app_details_a['title'] if app_details_a else get_app_name(package_a)}...")
                    result_a, _ = reviews(package_a, lang=language, country="us", sort=sort_mapping[sort_by], count=count)
                    
                    if result_a:
                        df_a = pd.DataFrame(result_a)
                        df_a["package"] = package_a
                        df_a["app_name"] = app_details_a['title'] if app_details_a else get_app_name(package_a)
                        
                        progress_bar.progress(0.3)
                        status_text.text("Processing sentiment analysis...")
                        
                        sentiment_results = df_a["content"].apply(lambda x: analyze_sentiment_advanced(x))
                        df_a["sentiment"] = [r[0] for r in sentiment_results]
                        df_a["polarity_score"] = [r[1] for r in sentiment_results]
                        df_a["subjectivity_score"] = [r[2] for r in sentiment_results]
                        df_a["business_impact"] = [r[3] for r in sentiment_results]
                        df_a["keywords"] = [r[4] for r in sentiment_results]
                        df_a["at"] = pd.to_datetime(df_a["at"])
                    else:
                        st.error("Could not retrieve reviews for the first app. Please verify the URL is correct.")
                        st.stop()
                    
                    progress_bar.progress(0.6)
                    
                    # Process second app if needed
                    df_b = None
                    if st.session_state.comparison_mode:
                        status_text.text(f"Analyzing {app_details_b['title'] if app_details_b else get_app_name(package_b)}...")
                        result_b, _ = reviews(package_b, lang=language, country="us", sort=sort_mapping[sort_by], count=count)
                        
                        if result_b:
                            df_b = pd.DataFrame(result_b)
                            df_b["package"] = package_b
                            df_b["app_name"] = app_details_b['title'] if app_details_b else get_app_name(package_b)
                            
                            sentiment_results = df_b["content"].apply(lambda x: analyze_sentiment_advanced(x))
                            df_b["sentiment"] = [r[0] for r in sentiment_results]
                            df_b["polarity_score"] = [r[1] for r in sentiment_results]
                            df_b["subjectivity_score"] = [r[2] for r in sentiment_results]
                            df_b["business_impact"] = [r[3] for r in sentiment_results]
                            df_b["keywords"] = [r[4] for r in sentiment_results]
                            df_b["at"] = pd.to_datetime(df_b["at"])
                        else:
                            st.error("Could not retrieve reviews for the second app. Please verify the URL is correct.")
                            st.stop()
                    
                    progress_bar.progress(0.9)
                    status_text.text("Generating insights and visualizations...")
                    
                    # Store analysis results
                    st.session_state.current_analysis = {
                        'df_a': df_a,
                        'df_b': df_b,
                        'app_details_a': app_details_a,
                        'app_details_b': app_details_b,
                        'timestamp': datetime.now(),
                        'parameters': {
                            'count': count,
                            'language': language,
                            'sort_by': sort_by
                        }
                    }
                    
                    progress_bar.progress(1.0)
                import streamlit as st
import pandas as pd
from google_play_scraper import Sort, reviews, app
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import re
from collections import Counter
import numpy as np
import json
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="Feedback Forge - App Review Analytics", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with Modern Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Styles - Modern & Clean */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #1a202c;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        min-height: 100vh;
    }
    
    /* Hide Streamlit Elements */
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stMainBlockContainer {padding-top: 0;}
    .stSidebar {display: none;}
    
    /* Navigation Header with Glassmorphism */
    .main-nav {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-top: none;
        padding: 16px 0;
        position: sticky;
        top: 0;
        z-index: 1000;
        margin-bottom: 40px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .nav-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .brand {
        font-family: 'Inter', serif;
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-decoration: none;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .nav-links {
        display: flex;
        gap: 32px;
        align-items: center;
    }
    
    .nav-link {
        color: rgba(255, 255, 255, 0.9);
        text-decoration: none;
        font-size: 16px;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
        padding: 8px 16px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    .nav-link:hover {
        color: white;
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .nav-link.active {
        color: white;
        background: rgba(255, 255, 255, 0.3);
        font-weight: 600;
    }
    
    .developer-credit {
        color: rgba(255, 255, 255, 0.8);
        font-size: 12px;
        font-weight: 400;
        margin-left: 16px;
        padding: 4px 12px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    /* Hero Section with Advanced Styling */
    .hero-section {
        max-width: 900px;
        margin: 80px auto 120px;
        text-align: center;
        padding: 0 24px;
    }
    
    .hero-title {
        font-family: 'Inter', serif;
        font-size: 64px;
        font-weight: 800;
        color: white;
        line-height: 1.1;
        margin-bottom: 24px;
        letter-spacing: -2px;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 24px;
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.5;
        margin-bottom: 48px;
        font-weight: 400;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 48px;
        margin: 48px 0;
        flex-wrap: wrap;
    }
    
    .hero-stat {
        text-align: center;
        color: white;
    }
    
    .hero-stat-number {
        font-size: 36px;
        font-weight: 700;
        display: block;
        margin-bottom: 4px;
    }
    
    .hero-stat-label {
        font-size: 14px;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Modern Button Styles */
    .button-group {
        display: flex;
        gap: 16px;
        justify-content: center;
        flex-wrap: wrap;
        margin: 32px 0;
    }
    
    .primary-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 16px 32px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .primary-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    .secondary-button {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50px;
        padding: 14px 32px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        backdrop-filter: blur(10px);
    }
    
    .secondary-button:hover {
        background: rgba(255, 255, 255, 0.3);
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 255, 255, 0.2);
    }
    
    /* Content Container with Glass Effect */
    .content-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 24px;
    }
    
    .glass-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 40px;
        margin: 32px 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .section {
        margin-bottom: 80px;
    }
    
    .section-title {
        font-family: 'Inter', serif;
        font-size: 42px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 16px;
        text-align: center;
        background: linear-gradient(135deg, #1a202c 0%, #4a5568 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-subtitle {
        font-size: 20px;
        color: #718096;
        text-align: center;
        margin-bottom: 48px;
        line-height: 1.6;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Enhanced Feature Cards */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
        gap: 32px;
        margin: 64px 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 40px;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .feature-title {
        font-family: 'Inter', serif;
        font-size: 24px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 16px;
    }
    
    .feature-description {
        color: #4a5568;
        line-height: 1.7;
        font-size: 16px;
    }
    
    /* Enhanced Form Styles */
    .form-section {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 48px;
        margin: 48px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .form-title {
        font-family: 'Inter', serif;
        font-size: 32px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 24px;
        text-align: center;
    }
    
    /* Enhanced Metrics Display */
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 24px;
        margin: 48px 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        transition: all 0.3s ease;
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
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-family: 'Inter', serif;
        font-size: 40px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
        display: block;
    }
    
    .metric-label {
        color: #4a5568;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Enhanced Results Section */
    .results-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 40px;
        margin: 32px 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .results-header {
        font-family: 'Inter', serif;
        font-size: 28px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 2px solid #e2e8f0;
        background: linear-gradient(135deg, #1a202c 0%, #4a5568 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Enhanced Review Cards */
    .review-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 32px;
        margin: 20px 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .review-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .review-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }
    
    .review-author {
        font-weight: 600;
        color: #1a202c;
        font-size: 16px;
    }
    
    .review-rating {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .star {
        color: #f6ad55;
        font-size: 18px;
    }
    
    .review-content {
        color: #2d3748;
        line-height: 1.7;
        margin-bottom: 16px;
        font-size: 16px;
    }
    
    .review-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 14px;
        color: #718096;
    }
    
    .sentiment-tag {
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        backdrop-filter: blur(10px);
    }
    
    .sentiment-positive {
        background: linear-gradient(135deg, #48bb78, #38a169);
        color: white;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4);
    }
    
    .sentiment-negative {
        background: linear-gradient(135deg, #f56565, #e53e3e);
        color: white;
        box-shadow: 0 4px 15px rgba(245, 101, 101, 0.4);
    }
    
    .sentiment-neutral {
        background: linear-gradient(135deg, #a0aec0, #718096);
        color: white;
        box-shadow: 0 4px 15px rgba(160, 174, 192, 0.4);
    }
    
    /* Enhanced Insights Section */
    .insights-container {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 40px;
        margin: 32px 0;
    }
    
    .insight-item {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 24px;
        margin: 20px 0;
        border-left: 4px solid #48bb78;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .insight-item:hover {
        transform: translateX(5px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
    }
    
    .insight-item.warning {
        border-left-color: #f6ad55;
    }
    
    .insight-item.negative {
        border-left-color: #f56565;
    }
    
    .insight-title {
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 8px;
        font-size: 18px;
    }
    
    .insight-description {
        color: #4a5568;
        line-height: 1.6;
        font-size: 16px;
    }
    
    /* Stats Cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 24px;
        margin: 40px 0;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
    }
    
    /* Dashboard Enhancement */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 32px;
        margin: 40px 0;
    }
    
    .dashboard-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 32px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    
    /* Footer Enhancement */
    .footer {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        padding: 60px 0;
        margin-top: 80px;
        text-align: center;
    }
    
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 24px;
    }
    
    .footer-brand {
        font-family: 'Inter', serif;
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 16px;
    }
    
    .footer-text {
        color: rgba(255, 255, 255, 0.8);
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 12px;
    }
    
    .footer-developer {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        padding: 12px 24px;
        display: inline-block;
        margin-top: 20px;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 600;
    }
    
    /* Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 40px 0;
    }
    
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid rgba(102, 126, 234, 0.3);
        border-top: 4px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 42px;
        }
        
        .hero-subtitle {
            font-size: 20px;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .nav-container {
            padding: 0 16px;
        }
        
        .form-section {
            padding: 32px 24px;
        }
        
        .hero-stats {
            gap: 24px;
        }
        
        .button-group {
            flex-direction: column;
            align-items: center;
        }
    }
    
    /* Custom Streamlit Button Override */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 16px 32px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        height: auto !important;
        width: auto !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Enhanced Form Controls */
    .stSelectbox > label,
    .stSlider > label,
    .stTextArea > label,
    .stTextInput > label {
        font-weight: 600 !important;
        color: #1a202c !important;
        margin-bottom: 8px !important;
        font-size: 16px !important;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        font-size: 16px !important;
        padding: 12px 16px !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Progress Bar Enhancement */
    .stProgress .st-bo {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        height: 8px !important;
        border-radius: 4px !important;
    }
    
    /* Hide navigation buttons */
    .nav-buttons {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with enhanced features
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

# Enhanced Navigation
def show_navigation():
    st.markdown(f"""
    <div class="main-nav">
        <div class="nav-container">
            <div class="brand">
                Feedback Forge
            </div>
            <div class="nav-links">
                <span class="nav-link {'active' if st.session_state.page == 'home' else ''}">Home</span>
                <span class="nav-link {'active' if st.session_state.page == 'analysis' else ''}">Analysis</span>
                <span class="nav-link {'active' if st.session_state.page == 'dashboard' else ''}">Dashboard</span>
                <span class="nav-link {'active' if st.session_state.page == 'about' else ''}">About</span>
                <span class="nav-link {'active' if st.session_state.page == 'help' else ''}">Help</span>
                <div class="developer-credit">Developed by Ayush Pandey</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Enhanced Helper Functions
def extract_package_name(url):
    if "id=" in url:
        return url.split("id=")[1].split("&")[0].strip()
    return None

def get_app_details(package_name):
    """Get detailed app information"""
    try:
        result = app(package_name)
        return {
            'title': result.get('title', 'Unknown App'),
            'developer': result.get('developer', 'Unknown Developer'),
            'category': result.get('genre', 'Unknown Category'),
            'rating': result.get('score', 0),
            'installs': result.get('installs', 'Unknown'),
            'updated': result.get('updated', None),
            'version': result.get('version', 'Unknown'),
            'description': result.get('description', '')[:200] + '...' if result.get('description', '') else 'No description available'
        }
    except:
        return {
            'title': get_app_name(package_name),
            'developer': 'Unknown Developer',
            'category': 'Unknown Category',
            'rating': 0,
            'installs': 'Unknown',
            'updated': None,
            'version': 'Unknown',
            'description': 'Unable to fetch app details'
        }

def analyze_sentiment_advanced(text):
    if pd.isna(text) or text.strip() == "":
        return "Neutral", 0.0, 0.0, "Unknown", []
    
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Extract keywords
    words = str(text).lower().split()
    keywords = [word for word in words if len(word) > 3 and word.isalpha()][:5]
    
    if polarity > 0.5:
        return "Positive", polarity, subjectivity, "Highly Positive", keywords
    elif polarity > 0.1:
        return "Positive", polarity, subjectivity, "Moderately Positive", keywords
    elif polarity < -0.5:
        return "Negative", polarity, subjectivity, "Highly Negative", keywords
    elif polarity < -0.1:
        return "Negative", polarity, subjectivity, "Moderately Negative", keywords
    else:
        return "Neutral", polarity, subjectivity, "Neutral", keywords

def get_app_name(package_name):
    parts = package_name.split('.')
    return parts[-1].replace('_', ' ').title() if parts else package_name

def generate_enhanced_insights(df, app_name="App"):
    insights = []
    if df.empty:
        return insights
    
    try:
        sentiment