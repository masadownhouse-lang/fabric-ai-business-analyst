# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "42fe6a59-535b-49eb-89be-e58388ee0ee2",
# META       "default_lakehouse_name": "gold_lakehouse",
# META       "default_lakehouse_workspace_id": "0c94de57-e2a9-43b8-b434-39b714e56a44",
# META       "known_lakehouses": [
# META         {
# META           "id": "42fe6a59-535b-49eb-89be-e58388ee0ee2"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.functions import *

print("Generating Gold Sales...")

# READ SILVER TABLES

df_sales = spark.read.table(
    "silver_lakehouse.dbo.f_sales_invoice_line"
)

df_item = spark.read.table(
    "silver_lakehouse.dbo.d_item"
)

df_customer = spark.read.table(
    "silver_lakehouse.dbo.d_customer"
)

# JOIN DIMENSIONS

df_gold = (
    df_sales.alias("s")
    .join(
        df_item.alias("i"),
        col("s.ItemKey") == col("i.ItemKey"),
        "left"
    )
    .join(
        df_customer.alias("c"),
        col("s.CustomerKey") == col("c.CustomerKey"),
        "left"
    )
)

# MONTHLY SALES MODEL

df_gold = (
    df_gold
    .withColumn(
        "SalesYear",
        year(col("InvoiceDate"))
    )
    .withColumn(
        "SalesMonth",
        month(col("InvoiceDate"))
    )
)

# AGGREGATE

df_gold = (
    df_gold
    .groupBy(
        "SalesYear",
        "SalesMonth",
        "Country",
        "Segment",
        "CategoryLevel1",
        "CategoryLevel2"
    )
    .agg(
        round(sum("Quantity"), 0).alias("Quantity"),
        round(sum("NetAmount"), 2).alias("Revenue"),
        round(sum("DiscountAmount"), 2).alias("DiscountAmount")
    )
)

# WRITE GOLD

spark.sql("""
DROP TABLE IF EXISTS gold_sales
""")

(
    df_gold.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("gold_sales")
)

# SUMMARY

row_count = df_gold.count()

print("=" * 60)
print("GOLD SALES COMPLETED")
print("=" * 60)
print(f"Rows Generated : {row_count}")
print("=" * 60)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
