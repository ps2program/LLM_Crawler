import streamlit as st
import requests

# Flask API URLs
SEARCH_API_URL = "https://llm-crawler-wv6a.onrender.com/search"
WARMUP_API_URL = "https://llm-crawler-wv6a.onrender.com/warmup"

# 🔥 Ping the warm-up endpoint on app startup
@st.cache_data
def warm_up_flask():
    try:
        response = requests.get(WARMUP_API_URL)
        if response.status_code == 200:
            st.session_state["flask_warmup"] = "✅ API is warm and ready!"
        else:
            st.session_state["flask_warmup"] = "⚠️ API might be slow due to cold start."
    except requests.exceptions.RequestException:
        st.session_state["flask_warmup"] = "❌ API is unreachable."

# Run the warm-up function when the app starts
warm_up_flask()

# Streamlit UI
st.title("LLM-Powered Web Crawler")
st.write("Enter a query to fetch, scrape, and summarize relevant web pages.")

# Show API warm-up status
st.info(st.session_state.get("flask_warmup", "Checking API status..."))

# User input
query = st.text_input("Search Query")
if st.button("Search") and query:
    with st.spinner("Fetching and processing data..."):
        response = requests.get(SEARCH_API_URL, params={"query": query})
        if response.status_code == 200:
            results = response.json()["results"]
            st.subheader("Results:")
            for result in results:
                st.markdown(f"### [{result['url']}]({result['url']})")
                st.write(result["summary"])
        else:
            st.error("Failed to fetch results. Please try again.")
