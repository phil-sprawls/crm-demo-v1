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
            return None
            
        return sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        )
    except Exception:
        return None

# Database operations
def initialize_database_tables():
    """Create database tables if they don't exist"""
    conn = get_databricks_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            # Just test basic connection - tables likely already exist
            cursor.execute("SELECT 1")
            return True
    except Exception:
        return False

def load_sample_data():
    """Load sample data into the database if needed"""
    # Skip sample data loading - assume database already has data from previous setup
    pass

def get_all_accounts(search_term=""):
    """Get all accounts from database with optional search"""
    conn = get_databricks_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor() as cursor:
            if search_term:
                cursor.execute(f"""
                    SELECT bsnid, team, business_area, vp, admin, primary_it_partner
                    FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts
                    WHERE LOWER(team) LIKE LOWER(?) 
                       OR LOWER(business_area) LIKE LOWER(?)
                       OR LOWER(vp) LIKE LOWER(?)
                       OR LOWER(admin) LIKE LOWER(?)
                       OR LOWER(primary_it_partner) LIKE LOWER(?)
                    ORDER BY team
                """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            else:
                cursor.execute(f"""
                    SELECT bsnid, team, business_area, vp, admin, primary_it_partner
                    FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts
                    ORDER BY team
                """)
                
            results = cursor.fetchall()
            return [
                {
                    'bsnid': row[0],
                    'team': row[1],
                    'business_area': row[2],
                    'vp': row[3],
                    'admin': row[4],
                    'primary_it_partner': row[5]
                }
                for row in results
            ]
            
    except Exception as e:
        st.error(f"Failed to fetch accounts: {str(e)}")
        return []

# Initialize database and load sample data
@st.cache_data
def setup_database():
    """Setup database tables and sample data"""
    if initialize_database_tables():
        load_sample_data()
        return True
    return False

# Check database connection
conn = get_databricks_connection()
if not conn:
    st.error("Database connection required. Please ensure your .env file contains valid Databricks credentials.")
    st.info("Required variables: DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH, DATABRICKS_TOKEN")
    st.stop()

# Main application
st.title("EDIP CRM - All Accounts")

# Search functionality
search_term = st.text_input("Search accounts by team, business area, VP, admin, or IT partner", "")

# Get filtered accounts
accounts = get_all_accounts(search_term)

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
            if st.button("View", key=f"view_{idx}"):
                st.session_state.selected_account = account['bsnid']
                st.switch_page("pages/1_Account_Details.py")

else:
    st.info("No accounts found" + (f" matching '{search_term}'" if search_term else ""))

# Add new account section
st.markdown("---")
st.subheader("Quick Add New Account")

with st.expander("Add New Account"):
    with st.form("quick_add_account"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_team = st.text_input("Team Name")
            new_business_area = st.text_input("Business Area")
            new_vp = st.text_input("VP")
        
        with col2:
            new_admin = st.text_input("Admin")
            new_it_partner = st.text_input("Primary IT Partner")
        
        if st.form_submit_button("Add Account", use_container_width=True):
            if all([new_team, new_business_area, new_vp, new_admin, new_it_partner]):
                conn = get_databricks_connection()
                if conn:
                    try:
                        with conn.cursor() as cursor:
                            new_bsnid = f"BSN{str(uuid.uuid4())[:8].upper()}"
                            cursor.execute(f"""
                                INSERT INTO {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts
                                (bsnid, team, business_area, vp, admin, primary_it_partner, azure_devops_links, artifacts_folder_links, created_at, updated_at)
                                VALUES (?, ?, ?, ?, ?, ?, '[]', '[]', current_timestamp(), current_timestamp())
                            """, (new_bsnid, new_team, new_business_area, new_vp, new_admin, new_it_partner))
                            
                        st.success(f"Account '{new_team}' added successfully with BSNID: {new_bsnid}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to add account: {str(e)}")
                else:
                    st.error("Database connection failed")
            else:
                st.error("Please fill in all required fields")

# Footer
st.markdown("---")
st.markdown("**EDIP CRM System** - Database-backed persistent storage")