import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

# Production CRM app following Databricks Apps cookbook patterns
st.set_page_config(
    page_title="EDIP CRM System",
    page_icon="📊",
    layout="wide"
)

# Initialize data management functions
@st.cache_data
def initialize_sample_data():
    """Initialize sample data for the CRM system"""
    accounts = {
        'BSN001': {
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
        'BSN002': {
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
        'BSN003': {
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
        },
        'BSN004': {
            'bsnid': 'BSN004',
            'team': 'Finance Analytics',
            'business_area': 'Finance',
            'vp': 'Michael Brown',
            'admin': 'Angela Lee',
            'primary_it_partner': 'SecureSync Technologies',
            'platforms_status': {
                'Databricks': 'In Progress',
                'Snowflake': 'Not Started',
                'Power Platform': 'In Progress'
            },
            'azure_devops_link': 'https://dev.azure.com/company/project4',
            'artifacts_folder_link': 'https://company.sharepoint.com/artifacts/project4'
        },
        'BSN005': {
            'bsnid': 'BSN005',
            'team': 'HR Analytics',
            'business_area': 'HR',
            'vp': 'Emily White',
            'admin': 'James Wilson',
            'primary_it_partner': 'SystemLink Solutions',
            'platforms_status': {
                'Databricks': 'Completed',
                'Snowflake': 'Completed',
                'Power Platform': 'Not Started'
            },
            'azure_devops_link': 'https://dev.azure.com/company/project5',
            'artifacts_folder_link': 'https://company.sharepoint.com/artifacts/project5'
        }
    }
    
    use_cases = {
        'uc001': {
            'id': 'uc001',
            'account_bsnid': 'BSN001',
            'problem': 'Need to optimize ETL pipeline performance for large-scale data processing',
            'solution': 'Implement Apache Spark optimization techniques and delta lake architecture',
            'leader': 'Mike Chen',
            'status': 'In Progress',
            'enablement_tier': 'Guided',
            'platform': 'Databricks'
        },
        'uc002': {
            'id': 'uc002',
            'account_bsnid': 'BSN002',
            'problem': 'Customer segmentation analysis required for targeted marketing campaigns',
            'solution': 'Build ML model for customer clustering using demographic and behavioral data',
            'leader': 'Lisa Rodriguez',
            'status': 'Completed',
            'enablement_tier': 'Self-Service',
            'platform': 'Snowflake'
        },
        'uc003': {
            'id': 'uc003',
            'account_bsnid': 'BSN003',
            'problem': 'Sales forecasting accuracy needs improvement',
            'solution': 'Implement time-series forecasting models with external data integration',
            'leader': 'Robert Kim',
            'status': 'Not Started',
            'enablement_tier': 'Managed',
            'platform': 'Power Platform'
        }
    }
    
    updates = {
        'upd001': {
            'id': 'upd001',
            'account_bsnid': 'BSN001',
            'author': 'Mike Chen',
            'date': '2024-07-08',
            'platform': 'Databricks',
            'description': 'Completed initial data pipeline setup and performance testing. Achieved 40% improvement in processing speed.'
        },
        'upd002': {
            'id': 'upd002',
            'account_bsnid': 'BSN002',
            'author': 'Lisa Rodriguez',
            'date': '2024-07-07',
            'platform': 'Snowflake',
            'description': 'Successfully deployed customer segmentation model. Generated insights for 5 distinct customer segments.'
        },
        'upd003': {
            'id': 'upd003',
            'account_bsnid': 'BSN003',
            'author': 'Robert Kim',
            'date': '2024-07-06',
            'platform': 'Power Platform',
            'description': 'Completed stakeholder requirements gathering and initial dashboard mockups.'
        }
    }
    
    return accounts, use_cases, updates

def search_accounts(accounts, search_term):
    """Search accounts by various fields"""
    if not search_term:
        return list(accounts.values())
    
    search_term = search_term.lower()
    filtered_accounts = []
    
    for account in accounts.values():
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

def get_account_use_cases(use_cases, account_bsnid):
    """Get use cases for specific account"""
    return [uc for uc in use_cases.values() if uc.get('account_bsnid') == account_bsnid]

def get_account_updates(updates, account_bsnid):
    """Get updates for specific account"""
    account_updates = [upd for upd in updates.values() if upd.get('account_bsnid') == account_bsnid]
    return sorted(account_updates, key=lambda x: x.get('date', ''), reverse=True)

def main():
    """Main application function"""
    # Initialize data
    accounts, use_cases, updates = initialize_sample_data()
    
    # Initialize session state
    if 'selected_account' not in st.session_state:
        st.session_state.selected_account = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'accounts'
    
    # Header
    st.title("EDIP CRM System")
    st.markdown("Professional Customer Relationship Management")
    
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
    if st.session_state.current_page == 'accounts':
        show_accounts_page(accounts)
    elif st.session_state.current_page == 'details' and st.session_state.selected_account:
        show_account_details_page(accounts, use_cases, updates)
    elif st.session_state.current_page == 'usecases':
        show_use_cases_page(accounts, use_cases)
    elif st.session_state.current_page == 'updates':
        show_updates_page(accounts, updates)
    else:
        show_accounts_page(accounts)

def show_accounts_page(accounts):
    """Display all accounts page"""
    st.subheader("All Accounts")
    
    # Search functionality
    search_term = st.text_input("Search accounts by team, business area, VP, admin, or IT partner", "")
    
    # Get filtered accounts
    filtered_accounts = search_accounts(accounts, search_term)
    
    if filtered_accounts:
        st.write(f"Found {len(filtered_accounts)} accounts")
        
        # Display accounts table
        df_data = []
        for account in filtered_accounts:
            df_data.append({
                'BSNID': account['bsnid'],
                'Team': account['team'],
                'Business Area': account['business_area'],
                'VP': account['vp'],
                'Admin': account['admin'],
                'Primary IT Partner': account['primary_it_partner']
            })
        
        df = pd.DataFrame(df_data)
        
        # Display with selection
        selected_indices = st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row"
        )
        
        # Handle selection
        if selected_indices.selection.rows:
            selected_idx = selected_indices.selection.rows[0]
            selected_bsnid = df.iloc[selected_idx]['BSNID']
            
            if st.button(f"View Details for {selected_bsnid}", use_container_width=True):
                st.session_state.selected_account = selected_bsnid
                st.session_state.current_page = 'details'
                st.rerun()
    
    else:
        if search_term:
            st.info("No accounts found matching your search criteria.")
        else:
            st.warning("No accounts available.")

def show_account_details_page(accounts, use_cases, updates):
    """Display account details page"""
    account_bsnid = st.session_state.selected_account
    account = accounts.get(account_bsnid)
    
    if not account:
        st.error("Account not found")
        return
    
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
    
    # Platform status
    st.subheader("Platform Status")
    
    platform_col1, platform_col2, platform_col3 = st.columns(3)
    platforms_status = account.get('platforms_status', {})
    
    with platform_col1:
        st.metric("Databricks", platforms_status.get('Databricks', 'Not Started'))
    
    with platform_col2:
        st.metric("Snowflake", platforms_status.get('Snowflake', 'Not Started'))
    
    with platform_col3:
        st.metric("Power Platform", platforms_status.get('Power Platform', 'Not Started'))
    
    # Use cases
    st.subheader("Use Cases")
    account_use_cases = get_account_use_cases(use_cases, account_bsnid)
    
    if account_use_cases:
        for uc in account_use_cases:
            with st.expander(f"{uc['problem'][:60]}..."):
                st.write("**Problem:**", uc['problem'])
                st.write("**Solution:**", uc['solution'])
                st.write("**Leader:**", uc['leader'])
                st.write("**Status:**", uc['status'])
                st.write("**Platform:**", uc['platform'])
                st.write("**Enablement Tier:**", uc['enablement_tier'])
    else:
        st.info("No use cases found for this account.")
    
    # Recent updates
    st.subheader("Recent Updates")
    account_updates = get_account_updates(updates, account_bsnid)
    
    if account_updates:
        for update in account_updates:
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

def show_use_cases_page(accounts, use_cases):
    """Display use cases management page"""
    st.subheader("Use Cases Management")
    
    # Display all use cases
    if use_cases:
        for uc in use_cases.values():
            account = accounts.get(uc['account_bsnid'], {})
            
            with st.expander(f"{uc['problem'][:60]}... ({account.get('team', 'Unknown Team')})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Account:**", f"{uc['account_bsnid']} - {account.get('team', 'Unknown')}")
                    st.write("**Problem:**", uc['problem'])
                    st.write("**Solution:**", uc['solution'])
                
                with col2:
                    st.write("**Leader:**", uc['leader'])
                    st.write("**Status:**", uc['status'])
                    st.write("**Platform:**", uc['platform'])
                    st.write("**Enablement Tier:**", uc['enablement_tier'])
    else:
        st.info("No use cases available.")

def show_updates_page(accounts, updates):
    """Display updates page"""
    st.subheader("Recent Updates")
    
    # Sort all updates by date
    all_updates = sorted(updates.values(), key=lambda x: x.get('date', ''), reverse=True)
    
    if all_updates:
        for update in all_updates:
            account = accounts.get(update['account_bsnid'], {})
            
            with st.container():
                col1, col2, col3 = st.columns([1, 2, 4])
                
                with col1:
                    st.write(f"**{update['date']}**")
                    st.write(f"*{update['platform']}*")
                
                with col2:
                    st.write(f"**{update['author']}**")
                    st.write(f"{update['account_bsnid']} - {account.get('team', 'Unknown')}")
                
                with col3:
                    st.write(update['description'])
                
                st.divider()
    else:
        st.info("No updates available.")

if __name__ == "__main__":
    main()