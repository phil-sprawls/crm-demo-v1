# EDIP CRM - Databricks Apps Deployment Checklist

## Pre-Deployment Requirements ✅

- [ ] Databricks workspace access (Premium or higher tier)
- [ ] Permissions to create apps in workspace
- [ ] Project files ready for upload

## Files to Upload 📁

### Core Application Files (Required)
- [ ] `app.py` - Main application entry point
- [ ] `pages/1_Account_Details.py` - Account details page
- [ ] `pages/2_Use_Cases.py` - Use cases management
- [ ] `pages/3_Admin.py` - Administrative functions  
- [ ] `pages/4_Updates.py` - Updates tracking
- [ ] `utils/data_manager.py` - Data management utilities

### Configuration Files (Required)
- [ ] `databricks-requirements.txt` - Python dependencies
- [ ] `.streamlit/config.toml` - Streamlit configuration

### Documentation Files (Optional)
- [ ] `README.md` - Project documentation
- [ ] `DATABRICKS_DEPLOYMENT.md` - Deployment guide
- [ ] `.gitignore` - Git ignore rules

## Deployment Steps 🚀

### Step 1: Create App in Databricks
- [ ] Open Databricks workspace
- [ ] Navigate to + New → Apps  
- [ ] Select "Custom" or "Streamlit" template
- [ ] Name the app: "EDIP CRM System"
- [ ] Add description: "Professional CRM for managing business accounts and use cases"

### Step 2: Upload Files
- [ ] Upload all core application files
- [ ] Upload configuration files
- [ ] Verify file structure is maintained
- [ ] Check file sizes (must be under 10 MB each)

### Step 3: Configure Dependencies
- [ ] Upload `databricks-requirements.txt`
- [ ] Verify all required packages are listed:
  - [ ] `databricks-sdk`
  - [ ] `databricks-sql-connector` 
  - [ ] `streamlit>=1.46.1`
  - [ ] `pandas>=2.3.0`

### Step 4: Deploy and Test
- [ ] Click "Deploy" in Databricks Apps interface
- [ ] Wait for deployment to complete
- [ ] Test app functionality:
  - [ ] Main dashboard loads
  - [ ] Account details page works
  - [ ] Use cases page functions
  - [ ] Admin panel accessible
  - [ ] Updates page operational
  - [ ] Search functionality works

### Step 5: Configure Access
- [ ] Set up user permissions
- [ ] Configure authentication if needed
- [ ] Test access with different user roles
- [ ] Document access procedures

## Post-Deployment Verification ✓

### Functionality Testing
- [ ] Create new account
- [ ] Add use case to account
- [ ] Update account information
- [ ] Search for accounts
- [ ] Add project updates
- [ ] Navigate between pages

### Performance Testing  
- [ ] App loads within reasonable time
- [ ] Navigation is responsive
- [ ] Search performs adequately
- [ ] No errors in application logs

### User Experience
- [ ] Professional appearance maintained
- [ ] EDIP CRM branding visible
- [ ] Forms save data correctly
- [ ] Confirmation messages appear
- [ ] Navigation works smoothly

## Optional Enhancements 🔧

### Unity Catalog Integration
- [ ] Set up Unity Catalog tables for persistent storage
- [ ] Configure SQL warehouse connection
- [ ] Update data manager for database operations
- [ ] Test data persistence across sessions

### Advanced Features
- [ ] Multi-user data sharing
- [ ] Role-based access control
- [ ] Data export capabilities
- [ ] Audit logging
- [ ] Backup and recovery

## Troubleshooting 🔧

### Common Issues
- [ ] Dependencies not installing → Check `databricks-requirements.txt`
- [ ] App won't start → Verify `app.py` syntax
- [ ] Pages not loading → Check file paths and imports
- [ ] Configuration errors → Review `.streamlit/config.toml`

### Support Resources
- [ ] Databricks Apps documentation
- [ ] Streamlit documentation  
- [ ] Internal IT support contact
- [ ] Project documentation files

## Success Criteria ✅

### Deployment Complete When:
- [ ] App is accessible via Databricks Apps URL
- [ ] All core functionality works as expected
- [ ] Users can access with appropriate permissions
- [ ] No critical errors in application logs
- [ ] Performance meets user expectations

### Ready for Production When:
- [ ] User acceptance testing completed
- [ ] Access controls properly configured
- [ ] Monitoring and alerting set up
- [ ] Documentation provided to users
- [ ] Support procedures established

---

**Deployment Date:** ___________  
**Deployed By:** ___________  
**App URL:** ___________  
**Notes:** ___________