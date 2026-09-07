import duckdb

class Database:

    # Create DB if it doesn't exist, then connect to it
    def __init__(self):
        try:
            self.conn = duckdb.connect("fx_rates.db")

            self.conn.execute("""CREATE TABLE IF NOT EXISTS exchange_rates (
                            date DATE,
                            base VARCHAR,
                            quote VARCHAR,
                            rate DECIMAL(18, 8),
                            PRIMARY KEY (date, base, quote)
                        );""")
            
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

    # Get all fx rates
    def get_fx_rates(self):
        return self.conn.execute("""
            SELECT *
            FROM exchange_rates
            ORDER BY date, base, quote
        """).fetchall()

    def close(self):
            self.conn.close()