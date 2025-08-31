import streamlit as st
import json
from sentiment_llm import SentimentAnalyzer
import time
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Movie Review Sentiment Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for professional styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        font-size: 3rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-size: 1.1rem !important;
        color: #64748b;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Input Styles */
    .stTextArea > div > div > textarea {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 20px !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Result Card Styles */
    .result-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 32px;
        margin: 24px 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    
    /* Evidence Styles */
    .evidence-chip {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        padding: 10px 16px;
        margin: 6px 3px;
        display: inline-block;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .evidence-chip:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar Styles */
    .sidebar-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .sidebar-content {
        font-size: 0.9rem;
        line-height: 1.6;
        color: #374151;
    }
    
    .sidebar-content ul {
        margin: 8px 0;
        padding-left: 20px;
    }
    
    .sidebar-content li {
        margin: 6px 0;
    }
    
    .sidebar-content strong {
        color: #1f2937;
        font-weight: 600;
    }
    
    /* History Styles */
    .history-item {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        border-left: 3px solid #667eea;
        transition: all 0.2s ease;
    }
    
    .history-item:hover {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transform: translateX(2px);
    }
    
    .history-sentiment {
        font-size: 0.8rem;
        color: #6b7280;
        margin-bottom: 4px;
        font-weight: 500;
    }
    
    .history-preview {
        font-size: 0.85rem;
        color: #374151;
    }
    
    /* Metrics */
    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 8px;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid #e2e8f0;
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem !important;
        }
        
        .result-card {
            padding: 20px;
            margin: 16px 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Initialize analyzer
@st.cache_resource
def get_analyzer():
    """Initialize and cache the sentiment analyzer"""
    return SentimentAnalyzer()

def create_confidence_chart(confidence, label):
    """Create a beautiful confidence visualization"""
    colors = {
        "Positive": "#10b981",
        "Negative": "#ef4444", 
        "Neutral": "#f59e0b"
    }
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = confidence,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Confidence Level"},
        gauge = {
            'axis': {'range': [None, 1]},
            'bar': {'color': colors.get(label, "#667eea")},
            'steps': [
                {'range': [0, 0.5], 'color': "lightgray"},
                {'range': [0.5, 1], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0.9
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def display_sentiment_result(result):
    """Display sentiment analysis results with enhanced visualization"""
    label = result["label"]
    confidence = result["confidence"]
    explanation = result["explanation"]
    evidence_phrases = result.get("evidence_phrases", [])
    
    # Define sentiment configurations
    sentiment_config = {
        "Positive": {"color": "#10b981", "icon": "✅"},
        "Negative": {"color": "#ef4444", "icon": "❌"},
        "Neutral": {"color": "#f59e0b", "icon": "⚪"}
    }
    
    config = sentiment_config.get(label, sentiment_config["Neutral"])
    
    # Main results container
    with st.container():
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        
        # Results header with two columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Use Streamlit native components for better reliability
            st.markdown(f"## {config['icon']} {label} Sentiment")
            
            # Confidence display using Streamlit's metric
            st.metric(
                label="Confidence Score",
                value=f"{confidence:.1%}",
                delta=None
            )
            
            # Visual progress bar
            st.progress(confidence)
            
            # Color-coded message based on sentiment
            if label == "Positive":
                st.success(f"✨ Strong positive sentiment detected with {confidence:.1%} confidence!")
            elif label == "Negative":
                st.error(f"⚠️ Strong negative sentiment detected with {confidence:.1%} confidence!")
            else:
                st.warning(f"🔍 Neutral sentiment detected with {confidence:.1%} confidence!")
        
        with col2:
            # Confidence gauge chart
            if confidence > 0:
                fig = create_confidence_chart(confidence, label)
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Explanation section
    st.markdown("### 📝 Analysis Explanation")
    st.info(f"💡 {explanation}")
    
    # Evidence phrases
    if evidence_phrases:
        st.markdown("### 🔍 Key Evidence Phrases")
        st.markdown("*The following phrases were identified as strong sentiment indicators:*")
        
        # Display evidence chips
        evidence_html = "".join([
            f'<span class="evidence-chip">📌 {phrase}</span>'
            for phrase in evidence_phrases
        ])
        
        st.markdown(f"""
        <div style="margin: 20px 0;">
            {evidence_html}
        </div>
        """, unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{confidence:.1%}</div>
            <div class="metric-label">Confidence</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(evidence_phrases)}</div>
            <div class="metric-label">Key Phrases</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        word_count = len(result.get("original_text", "").split()) if "original_text" in result else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{word_count}</div>
            <div class="metric-label">Words Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Raw JSON (collapsible)
    with st.expander("📊 Raw JSON Output", expanded=False):
        st.json(result)

def display_analysis_history():
    """Display recent analysis history"""
    if st.session_state.analysis_history:
        st.markdown("""
        <div class="sidebar-card">
            <div class="sidebar-title">📈 Recent Analyses</div>
        """, unsafe_allow_html=True)
        
        for i, analysis in enumerate(reversed(st.session_state.analysis_history[-5:])):
            preview = analysis['text'][:50] + "..." if len(analysis['text']) > 50 else analysis['text']
            sentiment = analysis['result']['label']
            confidence = analysis['result']['confidence']
            
            st.markdown(f"""
            <div class="history-item">
                <div class="history-sentiment">
                    {sentiment} ({confidence:.1%})
                </div>
                <div class="history-preview">
                    "{preview}"
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Sidebar with enhanced styling
    with st.sidebar:
        # How it works section
        st.markdown("""
        <div class="sidebar-card">
            <div class="sidebar-title">ℹ️ How It Works</div>
            <div class="sidebar-content">
                <ol>
                    <li>Enter your movie review text</li>
                    <li>Click 'Analyze Sentiment'</li>
                    <li>Get comprehensive analysis with:
                        <ul>
                            <li><strong>Sentiment classification</strong></li>
                            <li><strong>Confidence score</strong></li>
                            <li><strong>Detailed explanation</strong></li>
                            <li><strong>Key evidence phrases</strong></li>
                        </ul>
                    </li>
                </ol>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tips section
        st.markdown("""
        <div class="sidebar-card">
            <div class="sidebar-title">💡 Pro Tips</div>
            <div class="sidebar-content">
                <ul>
                    <li><strong>Be detailed:</strong> Longer reviews provide more context</li>
                    <li><strong>Include specifics:</strong> Mention acting, plot, direction</li>
                    <li><strong>Use natural language:</strong> Write as you normally would</li>
                    <li><strong>Multiple aspects:</strong> Discuss different movie elements</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Analysis history
        display_analysis_history()
        
        # Clear history button
        if st.session_state.analysis_history:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.analysis_history = []
                st.rerun()
    
    # Main content
    # Header section
    st.markdown('<h1 class="main-header">🎬 Movie Review Sentiment Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by Advanced AI • Get instant, detailed sentiment analysis for movie reviews</p>', unsafe_allow_html=True)
    
    # Input section
    st.markdown("### 📝 Enter Your Movie Review")
    
    # Sample reviews for quick testing
    sample_reviews = {
        "Select a sample review...": "",
        "Positive Review": "This movie was absolutely fantastic! The cinematography was breathtaking, and the performances were outstanding. Every scene kept me on the edge of my seat, and the emotional depth of the characters was truly remarkable. I would definitely watch it again and recommend it to everyone.",
        "Negative Review": "What a disappointing waste of time. The plot was confusing and poorly executed, the acting felt forced and unnatural, and the special effects looked cheap. I couldn't wait for it to end and regretted spending money on this terrible film.",
        "Mixed Review": "The movie had some good moments with decent special effects and a few laughs, but overall it felt average. The story was predictable and some of the acting was questionable. It's not bad enough to hate, but not good enough to love either."
    }
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        selected_sample = st.selectbox("Quick Test:", list(sample_reviews.keys()))
    
    review_text = st.text_area(
        "",
        value=sample_reviews[selected_sample],
        height=200,
        placeholder="Paste your movie review here...\n\nExample: 'This movie was absolutely fantastic! The acting was superb and the storyline kept me engaged throughout. The cinematography was breathtaking and the soundtrack perfectly complemented each scene...'",
        help="Enter the movie review text you want to analyze. Longer, more detailed reviews typically provide better analysis results."
    )
    
    # Character count and validation
    char_count = len(review_text)
    word_count = len(review_text.split()) if review_text else 0
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if char_count > 0:
            if char_count < 50:
                st.warning(f"⚠️ Short text ({char_count} characters, {word_count} words). Consider adding more detail for better analysis.")
            else:
                st.success(f"✅ Good length ({char_count} characters, {word_count} words)")
        else:
            st.info("💡 Enter your movie review above to get started")
    
    with col2:
        st.metric("Characters", char_count)
    
    with col3:
        st.metric("Words", word_count)
    
    # Analysis button
    analyze_clicked = st.button(
        "🚀 Analyze Sentiment", 
        type="primary", 
        use_container_width=True,
        disabled=not review_text.strip() or char_count < 10
    )
    
    # Analysis logic
    if analyze_clicked and review_text.strip():
        with st.spinner("🔍 Analyzing your review... This may take a few seconds"):
            try:
                analyzer = get_analyzer()
                
                # Add original text to result for metrics
                result = analyzer.analyze_sentiment(review_text)
                result["original_text"] = review_text
                
                # Store in history
                st.session_state.analysis_history.append({
                    'text': review_text,
                    'result': result,
                    'timestamp': time.time()
                })
                
                # Add a small delay for better UX
                time.sleep(0.5)
                
                # Display results
                st.markdown("---")
                st.markdown("## 📊 Analysis Results")
                display_sentiment_result(result)
                
                # Success message
                st.success("✅ Analysis completed successfully!")
                
            except Exception as e:
                st.error(f"❌ Error analyzing sentiment: {str(e)}")
                st.info("💡 Please try again or check your API configuration. If the problem persists, try with a different review text.")
                
                # Show error details in expander
                with st.expander("🔧 Error Details", expanded=False):
                    st.code(str(e))
    
    elif not review_text.strip() and analyze_clicked:
        st.warning("⚠️ Please enter a movie review to analyze")
    
    elif char_count < 10 and char_count > 0:
        st.warning("⚠️ Please enter a longer review (at least 10 characters)")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <div style="margin-bottom: 16px;">
            <strong>🎬 Movie Review Sentiment Analyzer</strong>
        </div>
        <p>Built with ❤️ using Streamlit and Google Gemini AI</p>
        
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()