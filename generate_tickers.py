
import os, json

# Read all available tickers from data/financials folder
tickers = []
fin_dir = "data/financials"
if os.path.exists(fin_dir):
    for f in sorted(os.listdir(fin_dir)):
        if f.endswith(".json"):
            tickers.append(f.replace(".json",""))

# Write tickers.json so website can discover all companies
with open("data/tickers.json", "w") as f:
    json.dump(tickers, f)

print(f"Found {len(tickers)} companies, wrote data/tickers.json")
