import sys

import requests

from database import Database
from fx_rates_source import FxRatesSource

# Get fx rates from frankfurter API and insert them into DB
# Only has to be called once in order to populate DB, no need to call it at every script execution
def import_fx_rates():

    source = FxRatesSource()

    try:
        rates = source.get_rates("2023-01-01", "2026-01-01") # The chosen dataset covers jan 2023 until jan 2026
    except requests.exceptions.RequestException as e:
        print(f"Could not reach FX rate API: {e}")
        sys.exit(1)

    db = Database()
    db.insert_fx_rates(rates)
    db.close()

if __name__ == "__main__":
    import_fx_rates()