import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, date
from databricks import sql
import os

# Databricks Unity Catalog Test Deployment
st.set_page_config(
    page_title="EDIP CRM System - Database Test",
    page_icon="🔬",
    layout="wide"
)

# Database connection with enhanced error handling for testing
@st.cache_resource
def get_databricks_connection():
    """Get cached Databricks SQL connection with test configuration"""
    try:
        # Environment variables (preferred for Databricks Apps)
        server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        http_path = os.getenv("DATABRICKS_HTTP_PATH")
        access_token = os.getenv("DATABRICKS_TOKEN")
        
        # Streamlit secrets fallback
        if not all([server_hostname, http_path, access_token]):
            try:
                server_hostname = st.secrets["DATABRICKS_SERVER_HOSTNAME"]
                http_path = st.secrets["DATABRICKS_HTTP_PATH"]
                access_token = st.secrets["DATABRICKS_TOKEN"]
            except KeyError as e:
                st.error(f"Missing secret: {str(e)}")
                st.info("Please configure your Databricks credentials in the app settings.")
                return None
        
        if not all([server_hostname, http_path, access_token]):
            st.error("Database credentials not configured.")
            st.info("""
            Required environment variables:
            - DATABRICKS_SERVER_HOSTNAME
            - DATABRICKS_HTTP_PATH  
            - DATABRICKS_TOKEN
            """)
            return None
            
        # Test connection
        conn = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        )
        
        # Verify connection works
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 as test")
            cursor.fetchone()
        
        return conn
        
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        st.info("Please check your Databricks workspace connection and credentials.")
        return None

def test_database_connection():
    """Test and display connection status"""
    conn = get_databricks_connection()
    if conn:
        st.success("✅ Database connection successful!")
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT current_user() as user, current_database() as db")
                result = cursor.fetchone()
                st.info(f"Connected as: {result[0]} | Database: {result[1]}")
        except Exception as e:
            st.warning(f"Connection test query failed: {str(e)}")
        return True
    else:
        st.error("❌ Database connection failed")
        return False

def initialize_test_database():
    """Create test database schema with enhanced error reporting"""
    conn = get_databricks_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            st.info("Creating test catalog and schema...")
            
            # Create catalog
            cursor.execute("CREATE CATALOG IF NOT EXISTS edip_crm_test")
            st.success("✅ Test catalog created")
            
            # Create schema
            cursor.execute("CREATE SCHEMA IF NOT EXISTS edip_crm_test.main")
            st.success("✅ Test schema created")
            
            # Create accounts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edip_crm_test.main.accounts (
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
            st.success("✅ Accounts table created")
            
            # Create platforms_status table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edip_crm_test.main.platforms_status (
                    id STRING,
                    account_bsnid STRING,
                    platform STRING,
                    status STRING,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                ) USING DELTA
            """)
            st.success("✅ Platform status table created")
            
            # Create use_cases table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edip_crm_test.main.use_cases (
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
            st.success("✅ Use cases table created")
            
            # Create updates table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edip_crm_test.main.updates (
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
            st.success("✅ Updates table created")
            
        return True
        
    except Exception as e:
        st.error(f"Failed to create database schema: {str(e)}")
        return False

def load_test_data():
    """Load sample data for testing"""
    conn = get_databricks_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            # Check if data exists
            cursor.execute("SELECT COUNT(*) FROM edip_crm_test.main.accounts")
            result = cursor.fetchone()
            
            if result[0] > 0:
                st.info("Test data already exists")
                return True
            
            st.info("Loading test data...")
            current_time = datetime.now()
            
            # Sample accounts
            test_accounts = [
                ('TEST001', 'Data Engineering Test', 'Engineering', 'Sarah Johnson', 'Mike Chen', 'TechCorp Solutions',
                 'https://dev.azure.com/test/project1', 'https://test.sharepoint.com/artifacts/project1'),
                ('TEST002', 'Marketing Analytics Test', 'Marketing', 'David Wilson', 'Lisa Rodriguez', 'DataFlow Partners',
                 'https://dev.azure.com/test/project2', 'https://test.sharepoint.com/artifacts/project2')
            ]
            
            for account in test_accounts:
                cursor.execute("""
                    INSERT INTO edip_crm_test.main.accounts 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, account + (current_time, current_time))
            
            # Sample platform statuses
            test_platforms = [
                ('TEST001', 'Databricks', 'Testing'),
                ('TEST001', 'Snowflake', 'In Progress'),
                ('TEST002', 'Power Platform', 'Testing')
            ]
            
            for platform in test_platforms:
                platform_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO edip_crm_test.main.platforms_status 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (platform_id,) + platform + (current_time, current_time))
            
            # Sample use case
            use_case_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO edip_crm_test.main.use_cases 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (use_case_id, 'TEST001', 'Test database integration performance',
                  'Verify Unity Catalog operations work correctly', 'Mike Chen',
                  'Testing', 'Guided', 'Databricks', current_time, current_time))
            
            # Sample update
            update_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO edip_crm_test.main.updates 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (update_id, 'TEST001', 'Test User', date.today(), 'Databricks',
                  'Database integration test completed successfully', current_time, current_time))
            
            st.success("✅ Test data loaded successfully")
            return True
            
    except Exception as e:
        st.error(f"Failed to load test data: {str(e)}")
        return False

def get_test_accounts():
    """Retrieve accounts from test database"""
    conn = get_databricks_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM edip_crm_test.main.accounts ORDER BY bsnid")
            df = cursor.fetchall_arrow().to_pandas()
            return df
    except Exception as e:
        st.error(f"Failed to load accounts: {str(e)}")
        return pd.DataFrame()

def search_test_accounts(search_term):
    """Search test accounts"""
    if not search_term:
        return get_test_accounts()
    
    conn = get_databricks_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        with conn.cursor() as cursor:
            search_pattern = f"%{search_term.lower()}%"
            cursor.execute("""
                SELECT * FROM edip_crm_test.main.accounts 
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

def get_test_platforms(account_bsnid):
    """Get platform statuses for test account"""
    conn = get_databricks_connection()
    if not conn:
        return {}
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT platform, status FROM edip_crm_test.main.platforms_status 
                WHERE account_bsnid = ?
            """, (account_bsnid,))
            results = cursor.fetchall()
            return {row[0]: row[1] for row in results}
    except Exception as e:
        st.error(f"Failed to load platform statuses: {str(e)}")
        return {}

def main():
    """Main test application"""
    st.title("EDIP CRM System - Database Integration Test")
    st.markdown("**Testing Unity Catalog Integration**")
    
    # Connection test section
    st.header("1. Database Connection Test")
    
    if st.button("Test Database Connection"):
        test_database_connection()
    
    # Database initialization
    st.header("2. Database Schema Setup")
    
    if st.button("Initialize Test Database"):
        if initialize_test_database():
            st.success("Database schema created successfully!")
        else:
            st.error("Database initialization failed")
    
    # Data loading test
    st.header("3. Data Operations Test")
    
    if st.button("Load Test Data"):
        if load_test_data():
            st.success("Test data loaded successfully!")
    
    # Basic CRM functionality test
    st.header("4. CRM Functionality Test")
    
    # Initialize session state
    if 'selected_test_account' not in st.session_state:
        st.session_state.selected_test_account = None
    
    # Search functionality
    search_term = st.text_input("Search test accounts", "")
    
    # Get and display accounts
    df = search_test_accounts(search_term)
    
    if not df.empty:
        st.write(f"Found {len(df)} test accounts")
        
        # Display accounts
        display_df = df[['bsnid', 'team', 'business_area', 'vp', 'admin', 'primary_it_partner']].copy()
        display_df.columns = ['BSNID', 'Team', 'Business Area', 'VP', 'Admin', 'Primary IT Partner']
        
        selected_indices = st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row"
        )
        
        # Account details test
        if selected_indices.selection.rows:
            selected_idx = selected_indices.selection.rows[0]
            selected_bsnid = display_df.iloc[selected_idx]['BSNID']
            
            st.subheader(f"Account Details: {selected_bsnid}")
            
            account = df[df['bsnid'] == selected_bsnid].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**BSNID:**", account['bsnid'])
                st.write("**Team:**", account['team'])
                st.write("**Business Area:**", account['business_area'])
            
            with col2:
                st.write("**VP:**", account['vp'])
                st.write("**Admin:**", account['admin'])
                st.write("**Primary IT Partner:**", account['primary_it_partner'])
            
            # Platform status test
            st.subheader("Platform Status")
            platforms = get_test_platforms(selected_bsnid)
            
            if platforms:
                for platform, status in platforms.items():
                    st.metric(platform, status)
            else:
                st.info("No platform data found")
    
    else:
        if search_term:
            st.info("No test accounts found matching search criteria")
        else:
            st.warning("No test accounts available - run 'Load Test Data' first")
    
    # Database status
    st.header("5. Database Status")
    
    conn = get_databricks_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Count records in each table
                tables = ['accounts', 'platforms_status', 'use_cases', 'updates']
                
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM edip_crm_test.main.{table}")
                        count = cursor.fetchone()[0]
                        st.metric(f"{table.replace('_', ' ').title()}", count)
                    except Exception as e:
                        st.error(f"Error querying {table}: {str(e)}")
                        
        except Exception as e:
            st.error(f"Failed to get database status: {str(e)}")

if __name__ == "__main__":
    main()