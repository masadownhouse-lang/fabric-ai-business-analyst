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
