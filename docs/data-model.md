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

### FactSalesInvoiceLine

Sales invoice line transactions.

### FactPurchaseInvoiceLine

Purchase invoice line transactions.

### FactInventoryTransaction

Inventory movements.

Examples:

- Purchase
- Sale
- Transfer
- Adjustment
- Write-Off
- Recall

### FactInventorySnapshot

Daily inventory balances and inventory value.

### FactGLEntry

General Ledger transactions.

### FactSalesPrice

Sales price history.

### FactPurchasePrice

Purchase price history.
