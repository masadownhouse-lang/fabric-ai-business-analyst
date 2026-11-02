# Source To Target Mapping

## Sales Invoice

### Source

Sales Invoice Header
Sales Invoice Line

### Target

FactSalesInvoiceLine

Key Columns

- Invoice Number
- Invoice Date
- Customer
- Product
- Lot Number
- Quantity
- Unit Price
- Revenue

---

## Purchase Invoice

### Source

Purchase Invoice Header
Purchase Invoice Line

### Target

FactPurchaseInvoiceLine

Key Columns

- Purchase Invoice Number
- Supplier
- Product
- Lot Number
- Quantity
- Unit Cost
- Cost Amount

---

## Inventory

### Source

Inventory Transactions

### Target

FactInventoryTransaction

Transaction Types

- Purchase
- Sale
- Transfer
- Adjustment
- Write-Off
- Recall

---

## Finance

### Source

GL Entries

### Target

FactGLEntry

Key Columns

- Posting Date
- Account
- Amount
- Document Number
