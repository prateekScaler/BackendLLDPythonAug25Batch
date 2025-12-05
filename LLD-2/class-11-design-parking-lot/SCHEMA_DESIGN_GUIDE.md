# Schema Design Guide - Parking Lot System

## Overview
This guide provides simple, practical tips for designing a database schema for the parking lot system. The schema should mirror your class diagram while considering database-specific concerns like indexing and querying patterns.

## Core Principles

### 1. One Table Per Entity
Each major class from your class diagram typically becomes a table:
- `parking_lot`
- `parking_floor`
- `parking_spot`
- `parking_ticket`
- `invoice`
- `payment`
- `vehicle`
- `parking_attendant`
- `parking_gate`

### 2. Foreign Keys for Relationships
Use foreign keys to represent relationships between entities:
```sql
-- Example: ParkingFloor belongs to ParkingLot
CREATE TABLE parking_floor (
    id INT PRIMARY KEY,
    floor_number INT NOT NULL,
    parking_lot_id INT NOT NULL,
    FOREIGN KEY (parking_lot_id) REFERENCES parking_lot(id)
);
```

### 3. Enums as VARCHAR or Separate Tables
For simple enums (status, type), use VARCHAR:
```sql
status VARCHAR(20) CHECK (status IN ('OCCUPIED', 'FREE', 'OUT_OF_ORDER'))
```

For complex enums with additional data, consider separate tables.

## Schema Tables

### parking_lot
```sql
id (INT, PRIMARY KEY)
name (VARCHAR)
address (VARCHAR)
created_at (TIMESTAMP)
```

### parking_floor
```sql
id (INT, PRIMARY KEY)
floor_number (INT)
parking_lot_id (INT, FOREIGN KEY)
```

### parking_spot
```sql
id (INT, PRIMARY KEY)
spot_number (INT)
spot_type (VARCHAR) -- SMALL, MEDIUM, LARGE
status (VARCHAR) -- OCCUPIED, FREE, OUT_OF_ORDER
parking_floor_id (INT, FOREIGN KEY)
```

### parking_ticket
```sql
id (INT, PRIMARY KEY)
ticket_id (VARCHAR, UNIQUE)
entry_time (TIMESTAMP)
parking_spot_id (INT, FOREIGN KEY)
vehicle_id (INT, FOREIGN KEY)
entry_gate_id (INT, FOREIGN KEY)
operator_id (INT, FOREIGN KEY)
```

### vehicle
```sql
id (INT, PRIMARY KEY)
license_plate (VARCHAR, UNIQUE)
vehicle_type (VARCHAR) -- CAR, TRUCK, BUS, BIKE, SCOOTER
```

### invoice
```sql
id (INT, PRIMARY KEY)
invoice_id (VARCHAR, UNIQUE)
exit_time (TIMESTAMP)
amount (DECIMAL)
parking_ticket_id (INT, FOREIGN KEY, UNIQUE)
payment_id (INT, FOREIGN KEY)
```

### payment
```sql
id (INT, PRIMARY KEY)
amount (DECIMAL)
payment_type (VARCHAR) -- CASH, CREDIT_CARD, UPI
status (VARCHAR) -- DONE, PENDING
payment_time (TIMESTAMP)
parking_ticket_id (INT, FOREIGN KEY)
```

### parking_gate
```sql
id (INT, PRIMARY KEY)
gate_id (VARCHAR)
gate_type (VARCHAR) -- ENTRY, EXIT
parking_lot_id (INT, FOREIGN KEY)
current_attendant_id (INT, FOREIGN KEY)
```

### parking_attendant
```sql
id (INT, PRIMARY KEY)
name (VARCHAR)
email (VARCHAR, UNIQUE)
```

## Indexing Strategy

Indexes speed up queries but slow down writes. Index columns that appear frequently in WHERE, JOIN, and ORDER BY clauses.

### When to Add Indexes

#### 1. Primary Keys (Automatic)
All primary keys automatically get indexes. No action needed.

#### 2. Foreign Keys
**Always index foreign keys** - they're used in JOINs constantly.
```sql
CREATE INDEX idx_parking_floor_lot ON parking_floor(parking_lot_id);
CREATE INDEX idx_parking_spot_floor ON parking_spot(parking_floor_id);
CREATE INDEX idx_ticket_spot ON parking_ticket(parking_spot_id);
CREATE INDEX idx_ticket_vehicle ON parking_ticket(vehicle_id);
```

**Why**: Finding all floors in a parking lot, all spots on a floor, or all tickets for a vehicle would require full table scans without indexes.

#### 3. Status Fields (Frequent Filters)
Index status columns when you frequently query by status:
```sql
CREATE INDEX idx_parking_spot_status ON parking_spot(status);
```

**Why**: "Find all available spots" queries will be much faster. This query runs every time someone enters the parking lot.

#### 4. Composite Indexes for Common Query Patterns
If you often filter by multiple columns together:
```sql
CREATE INDEX idx_spot_floor_status ON parking_spot(parking_floor_id, status);
```

**Why**: "Find available spots on floor 2" queries both columns. A composite index is more efficient than two separate indexes.

#### 5. Unique Constraints
Add unique indexes on columns that must be unique:
```sql
CREATE UNIQUE INDEX idx_vehicle_license ON vehicle(license_plate);
CREATE UNIQUE INDEX idx_ticket_id ON parking_ticket(ticket_id);
```

**Why**: Prevents duplicate license plates or ticket IDs and speeds up lookups by these values.

#### 6. Timestamp Columns (For Range Queries)
Index timestamps used in range queries:
```sql
CREATE INDEX idx_ticket_entry_time ON parking_ticket(entry_time);
```

**Why**: Queries like "tickets created in last hour" or "revenue for today" need to scan timestamps.

### When NOT to Index

- **Small tables** (< 1000 rows): Full table scans are faster
- **Columns with low cardinality**: e.g., a boolean with only 2 values
- **Rarely queried columns**: Only index what you actually query
- **Write-heavy columns**: Every insert/update/delete must update indexes

## Common Query Patterns

Understanding your queries helps design better schemas and indexes:

### 1. Finding Available Spots
```sql
SELECT * FROM parking_spot
WHERE parking_floor_id = ?
AND status = 'FREE'
AND spot_type = 'MEDIUM';
```
**Index needed**: `(parking_floor_id, status, spot_type)`

### 2. Getting Active Tickets
```sql
SELECT * FROM parking_ticket
WHERE parking_spot_id = ?
AND exit_time IS NULL;
```
**Index needed**: `(parking_spot_id)` or `(parking_spot_id, exit_time)`

### 3. Vehicle History
```sql
SELECT * FROM parking_ticket
WHERE vehicle_id = ?
ORDER BY entry_time DESC;
```
**Index needed**: `(vehicle_id, entry_time)`

### 4. Revenue Calculation
```sql
SELECT SUM(amount) FROM invoice
WHERE exit_time BETWEEN ? AND ?;
```
**Index needed**: `(exit_time)`

## Best Practices

### 1. Use Appropriate Data Types
- IDs: `INT` or `BIGINT` (auto-increment)
- Money: `DECIMAL(10,2)` (never FLOAT for currency)
- Timestamps: `TIMESTAMP` or `DATETIME`
- Status/Type: `VARCHAR(50)`
- Text: `VARCHAR(255)` for short text, `TEXT` for long content

### 2. Always Include Timestamps
Add `created_at` and `updated_at` to every table:
```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

**Why**: Debugging, auditing, and analytics become much easier.

### 3. NOT NULL Constraints
Use `NOT NULL` for fields that must have values:
```sql
parking_lot_id INT NOT NULL
```

### 4. Soft Deletes (Optional)
Instead of deleting records, mark them as deleted:
```sql
deleted_at TIMESTAMP NULL
```

**Why**: Preserves data for auditing and can be restored if needed.

### 5. Start Simple, Optimize Later
- Begin with basic schema and obvious indexes (PKs, FKs)
- Monitor slow queries in production
- Add indexes based on actual usage patterns
- Don't over-index early - it's easier to add than remove

## Migration Strategy

1. **Design schema based on class diagram**
2. **Add primary keys and foreign keys**
3. **Index all foreign keys**
4. **Add indexes for status/type fields**
5. **Deploy and monitor**
6. **Analyze slow query logs**
7. **Add composite indexes based on real query patterns**

## Example: Complete parking_spot Table

```sql
CREATE TABLE parking_spot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    spot_number INT NOT NULL,
    spot_type VARCHAR(20) NOT NULL CHECK (spot_type IN ('SMALL', 'MEDIUM', 'LARGE')),
    status VARCHAR(20) NOT NULL DEFAULT 'FREE' CHECK (status IN ('OCCUPIED', 'FREE', 'OUT_OF_ORDER')),
    parking_floor_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (parking_floor_id) REFERENCES parking_floor(id),
    INDEX idx_floor_id (parking_floor_id),
    INDEX idx_status (status),
    INDEX idx_floor_status_type (parking_floor_id, status, spot_type)
);
```

## Common Mistakes to Avoid

1. **Forgetting to index foreign keys** - Leads to slow JOINs
2. **Over-indexing** - Slows down writes unnecessarily
3. **Using FLOAT for money** - Causes rounding errors
4. **No timestamps** - Makes debugging impossible
5. **No unique constraints** - Allows duplicate data
6. **Missing NOT NULL constraints** - Creates data quality issues

## Summary

- **Mirror your class diagram** in database tables
- **Index foreign keys and frequently queried columns**
- **Use appropriate data types** (especially DECIMAL for money)
- **Add timestamps** to every table
- **Start simple**, optimize based on real usage
- **Monitor slow queries** and add indexes as needed
