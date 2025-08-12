#!/bin/bash

# EDIP CRM - Database Version Setup Script
echo "Setting up database version of EDIP CRM..."

# Backup current files
echo "Creating backups..."
cp app.py app_backup.py
cp -r .streamlit .streamlit_backup
cp pyproject.toml pyproject_backup.toml

# Replace with database versions
echo "Replacing files with database versions..."
cp app_database.py app.py
cp -r .streamlit_database/* .streamlit/
cp requirements_database.txt requirements.txt

# Create backup note
echo "Original project uses pyproject.toml for dependencies" > .database_version_active

echo "Database version setup complete!"
echo ""
echo "Next steps:"
echo "1. Create your .env file with Databricks credentials"
echo "2. Install dependencies: pip install -r requirements.txt"
echo "3. Test: streamlit run test_env_variables.py"
echo "4. Check permissions: streamlit run check_permissions.py"  
echo "5. Run CRM: The main workflow should now use the database version"
echo ""
echo "To restore original version, run: ./restore_original_version.sh"