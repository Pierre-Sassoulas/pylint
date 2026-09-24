import pandas as pd

print(pd.date_range(start=pd.Timestamp("now"), periods=3).date)
