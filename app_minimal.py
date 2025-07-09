import streamlit as st
import pandas as pd
import uuid

# Page configuration
st.set_page_config(
    page_title="EDIP CRM - All Accounts",
    page_icon="📊",
    layout="wide"
)

# Initialize sample data
@st.cache_data
def get_sample_data():
    """Get sample accounts data"""
    return [
        {
            'bsnid': 'BSN001',
            'team': 'Data Engineering',
            'business_area': 'Engineering',
            'vp': 'Sarah Johnson',
            'admin': 'Mike Chen',
            'primary_it_partner': 'TechCorp Solutions'
        },
        {
            'bsnid': 'BSN002',
            'team': 'Marketing Analytics',
            'business_area': 'Marketing',
            'vp': 'David Wilson',
            'admin': 'Lisa Rodriguez',
            'primary_it_partner': 'DataFlow Partners'
        },
        {
            'bsnid': 'BSN003',
            'team': 'Sales Operations',
            'business_area': 'Sales',
            'vp': 'Jennifer Davis',
            'admin': 'Robert Kim',
            'primary_it_partner': 'CloudNet Services'
        },
        {
            'bsnid': 'BSN004',
            'team': 'Finance Analytics',
            'business_area': 'Finance',
            'vp': 'Michael Brown',
            'admin': 'Angela Lee',
            'primary_it_partner': 'SecureSync Technologies'
        },
        {
            'bsnid': 'BSN005',
            'team': 'HR Analytics',
            'business_area': 'HR',
            'vp': 'Emily White',
            'admin': 'James Wilson',
            'primary_it_partner': 'SystemLink Solutions'
        }
    ]

def filter_accounts(accounts, search_term):
    """Filter accounts based on search term"""
    if not search_term:
        return accounts
    
    search_term = search_term.lower()
    filtered = []
    
    for account in accounts:
        # Search in all relevant fields
        searchable_text = f"{account['team']} {account['business_area']} {account['vp']} {account['admin']} {account['primary_it_partner']}".lower()
        
        if search_term in searchable_text:
            filtered.append(account)
    
    return filtered

def main():
    """Main application"""
    st.title("EDIP CRM - All Accounts")
    
    # Get sample data
    accounts = get_sample_data()
    
    # Search functionality
    search_term = st.text_input("Search accounts by team, business area, VP, admin, or IT partner", "")
    
    # Filter accounts
    filtered_accounts = filter_accounts(accounts, search_term)
    
    if filtered_accounts:
        st.subheader(f"Accounts ({len(filtered_accounts)} found)")
        
        # Display accounts in a table
        df = pd.DataFrame(filtered_accounts)
        
        # Rename columns for display
        df_display = df.rename(columns={
            'bsnid': 'BSNID',
            'team': 'Team',
            'business_area': 'Business Area',
            'vp': 'VP',
            'admin': 'Admin',
            'primary_it_partner': 'Primary IT Partner'
        })
        
        # Display the table
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Account selection
        st.subheader("Account Details")
        
        # Create selectbox for account selection
        account_options = {f"{acc['bsnid']} - {acc['team']}": acc['bsnid'] for acc in filtered_accounts}
        
        if account_options:
            selected_display = st.selectbox(
                "Select an account to view details:",
                options=list(account_options.keys()),
                index=0
            )
            
            selected_bsnid = account_options[selected_display]
            selected_account = next(acc for acc in filtered_accounts if acc['bsnid'] == selected_bsnid)
            
            # Display selected account details
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**BSNID:**", selected_account['bsnid'])
                st.write("**Team:**", selected_account['team'])
                st.write("**Business Area:**", selected_account['business_area'])
            
            with col2:
                st.write("**VP:**", selected_account['vp'])
                st.write("**Admin:**", selected_account['admin'])
                st.write("**Primary IT Partner:**", selected_account['primary_it_partner'])
            
            # Platform Status
            st.subheader("Platform Status")
            platforms = ['Databricks', 'Snowflake', 'Power Platform']
            statuses = ['Not Started', 'In Progress', 'Completed', 'On Hold']
            
            platform_col1, platform_col2, platform_col3 = st.columns(3)
            
            with platform_col1:
                st.write("**Databricks:**")
                st.select_slider("Status", options=statuses, value="In Progress", key="databricks_status")
            
            with platform_col2:
                st.write("**Snowflake:**")
                st.select_slider("Status", options=statuses, value="Not Started", key="snowflake_status")
            
            with platform_col3:
                st.write("**Power Platform:**")
                st.select_slider("Status", options=statuses, value="Completed", key="power_platform_status")
            
            # Use Cases Section
            st.subheader("Use Cases")
            
            # Sample use cases
            use_cases = [
                {
                    'problem': 'Need to optimize ETL pipeline performance',
                    'solution': 'Implement Apache Spark optimization techniques',
                    'leader': selected_account['admin'],
                    'status': 'In Progress',
                    'platform': 'Databricks'
                },
                {
                    'problem': 'Customer segmentation analysis required',
                    'solution': 'Build ML model for customer clustering',
                    'leader': selected_account['admin'],
                    'status': 'Completed',
                    'platform': 'Snowflake'
                }
            ]
            
            for i, use_case in enumerate(use_cases):
                with st.expander(f"Use Case {i+1}: {use_case['problem'][:50]}..."):
                    st.write("**Problem:**", use_case['problem'])
                    st.write("**Solution:**", use_case['solution'])
                    st.write("**Leader:**", use_case['leader'])
                    st.write("**Status:**", use_case['status'])
                    st.write("**Platform:**", use_case['platform'])
            
            # Recent Updates
            st.subheader("Recent Updates")
            
            sample_updates = [
                {
                    'date': '2024-07-08',
                    'author': selected_account['admin'],
                    'platform': 'Databricks',
                    'description': 'Completed initial data pipeline setup and testing'
                },
                {
                    'date': '2024-07-05',
                    'author': selected_account['admin'],
                    'platform': 'Snowflake',
                    'description': 'Started data warehouse configuration'
                }
            ]
            
            for update in sample_updates:
                with st.container():
                    st.write(f"**{update['date']}** - {update['author']} ({update['platform']})")
                    st.write(update['description'])
                    st.divider()
    
    else:
        if search_term:
            st.info("No accounts found matching your search criteria.")
        else:
            st.warning("No accounts available.")
    
    # Footer
    st.markdown("---")
    st.markdown("**EDIP CRM System** - Professional Customer Relationship Management")

if __name__ == "__main__":
    main()