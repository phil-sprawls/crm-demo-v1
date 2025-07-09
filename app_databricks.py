import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, date
from databricks import sql
import os

# Databricks-backed CRM application with Unity Catalog integration
st.set_page_config(
    page_title="EDIP CRM System",
    page_icon="📊",
    layout="wide"
)

# Database connection management
@st.cache_resource
def get_databricks_connection():
    """Get cached Databricks SQL connection"""
    try:
        # Try environment variables first (for deployed apps)
        server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        http_path = os.getenv("DATABRICKS_HTTP_PATH")
        access_token = os.getenv("DATABRICKS_TOKEN")
        
        if not all([server_hostname, http_path, access_token]):
            # Try Streamlit secrets for development
            server_hostname = st.secrets.get("DATABRICKS_SERVER_HOSTNAME")
            http_path = st.secrets.get("DATABRICKS_HTTP_PATH")
            access_token = st.secrets.get("DATABRICKS_TOKEN")
        
        if not all([server_hostname, http_path, access_token]):
            st.error("Database credentials not configured. Please set up your Databricks connection details.")
            return None
            
        return sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        )
    except Exception as e:
        st.error(f"Failed to connect to Databricks: {str(e)}")
        return None

def initialize_database_tables():
    """Create Unity Catalog tables if they don't exist"""
    conn = get_databricks_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            # Create catalog and schema if they don't exist
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
                    updated_at TIMESTAMP,
                    PRIMARY KEY (bsnid)
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
                    updated_at TIMESTAMP,
                    PRIMARY KEY (id),
                    FOREIGN KEY (account_bsnid) REFERENCES edip_crm.main.accounts(bsnid)
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
                    updated_at TIMESTAMP,
                    PRIMARY KEY (id),
                    FOREIGN KEY (account_bsnid) REFERENCES edip_crm.main.accounts(bsnid)
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
                    updated_at TIMESTAMP,
                    PRIMARY KEY (id),
                    FOREIGN KEY (account_bsnid) REFERENCES edip_crm.main.accounts(bsnid)
                ) USING DELTA
            """)
            
        return True
    except Exception as e:
        st.error(f"Failed to initialize database tables: {str(e)}")
        return False

def load_sample_data():
    """Load sample data into Unity Catalog tables if empty"""
    conn = get_databricks_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            # Check if accounts table is empty
            cursor.execute("SELECT COUNT(*) as count FROM edip_crm.main.accounts")
            result = cursor.fetchone()
            
            if result[0] == 0:  # Table is empty, load sample data
                # Insert sample accounts
                sample_accounts = [
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
                
                current_time = datetime.now()
                for account in sample_accounts:
                    cursor.execute("""
                        INSERT INTO edip_crm.main.accounts 
                        (bsnid, team, business_area, vp, admin, primary_it_partner, azure_devops_link, artifacts_folder_link, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, account + (current_time, current_time))
                
                # Insert sample platform statuses
                sample_platforms = [
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
                
                for platform in sample_platforms:
                    platform_id = str(uuid.uuid4())
                    cursor.execute("""
                        INSERT INTO edip_crm.main.platforms_status 
                        (id, account_bsnid, platform, status, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (platform_id,) + platform + (current_time, current_time))
                
                # Insert sample use cases
                sample_use_cases = [
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
                
                for use_case in sample_use_cases:
                    use_case_id = str(uuid.uuid4())
                    cursor.execute("""
                        INSERT INTO edip_crm.main.use_cases 
                        (id, account_bsnid, problem, solution, leader, status, enablement_tier, platform, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (use_case_id,) + use_case + (current_time, current_time))
                
                # Insert sample updates
                sample_updates = [
                    ('BSN001', 'Mike Chen', date(2024, 7, 8), 'Databricks',
                     'Completed initial data pipeline setup and performance testing. Achieved 40% improvement in processing speed.'),
                    ('BSN002', 'Lisa Rodriguez', date(2024, 7, 7), 'Snowflake',
                     'Successfully deployed customer segmentation model. Generated insights for 5 distinct customer segments.'),
                    ('BSN003', 'Robert Kim', date(2024, 7, 6), 'Power Platform',
                     'Completed stakeholder requirements gathering and initial dashboard mockups.')
                ]
                
                for update in sample_updates:
                    update_id = str(uuid.uuid4())
                    cursor.execute("""
                        INSERT INTO edip_crm.main.updates 
                        (id, account_bsnid, author, date, platform, description, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (update_id,) + update + (current_time, current_time))
                
                st.success("Sample data loaded successfully!")
        
        return True
    except Exception as e:
        st.error(f"Failed to load sample data: {str(e)}")
        return False

# Data access functions
def get_all_accounts():
    """Retrieve all accounts from Unity Catalog"""
    conn = get_databricks_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM edip_crm.main.accounts ORDER BY bsnid")
            return cursor.fetchall_arrow().to_pandas()
    except Exception as e:
        st.error(f"Failed to load accounts: {str(e)}")
        return pd.DataFrame()

def search_accounts(search_term):
    """Search accounts by various fields"""
    if not search_term:
        return get_all_accounts()
    
    conn = get_databricks_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        with conn.cursor() as cursor:
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

def get_account_platforms(account_bsnid):
    """Get platform statuses for an account"""
    conn = get_databricks_connection()
    if not conn:
        return {}
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT platform, status FROM edip_crm.main.platforms_status 
                WHERE account_bsnid = ?
            """, (account_bsnid,))
            results = cursor.fetchall()
            return {row[0]: row[1] for row in results}
    except Exception as e:
        st.error(f"Failed to load platform statuses: {str(e)}")
        return {}

def get_account_use_cases(account_bsnid):
    """Get use cases for an account"""
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
        st.error(f"Failed to load use cases: {str(e)}")
        return pd.DataFrame()

def get_account_updates(account_bsnid):
    """Get updates for an account"""
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
        st.error(f"Failed to load updates: {str(e)}")
        return pd.DataFrame()

def get_all_use_cases():
    """Get all use cases with account information"""
    conn = get_databricks_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT uc.*, a.team, a.business_area 
                FROM edip_crm.main.use_cases uc
                JOIN edip_crm.main.accounts a ON uc.account_bsnid = a.bsnid
                ORDER BY uc.created_at DESC
            """)
            return cursor.fetchall_arrow().to_pandas()
    except Exception as e:
        st.error(f"Failed to load use cases: {str(e)}")
        return pd.DataFrame()

def get_all_updates():
    """Get all updates with account information"""
    conn = get_databricks_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT u.*, a.team, a.business_area 
                FROM edip_crm.main.updates u
                JOIN edip_crm.main.accounts a ON u.account_bsnid = a.bsnid
                ORDER BY u.date DESC, u.created_at DESC
            """)
            return cursor.fetchall_arrow().to_pandas()
    except Exception as e:
        st.error(f"Failed to load updates: {str(e)}")
        return pd.DataFrame()

def main():
    """Main application function with error handling"""
    # Header
    st.title("EDIP CRM System")
    st.markdown("Professional Customer Relationship Management - Databricks Unity Catalog Edition")
    
    # Initialize database
    if 'db_initialized' not in st.session_state:
        with st.spinner("Initializing database connection..."):
            if initialize_database_tables():
                load_sample_data()
                st.session_state.db_initialized = True
            else:
                st.error("Failed to initialize database. Please check your Databricks connection.")
                st.stop()
    
    # Initialize session state
    if 'selected_account' not in st.session_state:
        st.session_state.selected_account = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'accounts'
    
    # Navigation
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("All Accounts", use_container_width=True):
            st.session_state.current_page = 'accounts'
            st.session_state.selected_account = None
    
    with col2:
        if st.button("Account Details", use_container_width=True, disabled=not st.session_state.selected_account):
            st.session_state.current_page = 'details'
    
    with col3:
        if st.button("Use Cases", use_container_width=True):
            st.session_state.current_page = 'usecases'
    
    with col4:
        if st.button("Updates", use_container_width=True):
            st.session_state.current_page = 'updates'
    
    st.divider()
    
    # Page content based on navigation
    try:
        if st.session_state.current_page == 'accounts':
            show_accounts_page()
        elif st.session_state.current_page == 'details' and st.session_state.selected_account:
            show_account_details_page()
        elif st.session_state.current_page == 'usecases':
            show_use_cases_page()
        elif st.session_state.current_page == 'updates':
            show_updates_page()
        else:
            show_accounts_page()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page or contact support if the issue persists.")

def show_accounts_page():
    """Display all accounts page with database integration"""
    st.subheader("All Accounts")
    
    # Search functionality
    search_term = st.text_input("Search accounts by team, business area, VP, admin, or IT partner", "")
    
    # Get filtered accounts from database
    df = search_accounts(search_term)
    
    if not df.empty:
        st.write(f"Found {len(df)} accounts")
        
        # Display accounts table with relevant columns
        display_df = df[['bsnid', 'team', 'business_area', 'vp', 'admin', 'primary_it_partner']].copy()
        display_df.columns = ['BSNID', 'Team', 'Business Area', 'VP', 'Admin', 'Primary IT Partner']
        
        # Display with selection
        selected_indices = st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row"
        )
        
        # Handle selection
        if selected_indices.selection.rows:
            selected_idx = selected_indices.selection.rows[0]
            selected_bsnid = display_df.iloc[selected_idx]['BSNID']
            
            if st.button(f"View Details for {selected_bsnid}", use_container_width=True):
                st.session_state.selected_account = selected_bsnid
                st.session_state.current_page = 'details'
                st.rerun()
    
    else:
        if search_term:
            st.info("No accounts found matching your search criteria.")
        else:
            st.warning("No accounts available. Database may be empty or connection failed.")

def show_account_details_page():
    """Display account details page with database integration"""
    account_bsnid = st.session_state.selected_account
    
    # Get account data from database
    accounts_df = get_all_accounts()
    account_data = accounts_df[accounts_df['bsnid'] == account_bsnid]
    
    if account_data.empty:
        st.error("Account not found")
        return
    
    account = account_data.iloc[0]
    
    st.subheader(f"Account Details: {account['bsnid']} - {account['team']}")
    
    # Basic information
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**BSNID:**", account['bsnid'])
        st.write("**Team:**", account['team'])
        st.write("**Business Area:**", account['business_area'])
    
    with col2:
        st.write("**VP:**", account['vp'])
        st.write("**Admin:**", account['admin'])
        st.write("**Primary IT Partner:**", account['primary_it_partner'])
    
    # External links
    st.subheader("External Links")
    col1, col2 = st.columns(2)
    
    with col1:
        if account.get('azure_devops_link'):
            st.markdown(f"[Azure DevOps Project]({account['azure_devops_link']})")
    
    with col2:
        if account.get('artifacts_folder_link'):
            st.markdown(f"[Artifacts Folder]({account['artifacts_folder_link']})")
    
    # Platform status from database
    st.subheader("Platform Status")
    
    platform_col1, platform_col2, platform_col3 = st.columns(3)
    platforms_status = get_account_platforms(account_bsnid)
    
    with platform_col1:
        st.metric("Databricks", platforms_status.get('Databricks', 'Not Started'))
    
    with platform_col2:
        st.metric("Snowflake", platforms_status.get('Snowflake', 'Not Started'))
    
    with platform_col3:
        st.metric("Power Platform", platforms_status.get('Power Platform', 'Not Started'))
    
    # Use cases from database
    st.subheader("Use Cases")
    use_cases_df = get_account_use_cases(account_bsnid)
    
    if not use_cases_df.empty:
        for _, uc in use_cases_df.iterrows():
            with st.expander(f"{uc['problem'][:60]}..."):
                st.write("**Problem:**", uc['problem'])
                st.write("**Solution:**", uc['solution'])
                st.write("**Leader:**", uc['leader'])
                st.write("**Status:**", uc['status'])
                st.write("**Platform:**", uc['platform'])
                st.write("**Enablement Tier:**", uc['enablement_tier'])
    else:
        st.info("No use cases found for this account.")
    
    # Recent updates from database
    st.subheader("Recent Updates")
    updates_df = get_account_updates(account_bsnid)
    
    if not updates_df.empty:
        for _, update in updates_df.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.write(f"**{update['date']}**")
                    st.write(f"*{update['platform']}*")
                with col2:
                    st.write(f"**{update['author']}**")
                    st.write(update['description'])
                st.divider()
    else:
        st.info("No updates found for this account.")

def show_use_cases_page():
    """Display use cases management page with database integration"""
    st.subheader("Use Cases Management")
    
    # Get all use cases from database
    use_cases_df = get_all_use_cases()
    
    if not use_cases_df.empty:
        for _, uc in use_cases_df.iterrows():
            with st.expander(f"{uc['problem'][:60]}... ({uc['team']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Account:**", f"{uc['account_bsnid']} - {uc['team']}")
                    st.write("**Problem:**", uc['problem'])
                    st.write("**Solution:**", uc['solution'])
                
                with col2:
                    st.write("**Leader:**", uc['leader'])
                    st.write("**Status:**", uc['status'])
                    st.write("**Platform:**", uc['platform'])
                    st.write("**Enablement Tier:**", uc['enablement_tier'])
    else:
        st.info("No use cases available.")

def show_updates_page():
    """Display updates page with database integration"""
    st.subheader("Recent Updates")
    
    # Get all updates from database
    updates_df = get_all_updates()
    
    if not updates_df.empty:
        for _, update in updates_df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([1, 2, 4])
                
                with col1:
                    st.write(f"**{update['date']}**")
                    st.write(f"*{update['platform']}*")
                
                with col2:
                    st.write(f"**{update['author']}**")
                    st.write(f"{update['account_bsnid']} - {update['team']}")
                
                with col3:
                    st.write(update['description'])
                
                st.divider()
    else:
        st.info("No updates available.")

if __name__ == "__main__":
    main()