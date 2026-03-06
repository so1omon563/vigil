#!/usr/bin/env python3
"""
Weather data collector for Vigil / so1omon.net
Fetches conditions from NWS API (no key required) and writes weather.json.
Designed to run once per autonomous session.

Locations:
  Mesa, AZ 85208 (primary — where Vigil runs)

Expand outward over time: add regional/national points as desired.
"""

import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "weather.json")

LOCATIONS = [
    {
        "name": "Mesa, AZ",
        "zip": "85208",
        "lat": 33.4152,
        "lon": -111.7235,
        "label": "local",
    },
]

USER_AGENT = "Vigil/1.0 (so1omon.net; contact via site)"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def collect_location(loc):
    """Fetch current conditions and short forecast for one location."""
    points_url = f"https://api.weather.gov/points/{loc['lat']},{loc['lon']}"
    points = fetch_json(points_url)
    props = points["properties"]

    forecast_url = props["forecast"]
    hourly_url = props["forecastHourly"]

    forecast = fetch_json(forecast_url)
    periods = forecast["properties"]["periods"]

    hourly = fetch_json(hourly_url)
    current_hour = hourly["properties"]["periods"][0]

    return {
        "name": loc["name"],
        "zip": loc["zip"],
        "label": loc["label"],
        "current": {
            "temperature_f": current_hour["temperature"],
            "wind_speed": current_hour["windSpeed"],
            "wind_direction": current_hour["windDirection"],
            "short_forecast": current_hour["shortForecast"],
            "is_daytime": current_hour["isDaytime"],
        },
        "periods": [
            {
                "name": p["name"],
                "temperature_f": p["temperature"],
                "short_forecast": p["shortForecast"],
                "wind_speed": p["windSpeed"],
                "wind_direction": p["windDirection"],
                "is_daytime": p["isDaytime"],
            }
            for p in periods[:6]
        ],
    }


def run():
    now = datetime.now(timezone.utc).isoformat()
    results = []

    for loc in LOCATIONS:
        try:
            data = collect_location(loc)
            data["error"] = None
            results.append(data)
            print(f"[weather] {loc['name']}: {data['current']['temperature_f']}°F, {data['current']['short_forecast']}")
        except Exception as e:
            results.append({
                "name": loc["name"],
                "zip": loc["zip"],
                "label": loc["label"],
                "error": str(e),
                "current": None,
                "periods": [],
            })
            print(f"[weather] {loc['name']}: ERROR — {e}")

    output = {
        "updated": now,
        "locations": results,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[weather] Written to {OUTPUT_FILE}")
    return output


if __name__ == "__main__":
    run()
