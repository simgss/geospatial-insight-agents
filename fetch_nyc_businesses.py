# utils/fetch_nyc_businesses.py
import requests
import pandas as pd

NYC_API = "https://data.cityofnewyork.us/resource/xx67-kt59.json?$limit=2000"

def fetch_nyc_businesses():
    r = requests.get(NYC_API)
    r.raise_for_status()
    df = pd.DataFrame(r.json())
    df = df[['dba','industry','zipcode','latitude','longitude']]
    df = df.dropna(subset=['latitude','longitude'])
    df.to_csv("data/nyc_businesses.csv", index=False)
    print("✅ Saved CSV with", len(df), "records.")
    
if __name__ == "__main__":
    fetch_nyc_businesses()
