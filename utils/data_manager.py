import streamlit as st
import uuid
from datetime import datetime

def initialize_data():
    """Initialize the data structures in session state if not already present"""
    if 'accounts' not in st.session_state:
        st.session_state.accounts = {}
    
    if 'use_cases' not in st.session_state:
        st.session_state.use_cases = {}
    
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
        'created_at': datetime.now()
    }
    return bsnid

def add_use_case(account_bsnid, problem, solution, leader, status, enablement_tier):
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
        'created_at': datetime.now()
    }
    
    st.session_state.use_cases[use_case_id] = use_case
    
    # Add use case to account
    if account_bsnid in st.session_state.accounts:
        st.session_state.accounts[account_bsnid]['use_cases'].append(use_case_id)
    
    return use_case_id

def update_use_case(use_case_id, problem, solution, leader, status, enablement_tier):
    """Update an existing use case"""
    if use_case_id in st.session_state.use_cases:
        st.session_state.use_cases[use_case_id].update({
            'problem': problem,
            'solution': solution,
            'leader': leader,
            'status': status,
            'enablement_tier': enablement_tier
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
