
import streamlit as st
import requests

# Streamlit UI
st.title("LLM-Powered Web Crawler")
st.write("Enter a query to fetch, scrape, and summarize relevant web pages.")

query = st.text_input("Search Query")
if st.button("Search") and query:
    with st.spinner("Fetching and processing data..."):
        # Change URL to your Render Flask API
        API_URL = "https://llm-crawler-wv6a.onrender.com/search"
        response = requests.get(API_URL, params={"query": query})
        if response.status_code == 200:
            results = response.json()["results"]
            st.subheader("Results:")
            for result in results:
                st.markdown(f"### [{result['url']}]({result['url']})")
                st.write(result["summary"])
        else:
            st.error("Failed to fetch results. Please try again.")
