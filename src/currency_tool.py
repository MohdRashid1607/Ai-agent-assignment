"""
currency_tool.py
A safe, read-only tool: converts an amount between two currencies.
Uses the Frankfurter API (ECB reference rates) - free, keyless, no signup.
"""

import requests

RATES_URL = "https://api.frankfurter.dev/v1/latest"


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Convert an amount from one currency to another.

    Returns a structured dict on success:
        {"status": "ok", "amount": ..., "from": ..., "to": ..., "converted": ..., "rate": ...}

    Returns a structured error dict on failure (never raises to the caller):
        {"status": "error", "reason": "..."}
    """
    if amount is None or not isinstance(amount, (int, float)) or amount < 0:
        return {"status": "error", "reason": "Amount must be a non-negative number."}
    if not from_currency or not to_currency:
        return {"status": "error", "reason": "Both from_currency and to_currency are required."}

    from_currency = from_currency.strip().upper()
    to_currency = to_currency.strip().upper()

    try:
        resp = requests.get(
            RATES_URL,
            params={"base": from_currency, "symbols": to_currency},
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        return {"status": "error", "reason": "Currency rate request timed out."}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "reason": f"Currency rate request failed: {e}"}

    rates = data.get("rates", {})
    rate = rates.get(to_currency)

    if rate is None:
        return {
            "status": "error",
            "reason": f"No rate found for {from_currency} -> {to_currency}. Check currency codes.",
        }

    return {
        "status": "ok",
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
        "converted": round(amount * rate, 4),
        "rate": rate,
    }