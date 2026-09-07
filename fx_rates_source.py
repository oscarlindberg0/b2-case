import requests

TARGET_CURRENCIES = "NOK,EUR,SEK,PLN,RON,DKK,CZK"
ENDPOINT_BASE = "https://api.frankfurter.dev/v2/rates?"

class FxRatesSource:

    # Get fx rates from frankfurter api
    def get_rates(self, start_date, end_date):
        try:
            response = requests.get(f"{ENDPOINT_BASE}from={start_date}&to={end_date}&quotes={TARGET_CURRENCIES}")

            response.raise_for_status()
            rates = response.json()

            return rates

        except requests.exceptions.RequestException as e:
            print(f"Could not reach API: {e}")