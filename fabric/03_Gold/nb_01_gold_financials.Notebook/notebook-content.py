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
from pyspark.sql.types import IntegerType

print("Starting Gold Financials generation...")

# READ SILVER TABLES

df_gl = spark.read.table(
    "silver_lakehouse.dbo.f_gl_entry"
)

df_coa = spark.read.table(
    "silver_lakehouse.dbo.d_chart_of_accounts"
)

# NORMALIZE ACCOUNTKEY DATATYPE

df_gl = (
    df_gl
    .withColumn(
        "AccountKey",
        col("AccountKey").cast(IntegerType())
    )
)

df_coa = (
    df_coa
    .withColumn(
        "AccountKey",
        col("AccountKey").cast(IntegerType())
    )
)

# DATE ATTRIBUTES

df_gl = (
    df_gl
    .withColumn(
        "PostingDate",
        to_date(col("PostingDate"))
    )
    .withColumn(
        "PostingYear",
        year(col("PostingDate"))
    )
    .withColumn(
        "PostingMonth",
        month(col("PostingDate"))
    )
)

# JOIN CHART OF ACCOUNTS

df_gold = (
    df_gl.alias("gl")
    .join(
        df_coa.alias("coa"),
        on="AccountKey",
        how="left"
    )
)

# HANDLE MISSING COA MATCHES

df_gold = (
    df_gold
    .withColumn(
        "AccountName",
        coalesce(
            col("AccountName"),
            lit("UNKNOWN ACCOUNT")
        )
    )
    .withColumn(
        "AccountGroup",
        coalesce(
            col("AccountGroup"),
            lit("UNKNOWN GROUP")
        )
    )
    .withColumn(
        "AccountCategory",
        coalesce(
            col("AccountCategory"),
            lit("UNKNOWN CATEGORY")
        )
    )
)

# SELECT FINAL STRUCTURE

df_gold = (
    df_gold.select(
        "GLEntryNumber",

        "PostingDate",
        "PostingYear",
        "PostingMonth",

        "DocumentNumber",
        "DocumentType",

        "CustomerKey",
        "SupplierKey",
        "ItemKey",

        "AccountKey",
        "AccountNumber",
        "AccountName",
        "AccountGroup",
        "AccountCategory",

        "Amount"
    )
)

# VALIDATION OUTPUT

print("=" * 60)
print("ACCOUNT GROUP DISTRIBUTION")
print("=" * 60)

display(
    df_gold
    .groupBy("AccountGroup")
    .agg(
        count("*").alias("Rows"),
        round(sum("Amount"), 2).alias("Amount")
    )
    .orderBy("AccountGroup")
)

# DROP OLD TABLE

spark.sql("""
DROP TABLE IF EXISTS gold_financials
""")

# WRITE GOLD

(
    df_gold.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("gold_financials")
)

# SUMMARY

row_count = df_gold.count()

account_groups = (
    df_gold
    .select("AccountGroup")
    .distinct()
    .count()
)

print("=" * 60)
print("GOLD FINANCIALS LOAD SUMMARY")
print("=" * 60)
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
