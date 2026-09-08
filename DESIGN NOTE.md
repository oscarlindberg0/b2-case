# Design note
## Data source - Frankfurter API
I chose this source for several reasons. It is free to use, has no rate limits, and uses official data from the European central bank. It also has a historical timeperiod endpoint that is very easy to use in order to backfill a database with historical data.

I initially also looked at exchangerate.host as an alternative. However, this provider has rate limits and costs that Frankfurter doesn't.

## Database - DuckDB
Very well suited for this project as it is made for OLAP analysis. It is easy to access from a python script and it is saved locally as a .db file, meaning that I can easily hand over access to someone else.

If I needed additional complexity like multiple concurrent writers for example, I would propably have went with a Postgres database instead.

## Visualization - Streamlit and Plotly
Streamlit is fast to build and interactive, which makes it a good option for demoing a project like this one. It is also much more modern looking than other UI options for Python like tkinter for example. It also runs seamlessly against DuckDB without additional complexity required.
Plotly is a good option for integrating charts and diagrams into the UI.

## Time window
I loaded three years of daily data, from 2023-01-01 to 2026-01-01. This is long enough to show meaningful monthly and yearly aggregations and to make correlations between currencies statistically meaningful, while staying small enough (roughly 750 trading days x 7 currencies) that the whole pipeline runs in seconds and the resulting database file stays small enough to hand over directly.

## Schema
All the fx rates are saved in the database only as EUR-based rates, meaning only one database entry for every currency is stored. Cross-rates (meaning rates that don't include the EUR as base currency, for example a SEK / NOK comparison) are calculated at read time using a preset query in the form of a database view.
This avoids redundancy and keeps the EUR rate as the single source of truth.
