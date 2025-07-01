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



st.title("EDIP CRM - All Accounts")

# Search functionality
search_term = st.text_input("Search accounts by team, business area, VP, admin, or IT partner", "")

# Get filtered accounts
accounts = search_accounts(search_term)

if accounts:
    # Display accounts in an HTML table with proper vertical centering
    st.subheader(f"Accounts ({len(accounts)} found)")
    
    # Create HTML table with proper styling
    table_html = """
    <style>
    .accounts-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-family: 'Source Sans Pro', sans-serif;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .accounts-table th {
        background-color: #f0f2f6;
        padding: 15px 12px;
        text-align: center;
        vertical-align: middle;
        font-weight: bold;
        border-bottom: 2px solid #e6e6e6;
        font-size: 14px;
    }
    .accounts-table td {
        padding: 15px 12px;
        text-align: center;
        vertical-align: middle;
        border-bottom: 1px solid #e6e6e6;
        font-size: 14px;
    }
    .accounts-table tr:hover {
        background-color: #f8f9fa;
    }
    .accounts-table tr:nth-child(even) {
        background-color: #fafafa;
    }
    </style>
    
    <table class="accounts-table">
        <thead>
            <tr>
                <th style="width: 20%">Team</th>
                <th style="width: 20%">Business Area</th>
                <th style="width: 20%">VP</th>
                <th style="width: 20%">Admin</th>
                <th style="width: 20%">Primary IT Partner</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for idx, account in enumerate(accounts):
        table_html += f"""
            <tr>
                <td>{account['team']}</td>
                <td>{account['business_area']}</td>
                <td>{account['vp']}</td>
                <td>{account['admin']}</td>
                <td>{account['primary_it_partner']}</td>
            </tr>
        """
    
    table_html += """
        </tbody>
    </table>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Streamlit buttons for account selection
    st.markdown("**Select an account to view details:**")
    cols = st.columns(min(len(accounts), 3))
    for idx, account in enumerate(accounts):
        with cols[idx % 3]:
            if st.button(f"View {account['team']}", key=f"view_{account['bsnid']}", use_container_width=True):
                st.session_state.selected_account = account['bsnid']
                st.switch_page("pages/1_Account_Details.py")

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