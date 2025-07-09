# EDIP CRM - Databricks Apps Deployment Guide

## Overview

This guide explains how to deploy the EDIP CRM system on Databricks Apps, which provides serverless hosting with Unity Catalog integration and enterprise security.

## Prerequisites

- Databricks workspace (Premium or higher - not Standard tier)
- Unity Catalog access (optional, for data integration)
- App deployment permissions in your workspace

## Deployment Steps

### 1. Create the App in Databricks

1. **Open your Databricks workspace**
2. **Click + New → Apps**
3. **Select "Custom" or "Streamlit" template**
4. **Configure the app:**
   - Name: `EDIP CRM System`
   - Description: `Professional CRM for managing business accounts and use cases`
   - Source: Upload files or connect to repository

### 2. Upload Project Files

Upload these key files to your Databricks app:

**Core Application Files:**
- `app.py` (main entry point)
- `pages/1_Account_Details.py`
- `pages/2_Use_Cases.py` 
- `pages/3_Admin.py`
- `pages/4_Updates.py`
- `utils/data_manager.py`

**Configuration Files:**
- `databricks-requirements.txt` (dependencies)
- `.streamlit/config.toml` (Streamlit configuration)

### 3. Dependencies Configuration

Use the `databricks-requirements.txt` file which includes:
```
databricks-sdk
databricks-sql-connector
streamlit>=1.46.1
pandas>=2.3.0
```

### 4. Configuration for Databricks

The app runs with the existing configuration but can be enhanced with Unity Catalog integration:

```python
# Optional: Add to app.py for Unity Catalog integration
from databricks.sdk.core import Config
from databricks import sql

# Initialize Databricks configuration
cfg = Config()

@st.cache_resource
def get_databricks_connection(http_path):
    """Create cached connection to Databricks SQL warehouse"""
    return sql.connect(
        server_hostname=cfg.host,
        http_path=http_path,
        credentials_provider=lambda: cfg.authenticate,
    )
```

## App Features on Databricks

### Current Functionality (Session-based)
- ✅ Account management and tracking
- ✅ Use case creation and editing
- ✅ Platform status monitoring
- ✅ Updates and progress tracking
- ✅ Search and filtering capabilities
- ✅ Professional enterprise UI

### Enhanced Databricks Integration (Optional)
- 🔄 Unity Catalog table storage for persistent data
- 🔄 SQL warehouse connectivity for data queries
- 🔄 Multi-user access with proper authentication
- 🔄 Data governance through Unity Catalog

## Deployment Process

### Option 1: Direct Upload
1. Zip your project files
2. Upload through Databricks Apps interface
3. Configure dependencies
4. Deploy and test

### Option 2: Git Integration
1. Push code to GitHub repository
2. Connect Databricks to your repository
3. Configure automatic deployment
4. Set up CI/CD pipeline

## Security and Permissions

### App Authorization
- App runs with service principal credentials
- Inherits Unity Catalog permissions
- Built-in OAuth 2.0 and SSO support

### Access Control
- Configure user permissions through workspace settings
- Restrict access to appropriate business users
- Monitor usage through Databricks audit logs

## Monitoring and Maintenance

### Logs and Debugging
- View application logs in Databricks Apps interface
- Monitor performance and usage metrics
- Debug issues through workspace console

### Updates and Versioning
- Deploy new versions through the Apps interface
- Rollback to previous versions if needed
- Maintain different environments (dev/staging/prod)

## Limitations

- **File Size**: Individual files limited to 10 MB
- **Compute**: Runs on managed serverless infrastructure
- **Data Persistence**: Session-based unless integrated with Unity Catalog
- **Workspace**: Not available on Standard tier workspaces

## Cost Considerations

- Serverless compute pricing
- No infrastructure management overhead
- Usage-based billing model
- Automatic scaling based on demand

## Support and Resources

- [Databricks Apps Documentation](https://docs.databricks.com/dev-tools/databricks-apps/)
- [Streamlit on Databricks Tutorial](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-apps/tutorial-streamlit)
- [Unity Catalog Integration Guide](https://docs.databricks.com/data-governance/unity-catalog/)

## Migration from Replit

Your current EDIP CRM system will work seamlessly on Databricks Apps with minimal changes:

1. **Keep existing functionality**: All current features remain intact
2. **Add data persistence**: Optionally integrate with Unity Catalog tables
3. **Enhanced security**: Benefit from enterprise-grade authentication
4. **Better scalability**: Automatic scaling and performance optimization

## Next Steps

1. Create the app in your Databricks workspace
2. Upload the project files
3. Configure dependencies
4. Test the deployment
5. Set up user permissions
6. Consider Unity Catalog integration for persistent data storage