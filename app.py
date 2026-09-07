import streamlit
import pandas as pd
import plotly.express as px
from datetime import date
from database import Database
from fx_rates_source import FxRatesSource

db = Database()

# Get fx rates from frankfurter API and insert them into DB
# Only has to be called once in order to populate DB, no need to call it at every script execution
def import_fx_rates():
    source = FxRatesSource()
    rates = source.get_rates("2023-01-01", "2026-01-01") # The chosen dataset covers jan 2023 until jan 2026

    db.insert_fx_rates(rates)


#####################################
#                                   #
#           Streamlit UI            #
#                                   #
#####################################
streamlit.title("FX rate dashboard")

start_date = streamlit.date_input(
    "Start date",
    value=date(2023, 1, 1)
)

end_date = streamlit.date_input(
    "End date",
    value=date(2026, 1, 1)
)

base_currency = streamlit.selectbox(
    "Base currency",
    ["EUR","NOK","SEK","PLN","RON","DKK","CZK"]
)

quote_currency = streamlit.selectbox(
    "Quote currencies",
    ["EUR","NOK","SEK","PLN","RON","DKK","CZK"]
)

if streamlit.button("Get FX Rates"):

    rates = db.get_cross_rates(
        start_date,
        end_date,
        base_currency,
        quote_currency
    )

    df = pd.DataFrame(
        rates,
        columns=["date", "base_currency", "quote_currency", "rate"]
    )

    fig = px.line(
        df,
        x="date",
        y="rate",
        title=f"{base_currency} / {quote_currency}",
        markers=True
    )

    streamlit.plotly_chart(fig, use_container_width=True)