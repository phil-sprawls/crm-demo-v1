import streamlit as st
import pandas as pd
from utils.data_manager import (
    initialize_data, add_account, update_primary_it_partner, 
    add_use_case, add_platform_to_account
)

# Page configuration
st.set_page_config(
    page_title="Admin Panel - CRM System",
    page_icon="⚙️",
    layout="wide"
)

# Initialize data
initialize_data()

st.title("⚙️ Admin Panel")

# Show persistent success message if exists
if 'admin_success_message' in st.session_state:
    st.success(st.session_state.admin_success_message)
    # Clear the message after showing it
    del st.session_state.admin_success_message

# Back button
if st.button("← Back to All Accounts"):
    st.switch_page("app.py")

st.markdown("---")

# Tab navigation for admin functions
tab1, tab2, tab3, tab4 = st.tabs(["👥 IT Partners", "🏢 Add Account", "💡 Add Use Case", "🚀 Add Platform"])

# Tab 1: Primary IT Partners Management
with tab1:
    st.subheader("🔧 Primary IT Partners by Business Area")
    st.write("Manage the primary IT partner assignments for each business area.")
    
    # Display current assignments
    st.write("**Current Assignments:**")
    partners_df = pd.DataFrame([
        {"Business Area": ba, "Primary IT Partner": partner} 
        for ba, partner in st.session_state.business_areas.items()
    ])
    st.dataframe(partners_df, use_container_width=True)
    
    st.markdown("---")
    
    # Update IT Partner form
    st.subheader("Update IT Partner Assignment")
    
    with st.form("update_partner_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            business_area = st.selectbox("Business Area", list(st.session_state.business_areas.keys()))
            current_partner = st.session_state.business_areas[business_area]
            st.write(f"**Current Partner:** {current_partner}")
        
        with col2:
            new_partner = st.text_input("New Primary IT Partner", value=current_partner)
        
        if st.form_submit_button("Update IT Partner", use_container_width=True):
            if new_partner:
                update_primary_it_partner(business_area, new_partner)
                st.session_state.admin_success_message = f"✅ Primary IT Partner for {business_area} has been successfully updated to {new_partner}!"
                st.rerun()
            else:
                st.error("Please enter a partner name")
    
    # Add new business area
    st.markdown("---")
    st.subheader("Add New Business Area")
    
    with st.form("add_business_area_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_ba_name = st.text_input("Business Area Name")
        
        with col2:
            new_ba_partner = st.text_input("Primary IT Partner")
        
        if st.form_submit_button("Add Business Area", use_container_width=True):
            if new_ba_name and new_ba_partner:
                if new_ba_name not in st.session_state.business_areas:
                    st.session_state.business_areas[new_ba_name] = new_ba_partner
                    st.success(f"✅ Business Area '{new_ba_name}' has been successfully created with IT Partner '{new_ba_partner}'!")
                    st.rerun()
                else:
                    st.error("Business Area already exists")
            else:
                st.error("Please fill in both fields")

# Tab 2: Add New Account
with tab2:
    st.subheader("➕ Add New Account")
    st.write("Create a new account in the CRM system.")
    
    with st.form("add_account_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            team_name = st.text_input("Team Name*", help="Name of the team or department")
            business_area = st.selectbox("Business Area*", list(st.session_state.business_areas.keys()))
            vp_name = st.text_input("VP Name*", help="Vice President overseeing this team")
        
        with col2:
            admin_name = st.text_input("Admin Name*", help="Administrator for this account")
            # Auto-populate IT partner based on business area
            it_partner = st.text_input("Primary IT Partner*", 
                                     value=st.session_state.business_areas.get(business_area, ""),
                                     help="Primary IT partner (auto-filled based on business area)")
        
        st.markdown("**Initial Platform Setup (Optional)**")
        
        # Platform selection
        platform_cols = st.columns(len(st.session_state.platforms))
        selected_platforms = {}
        
        for i, platform in enumerate(st.session_state.platforms):
            with platform_cols[i]:
                include_platform = st.checkbox(f"Include {platform}")
                if include_platform:
                    platform_status = st.selectbox(f"{platform} Status", 
                                                 st.session_state.onboarding_statuses,
                                                 key=f"status_{platform}")
                    selected_platforms[platform] = platform_status
        
        submitted = st.form_submit_button("Create Account", use_container_width=True)
        
        if submitted:
            if team_name and business_area and vp_name and admin_name and it_partner:
                bsnid = add_account(team_name, business_area, vp_name, admin_name, it_partner, selected_platforms)
                # Store success message to show after page refresh
                st.session_state.admin_success_message = f"✅ New account '{team_name}' has been successfully created! You can now find it in the All Accounts screen."
                st.balloons()
                st.rerun()
            else:
                st.error("Please fill in all required fields (marked with *)")

# Tab 3: Add Use Case
with tab3:
    st.subheader("💡 Add New Use Case")
    st.write("Create a new use case and assign it to an account.")
    
    if not st.session_state.accounts:
        st.warning("No accounts available. Please add accounts first.")
    else:
        with st.form("add_use_case_admin_form"):
            # Account selection
            account_options = {bsnid: f"{acc['team']} ({acc['business_area']})" 
                            for bsnid, acc in st.session_state.accounts.items()}
            selected_account = st.selectbox("Select Account*", 
                                          options=list(account_options.keys()),
                                          format_func=lambda x: account_options[x])
            
            col1, col2 = st.columns(2)
            
            with col1:
                problem = st.text_area("Problem Description*", height=100)
                solution = st.text_area("Solution Description*", height=100)
            
            with col2:
                leader = st.text_input("Leader*")
                status = st.selectbox("Status*", ["Active", "Completed", "On Hold", "Cancelled", "Planning"])
                enablement_tier = st.selectbox("Enablement Tier*", st.session_state.enablement_tiers)
            
            if st.form_submit_button("Create Use Case", use_container_width=True):
                if problem and solution and leader:
                    use_case_id = add_use_case(selected_account, problem, solution, leader, status, enablement_tier)
                    account_name = st.session_state.accounts[selected_account]['team']
                    st.session_state.admin_success_message = f"✅ New use case has been successfully created and added to {account_name}!"
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (marked with *)")

# Tab 4: Add Platform to Account
with tab4:
    st.subheader("🚀 Add Platform to Account")
    st.write("Add a new platform to an existing account.")
    
    if not st.session_state.accounts:
        st.warning("No accounts available. Please add accounts first.")
    else:
        with st.form("add_platform_form"):
            # Account selection
            account_options = {bsnid: f"{acc['team']} ({acc['business_area']})" 
                            for bsnid, acc in st.session_state.accounts.items()}
            selected_account = st.selectbox("Select Account*", 
                                          options=list(account_options.keys()),
                                          format_func=lambda x: account_options[x])
            
            # Show current platforms for selected account
            if selected_account:
                current_platforms = st.session_state.accounts[selected_account]['platforms_status']
                if current_platforms:
                    st.write("**Current Platforms:**")
                    for platform, status in current_platforms.items():
                        st.write(f"- {platform}: {status}")
                
                # Available platforms (not already added)
                available_platforms = [p for p in st.session_state.platforms if p not in current_platforms]
                
                if available_platforms:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        platform = st.selectbox("Platform*", available_platforms)
                    
                    with col2:
                        status = st.selectbox("Initial Status*", st.session_state.onboarding_statuses)
                    
                    if st.form_submit_button("Add Platform", use_container_width=True):
                        add_platform_to_account(selected_account, platform, status)
                        account_name = st.session_state.accounts[selected_account]['team']
                        st.success(f"✅ {platform} platform has been successfully added to {account_name} with status '{status}'!")
                        st.rerun()
                else:
                    st.info("All platforms are already added to this account.")

# System Statistics
st.markdown("---")
st.subheader("📊 System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Accounts", len(st.session_state.accounts))

with col2:
    st.metric("Total Use Cases", len(st.session_state.use_cases))

with col3:
    st.metric("Business Areas", len(st.session_state.business_areas))

with col4:
    total_platforms = sum(len(acc['platforms_status']) for acc in st.session_state.accounts.values())
    st.metric("Platform Instances", total_platforms)

# Recent Activity
if st.session_state.accounts or st.session_state.use_cases:
    st.markdown("---")
    st.subheader("📈 Recent Activity")
    
    # Show recent accounts
    if st.session_state.accounts:
        st.write("**Recent Accounts:**")
        recent_accounts = sorted(st.session_state.accounts.values(), 
                               key=lambda x: x['created_at'], reverse=True)[:3]
        for acc in recent_accounts:
            st.write(f"- {acc['team']} ({acc['business_area']}) - {acc['created_at'].strftime('%Y-%m-%d %H:%M')}")
    
    # Show recent use cases
    if st.session_state.use_cases:
        st.write("**Recent Use Cases:**")
        recent_use_cases = sorted(st.session_state.use_cases.values(), 
                                key=lambda x: x['created_at'], reverse=True)[:3]
        for uc in recent_use_cases:
            account_info = st.session_state.accounts.get(uc['account_bsnid'], {})
            st.write(f"- {uc['problem'][:50]}... ({account_info.get('team', 'Unknown Account')}) - {uc['created_at'].strftime('%Y-%m-%d %H:%M')}")

# Admin Navigation
st.sidebar.title("⚙️ Admin Functions")
st.sidebar.markdown("""
**Available Actions:**
- 👥 **IT Partners**: Manage primary IT partner assignments
- 🏢 **Add Account**: Create new accounts
- 💡 **Add Use Case**: Create new use cases
- 🚀 **Add Platform**: Add platforms to accounts

**Quick Tips:**
- IT partners are automatically assigned based on business area
- All fields marked with * are required
- Use the tabs above to navigate between different admin functions
""")

st.sidebar.markdown("---")
st.sidebar.subheader("🔧 System Configuration")
st.sidebar.write(f"**Available Platforms:** {', '.join(st.session_state.platforms)}")
st.sidebar.write(f"**Onboarding Statuses:** {', '.join(st.session_state.onboarding_statuses)}")
st.sidebar.write(f"**Enablement Tiers:** {', '.join(st.session_state.enablement_tiers)}")
