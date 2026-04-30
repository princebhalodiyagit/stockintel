
import requests
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime

def search_sebi_for_company(company_name, base_path="/content/drive/MyDrive/stockintel"):
    os.makedirs(f"{base_path}/data/sebi", exist_ok=True)
    print(f"\nSearching SEBI for: {company_name}")
    query = company_name.replace(" ", "+")
    url = f"https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doSearch=yes&searchText={query}&type=order"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        results = []
        for item in soup.find_all("div", class_="search-result"):
            results.append({
                "title":   item.find("a").get_text(strip=True) if item.find("a") else "N/A",
                "link":    item.find("a")["href"] if item.find("a") else "N/A",
                "summary": item.get_text(strip=True)[:300],
            })
        data = {
            "company": company_name,
            "searched_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_results": len(results),
            "violations": results
        }
        fname = company_name.replace(" ", "_")
        with open(f"{base_path}/data/sebi/{fname}_sebi.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Found {len(results)} records. Saved!")
        return results
    except Exception as e:
        print(f"  Error: {e}")
        return []

def get_mca_director_info(company_name, base_path="/content/drive/MyDrive/stockintel"):
    print(f"\nSaving MCA info for: {company_name}")
    director_info = {
        "company": company_name,
        "mca_portal": "https://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do",
        "instruction": f"Search for {company_name} on MCA21 portal to get DIN numbers of all directors",
        "tofler_api": "https://api.tofler.in — paid API for automated director data",
        "directors": []
    }
    fname = company_name.replace(" ", "_")
    with open(f"{base_path}/data/sebi/{fname}_directors.json", "w") as f:
        json.dump(director_info, f, indent=2)
    print(f"  Saved MCA info!")
    return director_info
