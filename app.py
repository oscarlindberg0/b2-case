import streamlit
from datetime import date
from database import Database

db = Database()

streamlit.title("FX rate dashboard")

start_date = streamlit.date_input(
    "Start date",
    value=date(2026, 8, 1)
)

end_date = streamlit.date_input(
    "End date",
    value=date(2026, 8, 31)
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

    streamlit.dataframe(rates)