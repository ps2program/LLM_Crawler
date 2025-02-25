import streamlit as st
import requests
import json  # ✅ Import JSON for safe parsing

# Set page title and favicon
st.set_page_config(page_title="Generative Search", page_icon="🔍")

# API_URL = "http://127.0.0.1:8000/search"
API_URL = "https://llm-crawler-wv6a.onrender.com/search"

st.title("Generative Search")
st.write("Enter a query to fetch, scrape, and summarize relevant web pages.")

query = st.text_input("Search Query")
if st.button("Search") and query:
    st.subheader("Results:")
    response = requests.get(API_URL, params={"query": query}, stream=True)
    
    result_placeholder = st.empty()
    result_text = ""

    for line in response.iter_lines():
        if line:
            try:
                data = line.decode("utf-8").replace("data: ", "").strip()
                json_data = json.loads(data)  # ✅ Safe JSON parsing

                if "url" in json_data:
                    result_text += f"\n### [{json_data['url']}]({json_data['url']})\n"
                if "summary" in json_data and json_data["summary"]:  # ✅ Check if summary is valid
                    result_text += json_data["summary"] + " "
                
                result_placeholder.markdown(result_text)
            except json.JSONDecodeError as e:
                st.error(f"Error processing response: {e}")
