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

# MARKDOWN ********************

# 1. Configuration
# 
# 2. Generate d_item
# 
# 3. Save d_item to bronze_lakehouse
# 
# 4. Validation


# CELL ********************

from pyspark.sql.types import *

print("Starting master data generation...")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

data = [
(1,"DAI-YOG-001","Greek Yogurt 200g","Nordic Foods","Dairy","Yogurt","PCS",30,0.75,1.95,True),
(2,"DAI-YOG-002","Strawberry Yogurt 200g","Nordic Foods","Dairy","Yogurt","PCS",30,0.75,1.95,True),
(3,"DAI-YOG-003","Vanilla Yogurt 200g","Nordic Foods","Dairy","Yogurt","PCS",30,0.75,1.95,True),

(4,"DAI-CHS-001","Premium Cheese 1kg","Nordic Foods","Dairy","Cheese","PCS",120,3.20,6.95,True),
(5,"DAI-CHS-002","Light Cheese 1kg","Nordic Foods","Dairy","Cheese","PCS",120,3.00,6.50,True),
(6,"DAI-CHS-003","Cheddar Cheese 1kg","Nordic Foods","Dairy","Cheese","PCS",120,3.40,7.20,True),

(7,"DAI-MLK-001","Whole Milk 1L","Nordic Foods","Dairy","Milk","PCS",14,0.45,1.29,True),
(8,"DAI-MLK-002","Low Fat Milk 1L","Nordic Foods","Dairy","Milk","PCS",14,0.42,1.25,True),
(9,"DAI-MLK-003","Lactose Free Milk 1L","Nordic Foods","Dairy","Milk","PCS",14,0.55,1.65,True),

(10,"FRO-PIZ-001","Pepperoni Pizza 300g","Nordic Foods","Frozen Food","Frozen Pizza","PCS",180,1.85,4.90,True),
(11,"FRO-PIZ-002","Margherita Pizza 300g","Nordic Foods","Frozen Food","Frozen Pizza","PCS",180,1.60,4.50,True),
(12,"FRO-PIZ-003","Ham Pizza 350g","Nordic Foods","Frozen Food","Frozen Pizza","PCS",180,1.95,5.20,True),

(13,"FRO-MEA-001","Chicken Rice Meal","Nordic Foods","Frozen Food","Frozen Meals","PCS",365,2.10,5.90,True),
(14,"FRO-MEA-002","Beef Pasta Meal","Nordic Foods","Frozen Food","Frozen Meals","PCS",365,2.25,6.20,True),
(15,"FRO-MEA-003","Vegetarian Meal","Nordic Foods","Frozen Food","Frozen Meals","PCS",365,1.95,5.50,True),

(16,"BEV-JUI-001","Orange Juice 1L","Nordic Foods","Beverages","Juice","PCS",365,0.85,2.50,True),
(17,"BEV-JUI-002","Apple Juice 1L","Nordic Foods","Beverages","Juice","PCS",365,0.80,2.40,True),
(18,"BEV-JUI-003","Mixed Fruit Juice 1L","Nordic Foods","Beverages","Juice","PCS",365,0.95,2.75,True),

(19,"BEV-SOF-001","Cola 500ml","Nordic Foods","Beverages","Soft Drinks","PCS",365,0.35,1.95,True),
(20,"BEV-SOF-002","Lemon Soda 500ml","Nordic Foods","Beverages","Soft Drinks","PCS",365,0.35,1.95,True),
(21,"BEV-SOF-003","Orange Soda 500ml","Nordic Foods","Beverages","Soft Drinks","PCS",365,0.35,1.95,True),

(22,"BEV-ENG-001","Energy Drink Original","Nordic Foods","Beverages","Energy Drinks","PCS",365,0.60,2.95,True),
(23,"BEV-ENG-002","Energy Drink Sugar Free","Nordic Foods","Beverages","Energy Drinks","PCS",365,0.60,2.95,True),

(24,"SNK-CHP-001","Salted Chips","Nordic Foods","Snacks","Chips","PCS",270,0.50,2.20,True),
(25,"SNK-CHP-002","Paprika Chips","Nordic Foods","Snacks","Chips","PCS",270,0.50,2.20,True),
(26,"SNK-CHP-003","Sour Cream Chips","Nordic Foods","Snacks","Chips","PCS",270,0.55,2.30,True),

(27,"SNK-NUT-001","Salted Peanuts","Nordic Foods","Snacks","Nuts","PCS",365,0.75,3.20,True),
(28,"SNK-NUT-002","Mixed Nuts","Nordic Foods","Snacks","Nuts","PCS",365,0.95,3.95,True),

(29,"RME-PAS-001","Chicken Pasta","Nordic Foods","Ready Meals","Pasta","PCS",90,1.75,4.90,True),
(30,"RME-PAS-002","Beef Pasta","Nordic Foods","Ready Meals","Pasta","PCS",90,1.95,5.20,True),

(31,"RME-RIC-001","Chicken Rice","Nordic Foods","Ready Meals","Rice Meals","PCS",90,1.80,4.90,True),
(32,"RME-RIC-002","Teriyaki Rice","Nordic Foods","Ready Meals","Rice Meals","PCS",90,1.90,5.10,True)
]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema = StructType([
    StructField("ItemKey", IntegerType(), False),
    StructField("ItemNumber", StringType(), False),
    StructField("ItemName", StringType(), False),
    StructField("Brand", StringType(), False),
    StructField("CategoryLevel1", StringType(), False),
    StructField("CategoryLevel2", StringType(), False),
    StructField("UnitOfMeasure", StringType(), False),
    StructField("ShelfLifeDays", IntegerType(), False),
    StructField("StandardCost", DoubleType(), False),
    StructField("ListPrice", DoubleType(), False),
    StructField("IsActive", BooleanType(), False)
])

df_item = spark.createDataFrame(data, schema)

display(df_item)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
    df_item.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("d_item")
)

row_count = df_item.count()

print("=" * 50)
print("MASTER DATA GENERATION COMPLETED")
print("=" * 50)
print(f"Table Created     : d_item")
print(f"Rows Generated    : {row_count}")
print(f"Active Products   : {df_item.filter('IsActive = true').count()}")
print(f"Categories        : {df_item.select('CategoryLevel1').distinct().count()}")
print("=" * 50)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import *

print("Starting Chart of Accounts generation...")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

data = [
(1,3000,"Sales Revenue Finland","Revenue","Sales Revenue","P&L",True),
(2,3010,"Sales Revenue Sweden","Revenue","Sales Revenue","P&L",True),
(3,3020,"Sales Revenue Estonia","Revenue","Sales Revenue","P&L",True),
(4,3100,"Sales Discounts","Revenue","Sales Discounts","P&L",True),
(5,3110,"Campaign Discounts","Revenue","Campaign Discounts","P&L",True),

(6,4000,"Raw Materials","COGS","Raw Materials","P&L",True),
(7,4010,"Dairy Raw Materials","COGS","Raw Materials","P&L",True),
(8,4020,"Frozen Food Raw Materials","COGS","Raw Materials","P&L",True),
(9,4030,"Beverage Raw Materials","COGS","Raw Materials","P&L",True),
(10,4100,"Packaging Cost","COGS","Packaging","P&L",True),
(11,4200,"Freight Cost","COGS","Freight","P&L",True),

(12,5000,"Warehouse Personnel Cost","Operating Expenses","Personnel","P&L",True),
(13,5010,"Sales Personnel Cost","Operating Expenses","Personnel","P&L",True),
(14,5020,"Administration Personnel Cost","Operating Expenses","Personnel","P&L",True),

(15,5100,"Warehouse Cost","Operating Expenses","Warehouse","P&L",True),
(16,5110,"Cold Storage Cost","Operating Expenses","Warehouse","P&L",True),

(17,5200,"Marketing Cost","Operating Expenses","Marketing","P&L",True),
(18,5210,"Campaign Cost","Operating Expenses","Marketing","P&L",True),

(19,5300,"Administration Cost","Operating Expenses","Administration","P&L",True),

(20,5400,"Inventory Write-Off","Operating Expenses","Inventory Write-Off","P&L",True),
(21,5410,"Expiry Write-Off","Operating Expenses","Expiry Write-Off","P&L",True),
(22,5420,"Recall Write-Off","Operating Expenses","Recall Write-Off","P&L",True),

(23,6000,"Depreciation","Depreciation","Depreciation","P&L",False),
(24,6010,"Amortization","Depreciation","Amortization","P&L",False),

(25,7000,"Interest Income","Financial Items","Financial","P&L",False),
(26,7100,"Interest Expense","Financial Items","Financial","P&L",False),

(27,1000,"Inventory Asset","Current Assets","Inventory","Balance Sheet",False),
(28,1100,"Accounts Receivable","Current Assets","Receivables","Balance Sheet",False),
(29,1200,"Cash and Bank","Current Assets","Cash","Balance Sheet",False),
(30,2000,"Accounts Payable","Current Liabilities","Payables","Balance Sheet",False)
]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema = StructType([
    StructField("AccountKey", IntegerType(), False),
    StructField("AccountNumber", IntegerType(), False),
    StructField("AccountName", StringType(), False),
    StructField("AccountGroup", StringType(), False),
    StructField("AccountCategory", StringType(), False),
    StructField("StatementType", StringType(), False),
    StructField("EBITDAImpact", BooleanType(), False)
])

df_coa = spark.createDataFrame(data, schema)

display(df_coa)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
    df_coa.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("d_chart_of_accounts")
)

row_count = df_coa.count()
group_count = df_coa.select("AccountGroup").distinct().count()

print("=" * 60)
print("BRONZE LAYER LOAD SUMMARY")
print("=" * 60)
print("Target Lakehouse : bronze_lakehouse")
print("Target Table     : d_chart_of_accounts")
print(f"Rows Generated   : {row_count}")
print(f"Account Groups   : {group_count}")
print("Load Status      : SUCCESS")
print("=" * 60)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import *

print("Starting Supplier Master Data generation...")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

data = [
(1,"SUP-DAI-001","Nordic Dairy Ingredients","Dairy Supplier","Finland",7,True),
(2,"SUP-DAI-002","Scandinavian Cheese Partners","Dairy Supplier","Sweden",10,True),
(3,"SUP-BEV-001","Baltic Juice Suppliers","Beverage Supplier","Estonia",14,True),
(4,"SUP-BEV-002","Nordic Beverage Group","Beverage Supplier","Finland",7,True),
(5,"SUP-FRO-001","Frozen Foods Manufacturing","Frozen Food Supplier","Finland",14,True),
(6,"SUP-FRO-002","Swedish Ready Meal Co","Frozen Food Supplier","Sweden",10,True),
(7,"SUP-PKG-001","Nordic Packaging Solutions","Packaging Supplier","Finland",5,True),
(8,"SUP-PKG-002","Baltic Food Packaging","Packaging Supplier","Estonia",7,True),
(9,"SUP-SNK-001","Scandinavian Snack Foods","Snack Supplier","Sweden",7,True),
(10,"SUP-SNK-002","Nordic Nut Imports","Snack Supplier","Finland",14,True)
]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema = StructType([
    StructField("SupplierKey", IntegerType(), False),
    StructField("SupplierNumber", StringType(), False),
    StructField("SupplierName", StringType(), False),
    StructField("SupplierCategory", StringType(), False),
    StructField("Country", StringType(), False),
    StructField("LeadTimeDays", IntegerType(), False),
    StructField("IsActive", BooleanType(), False)
])

df_supplier = spark.createDataFrame(data, schema)

display(df_supplier)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
    df_supplier.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("d_supplier")
)

row_count = df_supplier.count()
country_count = df_supplier.select("Country").distinct().count()

print("=" * 60)
print("BRONZE LAYER LOAD SUMMARY")
print("=" * 60)
print("Target Lakehouse : bronze_lakehouse")
print("Target Table     : d_supplier")
print(f"Rows Generated   : {row_count}")
print(f"Countries        : {country_count}")
print("Load Status      : SUCCESS")
print("=" * 60)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import *

print("Starting Customer Master Data generation...")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

data = [
(1,"CUST-FI-001","K-Market Helsinki","Finland","Retail",14,True),
(2,"CUST-FI-002","S-Market Tampere","Finland","Retail",14,True),
(3,"CUST-FI-003","Prisma Vantaa","Finland","Retail",14,True),
(4,"CUST-FI-004","FoodService Finland","Finland","Wholesale",30,True),
(5,"CUST-FI-005","Helsinki University Hospital","Finland","Public Sector",30,True),
(6,"CUST-FI-006","Restaurant Group Finland","Finland","Restaurant",14,True),

(7,"CUST-SE-001","ICA Stockholm","Sweden","Retail",14,True),
(8,"CUST-SE-002","Coop Sweden","Sweden","Retail",14,True),
(9,"CUST-SE-003","FoodService Sweden","Sweden","Wholesale",30,True),
(10,"CUST-SE-004","Restaurant Group Sweden","Sweden","Restaurant",14,True),

(11,"CUST-EE-001","Rimi Tallinn","Estonia","Retail",14,True),
(12,"CUST-EE-002","Selver Tallinn","Estonia","Retail",14,True),
(13,"CUST-EE-003","FoodService Estonia","Estonia","Wholesale",30,True),
(14,"CUST-EE-004","Restaurant Group Estonia","Estonia","Restaurant",14,True),
(15,"CUST-EE-005","Tallinn City Services","Estonia","Public Sector",30,True)
]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema = StructType([
    StructField("CustomerKey", IntegerType(), False),
    StructField("CustomerNumber", StringType(), False),
    StructField("CustomerName", StringType(), False),
    StructField("Country", StringType(), False),
    StructField("Segment", StringType(), False),
    StructField("PaymentTermsDays", IntegerType(), False),
    StructField("IsActive", BooleanType(), False)
])

df_customer = spark.createDataFrame(data, schema)

display(df_customer)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
    df_customer.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("d_customer")
)

row_count = df_customer.count()
country_count = df_customer.select("Country").distinct().count()
segment_count = df_customer.select("Segment").distinct().count()

print("=" * 60)
print("BRONZE LAYER LOAD SUMMARY")
print("=" * 60)
print("Target Lakehouse : bronze_lakehouse")
print("Target Table     : d_customer")
print(f"Rows Generated   : {row_count}")
print(f"Countries        : {country_count}")
print(f"Segments         : {segment_count}")
print("Load Status      : SUCCESS")
print("=" * 60)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import *

print("Starting Warehouse Master Data generation...")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

data = [
(1,"WH-FI-01","Helsinki Distribution Center","Finland","Helsinki","Distribution",True),
(2,"WH-FI-02","Tampere Cold Storage","Finland","Tampere","Cold Storage",True),
(3,"WH-SE-01","Stockholm Distribution Center","Sweden","Stockholm","Distribution",True),
(4,"WH-EE-01","Tallinn Distribution Center","Estonia","Tallinn","Distribution",True),
(5,"WH-CENTRAL","Nordic Central Warehouse","Finland","Vantaa","Central",True)
]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema = StructType([
    StructField("WarehouseKey", IntegerType(), False),
    StructField("WarehouseCode", StringType(), False),
    StructField("WarehouseName", StringType(), False),
    StructField("Country", StringType(), False),
    StructField("City", StringType(), False),
    StructField("WarehouseType", StringType(), False),
    StructField("IsActive", BooleanType(), False)
])

df_warehouse = spark.createDataFrame(data, schema)

display(df_warehouse)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
    df_warehouse.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("d_warehouse")
)

row_count = df_warehouse.count()
country_count = df_warehouse.select("Country").distinct().count()
warehouse_type_count = df_warehouse.select("WarehouseType").distinct().count()

print("=" * 60)
print("BRONZE LAYER LOAD SUMMARY")
print("=" * 60)
print("Target Lakehouse : bronze_lakehouse")
print("Target Table     : d_warehouse")
print(f"Rows Generated   : {row_count}")
print(f"Countries        : {country_count}")
print(f"Warehouse Types  : {warehouse_type_count}")
print("Load Status      : SUCCESS")
print("=" * 60)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import *

print("Starting Lot Master Data generation...")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

data = [
(1,"LOT-2026-000001",1,1,"2026-01-01","2026-01-31",30,False,None,None),
(2,"LOT-2026-000002",2,1,"2026-01-05","2026-02-04",30,False,None,None),
(3,"LOT-2026-000003",3,1,"2026-01-10","2026-02-09",30,False,None,None),

(4,"LOT-2026-000004",4,2,"2026-01-15","2026-05-15",120,False,None,None),
(5,"LOT-2026-000005",5,2,"2026-01-20","2026-05-20",120,False,None,None),
(6,"LOT-2026-000006",6,2,"2026-01-25","2026-05-25",120,False,None,None),

(7,"LOT-2026-000007",10,5,"2026-02-01","2026-07-31",180,False,None,None),
(8,"LOT-2026-000008",11,5,"2026-02-05","2026-08-04",180,False,None,None),
(9,"LOT-2026-000009",12,5,"2026-02-10","2026-08-09",180,False,None,None),

(10,"LOT-2026-000010",1,1,"2026-04-15","2026-05-15",30,True,"2026-10-12","Microbiological Risk")
]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema = StructType([
    StructField("LotKey", IntegerType(), False),
    StructField("LotNumber", StringType(), False),
    StructField("ItemKey", IntegerType(), False),
    StructField("SupplierKey", IntegerType(), False),
    StructField("ProductionDate", StringType(), False),
    StructField("ExpiryDate", StringType(), False),
    StructField("ShelfLifeDays", IntegerType(), False),
    StructField("RecallFlag", BooleanType(), False),
    StructField("RecallDate", StringType(), True),
    StructField("RecallReason", StringType(), True)
])

df_lot = spark.createDataFrame(data, schema)

display(df_lot)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
    df_lot.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("d_lot")
)

row_count = df_lot.count()
recall_count = df_lot.filter("RecallFlag = true").count()

print("=" * 60)
print("BRONZE LAYER LOAD SUMMARY")
print("=" * 60)
print("Target Lakehouse : bronze_lakehouse")
print("Target Table     : d_lot")
print(f"Rows Generated   : {row_count}")
print(f"Recall Lots      : {recall_count}")
print("Load Status      : SUCCESS")
print("=" * 60)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.types import *

print("Starting Date Dimension generation...")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

start_date = "2024-01-01"
end_date = "2026-12-31"

df_date = (
    spark.sql(f"""
    SELECT explode(
        sequence(
            to_date('{start_date}'),
            to_date('{end_date}'),
            interval 1 day
        )
    ) AS Date
    """)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_date = (
    df_date
    .withColumn("DateKey", date_format(col("Date"), "yyyyMMdd").cast("int"))
    .withColumn("Year", year(col("Date")))
    .withColumn("Quarter", concat(lit("Q"), quarter(col("Date"))))
    .withColumn("Month", month(col("Date")))
    .withColumn("MonthName", date_format(col("Date"), "MMMM"))
    .withColumn("MonthShortName", date_format(col("Date"), "MMM"))
    .withColumn("Week", weekofyear(col("Date")))
    .withColumn("DayOfMonth", dayofmonth(col("Date")))
    .withColumn("DayOfWeek", dayofweek(col("Date")))
    .withColumn("DayName", date_format(col("Date"), "EEEE"))
    .withColumn(
        "IsWeekend",
        when(dayofweek(col("Date")).isin([1, 7]), True).otherwise(False)
    )
)

display(df_date)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
    df_date.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("d_date")
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

row_count = df_date.count()

min_date = df_date.agg(min("Date")).collect()[0][0]
max_date = df_date.agg(max("Date")).collect()[0][0]

print("=" * 60)
print("BRONZE LAYER LOAD SUMMARY")
print("=" * 60)
print("Target Lakehouse : bronze_lakehouse")
print("Target Table     : d_date")
print(f"Rows Generated   : {row_count}")
print(f"Start Date       : {min_date}")
print(f"End Date         : {max_date}")
print("Load Status      : SUCCESS")
print("=" * 60)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.types import *

print("Starting Purchase Price Fact generation...")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_item = spark.table("d_item")

print(f"Items Found: {df_item.count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col, lit

df_purchase_price = (
    df_item
    .select(
        col("ItemKey"),
        col("StandardCost").alias("PurchasePrice")
    )
    .withColumn("PriceKey", col("ItemKey"))
    .withColumn("SupplierKey", lit(1))
    .withColumn("ValidFromDate", lit("2026-01-01"))
    .withColumn("ValidToDate", lit("2026-12-31"))
)

display(df_purchase_price)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

event_data = [
(1001,6,2,"2026-01-01","2026-03-31",3.40),
(1002,6,2,"2026-04-01","2026-06-30",3.75),
(1003,6,2,"2026-07-01","2026-12-31",4.15)
]

event_schema = StructType([
    StructField("PriceKey", IntegerType(), False),
    StructField("ItemKey", IntegerType(), False),
    StructField("SupplierKey", IntegerType(), False),
    StructField("ValidFromDate", StringType(), False),
    StructField("ValidToDate", StringType(), False),
    StructField("PurchasePrice", DoubleType(), False)
])

df_event_001 = spark.createDataFrame(
    event_data,
    event_schema
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_purchase_price = (
    df_purchase_price
    .filter(col("ItemKey") != 6)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_purchase_price = (
    df_purchase_price
    .unionByName(df_event_001)
)

display(df_purchase_price)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
    df_purchase_price.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("f_purchase_price")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

row_count = df_purchase_price.count()

event_rows = (
    df_purchase_price
    .filter(col("ItemKey") == 6)
    .count()
)

print("=" * 60)
print("BRONZE LAYER LOAD SUMMARY")
print("=" * 60)
print("Target Lakehouse : bronze_lakehouse")
print("Target Table     : f_purchase_price")
print(f"Rows Generated   : {row_count}")
print(f"Event 001 Rows   : {event_rows}")
print("Load Status      : SUCCESS")
print("=" * 60)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.types import *

print("Starting Purchase Invoice Fact generation...")

data = [

("PI-2026-000001",1,"2026-01-01",1,1,1,2,500,0.75,375.00),
("PI-2026-000001",2,"2026-01-01",1,2,2,2,400,0.75,300.00),
("PI-2026-000001",3,"2026-01-01",1,3,3,2,300,0.75,225.00),

("PI-2026-000002",1,"2026-01-05",2,4,4,2,300,3.20,960.00),
("PI-2026-000002",2,"2026-01-05",2,5,5,2,250,3.00,750.00),
("PI-2026-000002",3,"2026-01-05",2,6,6,2,200,3.40,680.00),

("PI-2026-000003",1,"2026-02-01",5,10,7,5,600,1.85,1110.00),
("PI-2026-000003",2,"2026-02-01",5,11,8,5,500,1.60,800.00),
("PI-2026-000003",3,"2026-02-01",5,12,9,5,450,1.95,877.50),

("PI-2026-000004",1,"2026-04-15",1,1,10,2,700,0.82,574.00),

# Event 001

("PI-2026-000100",1,"2026-01-15",2,6,6,2,500,3.40,1700.00),
("PI-2026-000200",1,"2026-04-15",2,6,6,2,500,3.75,1875.00),
("PI-2026-000300",1,"2026-07-15",2,6,6,2,500,4.15,2075.00)

]

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

spark.sql("""
DROP TABLE IF EXISTS f_purchase_invoice_line
""")

(
    df_purchase_invoice.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("f_purchase_invoice_line")
)

row_count = df_purchase_invoice.count()

event_rows = (
    df_purchase_invoice
    .filter(col("ItemKey") == 6)
    .count()
)

invoice_count = (
    df_purchase_invoice
    .select("PurchaseInvoiceNumber")
    .distinct()
    .count()
)

print("=" * 60)
print("BRONZE LAYER LOAD SUMMARY")
print("=" * 60)
print("Target Lakehouse : bronze_lakehouse")
print("Target Table     : f_purchase_invoice_line")
print(f"Rows Generated   : {row_count}")
print(f"Invoices         : {invoice_count}")
print(f"Event 001 Rows   : {event_rows}")
print("Load Status      : SUCCESS")
print("=" * 60)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.types import *

print("Starting Sales Invoice Fact generation...")

data = [

# Normal Sales

("SI-2026-000001",1,"2026-01-10",1,1,1,2,300,1.95,0.00,585.00),
("SI-2026-000001",2,"2026-01-10",1,2,2,2,250,1.95,0.00,487.50),

("SI-2026-000002",1,"2026-01-15",2,10,7,5,200,4.90,0.00,980.00),
("SI-2026-000002",2,"2026-01-15",2,11,8,5,180,4.50,0.00,810.00),

("SI-2026-000003",1,"2026-02-01",3,16,1,2,400,2.50,0.00,1000.00),
("SI-2026-000003",2,"2026-02-01",3,17,2,2,350,2.40,0.00,840.00),

# Event 001 - Cheddar Cheese Sales

("SI-2026-000500",1,"2026-07-20",1,6,6,2,300,7.20,0.00,2160.00),

# Event 002 - Promotion Campaign

("SI-2026-000600",1,"2026-06-05",1,10,7,5,150,4.90,73.50,661.50),

("SI-2026-000601",1,"2026-06-10",2,11,8,5,180,4.50,81.00,729.00),

("SI-2026-000602",1,"2026-06-15",3,12,9,5,200,5.20,104.00,936.00)

]

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

spark.sql("""
DROP TABLE IF EXISTS f_sales_invoice_line
""")

(
    df_sales_invoice.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("f_sales_invoice_line")
)

row_count = df_sales_invoice.count()

invoice_count = (
    df_sales_invoice
    .select("SalesInvoiceNumber")
    .distinct()
    .count()
)

promotion_rows = (
    df_sales_invoice
    .filter(col("DiscountAmount") > 0)
    .count()
)

print("=" * 60)
print("BRONZE LAYER LOAD SUMMARY")
print("=" * 60)
print("Target Lakehouse : bronze_lakehouse")
print("Target Table     : f_sales_invoice_line")
print(f"Rows Generated   : {row_count}")
print(f"Invoices         : {invoice_count}")
print(f"Promotion Rows   : {promotion_rows}")
print("Load Status      : SUCCESS")
print("=" * 60)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
