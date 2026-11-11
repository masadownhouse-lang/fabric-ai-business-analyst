# Root Cause Analysis

## Event 001

Business Event

Purchase Price Increase

### Root Cause Path

Purchase Price Increase

↓

FactPurchasePrice

↓

FactPurchaseInvoiceLine

↓

4010 Dairy Raw Materials

↓

COGS Increase

↓

Gross Margin Decrease

↓

EBITDA Decrease

### Affected Product

DAI-CHS-003

Cheddar Cheese 1kg

### Supporting Transactions

Purchase Price History

- 2026-01-01 → 3.40 €
- 2026-04-01 → 3.75 €
- 2026-07-01 → 4.15 €

Purchase Invoices

- PI-2026-000100
- PI-2026-000200
- PI-2026-000300

Sales Invoices

- SI-2026-000500

### Affected Account

- 4010 Dairy Raw Materials

### Affected KPIs

- COGS
- Gross Margin
- EBITDA

### Expected AI Answer

EBITDA decreased due to increased dairy raw material costs.

The primary contributing factor was the increase in Cheddar Cheese 1kg purchase prices from 3.40 € to 4.15 € during 2026.

The increased purchase costs were recorded on account 4010 Dairy Raw Materials and resulted in higher COGS, lower Gross Margin and lower EBITDA.

Supporting evidence was found in:

- FactPurchasePrice
- FactPurchaseInvoiceLine
- FactGLEntry

---

## Root Cause Query Example 001

Question

Why did EBITDA decrease in July 2026?

Analysis Path

EBITDA

↓

Gross Margin

↓

COGS

↓

4010 Dairy Raw Materials

↓

DAI-CHS-003 Cheddar Cheese 1kg

↓

Purchase Price Increase

Evidence

Purchase Price

2026-01-01 → 3.40 €

2026-04-01 → 3.75 €

2026-07-01 → 4.15 €

Supporting Transactions

PI-2026-000100

PI-2026-000200

PI-2026-000300

Expected AI Conclusion

EBITDA decreased because dairy raw material costs increased.

The largest contributing factor was Cheddar Cheese 1kg, whose purchase price increased from 3.40 € to 4.15 € during 2026.

The increase was recorded on account 4010 Dairy Raw Materials, increasing COGS and reducing Gross Margin.
