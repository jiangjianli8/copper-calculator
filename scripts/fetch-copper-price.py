#!/usr/bin/env python3
"""Fetch SHFE copper futures price from Sina Finance and save to JSON."""
import json, urllib.request, os, re, sys
from datetime import datetime

URL = 'https://hq.sinajs.cn/list=nf_CU0'
req = urllib.request.Request(URL, headers={'Referer': 'https://finance.sina.com.cn'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        text = resp.read().decode('gbk', errors='ignore')
        match = re.search(r'"([^"]*)"', text)
        if not match:
            print('ERROR: failed to parse Sina response')
            sys.exit(1)
        parts = match.group(1).split(',')
        if len(parts) < 4:
            print('ERROR: insufficient data fields')
            sys.exit(1)
        price = float(parts[3])
        if price <= 0:
            print('ERROR: invalid price')
            sys.exit(1)
        now = datetime.now()
        price_data = {
            'symbol': 'CU0 (沪铜连续)',
            'price': price,
            'unit': '元/吨',
            'date': now.strftime('%Y-%m-%d'),
            'updated_at': now.strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'sina_shfe_realtime'
        }
        out_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'price.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(price_data, f, ensure_ascii=False, indent=2)
        print(f'OK price={price:.0f} date={price_data["date"]}')
except Exception as e:
    print(f'ERROR {e}')
    sys.exit(1)
