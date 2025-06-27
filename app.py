import streamlit as st
import pandas as pd
from utils.data_manager import initialize_data, search_accounts, add_account

# Page configuration
st.set_page_config(
    page_title="CRM System",
    page_icon="🏢",
    layout="wide"
)

# Initialize data
initialize_data()

st.title("🏢 CRM System - All Accounts")

# Search functionality
search_term = st.text_input("🔍 Search accounts by team, business area, VP, admin, or IT partner", "")

# Get filtered accounts
accounts = search_accounts(search_term)

if accounts:
    # Convert to DataFrame for better display
    accounts_data = []
    for account in accounts:
        accounts_data.append({
            'Team': account['team'],
            'Business Area': account['business_area'],
            'VP': account['vp'],
            'Admin': account['admin'],
            'Primary IT Partner': account['primary_it_partner'],
            'BSNID': account['bsnid']
        })
    
    df = pd.DataFrame(accounts_data)
    
    # Display accounts table
    st.subheader(f"📋 Accounts ({len(accounts)} found)")
    
    # Create clickable rows
    for idx, account in enumerate(accounts):
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
        
        with col1:
            st.write(account['team'])
        with col2:
            st.write(account['business_area'])
        with col3:
            st.write(account['vp'])
        with col4:
            st.write(account['admin'])
        with col5:
            st.write(account['primary_it_partner'])
        with col6:
            if st.button("View", key=f"view_{account['bsnid']}", help="View account details"):
                st.session_state.selected_account = account['bsnid']
                st.switch_page("pages/1_Account_Details.py")
        
        if idx == 0:
            # Header row
            st.markdown("---")
    
    # Show the header after the first row
    if accounts:
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
        with col1:
            st.markdown("**Team**")
        with col2:
            st.markdown("**Business Area**")
        with col3:
            st.markdown("**VP**")
        with col4:
            st.markdown("**Admin**")
        with col5:
            st.markdown("**Primary IT Partner**")
        with col6:
            st.markdown("**Action**")
        st.markdown("---")
        
        # Re-display the data with proper formatting
        for idx, account in enumerate(accounts):
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
            
            with col1:
                st.write(account['team'])
            with col2:
                st.write(account['business_area'])
            with col3:
                st.write(account['vp'])
            with col4:
                st.write(account['admin'])
            with col5:
                st.write(account['primary_it_partner'])
            with col6:
                if st.button("View", key=f"view_btn_{account['bsnid']}", help="View account details"):
                    st.session_state.selected_account = account['bsnid']
                    st.switch_page("pages/1_Account_Details.py")

else:
    if search_term:
        st.info(f"No accounts found matching '{search_term}'")
    else:
        st.info("No accounts available. Use the Admin screen to add new accounts.")

# Quick actions
st.markdown("---")
st.subheader("🚀 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Add New Account", use_container_width=True):
        st.switch_page("pages/3_Admin.py")

with col2:
    if st.button("📊 Manage Use Cases", use_container_width=True):
        st.switch_page("pages/2_Use_Cases.py")

with col3:
    if st.button("⚙️ Admin Panel", use_container_width=True):
        st.switch_page("pages/3_Admin.py")

# Navigation info
st.sidebar.title("📋 Navigation")
st.sidebar.markdown("""
- **All Accounts**: View and search all accounts
- **Account Details**: View detailed information for a specific account
- **Use Cases**: Manage use cases across all accounts
- **Admin**: Administrative functions and data management
""")

# System stats
st.sidebar.markdown("---")
st.sidebar.subheader("📈 System Stats")
st.sidebar.metric("Total Accounts", len(st.session_state.accounts))
st.sidebar.metric("Total Use Cases", len(st.session_state.use_cases))
st.sidebar.metric("Business Areas", len(st.session_state.business_areas))
