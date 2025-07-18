import streamlit as st
import pandas as pd
import json
import shopsage_core as ss

# Page configuration
st.set_page_config(
    page_title="ShopSage - Smart Shopping Recommendations",
    page_icon="🛒",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .ranking-table {
        margin-top: 1rem;
    }
    .source-card {
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🛒 ShopSage – Ask & Decide")
st.markdown("""
Welcome to ShopSage! Your AI-powered shopping assistant that helps you make informed purchase decisions.

**How it works:**
- Ask any shopping question (e.g., "best headphones under $500")
- Compare products (e.g., "iPhone 15 Pro vs Pixel 8 Pro")
- Get AI-powered recommendations backed by real product data
""")

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Main input section
col1, col2 = st.columns([4, 1])
with col1:
    question = st.text_input(
        "Your shopping question",
        placeholder="e.g., 'best laptop under $1000' or 'Sony XM5 vs Apple AirPods Max'"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button("Get recommendation", type="primary", use_container_width=True)

# Sidebar with search history
with st.sidebar:
    st.header("⚙️ Settings")
    st.info("Using OpenAI GPT-4o-mini for AI analysis")
    
    st.markdown("---")
    st.header("📝 Recent Searches")
    if st.session_state.search_history:
        for i, item in enumerate(reversed(st.session_state.search_history[-5:])):
            if st.button(item["query"], key=f"history_{i}"):
                question = item["query"]
                search_button = True

# Process search
if search_button and question:
    with st.spinner("🔍 Searching for products and analyzing..."):
        try:
            # Create ShopSage instance
            sage = ss.ShopSage()
            result = sage.run_pipeline(question)
            
            # Add to search history
            st.session_state.search_history.append({
                "query": question,
                "result": result
            })
            
            # Display results
            st.markdown("---")
            
            # Winner section
            st.header("🏆 Verdict")
            st.success(f"**{result['winner']}**")
            
            # Reasoning section
            st.header("💡 Reasoning")
            for reason in result['reasons']:
                st.markdown(f"- {reason}")
            
            # Ranking section
            if result['ranking']:
                st.header("📊 Ranking")
                ranking_df = pd.DataFrame({
                    "Rank": range(1, len(result['ranking']) + 1),
                    "Product": result['ranking']
                })
                st.table(ranking_df)
            
            # Sources section
            with st.expander("📚 Sources", expanded=False):
                for i, source in enumerate(result['sources']):
                    st.markdown(f"### {i+1}. [{source['title']}]({source['url']})")
                    st.markdown(f"**Summary:** {source.get('summary', 'N/A')}")
                    st.markdown(f"**Snippet:** {source['snippet'][:200]}...")
                    st.markdown("---")
            
            # Download results
            col1, col2 = st.columns(2)
            with col1:
                json_str = json.dumps(result, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str.encode(),
                    file_name=f"shopsage_result_{question[:20].replace(' ', '_')}.json",
                    mime="application/json"
                )
            
            with col2:
                # Create a formatted text report
                report = f"""ShopSage Shopping Recommendation Report
=====================================

Query: {result['query']}

Winner: {result['winner']}

Reasoning:
{chr(10).join(f'- {r}' for r in result['reasons'])}

Product Ranking:
{chr(10).join(f'{i+1}. {p}' for i, p in enumerate(result['ranking']))}

Sources:
{chr(10).join(f'- {s["title"]}: {s["url"]}' for s in result['sources'])}
"""
                st.download_button(
                    label="📄 Download Report",
                    data=report.encode(),
                    file_name=f"shopsage_report_{question[:20].replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please check your API keys in the .env file")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Powered by Tavily Search API and AI | Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)