#!/usr/bin/env python3
"""
Fetch available units from Bridge at Arella Lakeline.
API: https://doorway-api.knockrentals.com/v1/property/2024885/units
"""

import urllib.request
import json
import time
import os
from datetime import datetime

URL = "https://doorway-api.knockrentals.com/v1/property/2024885/units"


def fetch_data():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["units_data"]


def fetch_units():
    return fetch_data()["units"]


def watch_units(unit_names: list[str]):
    data = fetch_data()
    units = data["units"]
    layouts = {l["id"]: l for l in data["layouts"]}

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n=== Watched Units — {now} ===\n")

    for name in unit_names:
        unit = next((u for u in units if u["name"] == name), None)
        if not unit:
            print(f"Unit {name}: NOT FOUND in API\n")
            continue

        layout = layouts.get(unit["layoutId"], {})
        deleted_by_vendor = layout.get("deletedByVendor")

        available = unit.get("available")
        price = unit.get("price", "N/A")
        avail_date = unit.get("availableOn", "N/A")
        beds = unit["bedrooms"]
        baths = unit["bathrooms"]
        area = unit["area"]
        layout_name = unit.get("layoutName", "?")

        hidden = unit.get("hidden")
        occupied = unit.get("occupied")
        notice_given = unit.get("noticeGiven")

        # Unit shows in UI only if: tenant is currently occupying AND has given notice to vacate
        visible_in_ui = occupied and notice_given

        status = "AVAILABLE" if available else "NOT AVAILABLE"
        knock_price = unit.get("knockPrice")
        modified_at = unit.get("modifiedAt", "N/A")
        price_display = f"${price}/mo" if price != "N/A" else "N/A"
        knock_price_display = f"${knock_price}/mo" if knock_price else "N/A"

        print(f"Unit {name} ({layout_name}):")
        print(f"  Status         : {status}")
        print(f"  Available      : {available}")
        print(f"  Hidden         : {hidden}")
        print(f"  Occupied       : {occupied}")
        print(f"  Notice Given   : {notice_given}")
        print(f"  Visible in UI  : {visible_in_ui}")
        print(f"  Price (Knock)  : {price_display}")
        print(f"  Price (UI)     : {knock_price_display}")
        print(f"  Available From : {avail_date}")
        print(f"  Bed/Bath/Area  : {beds}bd / {baths}ba / {area} sqft")
        print(f"  deletedByVendor: {deleted_by_vendor}  {'⚠ layout deleted in ResMan' if deleted_by_vendor else ''}")
        print(f"  Last Modified  : {modified_at}")
        print()


def display(units, bedrooms=None, available_only=True):
    if bedrooms:
        units = [u for u in units if u.get("bedrooms") == bedrooms]
    if available_only:
        units = [u for u in units if u.get("available")]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = f"{bedrooms}BR " if bedrooms else ""
    print(f"\n=== {label}Units available as of {now} — {len(units)} found ===\n")
    print(f"{'Unit':<10} {'Layout':<8} {'Bed':<5} {'Bath':<6} {'Area (sqft)':<14} {'Rent/mo':<12} {'Available Date'}")
    print("-" * 75)
    for u in sorted(units, key=lambda x: x.get("availableOn") or ""):
        print(
            f"{u['name']:<10} {u.get('layoutName','?'):<8} {u['bedrooms']:<5} "
            f"{u['bathrooms']:<6} {u['area']:<14} ${u.get('price','?'):<11} "
            f"{u.get('availableOn', 'N/A')}"
        )


POLL_INTERVAL = 30  # seconds


def parse_units(args: list[str]) -> list[str]:
    """Accept units as space-separated args or a single comma-separated string."""
    units = []
    for a in args:
        units.extend(u.strip() for u in a.split(",") if u.strip())
    return units


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]

    if args and args[0] == "watch":
        unit_names = parse_units(args[1:])
        if not unit_names:
            print("Usage: python bridge_arella_units.py watch <unit1>[,unit2,...] [unit3 ...]")
            sys.exit(1)
        print(f"Watching units: {', '.join(unit_names)}  (refreshing every {POLL_INTERVAL}s, Ctrl+C to stop)")
        try:
            while True:
                os.system("clear")
                try:
                    watch_units(unit_names)
                except Exception as e:
                    print(f"Error fetching data: {e}")
                print(f"Next refresh in {POLL_INTERVAL}s — Ctrl+C to stop")
                time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\nStopped.")
    else:
        units = fetch_units()
        bedrooms = int(args[0]) if args else None
        display(units, bedrooms=bedrooms)
