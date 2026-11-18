from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession


class SparkInit:
    def __init__(self):
        self.active_spark_session = None

    @property
    def spark(self) -> SparkSession:
        if self.active_spark_session is None:
            conf = SparkConf().setAppName("hi")
            self.active_spark_session = SparkSession.builder.config(conf=conf).getOrCreate()
        return self.active_spark_session

    @property
    def context(self) -> SparkContext:
        return self.spark.sparkContext


def main():
    # this passes
    spark_context = SparkInit().context
    spark_context.blabla()

    # this fails
    spark_context = SparkContext()
    spark_context.blabla()
