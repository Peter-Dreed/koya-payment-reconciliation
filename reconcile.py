#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json
from decimal import Decimal, ROUND_HALF_UP

latest = {}

with open("payments.jsonl", encoding="utf-8-sig") as f:
    for line in f:
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict) or not event.get("txn_id"):
            continue
        key = event["txn_id"]
        # Ties go to the later line in the file.
        if key not in latest or event["ts"] >= latest[key]["ts"]:
            latest[key] = event

total = Decimal(0)
count = 0

for event in latest.values():
    if event["status"] == "success":
        # Some amounts are strings with thousands separators, e.g. "4,804.15".
        total += Decimal(str(event["amount"]).replace(",", ""))
        count += 1

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{total.quantize(Decimal(1), rounding=ROUND_HALF_UP)}")
