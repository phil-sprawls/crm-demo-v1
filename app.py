"""
Main entry point for the EDIP CRM System
This file serves as a compatibility layer for deployment while maintaining 
the correct file structure for Streamlit's multi-page navigation.
"""

# Import and run the main application
import subprocess
import sys
import os

# Execute the main Streamlit application
if __name__ == "__main__":
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(current_dir, "0_All_Accounts.py")
    
    # Run the main application
    exec(open(main_file).read())