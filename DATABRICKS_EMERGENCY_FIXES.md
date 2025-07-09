# Emergency Fix Guide for Databricks Apps "App Exited Unexpectedly" Error

## Root Cause Analysis

Based on Databricks community reports, the "app exited unexpectedly" error typically occurs due to:

1. **Network connectivity issues** - Databricks Apps can't reach PyPI to install packages
2. **Dependency conflicts** - Package installation failures 
3. **Environment limitations** - Databricks Apps runtime restrictions
4. **File/import structure issues** - Complex imports failing in serverless environment

## IMMEDIATE SOLUTION: Ultra-Minimal Deployment

### Files to Upload:
1. **`app_ultra_minimal.py`** (rename to `app.py`)
2. **`requirements_ultra_minimal.txt`** (rename to `requirements.txt`)
3. **`.streamlit/config.toml`** (use existing)

### Why This Works:
- Only uses `streamlit` dependency (no pandas, no external libraries)
- All data hardcoded in session state
- No complex imports or file structure
- Minimal memory footprint

## Step-by-Step Emergency Deployment

### 1. Delete Current App
- Go to Databricks Apps dashboard
- Delete the failing app completely
- Start fresh to avoid cached errors

### 2. Create New App
- Click + New → Apps
- Select "Custom" template
- Name: "EDIP CRM Emergency"

### 3. Upload Only Essential Files
**Main App File:**
```python
# Upload app_ultra_minimal.py as app.py
```

**Requirements (ONLY this line):**
```
streamlit
```

**Config (keep existing):**
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

### 4. Deploy and Test
- Click Deploy
- Wait for "Running" status
- Test basic functionality

## Alternative Solutions if Still Failing

### Option A: Use Databricks Built-in Template
1. Create new app with built-in Streamlit template
2. Replace template code with our minimal version
3. Test deployment

### Option B: Local Development First
1. Test ultra-minimal app locally: `streamlit run app_ultra_minimal.py`
2. If it works locally, package for Databricks
3. Upload only working files

### Option C: Workspace-Level Issues
If still failing, the issue might be:
- Databricks workspace doesn't have internet access
- Package installation blocked by network policies
- Insufficient permissions for app deployment
- Databricks Apps not properly enabled

## Diagnostic Commands

Run these in a Databricks notebook to check environment:

```python
# Check internet connectivity
!ping pypi.org

# Check package installation
!pip install streamlit --dry-run

# Check environment variables
import os
print("Environment variables:", list(os.environ.keys()))

# Check Python path
import sys
print("Python path:", sys.path)
```

## Contact Information

If ultra-minimal deployment still fails:
1. **Databricks Support** - This indicates workspace-level configuration issues
2. **IT/Network Team** - May need to whitelist PyPI domains
3. **Workspace Admin** - Check Apps permissions and quotas

## Recovery Strategy

Once ultra-minimal version works:
1. Add features gradually
2. Test after each addition
3. Use session state for data persistence
4. Avoid external dependencies initially

## Success Metrics

Ultra-minimal deployment successful when:
- App starts without errors
- Main page displays 5 sample accounts
- Search functionality works
- Account details can be viewed
- Platform status dropdowns function
- Use case forms accept input

This minimal version provides core CRM functionality while avoiding all common deployment issues.