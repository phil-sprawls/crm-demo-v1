# Databricks Apps Deployment Troubleshooting Guide

## "App exited unexpectedly" Error Solutions

### 1. **Most Common Cause: Dependencies Issue**

**Problem**: The `databricks-sdk` and `databricks-sql-connector` packages may not be needed for a session-based app.

**Solution**: Use simplified requirements file:
```
streamlit==1.46.1
pandas==2.3.0
```

### 2. **File Structure Issues**

**Problem**: Import errors due to incorrect file paths or missing files.

**Solution**: Ensure these files are uploaded to Databricks:
- `app_databricks.py` (use this as main file instead of `app.py`)
- `utils/data_manager_databricks.py` (simplified data manager)
- `.streamlit/config.toml`
- `databricks-requirements.txt`

### 3. **Memory/Resource Issues**

**Problem**: App consuming too much memory on startup.

**Solution**: The simplified versions reduce memory usage by:
- Removing unnecessary imports
- Adding proper error handling
- Using smaller sample datasets

### 4. **Navigation Issues**

**Problem**: `st.switch_page()` may not work properly in Databricks Apps.

**Solution**: The `app_databricks.py` includes fallback navigation handling.

## Quick Fix Instructions

### Step 1: Use Simplified Files
Upload these files instead of the original ones:
- `app_databricks.py` → rename to `app.py` in Databricks
- `utils/data_manager_databricks.py` → rename to `utils/data_manager.py`
- Updated `databricks-requirements.txt` (streamlit and pandas only)

### Step 2: Minimal Dependencies
Use this requirements.txt content:
```
streamlit==1.46.1
pandas==2.3.0
```

### Step 3: Test Locally First
Before deploying to Databricks:
1. Run `streamlit run app_databricks.py` locally
2. Verify all pages load without errors
3. Test basic functionality

### Step 4: Gradual Deployment
1. Start with just the main app file
2. Add pages one by one
3. Test after each addition

## Alternative Deployment Strategy

### Option A: Single File App
Create a single file with all functionality embedded:
- No imports from utils
- All data management code in main file
- Simpler for Databricks deployment

### Option B: Minimal Multi-Page
- Main app with basic functionality
- Add pages gradually after main app works
- Test each page individually

## Debug Steps

### 1. Check Databricks Logs
- Navigate to your app in Databricks
- Click on "Logs" tab
- Look for Python errors or import failures

### 2. Test Components
- Comment out complex features
- Start with basic Streamlit app
- Add functionality incrementally

### 3. Verify File Uploads
- Ensure all files uploaded correctly
- Check file sizes (must be under 10MB)
- Verify folder structure maintained

## Common Error Messages and Solutions

### "ModuleNotFoundError: No module named 'utils'"
**Solution**: 
- Verify `utils` folder uploaded
- Check file structure in Databricks
- Use absolute imports

### "AttributeError: module 'streamlit' has no attribute 'switch_page'"
**Solution**:
- Use try/catch around navigation
- Implement fallback navigation
- Check Streamlit version compatibility

### "Memory Error" or "Resource Exhausted"
**Solution**:
- Reduce sample data size
- Remove unnecessary imports
- Optimize data structures

## Recovery Steps

If deployment keeps failing:

1. **Start Fresh**:
   - Delete the app in Databricks
   - Create new app with minimal code
   - Test basic functionality first

2. **Use Backup Files**:
   - Deploy `app_databricks.py` as main file
   - Use `data_manager_databricks.py` for data
   - Minimal requirements only

3. **Contact Support**:
   - If issues persist, contact Databricks support
   - Provide specific error logs
   - Include deployment configuration details

## Success Indicators

App deployment successful when:
- ✅ App starts without errors
- ✅ Main page loads and displays accounts
- ✅ Search functionality works
- ✅ Basic navigation between pages works
- ✅ No critical errors in logs

## Next Steps After Successful Deployment

1. Test all functionality thoroughly
2. Add remaining pages if needed
3. Configure user permissions
4. Set up monitoring and alerts
5. Plan for data persistence (Unity Catalog integration)