# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "55392c9d-8525-440b-8e37-cfddce4bb5e4",
# META       "default_lakehouse_name": "bronze_lakehouse",
# META       "default_lakehouse_workspace_id": "0c94de57-e2a9-43b8-b434-39b714e56a44",
# META       "known_lakehouses": [
# META         {
# META           "id": "55392c9d-8525-440b-8e37-cfddce4bb5e4"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.functions import *

print("Applying Event 003 - Demand Drop")

# Ready Meals

affected_items = [29, 30, 31, 32]

# Read current sales fact

df_sales = spark.read.table("f_sales_invoice_line")

original_rows = df_sales.count()

# Reduce volume by 35 %

df_sales_updated = (
    df_sales
    .withColumn(
        "Quantity",
        when(
            (
                col("ItemKey").isin(affected_items)
            )
            &
            (
                to_date(col("InvoiceDate")) >= lit("2026-08-01")
            )
            &
            (
                to_date(col("InvoiceDate")) <= lit("2026-10-31")
            ),
            round(col("Quantity") * 0.65).cast("int")
        )
        .otherwise(col("Quantity"))
    )
)

# Recalculate revenue

df_sales_updated = (
    df_sales_updated
    .withColumn(
        "NetAmount",
        round(
            (
                col("Quantity")
                * col("UnitPrice")
            )
            - col("DiscountAmount"),
            2
        )
    )
)

# Overwrite table

spark.sql("""
DROP TABLE IF EXISTS f_sales_invoice_line
""")

(
    df_sales_updated.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("f_sales_invoice_line")
)

# Validation

affected_rows = (
    df_sales_updated
    .filter(
        col("ItemKey").isin(affected_items)
    )
    .filter(
        to_date(col("InvoiceDate"))
        >= lit("2026-08-01")
    )
    .filter(
        to_date(col("InvoiceDate"))
        <= lit("2026-10-31")
    )
    .count()
)

print("=" * 60)
print("EVENT 003 APPLIED")
print("=" * 60)
print("Event            : Demand Drop")
print("Category         : Ready Meals")
print("Period           : 2026-08-01 → 2026-10-31")
print("Volume Impact    : -35%")
print(f"Rows Updated     : {affected_rows}")
print(f"Total Rows       : {original_rows}")
print("=" * 60)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
