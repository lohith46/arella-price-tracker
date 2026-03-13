# Bridge at Arella Lakeline — Unit Price Tracker

A lightweight Python script to fetch and monitor available apartment units at **Bridge at Arella Lakeline** via the Knock Rentals API. No third-party dependencies — just the Python standard library.

## What It Does

- Fetches live unit data from the property's Knock Rentals API endpoint.
- Displays available units with rent, bed/bath/sqft, and availability date.
- **Watch mode**: polls specific units every 30 seconds, showing detailed availability status including occupancy, notice-given state, pricing, and whether the unit is visible in the leasing UI.

## Requirements

- Python 3.10+

## Usage

### List all available units

```bash
python bridge_arella_units.py
```

### Filter by bedroom count

```bash
python bridge_arella_units.py 1   # 1-bedroom units
python bridge_arella_units.py 2   # 2-bedroom units
```

**Example output for `python bridge_arella_units.py 2`:**
```
=== 2BR Units available as of 2026-03-13 10:22:05 — 1 found ===

Unit       Layout   Bed   Bath   Area (sqft)    Rent/mo      Available Date
---------------------------------------------------------------------------
9206       B5       2     2      1065           $1519        2025-07-22
```

### Watch specific units (polls every 30 seconds)

```bash
# Watch a single unit
python bridge_arella_units.py watch 9206

# Watch multiple units (space-separated)
python bridge_arella_units.py watch 9206 9207

# Watch multiple units (comma-separated)
python bridge_arella_units.py watch 9206,9207,9208
```

**Example output:**
```
Watching units: 9206  (refreshing every 30s, Ctrl+C to stop)

=== Watched Units — 2026-03-13 10:22:05 ===

Unit 9206 (B5):
  Status         : AVAILABLE
  Available      : True
  Hidden         : False
  Occupied       : False
  Notice Given   : False
  Visible in UI  : False
  Price (Knock)  : $1519/mo
  Price (UI)     : N/A
  Available From : 2025-07-22
  Bed/Bath/Area  : 2bd / 2ba / 1065 sqft
  deletedByVendor: False
  Last Modified  : 2026-03-13T17:10:15.562

Next refresh in 30s — Ctrl+C to stop
```

Press `Ctrl+C` to stop watching.

## Watch Mode Output Fields

| Field            | Description                                                  |
|------------------|--------------------------------------------------------------|
| Status           | AVAILABLE or NOT AVAILABLE                                   |
| Available        | Raw availability flag from the API                          |
| Hidden           | Whether the unit is hidden from listings                     |
| Occupied         | Whether a tenant is currently in the unit                    |
| Notice Given     | Whether the current tenant has given notice to vacate        |
| Visible in UI    | `True` only if occupied AND notice given (shows on website)  |
| Price (Knock)    | Listed rent price                                            |
| Price (UI)       | Knock-adjusted price shown in the leasing portal             |
| Available From   | Date the unit becomes available                              |
| Bed/Bath/Area    | Layout details                                               |
| deletedByVendor  | Whether the layout was deleted in ResMan (property mgmt system) |
| Last Modified    | Timestamp of the last API update for this unit               |
