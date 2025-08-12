import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, date
from databricks import sql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database configuration from environment
CATALOG_NAME = os.getenv("DATABRICKS_CATALOG", "corporate_information_technology_raw_dev_000")
SCHEMA_NAME = os.getenv("DATABRICKS_SCHEMA", "developer_psprawls")
TABLE_PREFIX = os.getenv("DATABRICKS_TABLE_PREFIX", "edip_crm")

# Page configuration
st.set_page_config(
    page_title="All Accounts - EDIP CRM",
    page_icon="📊",
    layout="wide"
)

# Database connection
@st.cache_resource
def get_databricks_connection():
    """Get cached Databricks SQL connection"""
    try:
        server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        http_path = os.getenv("DATABRICKS_HTTP_PATH")
        access_token = os.getenv("DATABRICKS_TOKEN")
        
        if not all([server_hostname, http_path, access_token]):
            st.error("Database connection not configured. Please check your environment variables.")
            return None
            
        return sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        )
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        return None

def search_accounts(search_term=""):
    """Search accounts from database"""
    conn = get_databricks_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor() as cursor:
            if search_term:
                query = f"""
                SELECT bsnid, team, business_area, vp, admin, primary_it_partner
                FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts
                WHERE LOWER(team) LIKE LOWER('%{search_term}%')
                   OR LOWER(business_area) LIKE LOWER('%{search_term}%')
                   OR LOWER(vp) LIKE LOWER('%{search_term}%')
                   OR LOWER(admin) LIKE LOWER('%{search_term}%')
                   OR LOWER(primary_it_partner) LIKE LOWER('%{search_term}%')
                ORDER BY team
                """
            else:
                query = f"""
                SELECT bsnid, team, business_area, vp, admin, primary_it_partner
                FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts
                ORDER BY team
                """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            accounts = []
            for row in results:
                accounts.append({
                    'bsnid': row[0],
                    'team': row[1],
                    'business_area': row[2],
                    'vp': row[3],
                    'admin': row[4],
                    'primary_it_partner': row[5]
                })
            return accounts
    except Exception as e:
        st.error(f"Error searching accounts: {str(e)}")
        return []

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

# Database connection status and stats
conn = get_databricks_connection()
if conn:
    try:
        with conn.cursor() as cursor:
            # Count accounts
            cursor.execute(f"SELECT COUNT(*) FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts")
            account_count = cursor.fetchone()[0]
            st.sidebar.metric("Total Accounts", account_count)
            
            # Count use cases
            cursor.execute(f"SELECT COUNT(*) FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_use_cases")
            use_case_count = cursor.fetchone()[0]
            st.sidebar.metric("Total Use Cases", use_case_count)
            
            # Count business areas
            cursor.execute(f"SELECT COUNT(DISTINCT business_area) FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts")
            business_area_count = cursor.fetchone()[0]
            st.sidebar.metric("Business Areas", business_area_count)
            
    except Exception as e:
        st.sidebar.error("Database query failed")
        st.sidebar.error(str(e))
else:
    st.sidebar.error("❌ Database Connection Failed")
    st.sidebar.write("Update your .env file with real values:")
    st.sidebar.code("""
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-actual-warehouse-id
DATABRICKS_TOKEN=your-actual-access-token
    """)