from fx_rates_source import FxRatesSource
from database import Database

db = Database()

# Get fx rates from frankfurter API and insert them into DB
def import_fx_rates():
    source = FxRatesSource()
    rates = source.get_rates("2026-08-01", "2026-08-31") # I chose to use the month of August 2026

    db.insert_fx_rates(rates)
    db.close()
