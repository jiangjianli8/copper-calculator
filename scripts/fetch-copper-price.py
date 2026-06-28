#!/usr/bin/env python3
"""Fetch 1#电解铜 spot price from SMM AJAX API (no auth needed).
   Saves to data/price.json for GitHub Pages.
"""
import json, urllib.request, os
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)

SMM_PRODUCT_ID = "201102250376"
end_date = now.strftime("%Y-%m-%d")
start_date = (now - timedelta(days=30)).strftime("%Y-%m-%d")
SMM_API = f"https://hq.smm.cn/ajax/spot/history/{SMM_PRODUCT_ID}/{start_date}/{end_date}"

price_data = {
    "symbol": "1#电解铜 (SMM现货)",
    "price": 101570,
    "unit": "元/吨",
    "date": now.strftime("%Y-%m-%d"),
    "updated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
    "source": "smm_ajax",
}

try:
    req = urllib.request.Request(
        SMM_API,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": f"https://hq.smm.cn/copper/category/{SMM_PRODUCT_ID}",
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        smm = json.loads(resp.read().decode())
        if smm.get("code") == 0 and smm.get("data"):
            latest = smm["data"][-1]
            avg = latest.get("average", 0)
            if avg > 0:
                price_data["price"] = int(avg)
                price_data["smm_renew_date"] = latest.get("renew_date", "")
                price_data["smm_high"] = latest.get("high_show", "")
                price_data["smm_low"] = latest.get("low_show", "")
                print(f"SMM: {int(avg)} 元/吨 (updated: {latest.get('renew_date')})")
        else:
            print(f"WARN: SMM code={smm.get('code')}")
except Exception as e:
    print(f"WARN: SMM fetch failed - {e}")

out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, "price.json"), "w", encoding="utf-8") as f:
    json.dump(price_data, f, ensure_ascii=False, indent=2)

print(f"OK price={price_data['price']} yuan/ton")
