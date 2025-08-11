# EDIP CRM Database Test - Quick Setup Guide

## Your Specific Configuration

### Workspace Details
- **Workspace:** `[your-workspace-name]`
- **Catalog:** `corporate_information_technology_raw_dev_000`
- **Schema:** `developer_psprawls`

### Required Secrets
You need to gather these 3 pieces of information:

1. **DATABRICKS_SERVER_HOSTNAME**
   - Value: `your-workspace.cloud.databricks.com`

2. **DATABRICKS_HTTP_PATH**
   - Go to SQL Warehouses in your workspace
   - Click on any running warehouse
   - Copy the HTTP Path (looks like `/sql/1.0/warehouses/abc123def456`)

3. **DATABRICKS_TOKEN**
   - Profile icon → Settings → Developer → Access tokens
   - Generate new token and copy it

### Files to Upload
1. `app_databricks_test.py` → rename to `app.py`
2. `requirements_test.txt` → rename to `requirements.txt`
3. `app_test.yaml` → rename to `app.yaml`
4. `.streamlit_test/config.toml` → upload to `.streamlit/config.toml`

### Tables Created
The test will create these tables in your authorized schema:
- `corporate_information_technology_raw_dev_000.developer_psprawls.edip_crm_accounts`
- `corporate_information_technology_raw_dev_000.developer_psprawls.edip_crm_platforms_status`
- `corporate_information_technology_raw_dev_000.developer_psprawls.edip_crm_use_cases`
- `corporate_information_technology_raw_dev_000.developer_psprawls.edip_crm_updates`

### Test Process
1. **Create new Databricks App** with custom template
2. **Upload 4 files** (rename as indicated above)
3. **Configure 3 environment variables** with your specific values
4. **Deploy and test** using the app's step-by-step interface

### Success Indicators
- Connection test shows green checkmark
- All 4 tables create successfully
- Test data loads (2 accounts: TEST001, TEST002)
- Search functionality works
- Account details display correctly

Ready to start your database integration test!