from datetime import datetime, timezone

from pandas import date_range

start = datetime(2023, 1, 1, tzinfo=timezone.utc)
end = datetime.now(timezone.utc).replace(second=0, microsecond=0)
intervals = date_range(start, end, freq="MS").to_pydatetime().tolist()
print(intervals)
