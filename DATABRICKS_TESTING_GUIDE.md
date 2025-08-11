# EDIP CRM - Databricks Database Testing Guide

## Prerequisites

Before starting, ensure you have:
1. Access to a Databricks workspace
2. SQL Warehouse permissions
3. Unity Catalog access to your designated schema
4. Personal access token for authentication

## Step-by-Step Testing Process

### Step 1: Gather Your Databricks Credentials

You'll need three pieces of information:

1. **Server Hostname**: Your Databricks workspace URL
   - Format: `your-workspace.cloud.databricks.com` (without https://)
   - Find it in your Databricks workspace URL

2. **HTTP Path**: Your SQL Warehouse connection string
   - Format: `/sql/1.0/warehouses/your-warehouse-id`
   - Get this from: Databricks → SQL Warehouses → Your Warehouse → Connection Details

3. **Access Token**: Personal Access Token
   - Get this from: Databricks → User Settings → Access Tokens → Generate New Token

### Step 2: Install Database Dependencies

Run this command to install required packages:

```bash
pip install -r requirements_database.txt
```

This installs:
- databricks-sql-connector
- python-dotenv
- Other required dependencies

### Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the template if it exists, or create new file
touch .env
```

Add your credentials to the `.env` file:

```env
DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
DATABRICKS_TOKEN=your-actual-personal-access-token

# Optional: Customize database locations (use defaults if unsure)
DATABRICKS_CATALOG=corporate_information_technology_raw_dev_000
DATABRICKS_SCHEMA=developer_psprawls
DATABRICKS_TABLE_PREFIX=edip_crm
```

### Step 4: Test Environment Variables

First, verify your environment variables are loaded correctly:

```bash
streamlit run test_env_variables.py
```

This will show you what credentials were found without exposing sensitive data.

### Step 5: Check Database Permissions

Run the permission checker to verify your access:

```bash
streamlit run check_permissions.py
```

This comprehensive tool will test:
- Basic connection to Databricks
- SQL Warehouse access
- Catalog and schema permissions
- Table creation/modification rights
- Data insert/select capabilities

### Step 6: Run Database CRM Application

If all checks pass, launch the database-integrated CRM:

```bash
streamlit run app_database.py
```

The application will:
- Connect to your Databricks workspace
- Create necessary tables automatically
- Load sample data for testing
- Provide full CRM functionality with database persistence

## Testing Checklist

### ✅ Connection Test
- [ ] Environment variables loaded correctly
- [ ] Successful connection to Databricks
- [ ] SQL Warehouse responds to queries

### ✅ Schema Access
- [ ] Can access target catalog
- [ ] Can use target schema
- [ ] Schema shows up in available list

### ✅ Table Operations
- [ ] Can create tables
- [ ] Can insert sample data
- [ ] Can query existing data
- [ ] Can update records
- [ ] Can delete test records

### ✅ CRM Functionality
- [ ] Account search works
- [ ] Account details display correctly
- [ ] Use case creation/editing works
- [ ] Platform status updates persist
- [ ] Updates are saved to database

## Troubleshooting Common Issues

### Issue: "Import databricks could not be resolved"
**Solution**: Install database dependencies
```bash
pip install -r requirements_database.txt
```

### Issue: "Missing Databricks environment variables"
**Solution**: Check your .env file exists and has correct format

### Issue: "Connection timeout" or "Authentication failed"
**Solution**: Verify your credentials and SQL Warehouse is running

### Issue: "Permission denied" errors
**Solution**: Contact your Databricks admin to grant necessary permissions

### Issue: "Catalog/Schema not found"
**Solution**: Update DATABRICKS_CATALOG and DATABRICKS_SCHEMA in .env file

## Expected Database Schema

The application will create these tables:

### `edip_crm_accounts`
- bsnid (STRING) - Primary key
- team, business_area, vp, admin (STRING)
- primary_it_partner (STRING)
- azure_devops_links, artifacts_folder_links (STRING - JSON)
- created_at, updated_at (TIMESTAMP)

### `edip_crm_use_cases`
- use_case_id (STRING) - Primary key
- account_bsnid (STRING) - Foreign key
- platform, problem, solution (STRING)
- author (STRING)
- created_at, updated_at (TIMESTAMP)

### `edip_crm_platforms_status`
- platform_id (STRING) - Primary key
- account_bsnid, platform, status (STRING)
- enablement_tier (STRING)
- created_at, updated_at (TIMESTAMP)

### `edip_crm_updates`
- update_id (STRING) - Primary key
- account_bsnid (STRING) - Foreign key
- author, platform, description (STRING)
- update_date (DATE)
- created_at (TIMESTAMP)

## Success Indicators

You'll know the database integration is working when:
1. All permission checks pass
2. Tables are created automatically
3. Sample data loads without errors
4. CRM interface shows database-backed data
5. Changes persist between sessions
6. Multiple users can access shared data

## Next Steps After Successful Testing

Once database testing is complete:
1. Document any custom configuration needed
2. Test with real data (remove sample data)
3. Set up backup/recovery procedures
4. Configure user access controls
5. Plan deployment to production environment

## Support Resources

- Check `check_permissions.py` for detailed access testing
- Review `app_database.py` logs for connection details
- Consult `PERMISSIONS_GUIDE.md` for admin requests
- Use `debug_connection.py` for connection troubleshooting