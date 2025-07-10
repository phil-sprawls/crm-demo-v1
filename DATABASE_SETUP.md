# EDIP CRM - Database Integration Setup

## Files Overview

### Database Test Files (Renamed for Direct Use):
- `app_database.py` - Main database-integrated CRM application
- `requirements_database.txt` - Database dependencies including python-dotenv
- `app_database.yaml` - Databricks Apps deployment configuration
- `.streamlit_database/config.toml` - Streamlit configuration with EDIP theme
- `.env` - Environment variables configuration (update with your credentials)

## Quick Setup

### 1. Configure Environment Variables
Create your `.env` file from the template and add your actual Databricks credentials:

```bash
# Copy the template to create your .env file
cp .env.template .env
```

Then edit the `.env` file with your actual values:

```env
DATABRICKS_SERVER_HOSTNAME=adb-udap-cdp-npe-ws.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-actual-warehouse-id
DATABRICKS_TOKEN=your-actual-access-token
```

### 2. Install Dependencies
```bash
pip install -r requirements_database.txt
```

### 3. Test Environment Variables
```bash
streamlit run test_env_variables.py
```

### 4. Run Database CRM
```bash
streamlit run app_database.py
```

## Database Configuration

### Your Authorized Schema:
- **Catalog:** `corporate_information_technology_raw_dev_000`
- **Schema:** `developer_psprawls`

### Tables Created:
- `edip_crm_accounts` - Business accounts data
- `edip_crm_platforms_status` - Platform onboarding status
- `edip_crm_use_cases` - Use cases linked to accounts
- `edip_crm_updates` - Project updates and progress

## Features

### Database Integration:
- Real Unity Catalog persistence
- Multi-user data sharing
- Enterprise ACID transactions
- Audit trails with timestamps

### CRM Functionality:
- Account search and management
- Use case tracking
- Platform status monitoring
- Update logging with metadata

### Testing Interface:
- Connection validation
- Schema creation verification
- Data operations testing
- Performance monitoring

## Deployment Options

### Local Development:
Use the files as renamed for local testing and development.

### Databricks Apps Deployment:
1. Rename files for upload:
   - `app_database.py` → `app.py`
   - `requirements_database.txt` → `requirements.txt`
   - `app_database.yaml` → `app.yaml`
   - `.streamlit_database/config.toml` → `.streamlit/config.toml`

2. Configure environment variables in Databricks Apps settings

3. Deploy and test

## Support

The application includes comprehensive error handling and step-by-step testing to validate your database integration works correctly with your specific permissions and workspace configuration.