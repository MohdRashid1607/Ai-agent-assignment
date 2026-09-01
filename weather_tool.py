"""
weather_tool.py
A safe, read-only tool: given a city name, returns current weather.
Uses Open-Meteo's free, keyless public APIs (geocoding + forecast).
No API key required for this service.
"""

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(city: str) -> dict:
    """
    Look up current weather for a given city name.

    Returns a structured dict on success:
        {"status": "ok", "city": ..., "temperature_c": ..., "windspeed_kmh": ..., "weathercode": ...}

    Returns a structured error dict on failure (never raises to the caller):
        {"status": "error", "reason": "..."}
    """
    if not city or not isinstance(city, str) or not city.strip():
        return {"status": "error", "reason": "City name was empty or invalid."}

    try:
        geo_resp = requests.get(
            GEOCODE_URL,
            params={"name": city.strip(), "count": 1},
            timeout=5,
        )
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()
    except requests.exceptions.Timeout:
        return {"status": "error", "reason": "Geocoding request timed out."}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "reason": f"Geocoding request failed: {e}"}

    results = geo_data.get("results")
    if not results:
        return {"status": "error", "reason": f"No location found for '{city}'."}

    lat = results[0]["latitude"]
    lon = results[0]["longitude"]
    resolved_name = results[0].get("name", city)

    try:
        weather_resp = requests.get(
            FORECAST_URL,
            params={"latitude": lat, "longitude": lon, "current_weather": True},
            timeout=5,
        )
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()
    except requests.exceptions.Timeout:
        return {"status": "error", "reason": "Forecast request timed out."}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "reason": f"Forecast request failed: {e}"}

    current = weather_data.get("current_weather")
    if not current:
        return {"status": "error", "reason": "Forecast response missing current weather data."}

    return {
        "status": "ok",
        "city": resolved_name,
        "temperature_c": current.get("temperature"),
        "windspeed_kmh": current.get("windspeed"),
        "weathercode": current.get("weathercode"),
    }