import yfinance as yf
import requests
import xml.etree.ElementTree as ET
import json, os, time
from datetime import datetime

os.makedirs("data/financials", exist_ok=True)
os.makedirs("data/news", exist_ok=True)

COMPANIES = [
    {"name": "Reliance Industries",        "ticker": "RELIANCE",   "yf": "RELIANCE.NS"},
    {"name": "Tata Consultancy Services",  "ticker": "TCS",        "yf": "TCS.NS"},
    {"name": "HDFC Bank",                  "ticker": "HDFCBANK",   "yf": "HDFCBANK.NS"},
    {"name": "Infosys",                    "ticker": "INFY",       "yf": "INFY.NS"},
    {"name": "ICICI Bank",                 "ticker": "ICICIBANK",  "yf": "ICICIBANK.NS"},
    {"name": "Adani Enterprises",          "ticker": "ADANIENT",   "yf": "ADANIENT.NS"},
    {"name": "State Bank of India",        "ticker": "SBIN",       "yf": "SBIN.NS"},
    {"name": "Wipro",                      "ticker": "WIPRO",      "yf": "WIPRO.NS"},
    {"name": "Tata Motors",                "ticker": "TATAMOTORS", "yf": "TATAMOTORS.NS"},
    {"name": "Bajaj Finance",              "ticker": "BAJFINANCE", "yf": "BAJFINANCE.NS"},
]

def collect_financials(company):
    try:
        stock = yf.Ticker(company["yf"])
        info = stock.info
        data = {
            "ticker":        company["ticker"],
            "collected_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "company_info": {
                "name":           info.get("longName", "N/A"),
                "sector":         info.get("sector", "N/A"),
                "market_cap":     info.get("marketCap", "N/A"),
                "current_price":  info.get("currentPrice", "N/A"),
                "pe_ratio":       info.get("trailingPE", "N/A"),
                "pb_ratio":       info.get("priceToBook", "N/A"),
                "roe":            info.get("returnOnEquity", "N/A"),
                "debt_to_equity": info.get("debtToEquity", "N/A"),
                "revenue":        info.get("totalRevenue", "N/A"),
                "net_income":     info.get("netIncomeToCommon", "N/A"),
                "eps":            info.get("trailingEps", "N/A"),
                "52_week_high":   info.get("fiftyTwoWeekHigh", "N/A"),
                "52_week_low":    info.get("fiftyTwoWeekLow", "N/A"),
            }
        }
        with open(f"data/financials/{company['ticker']}.json", "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"  Financials saved for {company['ticker']}")
    except Exception as e:
        print(f"  Failed {company['ticker']}: {e}")

def collect_news(company):
    try:
        query = company["name"].replace(" ", "+") + "+NSE+stock"
        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        root = ET.fromstring(response.content)
        articles = []
        for item in root.findall(".//item")[:10]:
            articles.append({
                "title":     item.findtext("title", "N/A"),
                "link":      item.findtext("link", "N/A"),
                "published": item.findtext("pubDate", "N/A"),
                "source":    item.findtext("source", "N/A"),
            })
        data = {
            "company":      company["name"],
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "articles":     articles
        }
        with open(f"data/news/{company['ticker']}_news.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"  News saved for {company['ticker']}")
    except Exception as e:
        print(f"  Failed news {company['ticker']}: {e}")

print("Starting daily data refresh...")
for company in COMPANIES:
    collect_financials(company)
    collect_news(company)
    time.sleep(2)

print("\nAll done! Data files updated.")
