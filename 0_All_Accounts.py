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

# Custom CSS for center alignment in table
st.markdown("""
<style>
/* Center align table columns both horizontally and vertically */
.main .block-container [data-testid="column"] {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 50px;
}

/* Center align text in table columns */
.main .block-container [data-testid="column"] p {
    text-align: center;
    margin: auto;
}

/* Center align buttons in table */
.main .block-container [data-testid="column"] button {
    display: block;
    margin: auto;
}

/* Center align bold headers */
.main .block-container [data-testid="column"] strong {
    display: block;
    text-align: center;
    margin: auto;
}

/* Ensure divs within columns are centered */
.main .block-container [data-testid="column"] > div {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("EDIP CRM - All Accounts")

# Search functionality
search_term = st.text_input("Search accounts by team, business area, VP, admin, or IT partner", "")

# Get filtered accounts
accounts = search_accounts(search_term)

if accounts:
    # Display accounts in a table with selection
    st.subheader(f"Accounts ({len(accounts)} found)")
    
    # Column headers
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
    with col1:
        st.write("**Team**")
    with col2:
        st.write("**Business Area**")
    with col3:
        st.write("**VP**")
    with col4:
        st.write("**Admin**")
    with col5:
        st.write("**Primary IT Partner**")
    with col6:
        st.write("**Action**")
    
    st.divider()
    
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
            if st.button("View", key=f"view_{account['bsnid']}"):
                st.session_state.selected_account = account['bsnid']
                st.switch_page("pages/1_Account_Details.py")
        
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