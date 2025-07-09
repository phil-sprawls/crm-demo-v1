"""
Data Manager for Databricks Unity Catalog Integration
Provides database operations for the EDIP CRM system
"""

import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, date
from databricks import sql
import os

@st.cache_resource
def get_databricks_connection():
    """Get cached Databricks SQL connection with multiple auth methods"""
    try:
        # Method 1: Environment variables (for production deployment)
        server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        http_path = os.getenv("DATABRICKS_HTTP_PATH")
        access_token = os.getenv("DATABRICKS_TOKEN")
        
        # Method 2: Streamlit secrets (for development)
        if not all([server_hostname, http_path, access_token]):
            try:
                server_hostname = st.secrets["DATABRICKS_SERVER_HOSTNAME"]
                http_path = st.secrets["DATABRICKS_HTTP_PATH"]
                access_token = st.secrets["DATABRICKS_TOKEN"]
            except KeyError:
                pass
        
        # Method 3: Service principal (for production with OAuth)
        if not access_token:
            client_id = os.getenv("DATABRICKS_CLIENT_ID")
            client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")
            
            if client_id and client_secret:
                return sql.connect(
                    server_hostname=server_hostname,
                    http_path=http_path,
                    client_id=client_id,
                    client_secret=client_secret
                )
        
        if not all([server_hostname, http_path, access_token]):
            st.error("Databricks credentials not configured. Please set up connection details.")
            return None
            
        return sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        )
        
    except Exception as e:
        st.error(f"Failed to connect to Databricks: {str(e)}")
        return None

def initialize_data():
    """Initialize the data structures in session state if not already present"""
    if 'databricks_initialized' not in st.session_state:
        if create_database_schema():
            st.session_state.databricks_initialized = True
            # Load sample data if tables are empty
            _add_sample_data()
        else:
            st.error("Failed to initialize Databricks connection")

def create_database_schema():
    """Create Unity Catalog tables if they don't exist"""
    conn = get_databricks_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            # Create catalog and schema
            cursor.execute("CREATE CATALOG IF NOT EXISTS edip_crm")
            cursor.execute("CREATE SCHEMA IF NOT EXISTS edip_crm.main")
            
            # Create accounts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edip_crm.main.accounts (
                    bsnid STRING,
                    team STRING,
                    business_area STRING,
                    vp STRING,
                    admin STRING,
                    primary_it_partner STRING,
                    azure_devops_link STRING,
                    artifacts_folder_link STRING,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                ) USING DELTA
            """)
            
            # Create platforms_status table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edip_crm.main.platforms_status (
                    id STRING,
                    account_bsnid STRING,
                    platform STRING,
                    status STRING,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                ) USING DELTA
            """)
            
            # Create use_cases table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edip_crm.main.use_cases (
                    id STRING,
                    account_bsnid STRING,
                    problem STRING,
                    solution STRING,
                    leader STRING,
                    status STRING,
                    enablement_tier STRING,
                    platform STRING,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                ) USING DELTA
            """)
            
            # Create updates table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edip_crm.main.updates (
                    id STRING,
                    account_bsnid STRING,
                    author STRING,
                    date DATE,
                    platform STRING,
                    description STRING,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                ) USING DELTA
            """)
            
        return True
    except Exception as e:
        st.error(f"Failed to create database schema: {str(e)}")
        return False

def _add_sample_data():
    """Add sample data for demonstration purposes"""
    conn = get_databricks_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # Check if data already exists
            cursor.execute("SELECT COUNT(*) FROM edip_crm.main.accounts")
            result = cursor.fetchone()
            
            if result[0] > 0:  # Data already exists
                return
            
            current_time = datetime.now()
            
            # Sample accounts
            accounts_data = [
                ('BSN001', 'Data Engineering', 'Engineering', 'Sarah Johnson', 'Mike Chen', 'TechCorp Solutions',
                 'https://dev.azure.com/company/project1', 'https://company.sharepoint.com/artifacts/project1'),
                ('BSN002', 'Marketing Analytics', 'Marketing', 'David Wilson', 'Lisa Rodriguez', 'DataFlow Partners',
                 'https://dev.azure.com/company/project2', 'https://company.sharepoint.com/artifacts/project2'),
                ('BSN003', 'Sales Operations', 'Sales', 'Jennifer Davis', 'Robert Kim', 'CloudNet Services',
                 'https://dev.azure.com/company/project3', 'https://company.sharepoint.com/artifacts/project3'),
                ('BSN004', 'Finance Analytics', 'Finance', 'Michael Brown', 'Angela Lee', 'SecureSync Technologies',
                 'https://dev.azure.com/company/project4', 'https://company.sharepoint.com/artifacts/project4'),
                ('BSN005', 'HR Analytics', 'HR', 'Emily White', 'James Wilson', 'SystemLink Solutions',
                 'https://dev.azure.com/company/project5', 'https://company.sharepoint.com/artifacts/project5')
            ]
            
            for account in accounts_data:
                cursor.execute("""
                    INSERT INTO edip_crm.main.accounts 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, account + (current_time, current_time))
            
            # Sample platform statuses
            platforms_data = [
                ('BSN001', 'Databricks', 'Completed'),
                ('BSN001', 'Snowflake', 'In Progress'),
                ('BSN001', 'Power Platform', 'Not Started'),
                ('BSN002', 'Databricks', 'In Progress'),
                ('BSN002', 'Snowflake', 'Completed'),
                ('BSN002', 'Power Platform', 'Completed'),
                ('BSN003', 'Databricks', 'Not Started'),
                ('BSN003', 'Snowflake', 'In Progress'),
                ('BSN003', 'Power Platform', 'Completed'),
                ('BSN004', 'Databricks', 'In Progress'),
                ('BSN004', 'Snowflake', 'Not Started'),
                ('BSN004', 'Power Platform', 'In Progress'),
                ('BSN005', 'Databricks', 'Completed'),
                ('BSN005', 'Snowflake', 'Completed'),
                ('BSN005', 'Power Platform', 'Not Started')
            ]
            
            for platform in platforms_data:
                platform_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO edip_crm.main.platforms_status 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (platform_id,) + platform + (current_time, current_time))
            
            # Sample use cases
            use_cases_data = [
                ('BSN001', 'Need to optimize ETL pipeline performance for large-scale data processing',
                 'Implement Apache Spark optimization techniques and delta lake architecture',
                 'Mike Chen', 'In Progress', 'Guided', 'Databricks'),
                ('BSN002', 'Customer segmentation analysis required for targeted marketing campaigns',
                 'Build ML model for customer clustering using demographic and behavioral data',
                 'Lisa Rodriguez', 'Completed', 'Self-Service', 'Snowflake'),
                ('BSN003', 'Sales forecasting accuracy needs improvement',
                 'Implement time-series forecasting models with external data integration',
                 'Robert Kim', 'Not Started', 'Managed', 'Power Platform')
            ]
            
            for use_case in use_cases_data:
                use_case_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO edip_crm.main.use_cases 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (use_case_id,) + use_case + (current_time, current_time))
            
            # Sample updates
            updates_data = [
                ('BSN001', 'Mike Chen', date(2024, 7, 8), 'Databricks',
                 'Completed initial data pipeline setup and performance testing. Achieved 40% improvement in processing speed.'),
                ('BSN002', 'Lisa Rodriguez', date(2024, 7, 7), 'Snowflake',
                 'Successfully deployed customer segmentation model. Generated insights for 5 distinct customer segments.'),
                ('BSN003', 'Robert Kim', date(2024, 7, 6), 'Power Platform',
                 'Completed stakeholder requirements gathering and initial dashboard mockups.')
            ]
            
            for update in updates_data:
                update_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO edip_crm.main.updates 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (update_id,) + update + (current_time, current_time))
            
    except Exception as e:
        st.error(f"Failed to add sample data: {str(e)}")

def search_accounts(search_term):
    """Search accounts by team, business area, VP, admin, or IT partner"""
    conn = get_databricks_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        with conn.cursor() as cursor:
            if not search_term:
                cursor.execute("SELECT * FROM edip_crm.main.accounts ORDER BY bsnid")
            else:
                search_pattern = f"%{search_term.lower()}%"
                cursor.execute("""
                    SELECT * FROM edip_crm.main.accounts 
                    WHERE LOWER(team) LIKE ? 
                       OR LOWER(business_area) LIKE ? 
                       OR LOWER(vp) LIKE ? 
                       OR LOWER(admin) LIKE ? 
                       OR LOWER(primary_it_partner) LIKE ?
                    ORDER BY bsnid
                """, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
            
            return cursor.fetchall_arrow().to_pandas()
    except Exception as e:
        st.error(f"Failed to search accounts: {str(e)}")
        return pd.DataFrame()

def add_account(team, business_area, vp, admin, primary_it_partner, platforms_status=None):
    """Add a new account to the system"""
    conn = get_databricks_connection()
    if not conn:
        return None
    
    try:
        # Generate new BSNID
        bsnid = f"BSN{len(search_accounts('')) + 1:03d}"
        current_time = datetime.now()
        
        with conn.cursor() as cursor:
            # Insert account
            cursor.execute("""
                INSERT INTO edip_crm.main.accounts 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (bsnid, team, business_area, vp, admin, primary_it_partner, '', '', current_time, current_time))
            
            # Add platform statuses if provided
            if platforms_status:
                for platform, status in platforms_status.items():
                    platform_id = str(uuid.uuid4())
                    cursor.execute("""
                        INSERT INTO edip_crm.main.platforms_status 
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (platform_id, bsnid, platform, status, current_time, current_time))
        
        return bsnid
    except Exception as e:
        st.error(f"Failed to add account: {str(e)}")
        return None

def get_account_use_cases(account_bsnid):
    """Get all use cases for a specific account"""
    conn = get_databricks_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM edip_crm.main.use_cases 
                WHERE account_bsnid = ?
                ORDER BY created_at DESC
            """, (account_bsnid,))
            return cursor.fetchall_arrow().to_pandas()
    except Exception as e:
        st.error(f"Failed to get use cases: {str(e)}")
        return pd.DataFrame()

def add_use_case(account_bsnid, problem, solution, leader, status, enablement_tier, platform):
    """Add a new use case to an account"""
    conn = get_databricks_connection()
    if not conn:
        return None
    
    try:
        use_case_id = str(uuid.uuid4())
        current_time = datetime.now()
        
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO edip_crm.main.use_cases 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (use_case_id, account_bsnid, problem, solution, leader, status, enablement_tier, platform, current_time, current_time))
        
        return use_case_id
    except Exception as e:
        st.error(f"Failed to add use case: {str(e)}")
        return None

def get_account_updates(account_bsnid):
    """Get all updates for a specific account"""
    conn = get_databricks_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM edip_crm.main.updates 
                WHERE account_bsnid = ?
                ORDER BY date DESC, created_at DESC
            """, (account_bsnid,))
            return cursor.fetchall_arrow().to_pandas()
    except Exception as e:
        st.error(f"Failed to get updates: {str(e)}")
        return pd.DataFrame()