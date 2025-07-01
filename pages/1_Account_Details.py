import streamlit as st
import pandas as pd
from utils.data_manager import (
    initialize_data, get_account_use_cases, get_account_updates, add_azure_devops_link, 
    add_artifacts_folder_link, add_platform_to_account, update_platform_status
)

# Page configuration
st.set_page_config(
    page_title="Account Details - EDIP CRM",
    page_icon="📊",
    layout="wide"
)

# Initialize data
initialize_data()

st.title("Account Details")

# Show persistent success message if exists
if 'account_success_message' in st.session_state:
    st.success(st.session_state.account_success_message)
    del st.session_state.account_success_message

# Check if an account is selected
if 'selected_account' not in st.session_state or st.session_state.selected_account not in st.session_state.accounts:
    st.error("No account selected. Please go back to All Accounts and select an account.")
    if st.button("← Back to All Accounts"):
        # Use JavaScript redirect as it works reliably in deployment
        st.markdown("""
        <script>
        window.location.href = window.location.origin;
        </script>
        """, unsafe_allow_html=True)
        st.stop()
    st.stop()

# Get the selected account
account = st.session_state.accounts[st.session_state.selected_account]

# Back button - using JavaScript redirect for deployment compatibility
if st.button("← Back to All Accounts"):
    # Clear any editing states
    if 'edit_use_case_id' in st.session_state:
        del st.session_state.edit_use_case_id
    if 'selected_account' in st.session_state:
        del st.session_state.selected_account
    
    # Use JavaScript redirect as it works reliably in deployment
    st.markdown("""
    <script>
    window.location.href = window.location.origin;
    </script>
    """, unsafe_allow_html=True)
    st.stop()

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
    
    # Add new Azure DevOps link
    with st.expander("Add Azure DevOps Link"):
        new_azure_link = st.text_input("Azure DevOps URL", key="new_azure_link")
        if st.button("Add Azure DevOps Link"):
            if new_azure_link:
                add_azure_devops_link(account['bsnid'], new_azure_link)
                st.success("✅ Azure DevOps link has been successfully added to this account!")
                st.rerun()
            else:
                st.error("Please enter a valid URL before adding the link.")
    
    st.markdown("---")
    
    # Artifacts Folder Links
    st.write("**Artifacts Folder Links:**")
    if account['artifacts_folder_links']:
        for i, link in enumerate(account['artifacts_folder_links']):
            st.markdown(f"[Artifacts Folder {i+1}]({link})")
    else:
        st.write("No artifacts folder links available")
    
    # Add new artifacts folder link
    with st.expander("Add Artifacts Folder Link"):
        new_artifacts_link = st.text_input("Artifacts Folder URL", key="new_artifacts_link")
        if st.button("Add Artifacts Folder Link"):
            if new_artifacts_link:
                add_artifacts_folder_link(account['bsnid'], new_artifacts_link)
                st.success("✅ Artifacts folder link has been successfully added to this account!")
                st.rerun()
            else:
                st.error("Please enter a valid URL before adding the link.")

st.markdown("---")

# Platforms and Onboarding Status
st.subheader("Platforms & Onboarding Status")

platforms_col1, platforms_col2 = st.columns(2)

with platforms_col1:
    st.write("**Current Platform Status:**")
    if account['platforms_status']:
        for platform, status in account['platforms_status'].items():
            # Color coding for status
            if status == 'Completed':
                st.success(f"{platform}: {status}")
            elif status == 'In Progress':
                st.warning(f"{platform}: {status}")
            else:  # Requested
                st.info(f"{platform}: {status}")
    else:
        st.write("No platforms configured")

with platforms_col2:
    st.write("**Manage Platforms:**")
    
    # Add new platform
    with st.expander("Add Platform"):
        available_platforms = [p for p in st.session_state.platforms if p not in account['platforms_status']]
        if available_platforms:
            new_platform = st.selectbox("Select Platform", available_platforms, key="new_platform")
            new_platform_status = st.selectbox("Initial Status", st.session_state.onboarding_statuses, key="new_platform_status")
            if st.button("Add Platform"):
                add_platform_to_account(account['bsnid'], new_platform, new_platform_status)
                st.session_state.account_success_message = f"✅ {new_platform} platform has been successfully added with status '{new_platform_status}'!"
                st.rerun()
        else:
            st.write("All platforms already added")
    
    # Update platform status
    if account['platforms_status']:
        with st.expander("Update Platform Status"):
            platform_to_update = st.selectbox("Select Platform", list(account['platforms_status'].keys()), key="update_platform")
            new_status = st.selectbox("New Status", st.session_state.onboarding_statuses, key="update_status")
            if st.button("Update Status"):
                update_platform_status(account['bsnid'], platform_to_update, new_status)
                st.session_state.account_success_message = f"✅ {platform_to_update} status has been successfully updated to '{new_status}'!"
                st.rerun()

st.markdown("---")

# Use Cases
st.subheader("Use Cases")

use_cases = get_account_use_cases(account['bsnid'])

if use_cases:
    # Display use cases in a table format
    use_cases_data = []
    for uc in use_cases:
        use_cases_data.append({
            'Problem': uc['problem'][:50] + "..." if len(uc['problem']) > 50 else uc['problem'],
            'Solution': uc['solution'][:50] + "..." if len(uc['solution']) > 50 else uc['solution'],
            'Leader': uc['leader'],
            'Status': uc['status'],
            'Enablement Tier': uc['enablement_tier'],
            'Platform': uc.get('platform', 'Not specified'),
            'ID': uc['id']
        })
    
    df = pd.DataFrame(use_cases_data)
    st.dataframe(df.drop('ID', axis=1), use_container_width=True)
    
    # Edit use cases
    st.write("**Edit Use Cases:**")
    for uc in use_cases:
        with st.expander(f"Edit: {uc['problem'][:30]}..."):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Problem:** {uc['problem']}")
                st.write(f"**Solution:** {uc['solution']}")
            with col2:
                st.write(f"**Leader:** {uc['leader']}")
                st.write(f"**Status:** {uc['status']}")
                st.write(f"**Enablement Tier:** {uc['enablement_tier']}")
                st.write(f"**Platform:** {uc.get('platform', 'Not specified')}")
            
            if st.button(f"Edit Use Case", key=f"edit_uc_{uc['id']}"):
                st.session_state.edit_use_case_id = uc['id']
                st.switch_page("pages/2_Use_Cases.py")

else:
    st.info("No use cases found for this account")

st.markdown("---")

# Updates
st.subheader("Recent Updates")

updates = get_account_updates(account['bsnid'])

if updates:
    # Display the most recent updates
    recent_updates = sorted(updates, key=lambda x: x['date'], reverse=True)[:5]
    
    for update in recent_updates:
        with st.expander(f"{update['date'].strftime('%Y-%m-%d')} - {update['platform']}"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**Description:** {update['description']}")
            with col2:
                st.write(f"**Author:** {update['author']}")
                st.write(f"**Platform:** {update['platform']}")
                st.write(f"**Date:** {update['date'].strftime('%Y-%m-%d')}")
    
    if len(updates) > 5:
        st.info(f"Showing 5 most recent updates. Total updates: {len(updates)}")
        
else:
    st.info("No updates found for this account")

# Quick actions
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Add Use Case", use_container_width=True):
        st.session_state.selected_account_for_use_case = account['bsnid']
        st.switch_page("pages/2_Use_Cases.py")

with col2:
    if st.button("View All Use Cases", use_container_width=True):
        st.switch_page("pages/2_Use_Cases.py")
        
with col3:
    if st.button("View All Updates", use_container_width=True):
        st.switch_page("pages/4_Updates.py")

with col4:
    if st.button("Admin Panel", use_container_width=True):
        st.switch_page("pages/3_Admin.py")

# Account summary sidebar
st.sidebar.title("Account Summary")
st.sidebar.write(f"**Account:** {account['team']}")
st.sidebar.write(f"**Business Area:** {account['business_area']}")
st.sidebar.metric("Platforms", len(account['platforms_status']))
st.sidebar.metric("Use Cases", len(use_cases))
st.sidebar.metric("Azure DevOps Links", len(account['azure_devops_links']))
st.sidebar.metric("Artifacts Links", len(account['artifacts_folder_links']))

# Platform status summary
if account['platforms_status']:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Platform Status")
    for platform, status in account['platforms_status'].items():
        if status == 'Completed':
            st.sidebar.success(f"{platform}: {status}")
        elif status == 'In Progress':
            st.sidebar.warning(f"{platform}: {status}")
        else:
            st.sidebar.info(f"{platform}: {status}")
