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

def get_rates(start_date):
    try:
        response = requests.get(f"{ENDPOINT_BASE}from={start_date}&quotes={TARGET_CURRENCIES}")

        response.raise_for_status()

        rates = response.json()

        for row in rates:
            print(row)

    except requests.exceptions.RequestException as e:
            print(f"Could not reach API: {e}")

#get_day_rates()
get_rates("2026-09-01")