
import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime

def get_company_financials(ticker_symbol, base_path='/content/drive/MyDrive/stockintel'):
    os.makedirs(f"{base_path}/data/financials", exist_ok=True)
    print(f"\nFetching data for: {ticker_symbol}")
    stock = yf.Ticker(ticker_symbol)

    try:
        info = stock.info
        company_info = {
            "name":           info.get("longName", "N/A"),
            "sector":         info.get("sector", "N/A"),
            "industry":       info.get("industry", "N/A"),
            "website":        info.get("website", "N/A"),
            "description":    info.get("longBusinessSummary", "N/A"),
            "employees":      info.get("fullTimeEmployees", "N/A"),
            "headquarters":   info.get("city", "") + ", " + info.get("country", ""),
            "market_cap":     info.get("marketCap", "N/A"),
            "pe_ratio":       info.get("trailingPE", "N/A"),
            "pb_ratio":       info.get("priceToBook", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "52_week_high":   info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low":    info.get("fiftyTwoWeekLow", "N/A"),
            "current_price":  info.get("currentPrice", "N/A"),
            "roe":            info.get("returnOnEquity", "N/A"),
            "roa":            info.get("returnOnAssets", "N/A"),
            "debt_to_equity": info.get("debtToEquity", "N/A"),
            "current_ratio":  info.get("currentRatio", "N/A"),
            "revenue":        info.get("totalRevenue", "N/A"),
            "net_income":     info.get("netIncomeToCommon", "N/A"),
            "earnings_per_share": info.get("trailingEps", "N/A"),
        }
        print(f"  Basic info collected for {company_info['name']}")
    except Exception as e:
        print(f"  Could not get basic info: {e}")
        company_info = {}

    try:
        income_data = stock.financials.to_dict()
        print("  Income statement collected")
    except:
        income_data = {}

    try:
        balance_data = stock.balance_sheet.to_dict()
        print("  Balance sheet collected")
    except:
        balance_data = {}

    try:
        cashflow_data = stock.cashflow.to_dict()
        print("  Cash flow collected")
    except:
        cashflow_data = {}

    try:
        history = stock.history(period="5y", interval="1mo")
        history.index = history.index.strftime('%Y-%m-%d')
        price_data = history[["Open","High","Low","Close","Volume"]].to_dict()
        print(f"  Price history collected — {len(history)} months")
    except:
        price_data = {}

    full_data = {
        "ticker":           ticker_symbol,
        "collected_at":     datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "company_info":     company_info,
        "income_statement": str(income_data),
        "balance_sheet":    str(balance_data),
        "cash_flow":        str(cashflow_data),
        "price_history":    price_data,
    }

    clean_ticker = ticker_symbol.replace(".", "_")
    filename = f"{base_path}/data/financials/{clean_ticker}.json"
    with open(filename, "w") as f:
        json.dump(full_data, f, indent=2, default=str)
    print(f"  Saved to {filename}")
    return full_data


def collect_multiple_companies(tickers, base_path='/content/drive/MyDrive/stockintel'):
    results = []
    for i, ticker in enumerate(tickers, 1):
        print(f"\n[{i}/{len(tickers)}] Processing {ticker}...")
        try:
            data = get_company_financials(ticker, base_path)
            results.append({"ticker": ticker, "name": data["company_info"].get("name","N/A"), "status": "success"})
        except Exception as e:
            results.append({"ticker": ticker, "status": "failed", "error": str(e)})
    pd.DataFrame(results).to_csv(f"{base_path}/data/collection_summary.csv", index=False)
    print(f"\nDone! Summary saved.")
    return results
