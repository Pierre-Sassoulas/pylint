"""dummy docstring"""
import psycopg

client = psycopg.connect("dbname=test user=postgres")
with client:
    version = client.execute(
        """
        CREATE TABLE test (
            id serial PRIMARY KEY,
            num integer,
            data text)
        """
    ).fetchone()

