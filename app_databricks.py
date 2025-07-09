import streamlit as st
import pandas as pd
import traceback
import logging
import sys
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main application function with error handling"""
    try:
        # Page configuration
        st.set_page_config(
            page_title="All Accounts - EDIP CRM",
            page_icon="📊",
            layout="wide"
        )
        
        # Try to import data manager
        try:
            from utils.data_manager import initialize_data, search_accounts, add_account
        except ImportError as e:
            st.error(f"Failed to import data manager: {str(e)}")
            st.stop()
        
        # Initialize data with error handling
        try:
            initialize_data()
        except Exception as e:
            st.error(f"Failed to initialize data: {str(e)}")
            logger.error(f"Data initialization error: {str(e)}")
            st.stop()
        
        # Main app title
        st.title("EDIP CRM - All Accounts")
        
        # Search functionality
        search_term = st.text_input("Search accounts by team, business area, VP, admin, or IT partner", "")
        
        # Get filtered accounts with error handling
        try:
            accounts = search_accounts(search_term)
        except Exception as e:
            st.error(f"Failed to search accounts: {str(e)}")
            logger.error(f"Search error: {str(e)}")
            accounts = []
        
        if accounts:
            # Display accounts in a custom table with buttons in the rightmost column
            st.subheader(f"Accounts ({len(accounts)} found)")
            
            # Add CSS for improved table styling
            st.markdown("""
            <style>
            /* Center align columns and improve styling */
            div[data-testid="column"] {
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 35px;
            }
            div[data-testid="column"] p {
                text-align: center;
                margin: 0;
            }
            /* Style for header row */
            .table-header {
                text-align: center;
                font-size: 1.1em;
                font-weight: bold;
                padding: 6px;
                margin: 0;
            }
            /* Style for data rows */
            .table-cell {
                text-align: center;
                padding: 4px 8px;
                margin: 0;
                line-height: 1.2;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Create header row
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
            with col1:
                st.markdown("<div class='table-header'>Team</div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<div class='table-header'>Business Area</div>", unsafe_allow_html=True)
            with col3:
                st.markdown("<div class='table-header'>VP</div>", unsafe_allow_html=True)
            with col4:
                st.markdown("<div class='table-header'>Admin</div>", unsafe_allow_html=True)
            with col5:
                st.markdown("<div class='table-header'>Primary IT Partner</div>", unsafe_allow_html=True)
            with col6:
                st.markdown("<div class='table-header'>Action</div>", unsafe_allow_html=True)
            
            st.divider()
            
            # Create data rows with buttons
            for idx, account in enumerate(accounts):
                try:
                    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
                    
                    with col1:
                        st.markdown(f"<div class='table-cell'>{account.get('team', 'N/A')}</div>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<div class='table-cell'>{account.get('business_area', 'N/A')}</div>", unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"<div class='table-cell'>{account.get('vp', 'N/A')}</div>", unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"<div class='table-cell'>{account.get('admin', 'N/A')}</div>", unsafe_allow_html=True)
                    with col5:
                        st.markdown(f"<div class='table-cell'>{account.get('primary_it_partner', 'N/A')}</div>", unsafe_allow_html=True)
                    with col6:
                        if st.button("View", key=f"view_{account.get('bsnid', idx)}", use_container_width=True):
                            st.session_state.selected_account = account.get('bsnid')
                            # For Databricks, we'll use a more robust navigation approach
                            try:
                                st.switch_page("pages/1_Account_Details.py")
                            except Exception as nav_error:
                                st.error(f"Navigation error: {str(nav_error)}")
                                logger.error(f"Navigation error: {str(nav_error)}")
                    
                    if idx < len(accounts) - 1:  # Don't add divider after last row
                        st.divider()
                        
                except Exception as e:
                    st.error(f"Error displaying account row {idx}: {str(e)}")
                    logger.error(f"Account row error: {str(e)}")
                    continue
        
        else:
            if search_term:
                st.info("No accounts found matching your search criteria.")
            else:
                st.info("No accounts available. You can add new accounts from the Admin panel.")
        
        # Add debug information in development
        if st.checkbox("Show debug information"):
            st.subheader("Debug Information")
            st.write("Session state keys:", list(st.session_state.keys()))
            st.write("Python path:", sys.path[:3])
            st.write("Current working directory:", os.getcwd())
            
            if 'accounts' in st.session_state:
                st.write("Total accounts in session:", len(st.session_state.accounts))
    
    except Exception as e:
        st.error("Application Error")
        st.error(f"An unexpected error occurred: {str(e)}")
        logger.error(f"Main application error: {str(e)}")
        
        # Show detailed error in development mode
        if st.checkbox("Show detailed error information"):
            st.code(traceback.format_exc())
        
        # Offer to restart the app
        if st.button("Restart Application"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()