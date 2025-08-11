#!/bin/bash

# EDIP CRM - Restore Original Version Script
echo "Restoring original version of EDIP CRM..."

# Restore from backups
echo "Restoring files..."
cp app_backup.py app.py
cp -r .streamlit_backup/* .streamlit/
rm requirements.txt 2>/dev/null || echo "No requirements.txt to remove"
rm .database_version_active 2>/dev/null

# Note: Original project uses pyproject.toml for dependencies, not requirements.txt

echo "Original version restored!"
echo "The main workflow will now use the in-memory version again."