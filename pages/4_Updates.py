import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import (
    initialize_data, add_update, get_account_updates, update_update
)

# Page configuration
st.set_page_config(
    page_title="Updates - EDIP CRM",
    page_icon="📊",
    layout="wide"
)

# Initialize data
initialize_data()

st.title("Updates Management")

# Show persistent success message if exists
if 'update_success_message' in st.session_state:
    st.success(st.session_state.update_success_message)
    del st.session_state.update_success_message

# Back button - using JavaScript redirect for deployment compatibility
if st.button("← Back to All Accounts"):
    # Use JavaScript redirect as it works reliably in deployment
    st.markdown("""
    <script>
    window.location.href = window.location.origin;
    </script>
    """, unsafe_allow_html=True)
    st.stop()

st.markdown("---")

# Create tabs for Updates functionality
update_tab1, update_tab2 = st.tabs(["Add Update", "View All Updates"])

with update_tab1:
    st.subheader("Add New Update")
    
    with st.form("add_update_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Account selection for update
            if st.session_state.accounts:
                account_options = [(bsnid, f"{account['team']} ({account['business_area']})") 
                                 for bsnid, account in st.session_state.accounts.items()]
                account_labels = [label for _, label in account_options]
                account_values = [bsnid for bsnid, _ in account_options]
                
                selected_account_idx = st.selectbox("Select Account", 
                                                   range(len(account_labels)),
                                                   format_func=lambda x: account_labels[x],
                                                   help="Choose the account for this update")
                selected_update_account = account_values[selected_account_idx]
            else:
                st.error("No accounts available. Please add accounts first.")
                st.stop()
            
            # Author
            author = st.text_input("Author", 
                                 help="Person creating this update")
            
            # Date
            update_date = st.date_input("Date", 
                                      help="Date of this update")
            
        with col2:
            # Platform selection
            platform = st.selectbox("Platform", 
                                   st.session_state.platforms,
                                   help="Select the platform this update relates to")
            
            # Description
            description = st.text_area("Description", 
                                     height=100,
                                     help="Describe the update or progress made")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submitted_update = st.form_submit_button("Add Update", use_container_width=True)
        
        if submitted_update:
            if author and description and update_date:
                # Convert date to datetime for consistency
                update_datetime = datetime.combine(update_date, datetime.min.time())
                add_update(selected_update_account, author, update_datetime, platform, description)
                account_name = st.session_state.accounts[selected_update_account]['team']
                st.session_state.update_success_message = f"✅ Update has been successfully added to {account_name}!"
                st.rerun()
            else:
                st.error("Please fill in all required fields (Author, Date, and Description)")

with update_tab2:
    st.subheader("All Updates")
    
    if st.session_state.updates:
        # Create a comprehensive view of all updates
        updates_data = []
        for update_id, update in st.session_state.updates.items():
            account_info = st.session_state.accounts.get(update['account_bsnid'], {})
            updates_data.append({
                'Account': account_info.get('team', 'Unknown'),
                'Business Area': account_info.get('business_area', 'Unknown'),
                'Author': update['author'],
                'Date': update['date'].strftime('%Y-%m-%d %H:%M'),
                'Platform': update['platform'],
                'Description': update['description'][:80] + "..." if len(update['description']) > 80 else update['description'],
                'Full Description': update['description'],
                'ID': update_id
            })
        
        # Filter options for updates
        col1, col2, col3 = st.columns(3)
        
        with col1:
            update_business_areas = ['All'] + list(set([upd['Business Area'] for upd in updates_data]))
            selected_update_ba = st.selectbox("Filter by Business Area", update_business_areas, key="update_ba_filter")
        
        with col2:
            update_platforms = ['All'] + list(set([upd['Platform'] for upd in updates_data]))
            selected_update_platform = st.selectbox("Filter by Platform", update_platforms, key="update_platform_filter")
        
        with col3:
            update_authors = ['All'] + list(set([upd['Author'] for upd in updates_data]))
            selected_update_author = st.selectbox("Filter by Author", update_authors, key="update_author_filter")
        
        # Apply filters
        filtered_updates = updates_data
        if selected_update_ba != 'All':
            filtered_updates = [upd for upd in filtered_updates if upd['Business Area'] == selected_update_ba]
        if selected_update_platform != 'All':
            filtered_updates = [upd for upd in filtered_updates if upd['Platform'] == selected_update_platform]
        if selected_update_author != 'All':
            filtered_updates = [upd for upd in filtered_updates if upd['Author'] == selected_update_author]
        
        st.write(f"**Showing {len(filtered_updates)} of {len(updates_data)} updates**")
        
        # Display updates
        for update in filtered_updates:
            with st.expander(f"{update['Account']} - {update['Platform']} - {update['Date']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Account:** {update['Account']}")
                    st.write(f"**Business Area:** {update['Business Area']}")
                
                with col2:
                    st.write(f"**Author:** {update['Author']}")
                    st.write(f"**Platform:** {update['Platform']}")
                
                with col3:
                    st.write(f"**Date:** {update['Date']}")
                
                st.markdown("**Description:**")
                st.write(update['Full Description'])
    
    else:
        st.info("No updates available. Add your first update using the form above.")

# Statistics
st.markdown("---")
st.subheader("Update Statistics")

if st.session_state.updates:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Updates", len(st.session_state.updates))
    
    with col2:
        platform_counts = {}
        for update in st.session_state.updates.values():
            platform_counts[update['platform']] = platform_counts.get(update['platform'], 0) + 1
        if platform_counts:
            most_used_platform = sorted(platform_counts.items(), key=lambda x: x[1], reverse=True)[0][0]
        else:
            most_used_platform = "None"
        st.metric("Most Active Platform", most_used_platform)
    
    with col3:
        author_counts = {}
        for update in st.session_state.updates.values():
            author_counts[update['author']] = author_counts.get(update['author'], 0) + 1
        if author_counts:
            most_active_author = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[0][0]
        else:
            most_active_author = "None"
        st.metric("Most Active Author", most_active_author)
    
    with col4:
        business_area_counts = {}
        for update in st.session_state.updates.values():
            account_info = st.session_state.accounts.get(update['account_bsnid'], {})
            ba = account_info.get('business_area', 'Unknown')
            business_area_counts[ba] = business_area_counts.get(ba, 0) + 1
        if business_area_counts:
            most_active_ba = sorted(business_area_counts.items(), key=lambda x: x[1], reverse=True)[0][0]
        else:
            most_active_ba = "None"
        st.metric("Most Active Business Area", most_active_ba)

# Navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("""
- **Add Update**: Use the form above to add new updates
- **Filter**: Use the filter options to find specific updates
- **Statistics**: View update statistics and trends
""")

if st.session_state.updates:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Quick Stats")
    
    # Platform distribution
    platform_counts = {}
    for update in st.session_state.updates.values():
        platform_counts[update['platform']] = platform_counts.get(update['platform'], 0) + 1
    
    for platform, count in platform_counts.items():
        st.sidebar.write(f"**{platform}:** {count} updates")