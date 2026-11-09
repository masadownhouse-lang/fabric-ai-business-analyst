# Data Model

## Dimensions

### DimDate

Calendar dimension used by all fact tables.

### DimCustomer

Customer master data.

Attributes:

- Customer ID
- Customer Name
- Country
- Customer Segment

### DimSupplier

Supplier master data.

Attributes:

- Supplier ID
- Supplier Name
- Country

### DimItem

Product master data.

Attributes:

- Item Number
- Item Name
- Category Level 1
- Category Level 2
- Category Level 3
- Brand
- Shelf Life Days

### DimLot

Lot / Batch tracking information.

Attributes:

- Lot Number
- Production Date
- Expiry Date

### DimWarehouse

Warehouse information.

### DimChartOfAccounts

General Ledger account hierarchy.

Attributes:

- Account Number
- Account Name
- Account Group
- Account Category

### DimPromotion

Sales campaigns and promotions.

---

## Facts

## FactSalesInvoiceLine

Represents sales invoice line transactions.

### Grain

One row = one sales invoice line.

### Keys

- CustomerKey
- ItemKey
- LotKey
- WarehouseKey

### Document Information

- SalesInvoiceNumber
- SalesInvoiceLineNumber

### Quantities

- Quantity

### Pricing

- UnitPrice
- LineAmount
- DiscountAmount
- NetAmount

### Dates

- InvoiceDate


## FactPurchaseInvoiceLine

Represents purchase invoice lines received from suppliers.

### Grain

One row = one purchase invoice line.

### Keys

- InvoiceDateKey
- SupplierKey
- ItemKey
- LotKey
- WarehouseKey

### Document Information

- PurchaseInvoiceNumber
- PurchaseInvoiceLineNumber

### Quantities

- Quantity

### Costs

- UnitCost
- LineAmount

### Dates

- InvoiceDate

### Audit

- CreatedDate

## FactInventoryTransaction

Represents all inventory movements.

### Grain

One row = one inventory transaction.

### Keys

- TransactionDate
- ItemKey
- LotKey
- WarehouseKey

### Attributes

- InventoryTransactionNumber
- TransactionType

### Quantities

- Quantity
- UnitCost
- Amount

### References

- PurchaseInvoiceNumber
- SalesInvoiceNumber

### FactInventorySnapshot

Daily inventory balances and inventory value.

## FactGLEntry

Represents General Ledger postings.

### Grain

One row = one general ledger entry.

### Keys

- PostingDate
- AccountKey

### Document Information

- GLEntryNumber
- DocumentNumber
- DocumentType

### References

- CustomerKey
- SupplierKey
- ItemKey

### Financial Information

- Amount

### Organization

- Country
- BusinessUnit


### FactSalesPrice

Sales price history.

### FactPurchasePrice

Purchase price history.
