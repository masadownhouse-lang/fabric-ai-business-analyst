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
# META           "id": "c7365c89-ac0d-40cd-b656-3251515fc0eb"
# META         },
# META         {
# META           "id": "55392c9d-8525-440b-8e37-cfddce4bb5e4"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.types import *
import random
import builtins
from datetime import datetime, timedelta

print("Generating Sales Invoice Data...")

# PARAMETERS

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 12, 31)

MIN_DAILY_TRANSACTIONS = 1
MAX_DAILY_TRANSACTIONS = 5

# READ MASTER DATA

items = spark.read.table(
    "silver_lakehouse.dbo.d_item"
).collect()

customers = spark.read.table(
    "silver_lakehouse.dbo.d_customer"
).collect()

warehouses = spark.read.table(
    "silver_lakehouse.dbo.d_warehouse"
).collect()

# GENERATOR

data = []

invoice_counter = 1
line_counter = 1

current_date = START_DATE

while current_date <= END_DATE:

    daily_transactions = random.randint(
        MIN_DAILY_TRANSACTIONS,
        MAX_DAILY_TRANSACTIONS
    )

    for _ in range(daily_transactions):

        item = random.choice(items)
        customer = random.choice(customers)
        warehouse = random.choice(warehouses)

        quantity = random.randint(5, 100)

        list_price = float(item["ListPrice"])

        discount_amount = 0.0

        # EVENT 002
        # Summer Frozen Pizza Campaign

        if (
            current_date.year == 2026
            and current_date.month == 6
            and item["CategoryLevel2"] == "Frozen Pizza"
        ):

            quantity = int(quantity * 1.25)

            discount_amount = builtins.round(
                quantity * list_price * 0.10,
                2
            )

        net_amount = builtins.round(
            quantity * list_price - discount_amount,
            2
        )

        data.append(
            (
                f"SI-{invoice_counter:08d}",
                line_counter,
                current_date.strftime("%Y-%m-%d"),
                int(customer["CustomerKey"]),
                int(item["ItemKey"]),
                1,
                int(warehouse["WarehouseKey"]),
                int(quantity),
                float(list_price),
                float(discount_amount),
                float(net_amount)
            )
        )

        line_counter += 1
        invoice_counter += 1

    current_date += timedelta(days=1)

# SCHEMA

schema = StructType([
    StructField("SalesInvoiceNumber", StringType(), False),
    StructField("SalesInvoiceLineNumber", IntegerType(), False),
    StructField("InvoiceDate", StringType(), False),
    StructField("CustomerKey", IntegerType(), False),
    StructField("ItemKey", IntegerType(), False),
    StructField("LotKey", IntegerType(), False),
    StructField("WarehouseKey", IntegerType(), False),
    StructField("Quantity", IntegerType(), False),
    StructField("UnitPrice", DoubleType(), False),
    StructField("DiscountAmount", DoubleType(), False),
    StructField("NetAmount", DoubleType(), False)
])

df_sales_invoice = spark.createDataFrame(
    data,
    schema
)

# OVERWRITE TABLE

spark.sql("""
DROP TABLE IF EXISTS f_sales_invoice_line
""")

(
    df_sales_invoice.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("f_sales_invoice_line")
)

# SUMMARY

row_count = df_sales_invoice.count()

invoice_count = (
    df_sales_invoice
    .select("SalesInvoiceNumber")
    .distinct()
    .count()
)

print("=" * 60)
print("SALES INVOICE GENERATION COMPLETED")
print("=" * 60)
print(f"Rows Generated     : {row_count}")
print(f"Invoices Generated : {invoice_count}")
print("Period             : 2024-01-01 -> 2026-12-31")
print("=" * 60)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
