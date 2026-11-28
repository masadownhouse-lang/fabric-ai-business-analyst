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
# META           "id": "c7365c89-ac0d-40cd-b656-3251515fc0eb"
# META         },
# META         {
# META           "id": "42fe6a59-535b-49eb-89be-e58388ee0ee2"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.functions import *

print("Starting Gold KPI generation...")

# READ GOLD FINANCIALS

df = spark.read.table(
    "gold_lakehouse.dbo.gold_financials"
)

# MONTHLY KPI AGGREGATION

df_kpis = (
    df
    .groupBy(
        "PostingYear",
        "PostingMonth"
    )
    .agg(

        round(
            sum(
                when(
                    col("AccountGroup") == "Revenue",
                    col("Amount")
                ).otherwise(0)
            ),
            2
        ).alias("Revenue"),

        round(
            sum(
                when(
                    col("AccountGroup") == "COGS",
                    col("Amount")
                ).otherwise(0)
            ),
            2
        ).alias("COGS"),

        round(
            sum(
                when(
                    col("AccountGroup") == "Operating Expenses",
                    col("Amount")
                ).otherwise(0)
            ),
            2
        ).alias("OperatingExpenses")
    )
)

# KPI CALCULATIONS

df_kpis = (
    df_kpis
    .withColumn(
        "GrossMargin",
        round(
            col("Revenue") + col("COGS"),
            2
        )
    )
    .withColumn(
        "EBITDA",
        round(
            col("Revenue")
            + col("COGS")
            + col("OperatingExpenses"),
            2
        )
    )
    .withColumn(
        "GrossMarginPct",
        when(
            col("Revenue") != 0,
            round(
                (
                    col("GrossMargin")
                    / col("Revenue")
                ) * 100,
                2
            )
        )
    )
)

# ORDER

df_kpis = (
    df_kpis.orderBy(
        "PostingYear",
        "PostingMonth"
    )
)

# DROP OLD TABLE

spark.sql("""
DROP TABLE IF EXISTS gold_kpis
""")

# WRITE TABLE

(
    df_kpis.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("gold_kpis")
)

# SUMMARY

print("=" * 60)
print("GOLD KPI LOAD SUMMARY")
print("=" * 60)
print(f"Rows Generated : {df_kpis.count()}")
print("Target Table   : gold_kpis")
print("Load Status    : SUCCESS")
print("=" * 60)

display(df_kpis)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
