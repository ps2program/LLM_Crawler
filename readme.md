### **🚀 Hosting Flask + Streamlit on Render (Step-by-Step Guide)**  

You'll need to deploy **both the Flask backend** and the **Streamlit frontend** separately on Render.  

---

## **🛠️ 1️⃣ Set Up the Flask API (Backend) on Render**  

### **🔹 Step 1: Prepare Your Code**  
Ensure your Flask app (`app.py`) and a `requirements.txt` file exist.  

### **📜 `requirements.txt` (Backend)**  
```txt
flask
requests
bs4
playwright
openai
celery
redis
```
*(Add any other required packages.)*  

---

### **🔹 Step 2: Deploy Flask on Render**
1. Push your **Flask app** to **GitHub**.  
2. Go to **[Render](https://render.com/)** → Click **New Web Service**.  
3. Connect your **GitHub repository**.  
4. Set the following configurations:
   - **Runtime:** `Python`
   - **Build Command:**  
     ```bash
     pip install -r requirements.txt
     playwright install
     ```
   - **Start Command:**  
     ```bash
     gunicorn app:app --bind 0.0.0.0:8000
     ```
   - **Instance Type:** Free or Paid (Free tier works but may sleep).  
5. Click **"Deploy"**.  

🔗 Your API will be available at `https://your-flask-app.onrender.com`.

---

## **🖥️ 2️⃣ Set Up the Streamlit UI (Frontend) on Render**  

### **🔹 Step 1: Prepare Your Streamlit Code**
Modify `steamlit_ui.py` to point to the **Flask API on Render** instead of localhost.  

### **📜 `steamlit_ui.py` (Updated)**
```python
import streamlit as st
import requests

# Streamlit UI
st.title("LLM-Powered Web Crawler")
st.write("Enter a query to fetch, scrape, and summarize relevant web pages.")

query = st.text_input("Search Query")
if st.button("Search") and query:
    with st.spinner("Fetching and processing data..."):
        # Change URL to your Render Flask API
        API_URL = "https://your-flask-app.onrender.com/search"
        response = requests.get(API_URL, params={"query": query})
        if response.status_code == 200:
            results = response.json()["results"]
            st.subheader("Results:")
            for result in results:
                st.markdown(f"### [{result['url']}]({result['url']})")
                st.write(result["summary"])
        else:
            st.error("Failed to fetch results. Please try again.")
```

---

### **🔹 Step 2: Deploy Streamlit on Render**
1. Push **`steamlit_ui.py`** and a **`requirements.txt`** to a **separate GitHub repo**.  
2. Create a new **Web Service** on Render.  
3. Connect the **GitHub repository**.  
4. Set the following configurations:
   - **Runtime:** `Python`
   - **Build Command:**  
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**  
     ```bash
     streamlit run steamlit_ui.py --server.port 8501 --server.address 0.0.0.0
     ```
5. Click **"Deploy"**.

🔗 Your Streamlit UI will be available at `https://your-streamlit-app.onrender.com`.  

---

## **✅ Final Check**
- Visit your **Streamlit URL** → Enter a search query.  
- It should **fetch data from your Flask API** on Render.  

🎉 **Done! Your Flask & Streamlit apps are now live on Render!** 🚀  

Let me know if you hit any issues!