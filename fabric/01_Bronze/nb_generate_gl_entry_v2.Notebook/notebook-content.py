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
# META     },
# META     "environment": {
# META       "environmentId": "333b832c-6a0a-9cc3-480c-7bfa96ab53d2",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.window import Window

print("Generating General Ledger Entries...")

# READ FACTS

df_sales = spark.read.table(
    "silver_lakehouse.dbo.f_sales_invoice_line"
)

df_purchase = spark.read.table(
    "silver_lakehouse.dbo.f_purchase_invoice_line"
)

# SALES -> REVENUE

sales_gl = (
    df_sales
    .withColumn(
        "PostingDate",
        to_date(col("InvoiceDate"))
    )
    .withColumn(
        "AccountKey",
        lit(1)
    )
    .withColumn(
        "DocumentType",
        lit("SALE")
    )
    .withColumn(
        "DocumentNumber",
        col("SalesInvoiceNumber")
    )
    .withColumn(
        "Amount",
        col("NetAmount")
    )
    .select(
        "PostingDate",
        "DocumentNumber",
        "DocumentType",
        "AccountKey",
        "CustomerKey",
        "ItemKey",
        "Amount"
    )
)

# PURCHASE -> COGS

purchase_gl = (
    df_purchase
    .withColumn(
        "PostingDate",
        to_date(col("InvoiceDate"))
    )
    .withColumn(
        "AccountKey",
        when(
            col("ItemKey").isin([1,2,3,4,5,6,7,8,9]),
            lit(7)
        )
        .otherwise(lit(8))
    )
    .withColumn(
        "DocumentType",
        lit("PURCHASE")
    )
    .withColumn(
        "DocumentNumber",
        col("PurchaseInvoiceNumber")
    )
    .withColumn(
        "Amount",
        col("LineAmount") * -1
    )
    .select(
        "PostingDate",
        "DocumentNumber",
        "DocumentType",
        "AccountKey",
        "SupplierKey",
        "ItemKey",
        "Amount"
    )
)

# STANDARDIZE STRUCTURE

sales_gl = (
    sales_gl
    .withColumn("SupplierKey", lit(None).cast("int"))
)

purchase_gl = (
    purchase_gl
    .withColumn("CustomerKey", lit(None).cast("int"))
)

# UNION

df_gl = sales_gl.unionByName(
    purchase_gl
)

# GENERATE GL ENTRY NUMBER

window_spec = Window.orderBy(
    "PostingDate"
)

df_gl = (
    df_gl
    .withColumn(
        "GLEntryNumber",
        row_number().over(window_spec)
    )
)

# REORDER

df_gl = (
    df_gl.select(
        "GLEntryNumber",
        "PostingDate",
        "DocumentNumber",
        "DocumentType",
        "AccountKey",
        "CustomerKey",
        "SupplierKey",
        "ItemKey",
        "Amount"
    )
)

# REBUILD TABLE

spark.sql("""
DROP TABLE IF EXISTS f_gl_entry
""")

(
    df_gl.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("f_gl_entry")
)

# SUMMARY

row_count = df_gl.count()

print("=" * 60)
print("GL GENERATION COMPLETED")
print("=" * 60)
print(f"Rows Generated : {row_count}")
print("=" * 60)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
