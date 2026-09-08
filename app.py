import streamlit
import pandas as pd
import plotly.express as px
from datetime import date
from database import Database

@streamlit.cache_resource
def get_database():
    return Database()

db = get_database()

#####################################
#                                   #
#           Streamlit UI            #
#                                   #
#####################################
streamlit.title("FX rate dashboard")

min_date, max_date = db.get_date_range()

start_date = streamlit.date_input(
    "Start date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = streamlit.date_input(
    "End date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

base_currency = streamlit.selectbox(
    "Base currency",
    ["EUR","NOK","SEK","PLN","RON","DKK","CZK"]
)

quote_currencies = streamlit.multiselect(
    "Quote currencies",
    ["EUR","NOK","SEK","PLN","RON","DKK","CZK"],
    default=["SEK"]
)

granularity = streamlit.radio(
    "View",
    ["Daily", "Monthly", "Yearly"],
    horizontal=True
)

if streamlit.button("Get FX Rates"):

    if not quote_currencies:
        streamlit.warning("Select at least one quote currency")

    else:
        if granularity == "Daily":
            rates = db.get_cross_rates(
                start_date,
                end_date,
                base_currency,
                quote_currencies
            )

            df = pd.DataFrame(
                rates,
                columns=["date", "base_currency", "quote_currency", "rate"]
            )

        else:
            period = "month" if granularity == "Monthly" else "year"

            rates = db.get_cross_rates_aggregated(
                start_date,
                end_date,
                base_currency,
                quote_currencies,
                period
            )

            # Same column names as the daily case (date/base_currency/quote_currency/rate)
            # so the metrics and chart code below don't need to know which view is active.
            # rate_min/rate_max are the extra columns available for monthly/yearly views.
            df = pd.DataFrame(
                rates,
                columns=["date", "base_currency", "quote_currency", "rate", "rate_min", "rate_max"]
            )

        if df.empty:
            streamlit.warning("No rates found for selected time period")
        else:

            # Create columns for the selected currencies
            cols = streamlit.columns(len(quote_currencies))

            for col, currency in zip(cols, quote_currencies):

                currency_df = df[df["quote_currency"] == currency]

                if not currency_df.empty:
                    first_rate = currency_df["rate"].iloc[0]
                    last_rate = currency_df["rate"].iloc[-1]

                    pct_change = (
                        (last_rate - first_rate) / first_rate
                    ) * 100

                    col.metric(
                        label=currency,
                        value=f"{last_rate:.4f}",
                        delta=f"{pct_change:+.2f}%"
                    )

            # FX rate chart
            fig = px.line(
                df,
                x="date",
                y="rate",
                color="quote_currency",
                markers=True,
                title=f"{base_currency} cross rates ({granularity.lower()} average)" if granularity != "Daily" else None,
                labels={"rate": f"avg rate vs {base_currency}"} if granularity != "Daily" else {}
            )

            streamlit.plotly_chart(fig, use_container_width=True)