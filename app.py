"""
Streamlit Web Interface for Professional RAG System
David's RAG System - Web Interface

Beautiful, interactive web interface for the RAG system
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from pathlib import Path
import sys
import os

# Add the current directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from rag_agent import RAGAgent
    from document_processor import DocumentProcessor
    from chunking_engine import ChunkingEngine
    from embedding_generator import EmbeddingGenerator
except ImportError:
    st.error("⚠️ RAG system modules not found. Make sure you're running from the correct directory.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="🚀 David's Professional RAG System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    .user-message {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .source-citation {
        background: #fff3e0;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        font-size: 0.9em;
        border-left: 3px solid #ff9800;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'rag_agent' not in st.session_state:
    st.session_state.rag_agent = None
if 'system_stats' not in st.session_state:
    st.session_state.system_stats = {
        'total_queries': 0,
        'avg_response_time': 0,
        'avg_confidence': 0,
        'documents_processed': 0
    }

def initialize_rag_system():
    """Initialize the RAG system components"""
    try:
        with st.spinner("🚀 Initializing RAG System..."):
            agent = RAGAgent()
            st.session_state.rag_agent = agent
            
            # Check for existing collections
            collections = agent.vector_store.list_collections()
            st.session_state.available_collections = [col.name for col in collections]
            
            if collections:
                st.success(f"✅ RAG System initialized! Found {len(collections)} collection(s)")
                return True
            else:
                st.warning("⚠️ No document collections found. Please process some documents first.")
                return False
    except Exception as e:
        st.error(f"❌ Error initializing RAG system: {str(e)}")
        return False

def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 David's Professional RAG System</h1>
        <p>Complete Retrieval-Augmented Generation with Scientific Evaluation</p>
        <p><em>From Zero to RAG Master - Now with Beautiful Web Interface!</em></p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application"""
    render_header()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Dashboard", "ℹ️ About"])
    
    with tab1:
        st.header("💬 Chat with Your Documents")
        st.info("🚀 Complete implementation available in local version!")
    
    with tab2:
        st.header("📊 Performance Dashboard")
        st.info("📈 Real-time analytics available in local version!")
    
    with tab3:
        st.header("ℹ️ About This System")
        
        st.markdown("""
        ### 🚀 David's Professional RAG System
        
        This is a **complete, production-ready RAG (Retrieval-Augmented Generation) system** 
        with scientific evaluation and multiple strategies.
        
        #### ✨ Features:
        - **Multiple Chunking Strategies**: Recursive, Token-based, Semantic
        - **Scientific Evaluation**: LLM-as-Judge, performance metrics
        - **Advanced Techniques**: HyDE, adaptive retrieval
        - **Interactive Chat**: Real-time document Q&A
        - **Performance Dashboard**: Comprehensive analytics
        
        #### 🛠️ Technology Stack:
        - **Backend**: Python, LangChain, ChromaDB
        - **Frontend**: Streamlit
        - **LLM Providers**: OpenAI, Gemini
        - **Evaluation**: Automated metrics
        
        #### 🏆 Created by:
        **David De Cunto** - RAG Systems Specialist
        - Profile: ENFP-A, High IQ + ADHD (2e)
        - Expertise: AI, Psychology, Music, Digital Marketing
        - Achievement: Zero to RAG Master in one session!
        
        #### 📚 Learn More:
        - [GitHub Repository](https://github.com/Froggerr10/professional-rag-system)
        - [Standard Operating Procedure](https://github.com/Froggerr10/professional-rag-system/blob/main/POP.md)
        
        #### 🚀 Get Started:
        ```bash
        git clone https://github.com/Froggerr10/professional-rag-system.git
        cd professional-rag-system
        python setup.py
        python start_web.py
        ```
        """)
        
        st.balloons()

if __name__ == "__main__":
    main()