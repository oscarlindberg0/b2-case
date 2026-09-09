# FX rates program

## Running the script
1. Download the files.
2. Open a terminal window (Windows Powershell for example), and navigate to the "b2-case" folder.
3. Run the command `python .\fetch_and_load.py` - this will generate the database and populate it with data from the API.
3. Run the command `streamlit run .\app.py`.
4. A web interface will then start. Here you can play around with different currencies and time periods, and see how the graph changes accordingly.

## Functionality
* FX data for the desired currencies and time period is fetched from the Frankfurter API.
* API data is then formatted and inserted into the DuckDB database.
* A database table is created where fx rates compared to the EUR are stored (rate = units of currency per 1 EUR, e.g. a SEK rate of 11.14 means 1 EUR = 11.14 SEK). A cross-reference view is also created. This is to be able to be able to compare rates without having EUR as the base value. This way, we can calculate cross-rates dynamically without having to store every possible combination in the database.
* The user can select currencies and time periods from the streamlit UI. The resulting data is then plotted onto a plotly graph.

## Validation
Output can be validated from the UI.
