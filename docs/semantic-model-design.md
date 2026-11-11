# Semantic Model Design

## Event 001

### Business Question

Why did EBITDA decrease?

### Required Measures

Revenue

COGS

Gross Margin

Operating Expenses

EBITDA

### Required Dimensions

DimDate

DimItem

DimSupplier

DimChartOfAccounts

### Required Facts

FactPurchasePrice

FactPurchaseInvoiceLine

FactGLEntry

### Root Cause Path

Purchase Price Increase
↓
4010 Dairy Raw Materials
↓
COGS
↓
Gross Margin
↓
EBITDA

## Measures

### Revenue

Revenue =
Sales Revenue
- Discounts

### COGS

COGS =
Raw Materials
+ Packaging
+ Freight

### Gross Margin

Gross Margin =
Revenue - COGS

### Gross Margin %

Gross Margin / Revenue

### Operating Expenses

Personnel
+ Warehouse
+ Marketing
+ Administration
+ Write-Offs

### EBITDA

Gross Margin
- Operating Expenses
## Event 001 Validation

Business Event

Purchase Price Increase

Expected Metric Impact

Revenue

No significant impact

COGS

Increase

Gross Margin

Decrease

Gross Margin %

Decrease

Operating Expenses

No direct impact

EBITDA

Decrease

Expected AI Explanation

EBITDA decreased because purchase costs increased.

The largest contributor was Dairy Raw Materials (Account 4010) driven by increased purchase prices for DAI-CHS-003 Cheddar Cheese 1kg.
