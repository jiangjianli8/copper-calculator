#!/usr/bin/env python3
"""Fetch copper price from AKShare (Sina Futures data).
   Replaces SMM AJAX which blocks cloud/server IPs.
   Saves to data/price.json for GitHub Pages.
"""
import json, os, sys
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)


def fetch_price():
    """Fetch copper futures spot price via AKShare."""
    try:
        import akshare as ak
    except ImportError:
        print("ERROR: akshare not installed. Run: pip install akshare")
        sys.exit(1)

    df = ak.futures_zh_daily_sina(symbol="CU0")

    if df.empty:
        print("WARN: No data returned from AKShare")
        return None

    latest = df.iloc[-1]
    settle_price = float(latest.get("settle", 0))
    close_price = float(latest.get("close", 0))
    high_price = float(latest.get("high", 0))
    low_price = float(latest.get("low", 0))
    volume = int(latest.get("volume", 0))
    hold = int(latest.get("hold", 0))
    trade_date = str(latest.get("date", ""))

    price = settle_price if settle_price > 0 else close_price

    result = {
        "symbol": "\u6caa\u94dc\u8fde\u7eed (CU0) \u2014 \u5e7f\u671f\u6240/\u4e0a\u671f\u6240",
        "price": round(price),
        "unit": "\u5143/\u5428",
        "date": trade_date,
        "updated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "source": "akshare_sina_futures",
        "detail": {
            "open": float(latest.get("open", 0)),
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "settle": settle_price,
            "volume": volume,
            "hold": hold,
        }
    }

    if len(df) >= 2:
        prev = df.iloc[-2]
        prev_settle = float(prev.get("settle", 0))
        if prev_settle > 0 and settle_price > 0:
            change = settle_price - prev_settle
            change_pct = (change / prev_settle) * 100
            result["change"] = round(change)
            result["change_rate"] = round(change_pct, 2)
            result["trend"] = "up" if change > 0 else ("down" if change < 0 else "flat")

    return result


def main():
    price_data = fetch_price()

    if not price_data:
        print("ERROR: Failed to fetch price data")
        sys.exit(1)

    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "price.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(price_data, f, ensure_ascii=False, indent=2)

    print(f"Copper Price: {price_data['price']:,} \u5143/\u5428")
    print(f"Date: {price_data['date']}")
    if "change" in price_data:
        sign = "+" if price_data["change"] > 0 else ""
        print(f"Change: {sign}{price_data['change']:,} ({sign}{price_data['change_rate']}%)")
    print(f"Source: {price_data['source']}")
    print(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()
