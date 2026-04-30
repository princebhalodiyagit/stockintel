
import requests
import xml.etree.ElementTree as ET
import json
import os
import time
from datetime import datetime

def get_company_news(company_name, ticker, base_path="/content/drive/MyDrive/stockintel", max_articles=20):
    os.makedirs(f"{base_path}/data/news", exist_ok=True)
    print(f"\nFetching news for: {company_name}")
    query = company_name.replace(" ", "+") + "+NSE+stock"
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        root = ET.fromstring(response.content)
        articles = []
        for item in root.findall(".//item")[:max_articles]:
            articles.append({
                "title":       item.findtext("title", "N/A"),
                "link":        item.findtext("link", "N/A"),
                "published":   item.findtext("pubDate", "N/A"),
                "source":      item.findtext("source", "N/A"),
                "description": item.findtext("description", "N/A"),
            })
        print(f"  Found {len(articles)} articles")
        data = {
            "company": company_name, "ticker": ticker,
            "collected_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "articles": articles
        }
        with open(f"{base_path}/data/news/{ticker}_news.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Saved!")
        return articles
    except Exception as e:
        print(f"  Error: {e}")
        return []

def collect_news_for_all(companies, base_path="/content/drive/MyDrive/stockintel"):
    for company in companies:
        get_company_news(company["name"], company["ticker"], base_path)
        time.sleep(2)
    print("\nAll news collected!")
