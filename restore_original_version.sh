#!/bin/bash

# EDIP CRM - Restore Original Version Script
echo "Restoring original version of EDIP CRM..."

# Restore from backups
echo "Restoring files..."
cp app_backup.py app.py
cp -r .streamlit_backup/* .streamlit/
cp requirements_backup.txt requirements.txt 2>/dev/null || echo "No requirements backup to restore"

echo "Original version restored!"
echo "The main workflow will now use the in-memory version again."