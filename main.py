import requests

TARGET_CURRENCIES = "NOK,SEK,PLN,RON,DKK,CZK"

ENDPOINT_BASE = "https://api.frankfurter.dev/v2/rates?"
RATES_ENDPOINT = f"{ENDPOINT_BASE}quotes={TARGET_CURRENCIES}"

def get_day_rates():
    try:
        response = requests.get(RATES_ENDPOINT, timeout=10)

        response.raise_for_status()

        rates = response.json()

        for row in rates:
            print(row)

    except requests.exceptions.RequestException as e:
        print(f"Could not reach API: {e}")

def get_rates(timeperiod):
    pass

get_day_rates()