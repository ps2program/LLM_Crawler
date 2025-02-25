
import streamlit as st
import requests

# Streamlit UI
st.title("LLM-Powered Web Crawler")
st.write("Enter a query to fetch, scrape, and summarize relevant web pages.")

query = st.text_input("Search Query")
if st.button("Search") and query:
    with st.spinner("Fetching and processing data..."):
        response = requests.get("http://localhost:8000/search", params={"query": query})
        if response.status_code == 200:
            results = response.json()["results"]
            st.subheader("Results:")
            for result in results:
                st.markdown(f"### [{result['url']}]({result['url']})")
                st.write(result["summary"])
        else:
            st.error("Failed to fetch results. Please try again.")

# streamlit run steamlit_ui.py
