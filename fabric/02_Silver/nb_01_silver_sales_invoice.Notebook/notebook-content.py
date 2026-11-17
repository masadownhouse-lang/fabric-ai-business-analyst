# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "c7365c89-ac0d-40cd-b656-3251515fc0eb",
# META       "default_lakehouse_name": "silver_lakehouse",
# META       "default_lakehouse_workspace_id": "0c94de57-e2a9-43b8-b434-39b714e56a44",
# META       "known_lakehouses": [
# META         {
# META           "id": "55392c9d-8525-440b-8e37-cfddce4bb5e4"
# META         },
# META         {
# META           "id": "c7365c89-ac0d-40cd-b656-3251515fc0eb"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************


from pyspark.sql.functions import *
from pyspark.sql.types import *

print("Starting Bronze to Silver transformation...")

# 1. Read Bronze data
df = spark.read.table("bronze_lakehouse.dbo.f_sales_invoice_line")

# 2. Transform data types
df_silver = (
    df
    .withColumn("InvoiceDate", to_date(col("InvoiceDate"), "yyyy-MM-dd"))
    .withColumn("UnitPrice", col("UnitPrice").cast(DecimalType(18, 2)))
    .withColumn("DiscountAmount", col("DiscountAmount").cast(DecimalType(18, 2)))
    .withColumn("NetAmount", col("NetAmount").cast(DecimalType(18, 2)))
)

# 3. Remove exact duplicates
df_silver = df_silver.dropDuplicates()

# 4. Check data
print("Silver schema:")
df_silver.printSchema()

print("Silver data:")
df_silver.show(truncate=False)

# 5. Write to Silver Lakehouse
(
    df_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("f_sales_invoice_line")
)

# 6. Load summary
print("BRONZE TO SILVER COMPLETED")
print(f"Rows written: {df_silver.count()}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
