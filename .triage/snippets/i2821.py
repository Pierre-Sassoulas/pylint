from unittest.mock import MagicMock


def test1():
    bigquery = MagicMock()

    def get_table(ds_table):
        return ds_table

    bigquery.get_table = get_table


def test2():
    bigquery = MagicMock()
    bigquery.get_table = lambda x: x
    print(bigquery.get_table(1))
