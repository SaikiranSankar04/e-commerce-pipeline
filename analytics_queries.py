from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round

spark = SparkSession.builder.appName("AnalyticsQueries").getOrCreate()

# Read the cleaned data
df = spark.read.option("header", True).csv("/opt/workspace/cleaned_orders.csv")
# Step 2: Cast `price` and `quantity` as float and int
df = df.withColumn("price", col("price").cast("float")).withColumn(
    "quantity", col("quantity").cast("int")
)

# Register as temporary view

df.createOrReplaceTempView("ecommerce_orders")

# Top 5 categories by total sales
print("\n🔹 Top 5 Categories by Total Sales")
spark.sql(
    """
SELECT category, ROUND(SUM(price * quantity), 2) AS total_sales
FROM ecommerce_orders
GROUP BY category
ORDER BY total_sales DESC
LIMIT 5
"""
).show()

# Top 10 countries by revenue
print("\n🔹 Top 10 Countries by Revenue")
spark.sql(
    """
SELECT country, ROUND(SUM(price * quantity), 2) AS revenue
FROM ecommerce_orders
GROUP BY country
ORDER BY revenue DESC
LIMIT 10
"""
).show()

# Orders per day
print("\n🔹 Orders per Day")
spark.sql(
    """
SELECT order_date, COUNT(*) AS total_orders, ROUND(SUM(price * quantity), 2) AS total_revenue
FROM ecommerce_orders
GROUP BY order_date
ORDER BY order_date
"""
).show()
