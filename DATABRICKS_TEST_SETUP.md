# EDIP CRM - Database Integration Test Setup

## Overview

This test deployment allows you to safely validate the Unity Catalog database integration without affecting your production app. The test version creates a separate catalog (`edip_crm_test`) and includes comprehensive testing features.

## Test Deployment Files

### Ready for Upload to Databricks Apps:

1. **`app_databricks_test.py`** → Upload as `app.py`
2. **`requirements_test.txt`** → Upload as `requirements.txt`
3. **`app_test.yaml`** → Upload as `app.yaml`
4. **`.streamlit_test/config.toml`** → Upload as `.streamlit/config.toml`

## Test Features

### Enhanced Error Reporting
- Detailed connection status messages
- Step-by-step database initialization feedback
- Clear error descriptions with troubleshooting hints

### Database Testing Tools
- **Connection Test** - Verify Databricks credentials work
- **Schema Creation** - Test catalog and table creation permissions
- **Data Operations** - Validate insert/select/update operations
- **Search Functionality** - Test SQL-based filtering

### Isolated Test Environment
- Uses `edip_crm_test` catalog (separate from production)
- Test data with "TEST" prefix accounts
- No interference with existing data

## Setup Instructions

### Step 1: Gather Databricks Information

You'll need these three pieces of information from your Databricks workspace:

1. **Server Hostname**
   - Go to your Databricks workspace
   - Look at the URL: `https://your-workspace.cloud.databricks.com`
   - The hostname is: `your-workspace.cloud.databricks.com`

2. **SQL Warehouse HTTP Path**
   - In Databricks, go to SQL Warehouses
   - Click on any running warehouse
   - Copy the "HTTP Path" (looks like `/sql/1.0/warehouses/abc123def456`)

3. **Personal Access Token**
   - In Databricks, click your profile icon → Settings
   - Go to Developer → Access tokens
   - Click "Generate new token"
   - Copy the token (starts with `dapi...`)

### Step 2: Create Test App in Databricks

1. **Create New App**
   - In Databricks, click + New → Apps
   - Choose "Custom" template
   - Name: "EDIP CRM Database Test"

2. **Upload Test Files**
   - `app_databricks_test.py` → rename to `app.py`
   - `requirements_test.txt` → rename to `requirements.txt`
   - `app_test.yaml` → rename to `app.yaml`
   - `.streamlit_test/config.toml` → upload to `.streamlit/config.toml`

3. **Configure Secrets**
   In the app settings, add these environment variables:
   ```
   DATABRICKS_SERVER_HOSTNAME = your-workspace.cloud.databricks.com
   DATABRICKS_HTTP_PATH = /sql/1.0/warehouses/your-warehouse-id
   DATABRICKS_TOKEN = your-personal-access-token
   ```

4. **Deploy and Test**
   - Click Deploy
   - Wait for app to start
   - Open the app URL

## Testing Checklist

### ✅ Basic Connectivity
- [ ] Database connection test passes
- [ ] User and database information displays correctly
- [ ] No authentication errors

### ✅ Schema Creation
- [ ] Test catalog creates successfully
- [ ] All four tables (accounts, platforms_status, use_cases, updates) create
- [ ] No permission errors during schema creation

### ✅ Data Operations
- [ ] Test data loads without errors
- [ ] Account data displays in table
- [ ] Search functionality works
- [ ] Account details show correctly
- [ ] Platform status displays

### ✅ Performance
- [ ] Page loads quickly (< 5 seconds)
- [ ] Search responds promptly
- [ ] No timeout errors during operations

## Common Issues & Solutions

### Connection Failures
- **Error:** "Failed to connect to Databricks"
- **Solution:** Verify server hostname and access token
- **Check:** Ensure SQL warehouse is running

### Permission Errors
- **Error:** "Permission denied" during catalog creation
- **Solution:** User needs CATALOG_CREATE permission
- **Alternative:** Use existing catalog instead of creating new one

### Timeout Issues
- **Error:** Connection timeout or slow responses
- **Solution:** Check SQL warehouse size and auto-scaling settings
- **Alternative:** Try during off-peak hours

### Missing Dependencies
- **Error:** Import errors for databricks packages
- **Solution:** Verify requirements.txt uploaded correctly
- **Check:** App logs for specific missing packages

## Test Results Validation

### Expected Behavior
- Connection test shows green checkmark
- All table creation steps show success messages
- Test data loads showing 2 accounts
- Search for "Test" returns both accounts
- Account details display complete information

### Success Criteria
- All database operations complete without errors
- UI responds quickly and smoothly
- Data persists between page refreshes
- Search and filtering work correctly

## Next Steps After Successful Test

1. **Verify Multi-User Access**
   - Share test app URL with another user
   - Both users should see same data

2. **Test Data Persistence**
   - Refresh the app
   - Data should remain from previous session

3. **Performance Validation**
   - Add more test data if needed
   - Verify search performance with larger datasets

4. **Security Testing**
   - Test with different user permissions
   - Verify appropriate access controls

## Migration to Production

Once testing is successful:

1. **Export Production Configuration**
   - Use same credentials for production app
   - Change catalog name from `edip_crm_test` to `edip_crm`

2. **Update Production App**
   - Replace production app.py with database version
   - Update requirements.txt with database dependencies
   - Configure same environment variables

3. **Data Migration**
   - If needed, export existing data and import to database
   - Or start fresh with new database-backed system

## Support

If you encounter issues:
1. Check the app logs in Databricks Apps console
2. Verify SQL warehouse is running and accessible
3. Test credentials with Databricks SQL directly
4. Review Unity Catalog permissions

---

**Test Environment:** `corporate_information_technology_raw_dev_000.developer_psprawls` schema
**Production Environment:** Same schema (tables will be prefixed with `edip_crm_`)
**Isolation:** Complete separation between test and production data