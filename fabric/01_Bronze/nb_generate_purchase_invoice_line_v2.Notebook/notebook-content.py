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

print("Generating Purchase Invoice Data...")

# PARAMETERS

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 12, 31)

MIN_DAILY_INVOICES = 1
MAX_DAILY_INVOICES = 3

# READ MASTER DATA

items = spark.read.table(
    "silver_lakehouse.dbo.d_item"
).collect()

suppliers = spark.read.table(
    "silver_lakehouse.dbo.d_supplier"
).collect()

warehouses = spark.read.table(
    "silver_lakehouse.dbo.d_warehouse"
).collect()

# GENERATOR

data = []

invoice_counter = 1

current_date = START_DATE

while current_date <= END_DATE:

    daily_invoices = random.randint(
        MIN_DAILY_INVOICES,
        MAX_DAILY_INVOICES
    )

    for _ in range(daily_invoices):

        supplier = random.choice(suppliers)

        line_count = random.randint(1, 5)

        for line_no in range(1, line_count + 1):

            item = random.choice(items)
            warehouse = random.choice(warehouses)

            quantity = random.randint(20, 500)

            unit_cost = float(item["StandardCost"])

            #
            # EVENT 001
            # Cheddar Cheese Price Increase
            #

            if int(item["ItemKey"]) == 6:

                if current_date >= datetime(2026, 7, 1):
                    unit_cost = 4.15

                elif current_date >= datetime(2026, 4, 1):
                    unit_cost = 3.75

                else:
                    unit_cost = 3.40

            line_amount = builtins.round(
                quantity * unit_cost,
                2
            )

            data.append(
                (
                    f"PI-{invoice_counter:08d}",
                    line_no,
                    current_date.strftime("%Y-%m-%d"),
                    int(supplier["SupplierKey"]),
                    int(item["ItemKey"]),
                    min(
                        int(item["ItemKey"]),
                        10
                    ),
                    int(warehouse["WarehouseKey"]),
                    quantity,
                    float(unit_cost),
                    float(line_amount)
                )
            )

        invoice_counter += 1

    current_date += timedelta(days=1)

# SCHEMA

schema = StructType([
    StructField("PurchaseInvoiceNumber", StringType(), False),
    StructField("PurchaseInvoiceLineNumber", IntegerType(), False),
    StructField("InvoiceDate", StringType(), False),
    StructField("SupplierKey", IntegerType(), False),
    StructField("ItemKey", IntegerType(), False),
    StructField("LotKey", IntegerType(), False),
    StructField("WarehouseKey", IntegerType(), False),
    StructField("Quantity", IntegerType(), False),
    StructField("UnitCost", DoubleType(), False),
    StructField("LineAmount", DoubleType(), False)
])

df_purchase_invoice = spark.createDataFrame(
    data,
    schema
)

# REBUILD TABLE

spark.sql("""
DROP TABLE IF EXISTS f_purchase_invoice_line
""")

(
    df_purchase_invoice.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("f_purchase_invoice_line")
)

# SUMMARY

row_count = df_purchase_invoice.count()

invoice_count = (
    df_purchase_invoice
    .select("PurchaseInvoiceNumber")
    .distinct()
    .count()
)

print("=" * 60)
print("PURCHASE INVOICE GENERATION COMPLETED")
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
