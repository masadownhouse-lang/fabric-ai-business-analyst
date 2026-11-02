# KPI Definitions

## Revenue

Definition

Total invoiced sales revenue.

Source

FactSalesInvoiceLine

Business Meaning

Measures total sales generated from customers.

---

## COGS (Cost of Goods Sold)

Definition

Direct costs associated with sold products.

Source

FactGLEntry

Account Categories

- Raw Materials
- Packaging
- Transportation

Business Meaning

Represents the direct cost of generating revenue.

---

## Gross Margin

Formula

Revenue - COGS

Business Meaning

Measures product profitability before operating expenses.

Root Cause Drivers

- Purchase Price Changes
- Sales Price Changes
- Promotions
- Inventory Write-Offs

---

## Gross Margin %

Formula

Gross Margin / Revenue

Business Meaning

Measures profitability efficiency.

---

## Inventory Value

Definition

Current value of inventory on hand.

Source

FactInventorySnapshot

Business Meaning

Represents capital tied up in inventory.

---

## Inventory Turnover

Formula

COGS / Average Inventory Value

Business Meaning

Measures how efficiently inventory is sold.

Root Cause Drivers

- Demand Changes
- Overstock
- Forecasting Errors

---

## Write-Off Value

Definition

Inventory value removed due to expiry, damage or recall.

Source

FactInventoryTransaction

Transaction Types

- Write-Off
- Recall

Business Meaning

Measures inventory losses.

---

## EBITA

Formula

Revenue
- COGS
- Operating Expenses

Business Meaning

Measures operating profitability.

Root Cause Drivers

- Revenue Changes
- Purchase Cost Changes
- Inventory Write-Offs
- Operating Expense Changes

Analysis Expectations

When EBITA decreases:

1. Analyze Revenue change
2. Analyze COGS change
3. Analyze Operating Expense change
4. Quantify contribution of each driver
