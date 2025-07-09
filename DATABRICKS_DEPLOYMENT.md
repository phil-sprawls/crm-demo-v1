# EDIP CRM - Databricks Unity Catalog Integration

## Overview

This implementation provides a production-ready EDIP CRM system with full Unity Catalog database integration, replacing the in-memory data storage with persistent database tables.

## Database Architecture

### Unity Catalog Structure
```
edip_crm                    (Catalog)
└── main                    (Schema)
    ├── accounts            (Delta Table)
    ├── platforms_status    (Delta Table)
    ├── use_cases          (Delta Table)
    └── updates            (Delta Table)
```

### Table Schemas

#### accounts
- `bsnid` (STRING, PRIMARY KEY)
- `team` (STRING)
- `business_area` (STRING)
- `vp` (STRING)
- `admin` (STRING)
- `primary_it_partner` (STRING)
- `azure_devops_link` (STRING)
- `artifacts_folder_link` (STRING)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

#### platforms_status
- `id` (STRING, PRIMARY KEY)
- `account_bsnid` (STRING, FOREIGN KEY)
- `platform` (STRING)
- `status` (STRING)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

#### use_cases
- `id` (STRING, PRIMARY KEY)
- `account_bsnid` (STRING, FOREIGN KEY)
- `problem` (STRING)
- `solution` (STRING)
- `leader` (STRING)
- `status` (STRING)
- `enablement_tier` (STRING)
- `platform` (STRING)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

#### updates
- `id` (STRING, PRIMARY KEY)
- `account_bsnid` (STRING, FOREIGN KEY)
- `author` (STRING)
- `date` (DATE)
- `platform` (STRING)
- `description` (STRING)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

## Authentication & Configuration

### Required Environment Variables/Secrets

#### For Databricks Apps Deployment:
```bash
DATABRICKS_SERVER_HOSTNAME="your-workspace.cloud.databricks.com"
DATABRICKS_HTTP_PATH="/sql/1.0/warehouses/your-warehouse-id"
DATABRICKS_TOKEN="your-access-token"
```

#### For Local Development (.streamlit/secrets.toml):
```toml
DATABRICKS_SERVER_HOSTNAME = "your-workspace.cloud.databricks.com"
DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/your-warehouse-id"
DATABRICKS_TOKEN = "your-personal-access-token"
```

### Authentication Methods Supported

1. **Personal Access Token (PAT)** - For development
2. **Service Principal OAuth** - For production
3. **On-behalf-of-user** - For Databricks Apps with user context

## Key Features

### Database Integration
- **Automatic table creation** with proper Delta Lake format
- **Foreign key relationships** for data integrity
- **Sample data initialization** for immediate usability
- **Connection caching** for optimal performance

### Data Management
- **Real-time database operations** - all CRUD operations persist to Unity Catalog
- **Search functionality** with SQL-based filtering
- **Relationship management** between accounts, use cases, and updates
- **Transaction safety** with proper error handling

### Performance Optimizations
- **Connection pooling** using `@st.cache_resource`
- **Arrow format** for efficient data transfer
- **Lazy loading** of related data
- **Optimized queries** with proper indexing

## Deployment Options

### Option 1: Replace Existing Deployed App
1. Replace `app.py` content with `app_databricks.py`
2. Update `requirements.txt` with `databricks-requirements.txt`
3. Configure Databricks connection secrets
4. Redeploy the app

### Option 2: Create New Database-Backed App
1. Create new Databricks App
2. Upload files:
   - `app_databricks.py` → `app.py`
   - `databricks-requirements.txt` → `requirements.txt`
   - `app.yaml` (same command configuration)
   - `.streamlit/config.toml` (same theme)

## Setup Instructions

### Step 1: Databricks Prerequisites
1. **SQL Warehouse** - Ensure you have a running SQL warehouse
2. **Unity Catalog** - Must be enabled in your workspace
3. **Permissions** - User/service principal needs:
   - `CREATE CATALOG` permission (or use existing catalog)
   - `CREATE SCHEMA` permission
   - `CREATE TABLE` permission
   - `SELECT`, `INSERT`, `UPDATE`, `DELETE` on tables

### Step 2: Configure Authentication
1. **Generate Personal Access Token** in Databricks workspace
2. **Get SQL Warehouse HTTP Path** from warehouse details
3. **Set environment variables** or Streamlit secrets

### Step 3: Deploy Application
1. **Upload database-enabled app** to Databricks Apps
2. **Configure secrets** in the app environment
3. **Test connection** - app will auto-create tables on first run

### Step 4: Verify Database Integration
1. **Check table creation** in Unity Catalog
2. **Verify sample data** loads correctly
3. **Test all CRUD operations** through the UI

## Data Migration

### From Existing In-Memory App
If you have existing data in the in-memory version:

1. **Export current data** using the admin functions
2. **Format for database insertion** matching table schemas
3. **Use SQL INSERT statements** to populate Unity Catalog tables
4. **Verify data integrity** after migration

### Sample Data Included
The app automatically loads sample data including:
- 5 business accounts with complete information
- Platform status tracking for all major platforms
- Sample use cases with realistic scenarios
- Recent updates with proper chronological order

## Advanced Features

### Real-Time Collaboration
- Multiple users can access the same data simultaneously
- All changes are immediately visible to other users
- Proper concurrency handling with Delta Lake

### Audit Trail
- All tables include `created_at` and `updated_at` timestamps
- Full history tracking with Delta Lake time travel
- Ability to query historical states of data

### Scalability
- Unity Catalog can handle enterprise-scale data
- Delta Lake provides ACID transactions
- Horizontal scaling through Databricks compute

### Security
- Row-level security available through Unity Catalog
- Column-level permissions supported
- Integration with existing authentication systems

## Troubleshooting

### Connection Issues
- Verify SQL warehouse is running
- Check network connectivity to Databricks
- Validate access token permissions

### Permission Errors
- Ensure Unity Catalog is enabled
- Verify user has catalog/schema creation rights
- Check table-level permissions

### Performance Issues
- Monitor SQL warehouse auto-scaling
- Consider query optimization for large datasets
- Review connection caching configuration

## Support & Maintenance

### Monitoring
- Use Databricks SQL query history for performance monitoring
- Set up alerts for connection failures
- Monitor Unity Catalog usage metrics

### Backup & Recovery
- Delta Lake provides automatic versioning
- Configure retention policies for historical data
- Set up regular metadata backups

### Updates & Patches
- Database schema changes require migration scripts
- Use Delta Lake ALTER TABLE for schema evolution
- Test changes in development environment first

---

**Created:** $(date)
**Version:** Unity Catalog Integration v1.0
**Dependencies:** Databricks Runtime 11.3+ with Unity Catalog enabled