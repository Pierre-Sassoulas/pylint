#!/usr/bin/env python
"""Example application to demonstrate pylint false positives"""
import os

from alpha_vantage.timeseries import TimeSeries

api_key = os.getenv("AV_API_KEY")
time_series = TimeSeries(key=api_key)
av_data, _ = time_series.get_daily_adjusted("IBM", "compact")
av_quote_dates = av_data.keys()
for quote_date in av_quote_dates:
    print(f"{quote_date} : {av_data[quote_date]['4. close']}")
