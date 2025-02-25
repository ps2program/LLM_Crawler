from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from openai import OpenAI
import asyncio
from celery import Celery

# Initialize Flask app
app = Flask(__name__)

# Celery configuration (for async crawling)
celery = Celery("tasks", broker="redis://localhost:6379/0")

# Initialize OpenAI client (Local LM Studio)
client = OpenAI(base_url="https://major-legible-walrus.ngrok-free.app/v1", api_key="lm-studio")

def fetch_urls(query):
    """Fetch relevant URLs using Tavily API"""
    url = "https://api.tavily.com/search"
    payload = {
        "query": query,
        "topic": "general",
        "search_depth": "basic",
        "max_results": 5,
        "time_range": None,
        "days": 3,
        "include_answer": True,
        "include_raw_content": False,
        "include_images": False,
        "include_image_descriptions": False,
        "include_domains": [],
        "exclude_domains": []
    }
    headers = {
        "Authorization": "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",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("results", [])

@celery.task
def scrape_content(url):
    """Scrape content from a given URL asynchronously."""
    return asyncio.run(scrape_content_async(url))

async def scrape_content_async(url):
    """Async scraping function using Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=15000)
        content = await page.content()
        await browser.close()
    soup = BeautifulSoup(content, "html.parser")
    paragraphs = soup.find_all("p")
    return " ".join([p.text for p in paragraphs[:5]])  # Extract first 5 paragraphs

def summarize_content(text):
    """Summarize extracted content using local LLM."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize the following article:"},
            {"role": "user", "content": text},
        ]
    )
    return response.choices[0].message.content

@app.route("/search", methods=["GET"])
def search():
    """Handle search requests: Fetch URLs, scrape, and summarize."""
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    urls = fetch_urls(query)
    results = []
    
    for url_data in urls:
        try:
            url = url_data["url"]
            content = scrape_content(url)
            summary = summarize_content(content)
            results.append({"url": url, "summary": summary})
        except Exception as e:
            results.append({"url": url, "summary": f"Error: {str(e)}"})
    
    return jsonify({"query": query, "results": results})
# @app.route("/search", methods=["GET"])
# def search():
#     """Handle search requests: Fetch URLs, scrape content, combine with provided data, and summarize."""
#     query = request.args.get("query")
#     if not query:
#         return jsonify({"error": "Query parameter is required"}), 400
    
#     urls = fetch_urls(query)
#     results = []
    
#     for url_data in urls:
#         try:
#             url = url_data["url"]
#             provided_content = url_data["url"] # Get Tavily's content if available

#             # Scrape content from the webpage
#             scraped_content = scrape_content(url)

#             # Combine both sources
#             full_content = f"{provided_content}\n\n{scraped_content}".strip()

#             # Summarize the combined content
#             summary = summarize_content(full_content)
#             results.append({"url": url, "summary": summary})
#         except Exception as e:
#             results.append({"url": url, "summary": f"Error: {str(e)}"})

#     return jsonify({"query": query, "results": results})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
