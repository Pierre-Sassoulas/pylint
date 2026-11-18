"""dummy docstring"""
import psycopg


with psycopg.connect("dbname=test user=postgres") as client:
    version = client.execute(
        """
        CREATE TABLE test (
            id serial PRIMARY KEY,
            num integer,
            data text)
        """
    ).fetchone()

