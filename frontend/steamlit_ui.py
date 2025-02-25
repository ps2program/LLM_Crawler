import streamlit as st
import requests

# Flask API URLs
SEARCH_API_URL = "https://llm-crawler-wv6a.onrender.com/search"
WARMUP_API_URL = "https://llm-crawler-wv6a.onrender.com/warmup"

# 🔥 Check if the warm-up status is already stored in the query parameters
query_params = st.query_params
warmup_status = query_params.get("warmup", "Checking API status...")

# 🔥 Ping the warm-up endpoint only if not already warmed up
@st.cache_data
def warm_up_flask():
    global warmup_status
    if warmup_status == "✅ API is warm and ready!":
        return  # Don't ping if already warm

    try:
        response = requests.get(WARMUP_API_URL)
        if response.status_code == 200:
            warmup_status = "✅ API is warm and ready!"
        else:
            warmup_status = "⚠️ API might be slow due to cold start."
    except requests.exceptions.RequestException:
        warmup_status = "❌ API is unreachable."

    # Store warm-up status in URL query parameters
    st.query_params["warmup"] = warmup_status

# Run the warm-up function on app start
warm_up_flask()

# Streamlit UI
st.title("LLM-Powered Web Crawler")
st.write("Enter a query to fetch, scrape, and summarize relevant web pages.")

# Show API warm-up status (persistent even after refresh)
st.info(warmup_status)

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
