import duckdb

class Database:

    # Create DB if it doesn't exist, then connect to it
    def __init__(self):
        try:
            self.conn = duckdb.connect("fx_rates.db")

            # Create base table
            self.conn.execute("""CREATE TABLE IF NOT EXISTS exchange_rates (
                            date DATE,
                            base VARCHAR,
                            quote VARCHAR,
                            rate DECIMAL(18, 8),
                            PRIMARY KEY (date, base, quote)
                        );""")

            # Create cross-rate view
            self.conn.execute("""
                            CREATE OR REPLACE VIEW fx_cross_rates AS
                            SELECT
                                a.date,
                                a.quote AS base_currency,
                                b.quote AS quote_currency,
                                b.rate / a.rate AS rate
                            FROM exchange_rates a
                            JOIN exchange_rates b
                                ON a.date = b.date
                            WHERE a.quote <> b.quote;
                        """)
            
        except duckdb.FatalException as e:
            print(f"Could not connect to database: {e}")

    # Insert a list of fx rate entries into the DB
    def insert_fx_rates(self, rows: list[dict]):
        cleaned_rows = []
        for row in rows:
            cleaned_rows.append((
                row["date"],
                row["base"],
                row["quote"],
                row["rate"]
            ))

        self.conn.executemany(
            """
            INSERT INTO exchange_rates (date, base, quote, rate)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (date, base, quote) DO NOTHING
            """,
            cleaned_rows
        )

    # Get rates for specific currency comparison and time period
    def get_cross_rates(
        self,
        start_date,
        end_date,
        base_currency,
        quote_currencies
    ):
        placeholders = ",".join(["?"] * len(quote_currencies))

        return self.conn.execute(
            f"""
            SELECT date, base_currency, quote_currency, rate
            FROM fx_cross_rates
            WHERE date BETWEEN ? AND ?
            AND base_currency = ?
            AND quote_currency IN ({placeholders})
            ORDER BY date, quote_currency
            """,
            [
                start_date,
                end_date,
                base_currency,
                *quote_currencies
            ]
        ).fetchall()