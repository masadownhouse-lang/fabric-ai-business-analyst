# KPI Definitions

## Revenue

Definition

Total invoiced sales revenue after discounts.

Source

FactGLEntry

Related Accounts

- 3000 Sales Revenue Finland
- 3010 Sales Revenue Sweden
- 3020 Sales Revenue Estonia
- 3100 Sales Discounts
- 3110 Campaign Discounts

Formula

Revenue =
Sales Revenue Finland
+ Sales Revenue Sweden
+ Sales Revenue Estonia
- Sales Discounts
- Campaign Discounts

Business Meaning

Measures invoiced sales generated from customers after discounts.

Root Cause Drivers

- Sales Volume Changes
- Sales Price Changes
- Product Mix Changes
- Campaign Discounts

---

## COGS (Cost of Goods Sold)

Definition

Direct costs associated with sold products.

Source

FactGLEntry

Related Accounts

- 4000 Raw Materials
- 4010 Dairy Raw Materials
- 4020 Frozen Food Raw Materials
- 4030 Beverage Raw Materials
- 4100 Packaging Cost
- 4200 Freight Cost

Formula

COGS =
Raw Materials
+ Packaging Cost
+ Freight Cost

Business Meaning

Represents the direct cost of generating revenue.

Root Cause Drivers

- Purchase Price Changes
- Supplier Changes
- Freight Cost Changes
- Product Mix Changes

---

## Gross Margin

Formula

Gross Margin =
Revenue
- COGS

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

Root Cause Drivers

- Demand Changes
- Overstocking
- Purchasing Decisions

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
- Slow Moving Products

---

## Write-Off Value

Definition

Inventory value removed due to expiry, damage or recall.

Source

FactGLEntry

Related Accounts

- 5400 Inventory Write-Off
- 5410 Expiry Write-Off
- 5420 Recall Write-Off

Business Meaning

Measures inventory losses.

Root Cause Drivers

- Product Expiry
- Product Recall
- Inventory Damage

---

## Operating Expenses

Definition

Operating costs excluding Cost of Goods Sold.

Source

FactGLEntry

Related Accounts

- 5000 Warehouse Personnel Cost
- 5010 Sales Personnel Cost
- 5020 Administration Personnel Cost
- 5100 Warehouse Cost
- 5110 Cold Storage Cost
- 5200 Marketing Cost
- 5210 Campaign Cost
- 5300 Administration Cost
- 5400 Inventory Write-Off
- 5410 Expiry Write-Off
- 5420 Recall Write-Off

Business Meaning

Represents costs required to run the business.

Root Cause Drivers

- Personnel Changes
- Marketing Campaigns
- Inventory Losses
- Storage Costs

---

## EBITDA

Formula

Gross Margin
- Operating Expenses

Business Meaning

Measures operating profitability before depreciation and amortization.

Root Cause Drivers

- Revenue Changes
- COGS Changes
- Operating Expense Changes

Analysis Expectations

When EBITDA decreases:

1. Analyze Revenue variance
2. Analyze COGS variance
3. Analyze Operating Expense variance
4. Identify top contributing account groups
5. Identify top contributing account categories
6. Quantify impact in euros
7. Link findings to business events

---

## EBIT

Formula

EBITDA
- Depreciation
- Amortization

Source

FactGLEntry

Related Accounts

- 6000 Depreciation
- 6010 Amortization

Business Meaning

Measures operating profit after depreciation and amortization.
