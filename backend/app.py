from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from openai import OpenAI
import asyncio
import json

app = Flask(__name__)

# Initialize OpenAI client (Local LM Studio)
client = OpenAI(base_url="https://major-legible-walrus.ngrok-free.app/v1", api_key="lm-studio")

def fetch_urls(query):
    """Fetch relevant URLs using Tavily API."""
    url = "https://api.tavily.com/search"
    payload = {
        "query": query,
        "topic": "general",
        "search_depth": "basic",
        "max_results": 5
    }
    headers = {
        "Authorization": "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",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("results", [])

async def scrape_content(url):
    """Scrape content from a given URL asynchronously using Playwright."""
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
    """Stream summarization using Local LLM."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize the following article:"},
            {"role": "user", "content": text},
        ],
        stream=True  # Enable streaming
    )
    for chunk in response:
        yield json.dumps({"summary": chunk.choices[0].delta.content}) + "\n"

@app.route("/search", methods=["GET"])
def search():
    """Streaming search results: Fetch URLs, scrape content, summarize progressively."""
    query = request.args.get("query")
    if not query:
        return Response("Query parameter is required", status=400)

    urls = fetch_urls(query)

    def stream_results():
        """Generator function to stream results as they are ready."""
        for url_data in urls:
            try:
                url = url_data["url"]
                content = url_data["content"]  # Placeholder: use real scraping if needed

                yield f"data: {json.dumps({'url': url, 'status': 'scraped'})}\n\n"
                
                summary_stream = summarize_content(content)
                for chunk in summary_stream:
                    yield f"data: {chunk}\n\n"  # SSE format
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(stream_results(), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
