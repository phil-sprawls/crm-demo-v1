import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, date
from databricks import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="EDIP CRM",
    page_icon="📊",
    layout="wide"
)

# Database configuration from environment variables
CATALOG_NAME = os.getenv("DATABRICKS_CATALOG", "corporate_information_technology_raw_dev_000")
SCHEMA_NAME = os.getenv("DATABRICKS_SCHEMA", "developer_psprawls")
TABLE_PREFIX = os.getenv("DATABRICKS_TABLE_PREFIX", "edip_crm")

# Database connection
@st.cache_resource
def get_databricks_connection():
    """Get cached Databricks SQL connection"""
    try:
        server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        http_path = os.getenv("DATABRICKS_HTTP_PATH")
        access_token = os.getenv("DATABRICKS_TOKEN")
        
        if not all([server_hostname, http_path, access_token]):
            return None
            
        return sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        )
    except Exception:
        return None

# Data access functions
def get_all_accounts(search_term=""):
    """Get all accounts from database with optional search"""
    conn = get_databricks_connection()
    if not conn:
        st.error("Database connection not available")
        return []
    
    try:
        with conn.cursor() as cursor:
            if search_term:
                search_pattern = f"%{search_term.lower()}%"
                cursor.execute(f"""
                    SELECT bsnid, team, business_area, vp, admin, primary_it_partner 
                    FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts
                    WHERE LOWER(team) LIKE ? 
                       OR LOWER(business_area) LIKE ? 
                       OR LOWER(vp) LIKE ? 
                       OR LOWER(admin) LIKE ? 
                       OR LOWER(primary_it_partner) LIKE ?
                    ORDER BY bsnid
                """, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
            else:
                cursor.execute(f"""
                    SELECT bsnid, team, business_area, vp, admin, primary_it_partner 
                    FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts
                    ORDER BY bsnid
                """)
            
            results = cursor.fetchall()
            return [dict(zip([desc[0] for desc in cursor.description], row)) for row in results]
            
    except Exception as e:
        st.error(f"Failed to fetch accounts: {str(e)}")
        return []

def add_account(bsnid, team, business_area, vp, admin, it_partner):
    """Add new account to database"""
    conn = get_databricks_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            current_time = datetime.now()
            cursor.execute(f"""
                INSERT INTO {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts
                (bsnid, team, business_area, vp, admin, primary_it_partner, azure_devops_links, artifacts_folder_links, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, '[]', '[]', ?, ?)
            """, (bsnid, team, business_area, vp, admin, it_partner, current_time, current_time))
            return True
    except Exception as e:
        st.error(f"Failed to add account: {str(e)}")
        return False

# Check database connection
conn = get_databricks_connection()
if not conn:
    st.error("Database connection required. Please ensure your .env file contains valid Databricks credentials.")
    st.info("Required variables: DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH, DATABRICKS_TOKEN")
    st.stop()

# Main application
st.title("EDIP CRM")
st.subheader("All Accounts")

# Search functionality
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    search_term = st.text_input(
        "Search accounts by team, business area, VP, admin, or IT partner:",
        placeholder="Enter search term..."
    )

with col3:
    if st.button("Add New Account", type="primary"):
        st.session_state.show_add_form = True

# Add account form
if st.session_state.get('show_add_form', False):
    with st.expander("Add New Account", expanded=True):
        with st.form("add_account_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_bsnid = st.text_input("BSNID*")
                new_team = st.text_input("Team*")
                new_business_area = st.selectbox("Business Area*", [
                    "", "Finance", "Marketing", "Operations", "Sales", "HR", "IT", "Engineering"
                ])
            
            with col2:
                new_vp = st.text_input("VP*")
                new_admin = st.text_input("Admin*")
                new_it_partner = st.text_input("Primary IT Partner*")
            
            submitted = st.form_submit_button("Save Account")
            
            if submitted:
                if all([new_bsnid, new_team, new_business_area, new_vp, new_admin, new_it_partner]):
                    if add_account(new_bsnid, new_team, new_business_area, new_vp, new_admin, new_it_partner):
                        st.success(f"Successfully added account {new_bsnid}")
                        st.session_state.show_add_form = False
                        st.rerun()
                    else:
                        st.error("Failed to add account")
                else:
                    st.error("Please fill in all required fields")

# Display accounts
accounts = get_all_accounts(search_term)

if accounts:
    st.write(f"**{len(accounts)} accounts found**")
    
    # Create DataFrame for table display
    display_data = []
    for account in accounts:
        display_data.append({
            'BSNID': account['bsnid'],
            'Team': account['team'],
            'Business Area': account['business_area'],
            'VP': account['vp'],
            'Admin': account['admin'],
            'IT Partner': account['primary_it_partner']
        })
    
    df = pd.DataFrame(display_data)
    
    # Display table with custom CSS for alignment
    st.markdown("""
    <style>
    .stDataFrame td {
        text-align: left !important;
    }
    .stDataFrame th {
        text-align: left !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the dataframe
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Account selection dropdown
    st.subheader("Account Actions")
    selected_bsnid = st.selectbox(
        "Select an account to view details:",
        options=[""] + [account['bsnid'] for account in accounts],
        format_func=lambda x: "Choose an account..." if x == "" else f"{x} - {next(acc['team'] for acc in accounts if acc['bsnid'] == x)}"
    )
    
    if selected_bsnid:
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("View Details"):
                st.session_state.selected_account = selected_bsnid
                st.switch_page("pages/1_Account_Details.py")
else:
    if search_term:
        st.info("No accounts found matching your search criteria.")
    else:
        st.info("No accounts available in the database.")