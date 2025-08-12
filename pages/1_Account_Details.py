import streamlit as st
import pandas as pd
from utils.database_manager import (
    get_account_by_bsnid, get_account_use_cases, get_account_updates, get_platform_status
)

# Page configuration
st.set_page_config(
    page_title="Account Details - EDIP CRM",
    page_icon="📊",
    layout="wide"
)

st.title("Account Details")

# Show persistent success message if exists
if 'account_success_message' in st.session_state:
    st.success(st.session_state.account_success_message)
    del st.session_state.account_success_message

# Check if an account is selected
if 'selected_account' not in st.session_state:
    st.error("No account selected. Please go back to All Accounts and select an account.")
    if st.button("← Back to All Accounts"):
        st.switch_page("app.py")
    st.stop()

# Test database connection first
from utils.database_manager import get_databricks_connection
conn = get_databricks_connection()
if not conn:
    st.error("Database connection failed. Please check your .env file configuration:")
    st.code("""
DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
DATABRICKS_TOKEN=your-access-token
    """)
    if st.button("← Back to All Accounts"):
        st.switch_page("app.py") 
    st.stop()

# Get the selected account from database
account = get_account_by_bsnid(st.session_state.selected_account)
if not account:
    st.error(f"Account with BSNID '{st.session_state.selected_account}' not found in database.")
    st.info("This could mean the account doesn't exist or there's a database permission issue.")
    if st.button("← Back to All Accounts"):
        st.switch_page("app.py")
    st.stop()

# Back button
if st.button("← Back to All Accounts"):
    # Clear any editing states
    if 'edit_use_case_id' in st.session_state:
        del st.session_state.edit_use_case_id
    if 'selected_account' in st.session_state:
        del st.session_state.selected_account
    
    st.switch_page("app.py")

st.markdown("---")

# Account basic information
col1, col2 = st.columns(2)

with col1:
    st.subheader("Basic Information")
    st.write(f"**BSNID (UID):** {account['bsnid']}")
    st.write(f"**Team:** {account['team']}")
    st.write(f"**Business Area:** {account['business_area']}")
    st.write(f"**VP:** {account['vp']}")
    st.write(f"**Admin:** {account['admin']}")
    st.write(f"**Primary IT Partner:** {account['primary_it_partner']}")

with col2:
    st.subheader("External Links")
    
    # Azure DevOps Links
    st.write("**Azure DevOps Support Tickets:**")
    if account['azure_devops_links']:
        for i, link in enumerate(account['azure_devops_links']):
            st.markdown(f"[Support Ticket {i+1}]({link})")
    else:
        st.write("No Azure DevOps links available")
    
    st.markdown("---")
    
    # Artifacts Folder Links
    st.write("**Artifacts Folder Links:**")
    if account['artifacts_folder_links']:
        for i, link in enumerate(account['artifacts_folder_links']):
            st.markdown(f"[Artifacts Folder {i+1}]({link})")
    else:
        st.write("No artifacts folder links available")

st.markdown("---")

# Platforms and Onboarding Status
st.subheader("Platforms & Onboarding Status")

platforms_status = get_platform_status(account['bsnid'])

if platforms_status:
    # Display platform status
    st.write("**Current Platform Status:**")
    for platform, status_info in platforms_status.items():
        status = status_info.get('status', 'Unknown')
        tier = status_info.get('enablement_tier', 'Unknown')
        
        # Color coding for status
        if status == 'Completed':
            st.success(f"**{platform}**: {status} | Enablement Tier: {tier}")
        elif status == 'In Progress':
            st.warning(f"**{platform}**: {status} | Enablement Tier: {tier}")
        else:  # Requested
            st.info(f"**{platform}**: {status} | Enablement Tier: {tier}")
else:
    st.info("No platforms configured for this account")

st.markdown("---")

# Use Cases
st.subheader("Use Cases")

use_cases = get_account_use_cases(account['bsnid'])

if use_cases:
    # Display use cases in a table format
    use_cases_data = []
    for uc in use_cases:
        use_cases_data.append({
            'Platform': uc.get('platform', 'Not specified'),
            'Problem': uc['problem'][:50] + "..." if len(uc['problem']) > 50 else uc['problem'],
            'Solution': uc['solution'][:50] + "..." if len(uc['solution']) > 50 else uc['solution'],
            'Author': uc['author'],
            'Created': uc['created_at'].strftime('%Y-%m-%d') if uc['created_at'] else 'Unknown'
        })
    
    df = pd.DataFrame(use_cases_data)
    st.dataframe(df, use_container_width=True)
    
    # Display detailed use cases
    st.write("**Detailed Use Cases:**")
    for uc in use_cases:
        with st.expander(f"Platform: {uc.get('platform', 'Not specified')} - {uc['problem'][:30]}..."):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Problem:** {uc['problem']}")
                st.write(f"**Solution:** {uc['solution']}")
            with col2:
                st.write(f"**Platform:** {uc.get('platform', 'Not specified')}")
                st.write(f"**Author:** {uc['author']}")
                st.write(f"**Created:** {uc['created_at'] if uc['created_at'] else 'Unknown'}")

else:
    st.info("No use cases found for this account")
    
if st.button("Add New Use Case"):
    st.switch_page("pages/2_Use_Cases.py")

st.markdown("---")

# Updates
st.subheader("Recent Updates")

updates = get_account_updates(account['bsnid'])

if updates:
    # Display updates in chronological order
    st.write("**Recent Project Updates:**")
    for update in updates:
        with st.expander(f"{update['platform']} - {update['update_date']} - by {update['author']}"):
            st.write(f"**Platform:** {update['platform']}")
            st.write(f"**Author:** {update['author']}")
            st.write(f"**Date:** {update['update_date']}")
            st.write(f"**Description:** {update['description']}")
            st.write(f"**Created:** {update['created_at'] if update['created_at'] else 'Unknown'}")
else:
    st.info("No recent updates found for this account")
    
if st.button("Add New Update"):
    st.switch_page("pages/4_Updates.py")

st.markdown("---")

# Quick actions
st.subheader("Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Manage Use Cases", use_container_width=True):
        st.switch_page("pages/2_Use_Cases.py")

with col2:
    if st.button("Manage Updates", use_container_width=True):
        st.switch_page("pages/4_Updates.py")

with col3:
    if st.button("Admin Panel", use_container_width=True):
        st.switch_page("pages/3_Admin.py")