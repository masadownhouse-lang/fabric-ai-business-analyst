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

print("Starting Gold Financials generation...")

# Read Silver tables
df_gl = spark.read.table("silver_lakehouse.dbo.f_gl_entry")

df_coa = spark.read.table("silver_lakehouse.dbo.d_chart_of_accounts")

# Join GL with Chart of Accounts
df_gold = (
    df_gl.alias("gl")
    .join(
        df_coa.alias("coa"),
        col("gl.AccountKey") == col("coa.AccountKey"),
        "inner"
    )
)

# Aggregate to Financial Level
df_gold = (
    df_gold
    .groupBy(
        "PostingYear",
        "PostingMonth",
        "AccountGroup",
        "AccountCategory"
    )
    .agg(
        round(sum("Amount"), 2).alias("Amount")
    )
    .orderBy(
        "PostingYear",
        "PostingMonth",
        "AccountGroup",
        "AccountCategory"
    )
)

# Drop old table
spark.sql("""
DROP TABLE IF EXISTS gold_financials
""")

# Write Gold table
(
    df_gold.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("gold_financials")
)

# Summary

row_count = df_gold.count()

account_groups = (
    df_gold
    .select("AccountGroup")
    .distinct()
    .count()
)

print("=" * 60)
print("GOLD LAYER LOAD SUMMARY")
print("=" * 60)
print("Target Lakehouse : gold_lakehouse")
print("Target Table     : gold_financials")
print(f"Rows Generated   : {row_count}")
print(f"Account Groups   : {account_groups}")
print("Load Status      : SUCCESS")
print("=" * 60)

display(df_gold)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
