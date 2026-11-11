# Ontology Design

## Entities

Customer
Supplier
Product
Lot
Warehouse

## Metrics

Revenue
Gross Margin
EBITDA

## Business Events

Purchase Price Increase

## Relationships

Supplier supplies Product

Product belongs to Lot

Lot stored in Warehouse

Product sold to Customer

Purchase Price Increase impacts COGS

COGS impacts Gross Margin

Gross Margin impacts EBITDA

## Root Cause Relationships

Purchase Price Increase

impacts

COGS

COGS

impacts

Gross Margin

Gross Margin

impacts

EBITDA

---

Promotion Campaign

impacts

Revenue

Promotion Campaign

impacts

Gross Margin %

Promotion Campaign

impacts

Operating Expenses

Operating Expenses

impacts

EBITDA
