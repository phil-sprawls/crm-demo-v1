# Databricks Permissions Guide for EDIP CRM

## Overview

The database integration requires specific Unity Catalog permissions to create and manage CRM tables in your authorized schema.

## Required Permissions

### Minimum Required Access
1. **SQL Warehouse Access** - Connect to compute resources
2. **USE CATALOG** - Access `corporate_information_technology_raw_dev_000`
3. **USE SCHEMA** - Access `developer_psprawls` schema
4. **CREATE TABLE** - Create new tables in the schema
5. **SELECT/INSERT/UPDATE** - Read and write data

### Complete Permission List
```sql
-- Catalog level
GRANT USE CATALOG ON CATALOG corporate_information_technology_raw_dev_000 TO [user];

-- Schema level  
GRANT USE SCHEMA ON SCHEMA corporate_information_technology_raw_dev_000.developer_psprawls TO [user];
GRANT CREATE TABLE ON SCHEMA corporate_information_technology_raw_dev_000.developer_psprawls TO [user];

-- Table level (after tables are created)
GRANT SELECT, INSERT, UPDATE ON TABLE corporate_information_technology_raw_dev_000.developer_psprawls.edip_crm_* TO [user];
```

## How to Check Your Permissions

### 1. Run the Permission Checker
```bash
streamlit run check_permissions.py
```

This tool will test each permission level and show you exactly what access you have.

### 2. Manual SQL Checks
If you have direct SQL access, you can run these queries:

```sql
-- Check catalogs you can access
SHOW CATALOGS;

-- Check schemas in target catalog
USE CATALOG corporate_information_technology_raw_dev_000;
SHOW SCHEMAS;

-- Check current permissions
USE SCHEMA corporate_information_technology_raw_dev_000.developer_psprawls;
SHOW TABLES;

-- Test table creation (will fail if no permission)
CREATE TABLE test_permission_check (id STRING) USING DELTA;
DROP TABLE test_permission_check;
```

## Common Permission Issues

### 1. "PERMISSION_DENIED" Errors
**Cause:** Missing CREATE TABLE or schema access permissions  
**Solution:** Request schema-level permissions from admin

### 2. "ACCESS_DENIED" Errors  
**Cause:** Cannot access catalog or schema  
**Solution:** Request USE CATALOG and USE SCHEMA permissions

### 3. "Invalid access token" Errors
**Cause:** Token expired or doesn't have SQL warehouse access  
**Solution:** Generate new token with SQL access permissions

### 4. Connection Timeout/Spinning
**Cause:** SQL warehouse not running or no compute access  
**Solution:** Check warehouse status, request warehouse access

## Requesting Permissions

### Email Template for Admin
```
Subject: Databricks Unity Catalog Permissions Request - EDIP CRM

Dear [Admin],

I need Unity Catalog permissions for the EDIP CRM database integration:

User: [your-email@company.com]
Workspace: [your-workspace-name]
Catalog: corporate_information_technology_raw_dev_000  
Schema: developer_psprawls

Required Permissions:
- USE CATALOG on corporate_information_technology_raw_dev_000
- USE SCHEMA on developer_psprawls
- CREATE TABLE in developer_psprawls  
- SELECT, INSERT, UPDATE on tables prefixed with 'edip_crm_'
- SQL warehouse access for connections

Purpose: Business account tracking CRM system with these tables:
- edip_crm_accounts (business account data)
- edip_crm_platforms_status (platform onboarding status)  
- edip_crm_use_cases (use cases linked to accounts)
- edip_crm_updates (project updates and progress)

Please let me know if you need additional information.

Thank you,
[Your Name]
```

### Alternative: Self-Service Request
Some organizations have self-service permission requests:
1. Go to Databricks workspace
2. Navigate to Data → [Catalog] → [Schema]  
3. Look for "Request Access" button
4. Submit request with business justification

## Verification Steps

After permissions are granted:

1. **Run permission checker:**
   ```bash
   streamlit run check_permissions.py
   ```

2. **Test database connection:**
   ```bash
   streamlit run debug_connection.py
   ```

3. **Deploy CRM application:**
   ```bash
   streamlit run app_database.py
   ```

## Troubleshooting Permission Issues

### Error: "Cannot access catalog"
- Request USE CATALOG permission
- Verify catalog name spelling
- Check if catalog exists in workspace

### Error: "Cannot access schema"  
- Request USE SCHEMA permission
- Verify schema exists in catalog
- Check schema name spelling

### Error: "Cannot create table"
- Request CREATE TABLE permission on schema
- Verify you're in correct schema context
- Check for naming conflicts

### Error: "SQL warehouse access denied"
- Request SQL warehouse permissions
- Verify warehouse is running
- Check HTTP path format

## Best Practices

1. **Request minimal permissions first** - Start with read access, add write as needed
2. **Use specific table prefixes** - Request permissions for 'edip_crm_*' tables only  
3. **Document business justification** - Explain CRM purpose and data usage
4. **Test incrementally** - Verify each permission level before proceeding
5. **Clean up test data** - Remove test tables after permission verification

## Support

If permission requests are denied or delayed:
- Explain business value of CRM system
- Offer to start with read-only permissions
- Suggest time-limited trial permissions
- Provide detailed technical requirements
- Schedule call with admin to discuss data governance