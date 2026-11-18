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

print("Starting Bronze to Silver transformation...")

# Read Bronze data
df = spark.read.table("bronze_lakehouse.dbo.d_lot")

# Transform
df_silver = (
    df
    .withColumn("ProductionDate", to_date(col("ProductionDate")))
    .withColumn("ExpiryDate", to_date(col("ExpiryDate")))
    .withColumn(
        "DaysToExpiry",
        datediff(col("ExpiryDate"), col("ProductionDate"))
    )
)

# Remove duplicates
df_silver = df_silver.dropDuplicates()

# Write to Silver
(
    df_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("d_lot")
)

# Summary
print("BRONZE TO SILVER COMPLETED")
print(f"Rows written: {df_silver.count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
