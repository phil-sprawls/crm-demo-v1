import streamlit as st
import uuid
from datetime import datetime

def initialize_data():
    """Initialize the data structures in session state if not already present"""
    # Initialize all session state variables first
    if 'accounts' not in st.session_state:
        st.session_state.accounts = {}
    
    if 'use_cases' not in st.session_state:
        st.session_state.use_cases = {}
    
    if 'updates' not in st.session_state:
        st.session_state.updates = {}
    
    if 'business_areas' not in st.session_state:
        st.session_state.business_areas = {
            'Finance': 'John Smith',
            'Marketing': 'Sarah Johnson', 
            'Operations': 'Mike Davis',
            'HR': 'Lisa Brown'
        }
    
    if 'platforms' not in st.session_state:
        st.session_state.platforms = ['Databricks', 'Snowflake', 'Power Platform']
    
    if 'onboarding_statuses' not in st.session_state:
        st.session_state.onboarding_statuses = ['Requested', 'In Progress', 'Completed']
    
    if 'enablement_tiers' not in st.session_state:
        st.session_state.enablement_tiers = ['Tier 1', 'Tier 2', 'Tier 3', 'None']
    
    # Check if sample data needs to be added (only if accounts is empty)
    if not st.session_state.accounts and 'sample_data_loaded' not in st.session_state:
        _add_sample_data()
        st.session_state.sample_data_loaded = True
        # Add sample updates after all data is loaded
        if hasattr(st.session_state, 'accounts') and st.session_state.accounts:
            _add_sample_updates()

def _add_sample_data():
    """Add sample data for demonstration purposes"""
    # Sample accounts
    sample_accounts = [
        {
            'team': 'Analytics Team',
            'business_area': 'Finance',
            'vp': 'Jennifer Walsh',
            'admin': 'Mark Thompson',
            'primary_it_partner': 'John Smith',
            'platforms_status': {'Databricks': 'Completed', 'Snowflake': 'In Progress'}
        },
        {
            'team': 'Sales Analytics',
            'business_area': 'Marketing',
            'vp': 'Robert Kim',
            'admin': 'Sarah Chen',
            'primary_it_partner': 'Sarah Johnson',
            'platforms_status': {'Power Platform': 'Requested', 'Databricks': 'In Progress'}
        },
        {
            'team': 'Operations Intelligence',
            'business_area': 'Operations',
            'vp': 'David Rodriguez',
            'admin': 'Lisa Wang',
            'primary_it_partner': 'Mike Davis',
            'platforms_status': {'Snowflake': 'Completed'}
        }
    ]
    
    for account_data in sample_accounts:
        bsnid = add_account(
            account_data['team'],
            account_data['business_area'], 
            account_data['vp'],
            account_data['admin'],
            account_data['primary_it_partner'],
            account_data['platforms_status']
        )
        
        # Add sample use cases for each account
        if account_data['team'] == 'Analytics Team':
            add_use_case(bsnid, 
                        "Financial reporting takes too long to generate",
                        "Implement automated reporting dashboard using Databricks",
                        "Mark Thompson",
                        "Active",
                        "Tier 1",
                        "Databricks")
        elif account_data['team'] == 'Sales Analytics':
            add_use_case(bsnid,
                        "Sales forecasting accuracy is below 70%",
                        "Build ML-powered forecasting model with real-time data",
                        "Sarah Chen", 
                        "Planning",
                        "Tier 2",
                        "Snowflake")
        elif account_data['team'] == 'Operations Intelligence':
            add_use_case(bsnid,
                        "Supply chain visibility is limited",
                        "Create real-time tracking dashboard for inventory and logistics",
                        "Lisa Wang",
                        "Completed", 
                        "Tier 1",
                        "Power Platform")
    
    # Add sample updates for demonstration
    # _add_sample_updates()  # Will be called after initialization

def add_account(team, business_area, vp, admin, primary_it_partner, platforms_status=None):
    """Add a new account to the system"""
    bsnid = str(uuid.uuid4())
    if platforms_status is None:
        platforms_status = {}
    
    st.session_state.accounts[bsnid] = {
        'bsnid': bsnid,
        'team': team,
        'business_area': business_area,
        'vp': vp,
        'admin': admin,
        'primary_it_partner': primary_it_partner,
        'azure_devops_links': [],
        'artifacts_folder_links': [],
        'platforms_status': platforms_status,
        'use_cases': [],
        'updates': [],
        'created_at': datetime.now()
    }
    return bsnid

def add_use_case(account_bsnid, problem, solution, leader, status, enablement_tier, platform):
    """Add a new use case to an account"""
    use_case_id = str(uuid.uuid4())
    use_case = {
        'id': use_case_id,
        'account_bsnid': account_bsnid,
        'problem': problem,
        'solution': solution,
        'leader': leader,
        'status': status,
        'enablement_tier': enablement_tier,
        'platform': platform,
        'created_at': datetime.now()
    }
    
    st.session_state.use_cases[use_case_id] = use_case
    
    # Add use case to account
    if account_bsnid in st.session_state.accounts:
        st.session_state.accounts[account_bsnid]['use_cases'].append(use_case_id)
    
    return use_case_id

def update_use_case(use_case_id, problem, solution, leader, status, enablement_tier, platform):
    """Update an existing use case"""
    if use_case_id in st.session_state.use_cases:
        st.session_state.use_cases[use_case_id].update({
            'problem': problem,
            'solution': solution,
            'leader': leader,
            'status': status,
            'enablement_tier': enablement_tier,
            'platform': platform
        })

def get_account_use_cases(account_bsnid):
    """Get all use cases for a specific account"""
    if account_bsnid not in st.session_state.accounts:
        return []
    
    use_case_ids = st.session_state.accounts[account_bsnid]['use_cases']
    return [st.session_state.use_cases[uc_id] for uc_id in use_case_ids if uc_id in st.session_state.use_cases]

def update_primary_it_partner(business_area, partner_name):
    """Update the primary IT partner for a business area"""
    st.session_state.business_areas[business_area] = partner_name

def search_accounts(search_term):
    """Search accounts by team, business area, VP, admin, or IT partner"""
    if not search_term:
        return list(st.session_state.accounts.values())
    
    search_term = search_term.lower()
    filtered_accounts = []
    
    for account in st.session_state.accounts.values():
        if (search_term in account['team'].lower() or
            search_term in account['business_area'].lower() or
            search_term in account['vp'].lower() or
            search_term in account['admin'].lower() or
            search_term in account['primary_it_partner'].lower()):
            filtered_accounts.append(account)
    
    return filtered_accounts

def add_platform_to_account(account_bsnid, platform, status):
    """Add a platform with status to an account"""
    if account_bsnid in st.session_state.accounts:
        st.session_state.accounts[account_bsnid]['platforms_status'][platform] = status

def update_platform_status(account_bsnid, platform, status):
    """Update the onboarding status of a platform for an account"""
    if account_bsnid in st.session_state.accounts:
        st.session_state.accounts[account_bsnid]['platforms_status'][platform] = status

def add_azure_devops_link(account_bsnid, link):
    """Add an Azure DevOps link to an account"""
    if account_bsnid in st.session_state.accounts:
        st.session_state.accounts[account_bsnid]['azure_devops_links'].append(link)

def add_artifacts_folder_link(account_bsnid, link):
    """Add an artifacts folder link to an account"""
    if account_bsnid in st.session_state.accounts:
        st.session_state.accounts[account_bsnid]['artifacts_folder_links'].append(link)

def add_update(account_bsnid, author, date, platform, description):
    """Add a new update to an account"""
    update_id = str(uuid.uuid4())
    update = {
        'id': update_id,
        'account_bsnid': account_bsnid,
        'author': author,
        'date': date,
        'platform': platform,
        'description': description,
        'created_at': datetime.now()
    }
    
    st.session_state.updates[update_id] = update
    
    # Add update to account
    if account_bsnid in st.session_state.accounts:
        if 'updates' not in st.session_state.accounts[account_bsnid]:
            st.session_state.accounts[account_bsnid]['updates'] = []
        st.session_state.accounts[account_bsnid]['updates'].append(update_id)
    
    return update_id

def get_account_updates(account_bsnid):
    """Get all updates for a specific account"""
    if account_bsnid not in st.session_state.accounts:
        return []
    
    if 'updates' not in st.session_state.accounts[account_bsnid]:
        return []
        
    update_ids = st.session_state.accounts[account_bsnid]['updates']
    return [st.session_state.updates[update_id] for update_id in update_ids if update_id in st.session_state.updates]

def update_update(update_id, author, date, platform, description):
    """Update an existing update"""
    if update_id in st.session_state.updates:
        st.session_state.updates[update_id].update({
            'author': author,
            'date': date,
            'platform': platform,
            'description': description
        })

def _add_sample_updates():
    """Add sample updates for demonstration purposes"""
    from datetime import datetime, timedelta
    
    # Get account BSNIDs to add updates
    account_bsnids = list(st.session_state.accounts.keys())
    
    if len(account_bsnids) >= 3:
        # Find specific accounts to add updates to
        analytics_bsnid = None
        sales_bsnid = None
        operations_bsnid = None
        
        for bsnid, account in st.session_state.accounts.items():
            if account['team'] == 'Analytics Team':
                analytics_bsnid = bsnid
            elif account['team'] == 'Sales Analytics':
                sales_bsnid = bsnid
            elif account['team'] == 'Operations Intelligence':
                operations_bsnid = bsnid
        
        # Analytics Team Updates
        if analytics_bsnid:
            add_update(analytics_bsnid, "Mark Thompson", 
                      datetime.now() - timedelta(days=2),
                      "Databricks", 
                      "Completed initial data pipeline setup. Dashboard framework is ready for testing.")
            
            add_update(analytics_bsnid, "Jennifer Lee", 
                      datetime.now() - timedelta(days=5),
                      "Databricks", 
                      "Data source connections established. Beginning ETL process development.")
            
            add_update(analytics_bsnid, "Mark Thompson", 
                      datetime.now() - timedelta(days=10),
                      "Databricks", 
                      "Project kickoff meeting completed. Requirements gathered and documented.")
        
        # Sales Analytics Updates
        if sales_bsnid:
            add_update(sales_bsnid, "Sarah Chen", 
                      datetime.now() - timedelta(days=1),
                      "Snowflake", 
                      "ML model training in progress. Initial accuracy showing 85% improvement.")
            
            add_update(sales_bsnid, "Robert Kim", 
                      datetime.now() - timedelta(days=7),
                      "Power Platform", 
                      "Data quality assessment completed. Ready to begin model development.")
            
            add_update(sales_bsnid, "Sarah Chen", 
                      datetime.now() - timedelta(days=14),
                      "Snowflake", 
                      "Historical sales data migration to Snowflake completed successfully.")
        
        # Operations Intelligence Updates
        if operations_bsnid:
            add_update(operations_bsnid, "Lisa Wang", 
                      datetime.now() - timedelta(days=3),
                      "Power Platform", 
                      "Supply chain dashboard deployed to production. User training scheduled for next week.")
            
            add_update(operations_bsnid, "David Rodriguez", 
                      datetime.now() - timedelta(days=8),
                      "Power Platform", 
                      "Dashboard testing phase completed. All KPIs displaying correctly.")
            
            add_update(operations_bsnid, "Lisa Wang", 
                      datetime.now() - timedelta(days=12),
                      "Power Platform", 
                      "Real-time data connectors configured. Beginning dashboard development.")
