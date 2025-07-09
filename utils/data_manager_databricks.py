import streamlit as st
import uuid
import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_data():
    """Initialize the data structures in session state if not already present"""
    try:
        # Initialize accounts if not present
        if 'accounts' not in st.session_state:
            st.session_state.accounts = {}
            logger.info("Initialized accounts in session state")
        
        # Initialize use cases if not present
        if 'use_cases' not in st.session_state:
            st.session_state.use_cases = {}
            logger.info("Initialized use cases in session state")
        
        # Initialize business areas if not present
        if 'business_areas' not in st.session_state:
            st.session_state.business_areas = {
                'Engineering': 'TechCorp Solutions',
                'Marketing': 'DataFlow Partners',
                'Sales': 'CloudNet Services',
                'Finance': 'SecureSync Technologies',
                'Operations': 'InfoBridge Consulting',
                'HR': 'SystemLink Solutions'
            }
            logger.info("Initialized business areas in session state")
        
        # Initialize platforms if not present
        if 'platforms' not in st.session_state:
            st.session_state.platforms = ['Databricks', 'Snowflake', 'Power Platform']
            logger.info("Initialized platforms in session state")
        
        # Initialize statuses if not present
        if 'statuses' not in st.session_state:
            st.session_state.statuses = ['Not Started', 'In Progress', 'Completed', 'On Hold']
            logger.info("Initialized statuses in session state")
        
        # Initialize enablement tiers if not present
        if 'enablement_tiers' not in st.session_state:
            st.session_state.enablement_tiers = ['Self-Service', 'Guided', 'Managed']
            logger.info("Initialized enablement tiers in session state")
        
        # Initialize updates if not present
        if 'updates' not in st.session_state:
            st.session_state.updates = {}
            logger.info("Initialized updates in session state")
        
        # Add sample data if accounts are empty
        if len(st.session_state.accounts) == 0:
            _add_sample_data()
            logger.info("Added sample data to session state")
            
    except Exception as e:
        logger.error(f"Error initializing data: {str(e)}")
        raise

def _add_sample_data():
    """Add sample data for demonstration purposes"""
    try:
        sample_accounts = [
            {
                'bsnid': 'BSN001',
                'team': 'Data Engineering',
                'business_area': 'Engineering',
                'vp': 'Sarah Johnson',
                'admin': 'Mike Chen',
                'primary_it_partner': 'TechCorp Solutions',
                'platforms_status': {
                    'Databricks': 'Completed',
                    'Snowflake': 'In Progress',
                    'Power Platform': 'Not Started'
                },
                'azure_devops_link': 'https://dev.azure.com/company/project1',
                'artifacts_folder_link': 'https://company.sharepoint.com/artifacts/project1'
            },
            {
                'bsnid': 'BSN002',
                'team': 'Marketing Analytics',
                'business_area': 'Marketing',
                'vp': 'David Wilson',
                'admin': 'Lisa Rodriguez',
                'primary_it_partner': 'DataFlow Partners',
                'platforms_status': {
                    'Databricks': 'In Progress',
                    'Snowflake': 'Completed',
                    'Power Platform': 'Completed'
                },
                'azure_devops_link': 'https://dev.azure.com/company/project2',
                'artifacts_folder_link': 'https://company.sharepoint.com/artifacts/project2'
            },
            {
                'bsnid': 'BSN003',
                'team': 'Sales Operations',
                'business_area': 'Sales',
                'vp': 'Jennifer Davis',
                'admin': 'Robert Kim',
                'primary_it_partner': 'CloudNet Services',
                'platforms_status': {
                    'Databricks': 'Not Started',
                    'Snowflake': 'In Progress',
                    'Power Platform': 'Completed'
                },
                'azure_devops_link': 'https://dev.azure.com/company/project3',
                'artifacts_folder_link': 'https://company.sharepoint.com/artifacts/project3'
            }
        ]
        
        # Add sample accounts
        for account in sample_accounts:
            st.session_state.accounts[account['bsnid']] = account
        
        # Add sample use cases
        sample_use_cases = [
            {
                'id': str(uuid.uuid4()),
                'account_bsnid': 'BSN001',
                'problem': 'Need to optimize ETL pipeline performance',
                'solution': 'Implement Apache Spark optimization techniques',
                'leader': 'Mike Chen',
                'status': 'In Progress',
                'enablement_tier': 'Guided',
                'platform': 'Databricks'
            },
            {
                'id': str(uuid.uuid4()),
                'account_bsnid': 'BSN002',
                'problem': 'Customer segmentation analysis required',
                'solution': 'Build ML model for customer clustering',
                'leader': 'Lisa Rodriguez',
                'status': 'Completed',
                'enablement_tier': 'Self-Service',
                'platform': 'Snowflake'
            }
        ]
        
        for use_case in sample_use_cases:
            st.session_state.use_cases[use_case['id']] = use_case
            
        logger.info("Successfully added sample data")
        
    except Exception as e:
        logger.error(f"Error adding sample data: {str(e)}")
        raise

def search_accounts(search_term):
    """Search accounts by team, business area, VP, admin, or IT partner"""
    try:
        if not search_term:
            return list(st.session_state.accounts.values())
        
        search_term = search_term.lower()
        filtered_accounts = []
        
        for account in st.session_state.accounts.values():
            # Search in all relevant fields
            searchable_fields = [
                account.get('team', '').lower(),
                account.get('business_area', '').lower(),
                account.get('vp', '').lower(),
                account.get('admin', '').lower(),
                account.get('primary_it_partner', '').lower()
            ]
            
            if any(search_term in field for field in searchable_fields):
                filtered_accounts.append(account)
        
        return filtered_accounts
        
    except Exception as e:
        logger.error(f"Error searching accounts: {str(e)}")
        return []

def add_account(team, business_area, vp, admin, primary_it_partner, platforms_status=None):
    """Add a new account to the system"""
    try:
        # Generate unique BSNID
        bsnid = f"BSN{str(len(st.session_state.accounts) + 1).zfill(3)}"
        
        # Create account object
        account = {
            'bsnid': bsnid,
            'team': team,
            'business_area': business_area,
            'vp': vp,
            'admin': admin,
            'primary_it_partner': primary_it_partner,
            'platforms_status': platforms_status or {
                'Databricks': 'Not Started',
                'Snowflake': 'Not Started',
                'Power Platform': 'Not Started'
            },
            'azure_devops_link': '',
            'artifacts_folder_link': ''
        }
        
        # Add to session state
        st.session_state.accounts[bsnid] = account
        logger.info(f"Added new account: {bsnid}")
        
        return bsnid
        
    except Exception as e:
        logger.error(f"Error adding account: {str(e)}")
        raise

def get_account_use_cases(account_bsnid):
    """Get all use cases for a specific account"""
    try:
        use_cases = []
        for use_case in st.session_state.use_cases.values():
            if use_case.get('account_bsnid') == account_bsnid:
                use_cases.append(use_case)
        return use_cases
        
    except Exception as e:
        logger.error(f"Error getting use cases for account {account_bsnid}: {str(e)}")
        return []

def add_use_case(account_bsnid, problem, solution, leader, status, enablement_tier, platform):
    """Add a new use case to an account"""
    try:
        use_case_id = str(uuid.uuid4())
        
        use_case = {
            'id': use_case_id,
            'account_bsnid': account_bsnid,
            'problem': problem,
            'solution': solution,
            'leader': leader,
            'status': status,
            'enablement_tier': enablement_tier,
            'platform': platform
        }
        
        st.session_state.use_cases[use_case_id] = use_case
        logger.info(f"Added new use case: {use_case_id}")
        
        return use_case_id
        
    except Exception as e:
        logger.error(f"Error adding use case: {str(e)}")
        raise

def get_account_updates(account_bsnid):
    """Get all updates for a specific account"""
    try:
        updates = []
        for update in st.session_state.updates.values():
            if update.get('account_bsnid') == account_bsnid:
                updates.append(update)
        # Sort by date (newest first)
        updates.sort(key=lambda x: x.get('date', ''), reverse=True)
        return updates
        
    except Exception as e:
        logger.error(f"Error getting updates for account {account_bsnid}: {str(e)}")
        return []