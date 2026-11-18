"""simple testing file for issue report to pylint"""
from functools import reduce
from pyspark.sql.functions import col, when
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

df = spark.createDataFrame(
    [(True, False, False)],
    ["bool_col1", "bool_col2", "bool_col3"],
)


bool_cols = [
    "bool_col1",
    "bool_col2",
    "bool_col3",
]
conditions = reduce(lambda a, b: a | b, [col(c) for c in bool_cols])

df.withColumn("one_col_is_true", when(conditions, True).otherwise(False)).withColumn(
    "no_col_is_true", when(~conditions, True).otherwise(False)
).show()
