# pylint: disable=missing-module-docstring
# pylint: enable=unsubscriptable-object,unsupported-assignment-operation,no-member
import pandas as pd

data_frame = pd.read_csv("foo.csv")
print(data_frame.shape)
for column in data_frame.columns:
    data_frame[column] = data_frame[column].astype("S")
