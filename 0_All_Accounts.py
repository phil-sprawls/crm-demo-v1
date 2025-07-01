import streamlit as st
import pandas as pd
from utils.data_manager import initialize_data, search_accounts, add_account

# Page configuration
st.set_page_config(
    page_title="All Accounts - EDIP CRM",
    page_icon="📊",
    layout="wide"
)

# Initialize data
initialize_data()

# Handle navigation fallback from deployment compatibility
if 'navigate_to_home' in st.session_state:
    del st.session_state.navigate_to_home
    # Clear any selection states to ensure clean home page
    if 'selected_account' in st.session_state:
        del st.session_state.selected_account
    if 'edit_use_case_id' in st.session_state:
        del st.session_state.edit_use_case_id

st.title("EDIP CRM - All Accounts")

# Search functionality
search_term = st.text_input("Search accounts by team, business area, VP, admin, or IT partner", "")

# Get filtered accounts
accounts = search_accounts(search_term)

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
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
        
        with col1:
            st.markdown(f"<div class='table-cell'>{account['team']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='table-cell'>{account['business_area']}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='table-cell'>{account['vp']}</div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='table-cell'>{account['admin']}</div>", unsafe_allow_html=True)
        with col5:
            st.markdown(f"<div class='table-cell'>{account['primary_it_partner']}</div>", unsafe_allow_html=True)
        with col6:
            if st.button("View", key=f"view_{account['bsnid']}", use_container_width=True):
                st.session_state.selected_account = account['bsnid']
                st.switch_page("pages/1_Account_Details.py")
        
        if idx < len(accounts) - 1:  # Don't add divider after last row
            st.divider()

else:
    if search_term:
        st.info("No accounts found matching your search criteria.")
    else:
        st.info("No accounts available. Use the Admin panel to add new accounts.")

# Quick action buttons
st.markdown("---")
st.subheader("Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Add New Account", use_container_width=True):
        st.switch_page("pages/3_Admin.py")

with col2:
    if st.button("Manage Use Cases", use_container_width=True):
        st.switch_page("pages/2_Use_Cases.py")

with col3:
    if st.button("Manage Updates", use_container_width=True):
        st.switch_page("pages/4_Updates.py")

with col4:
    if st.button("Admin Panel", use_container_width=True):
        st.switch_page("pages/3_Admin.py")

# Navigation info
st.sidebar.title("Navigation")
st.sidebar.markdown("""
- **All Accounts**: View and search all accounts
- **Account Details**: View detailed information for a specific account
- **Use Cases**: Manage use cases across all accounts
- **Updates**: Dedicated updates management with Author, Date, Platform, Description
- **Admin**: Administrative functions and data management
""")

# System stats
st.sidebar.markdown("---")
st.sidebar.subheader("System Stats")
st.sidebar.metric("Total Accounts", len(st.session_state.accounts))
st.sidebar.metric("Total Use Cases", len(st.session_state.use_cases))
st.sidebar.metric("Business Areas", len(st.session_state.business_areas))

# Quick stats
if st.session_state.accounts:
    platform_counts = {}
    for account in st.session_state.accounts.values():
        for platform in account['platforms_status'].keys():
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
    
    if platform_counts:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Platform Distribution")
        for platform, count in platform_counts.items():
            st.sidebar.write(f"**{platform}**: {count} accounts")