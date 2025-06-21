from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, upper


spark = (
    SparkSession.builder.appName("EcommerceOrdersETL")
    .config("spark.hadoop.security.authentication", "simple")
    .config("spark.hadoop.security.authorization", "false")
    .config("spark.hadoop.fs.viewfs.impl.disable.cache", "true")
    .getOrCreate()
)


df_raw = spark.read.option("header", True).csv(
    "/opt/workspace/raw_orders.csv", inferSchema=True
)

df_clean = (
    df_raw.dropna(subset=["order_id", "customer_name", "email", "price"])
    .withColumn("category", upper(col("category")))
    .withColumn("total_price", col("price") * col("quantity"))
)

df_clean.show(10, truncate=False)


df_clean.coalesce(1).write.mode("overwrite").option("header", True).csv(
    "/opt/workspace/clean_orders"
)
# After all transformations
df_raw.createOrReplaceTempView("ecommerce_orders")

# Optionally save to disk for later querying or dashboarding
df_raw.write.mode("overwrite").option("header", True).csv(
    "/opt/workspace/output/cleaned_orders"
)

spark.stop()
