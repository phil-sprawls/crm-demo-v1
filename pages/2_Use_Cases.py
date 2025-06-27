import streamlit as st
import pandas as pd
from utils.data_manager import (
    initialize_data, add_use_case, update_use_case, get_account_use_cases
)

# Page configuration
st.set_page_config(
    page_title="Use Cases - CRM System",
    page_icon="💡",
    layout="wide"
)

# Initialize data
initialize_data()

st.title("💡 Use Cases Management")

# Back button
if st.button("← Back to All Accounts"):
    st.switch_page("app.py")

st.markdown("---")

# Check if editing a specific use case
edit_mode = False
if 'edit_use_case_id' in st.session_state and st.session_state.edit_use_case_id in st.session_state.use_cases:
    edit_mode = True
    use_case_to_edit = st.session_state.use_cases[st.session_state.edit_use_case_id]
    st.info(f"Editing use case: {use_case_to_edit['problem'][:50]}...")

# Add/Edit Use Case Form
st.subheader("➕ Add New Use Case" if not edit_mode else "✏️ Edit Use Case")

with st.form("use_case_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        # Account selection
        if not edit_mode and 'selected_account_for_use_case' in st.session_state:
            selected_account = st.session_state.selected_account_for_use_case
            account_options = {bsnid: f"{acc['team']} ({acc['business_area']})" 
                            for bsnid, acc in st.session_state.accounts.items()}
            selected_account_display = account_options.get(selected_account, "Unknown Account")
            st.write(f"**Account:** {selected_account_display}")
        else:
            account_options = {bsnid: f"{acc['team']} ({acc['business_area']})" 
                            for bsnid, acc in st.session_state.accounts.items()}
            if account_options:
                if edit_mode:
                    # Find the current account for the use case
                    current_account = use_case_to_edit['account_bsnid']
                    current_index = list(account_options.keys()).index(current_account) if current_account in account_options else 0
                    selected_account = st.selectbox("Select Account", 
                                                  options=list(account_options.keys()),
                                                  format_func=lambda x: account_options[x],
                                                  index=current_index)
                else:
                    selected_account = st.selectbox("Select Account", 
                                                  options=list(account_options.keys()),
                                                  format_func=lambda x: account_options[x])
            else:
                st.error("No accounts available. Please add accounts first.")
                st.stop()
        
        # Problem description
        problem = st.text_area("Problem Description", 
                             value=use_case_to_edit['problem'] if edit_mode else "",
                             height=100,
                             help="Describe the business problem or challenge")
        
        # Solution description
        solution = st.text_area("Solution Description", 
                              value=use_case_to_edit['solution'] if edit_mode else "",
                              height=100,
                              help="Describe the proposed or implemented solution")
    
    with col2:
        # Leader
        leader = st.text_input("Leader", 
                             value=use_case_to_edit['leader'] if edit_mode else "",
                             help="Person responsible for this use case")
        
        # Status
        status_options = ["Active", "Completed", "On Hold", "Cancelled", "Planning"]
        current_status_index = 0
        if edit_mode and use_case_to_edit['status'] in status_options:
            current_status_index = status_options.index(use_case_to_edit['status'])
        
        status = st.selectbox("Status", 
                            options=status_options,
                            index=current_status_index)
        
        # Enablement Tier
        tier_index = 0
        if edit_mode and use_case_to_edit['enablement_tier'] in st.session_state.enablement_tiers:
            tier_index = st.session_state.enablement_tiers.index(use_case_to_edit['enablement_tier'])
        
        enablement_tier = st.selectbox("Enablement Tier", 
                                     st.session_state.enablement_tiers,
                                     index=tier_index,
                                     help="Select the appropriate enablement tier")
    
    # Form submission
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        submitted = st.form_submit_button("Update Use Case" if edit_mode else "Add Use Case", 
                                        use_container_width=True)
    
    with col2:
        if edit_mode:
            cancelled = st.form_submit_button("Cancel Edit", use_container_width=True)
            if cancelled:
                if 'edit_use_case_id' in st.session_state:
                    del st.session_state.edit_use_case_id
                st.rerun()
    
    if submitted:
        if problem and solution and leader:
            if edit_mode:
                update_use_case(st.session_state.edit_use_case_id, problem, solution, leader, status, enablement_tier)
                st.success("Use case updated successfully!")
                if 'edit_use_case_id' in st.session_state:
                    del st.session_state.edit_use_case_id
            else:
                use_case_id = add_use_case(selected_account, problem, solution, leader, status, enablement_tier)
                st.success(f"Use case added successfully! ID: {use_case_id}")
                if 'selected_account_for_use_case' in st.session_state:
                    del st.session_state.selected_account_for_use_case
            st.rerun()
        else:
            st.error("Please fill in all required fields (Problem, Solution, Leader)")

st.markdown("---")

# Display all use cases
st.subheader("📋 All Use Cases")

if st.session_state.use_cases:
    # Create a comprehensive view of all use cases
    use_cases_data = []
    for uc_id, uc in st.session_state.use_cases.items():
        account_info = st.session_state.accounts.get(uc['account_bsnid'], {})
        use_cases_data.append({
            'Account': account_info.get('team', 'Unknown'),
            'Business Area': account_info.get('business_area', 'Unknown'),
            'Problem': uc['problem'][:60] + "..." if len(uc['problem']) > 60 else uc['problem'],
            'Solution': uc['solution'][:60] + "..." if len(uc['solution']) > 60 else uc['solution'],
            'Leader': uc['leader'],
            'Status': uc['status'],
            'Enablement Tier': uc['enablement_tier'],
            'ID': uc_id
        })
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        business_areas = ['All'] + list(set([uc['Business Area'] for uc in use_cases_data]))
        selected_ba = st.selectbox("Filter by Business Area", business_areas)
    
    with col2:
        statuses = ['All'] + list(set([uc['Status'] for uc in use_cases_data]))
        selected_status = st.selectbox("Filter by Status", statuses)
    
    with col3:
        tiers = ['All'] + list(set([uc['Enablement Tier'] for uc in use_cases_data]))
        selected_tier = st.selectbox("Filter by Enablement Tier", tiers)
    
    # Apply filters
    filtered_data = use_cases_data.copy()
    if selected_ba != 'All':
        filtered_data = [uc for uc in filtered_data if uc['Business Area'] == selected_ba]
    if selected_status != 'All':
        filtered_data = [uc for uc in filtered_data if uc['Status'] == selected_status]
    if selected_tier != 'All':
        filtered_data = [uc for uc in filtered_data if uc['Enablement Tier'] == selected_tier]
    
    st.write(f"**Showing {len(filtered_data)} of {len(use_cases_data)} use cases**")
    
    # Display filtered use cases
    if filtered_data:
        for i, uc_data in enumerate(filtered_data):
            with st.expander(f"🎯 {uc_data['Account']} - {uc_data['Problem'][:40]}..."):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Account:** {uc_data['Account']}")
                    st.write(f"**Business Area:** {uc_data['Business Area']}")
                    st.write(f"**Problem:** {st.session_state.use_cases[uc_data['ID']]['problem']}")
                    st.write(f"**Solution:** {st.session_state.use_cases[uc_data['ID']]['solution']}")
                
                with col2:
                    st.write(f"**Leader:** {uc_data['Leader']}")
                    st.write(f"**Status:** {uc_data['Status']}")
                    st.write(f"**Enablement Tier:** {uc_data['Enablement Tier']}")
                    
                    # Action buttons
                    col_edit, col_view = st.columns(2)
                    with col_edit:
                        if st.button(f"Edit", key=f"edit_{uc_data['ID']}"):
                            st.session_state.edit_use_case_id = uc_data['ID']
                            st.rerun()
                    with col_view:
                        if st.button(f"View Account", key=f"view_{uc_data['ID']}"):
                            st.session_state.selected_account = st.session_state.use_cases[uc_data['ID']]['account_bsnid']
                            st.switch_page("pages/1_Account_Details.py")
    else:
        st.info("No use cases match the selected filters.")
        
else:
    st.info("No use cases available. Add your first use case using the form above.")

# Statistics
st.markdown("---")
st.subheader("📊 Use Case Statistics")

if st.session_state.use_cases:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Use Cases", len(st.session_state.use_cases))
    
    with col2:
        active_count = len([uc for uc in st.session_state.use_cases.values() if uc['status'] == 'Active'])
        st.metric("Active Use Cases", active_count)
    
    with col3:
        completed_count = len([uc for uc in st.session_state.use_cases.values() if uc['status'] == 'Completed'])
        st.metric("Completed Use Cases", completed_count)
    
    with col4:
        tier1_count = len([uc for uc in st.session_state.use_cases.values() if uc['enablement_tier'] == 'Tier 1'])
        st.metric("Tier 1 Use Cases", tier1_count)

# Navigation
st.sidebar.title("🧭 Navigation")
st.sidebar.markdown("""
- **Add/Edit**: Use the form above to add new or edit existing use cases
- **Filter**: Use the filter options to find specific use cases
- **View Account**: Click "View Account" to see the full account details
""")

if st.session_state.use_cases:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Quick Stats")
    
    # Status distribution
    status_counts = {}
    for uc in st.session_state.use_cases.values():
        status_counts[uc['status']] = status_counts.get(uc['status'], 0) + 1
    
    for status, count in status_counts.items():
        st.sidebar.write(f"**{status}:** {count}")
