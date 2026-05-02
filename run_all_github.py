import yfinance as yf
import requests
import xml.etree.ElementTree as ET
import json, os, time
from datetime import datetime

os.makedirs("data/financials", exist_ok=True)
os.makedirs("data/news", exist_ok=True)

COMPANIES = [
    {"name": "Reliance Industries",        "ticker": "RELIANCE",    "yf": "RELIANCE.NS"},
    {"name": "Tata Consultancy Services",  "ticker": "TCS",         "yf": "TCS.NS"},
    {"name": "HDFC Bank",                  "ticker": "HDFCBANK",    "yf": "HDFCBANK.NS"},
    {"name": "Infosys",                    "ticker": "INFY",        "yf": "INFY.NS"},
    {"name": "ICICI Bank",                 "ticker": "ICICIBANK",   "yf": "ICICIBANK.NS"},
    {"name": "Adani Enterprises",          "ticker": "ADANIENT",    "yf": "ADANIENT.NS"},
    {"name": "State Bank of India",        "ticker": "SBIN",        "yf": "SBIN.NS"},
    {"name": "Wipro",                      "ticker": "WIPRO",       "yf": "WIPRO.NS"},
    {"name": "Tata Motors",                "ticker": "TATAMOTORS",  "yf": "TATAMOTORS.NS"},
    {"name": "Bajaj Finance",              "ticker": "BAJFINANCE",  "yf": "BAJFINANCE.NS"},
    {"name": "Hindustan Unilever",         "ticker": "HINDUNILVR",  "yf": "HINDUNILVR.NS"},
    {"name": "Bharti Airtel",              "ticker": "BHARTIARTL",  "yf": "BHARTIARTL.NS"},
    {"name": "Kotak Mahindra Bank",        "ticker": "KOTAKBANK",   "yf": "KOTAKBANK.NS"},
    {"name": "Axis Bank",                  "ticker": "AXISBANK",    "yf": "AXISBANK.NS"},
    {"name": "Larsen and Toubro",          "ticker": "LT",          "yf": "LT.NS"},
    {"name": "Sun Pharmaceutical",         "ticker": "SUNPHARMA",   "yf": "SUNPHARMA.NS"},
    {"name": "Maruti Suzuki",              "ticker": "MARUTI",      "yf": "MARUTI.NS"},
    {"name": "Titan Company",              "ticker": "TITAN",       "yf": "TITAN.NS"},
    {"name": "UltraTech Cement",           "ticker": "ULTRACEMCO",  "yf": "ULTRACEMCO.NS"},
    {"name": "Asian Paints",               "ticker": "ASIANPAINT",  "yf": "ASIANPAINT.NS"},
    {"name": "HCL Technologies",           "ticker": "HCLTECH",     "yf": "HCLTECH.NS"},
    {"name": "ITC Limited",                "ticker": "ITC",         "yf": "ITC.NS"},
    {"name": "Power Grid Corporation",     "ticker": "POWERGRID",   "yf": "POWERGRID.NS"},
    {"name": "NTPC Limited",               "ticker": "NTPC",        "yf": "NTPC.NS"},
    {"name": "Tata Steel",                 "ticker": "TATASTEEL",   "yf": "TATASTEEL.NS"},
    {"name": "JSW Steel",                  "ticker": "JSWSTEEL",    "yf": "JSWSTEEL.NS"},
    {"name": "Oil and Natural Gas Corp",   "ticker": "ONGC",        "yf": "ONGC.NS"},
    {"name": "Coal India",                 "ticker": "COALINDIA",   "yf": "COALINDIA.NS"},
    {"name": "Bajaj Auto",                 "ticker": "BAJAJAUTO",   "yf": "BAJAJ-AUTO.NS"},
    {"name": "Hero MotoCorp",              "ticker": "HEROMOTOCO",  "yf": "HEROMOTOCO.NS"},
    {"name": "Divis Laboratories",         "ticker": "DIVISLAB",    "yf": "DIVISLAB.NS"},
    {"name": "Dr Reddys Laboratories",     "ticker": "DRREDDY",     "yf": "DRREDDY.NS"},
    {"name": "Cipla",                      "ticker": "CIPLA",       "yf": "CIPLA.NS"},
    {"name": "Eicher Motors",              "ticker": "EICHERMOT",   "yf": "EICHERMOT.NS"},
    {"name": "Mahindra and Mahindra",      "ticker": "MM",          "yf": "M&M.NS"},
    {"name": "Tech Mahindra",              "ticker": "TECHM",       "yf": "TECHM.NS"},
    {"name": "Nestle India",               "ticker": "NESTLEIND",   "yf": "NESTLEIND.NS"},
    {"name": "Britannia Industries",       "ticker": "BRITANNIA",   "yf": "BRITANNIA.NS"},
    {"name": "Adani Ports",                "ticker": "ADANIPORTS",  "yf": "ADANIPORTS.NS"},
    {"name": "Adani Green Energy",         "ticker": "ADANIGREEN",  "yf": "ADANIGREEN.NS"},
    {"name": "Hindalco Industries",        "ticker": "HINDALCO",    "yf": "HINDALCO.NS"},
    {"name": "Grasim Industries",          "ticker": "GRASIM",      "yf": "GRASIM.NS"},
    {"name": "IndusInd Bank",              "ticker": "INDUSINDBK",  "yf": "INDUSINDBK.NS"},
    {"name": "Bajaj Finserv",              "ticker": "BAJAJFINSV",  "yf": "BAJAJFINSV.NS"},
    {"name": "SBI Life Insurance",         "ticker": "SBILIFE",     "yf": "SBILIFE.NS"},
    {"name": "HDFC Life Insurance",        "ticker": "HDFCLIFE",    "yf": "HDFCLIFE.NS"},
    {"name": "Tata Consumer Products",     "ticker": "TATACONSUM",  "yf": "TATACONSUM.NS"},
    {"name": "Pidilite Industries",        "ticker": "PIDILITIND",  "yf": "PIDILITIND.NS"},
    {"name": "Havells India",              "ticker": "HAVELLS",     "yf": "HAVELLS.NS"},
    {"name": "Siemens India",              "ticker": "SIEMENS",     "yf": "SIEMENS.NS"},
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
                "industry":       info.get("industry", "N/A"),
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
                "dividend_yield": info.get("dividendYield", "N/A"),
            }
        }
        with open(f"data/financials/{company['ticker']}.json", "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"  Saved {company['ticker']}")
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
        print(f"  News saved {company['ticker']}")
    except Exception as e:
        print(f"  Failed news {company['ticker']}: {e}")

print("Starting data collection for 50 companies...")
for i, company in enumerate(COMPANIES, 1):
    print(f"[{i}/50] {company['ticker']}")
    collect_financials(company)
    collect_news(company)
    time.sleep(1)

print("\nAll 50 companies done!")
