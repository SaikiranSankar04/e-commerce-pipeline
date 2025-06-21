from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ReadCleanedData").getOrCreate()

df_output = spark.read.option("header", True).csv("/opt/workspace/clean_orders")
df_output.show(10, truncate=False)

spark.stop()
