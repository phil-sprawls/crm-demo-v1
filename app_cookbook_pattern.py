import streamlit as st
import pandas as pd

# Follow the exact pattern from databricks-apps-cookbook
st.set_page_config(layout="wide")
st.title("📊 EDIP CRM System")

# Initialize sample data using the cookbook pattern
@st.cache_data
def load_accounts():
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

def main():
    # Load data
    accounts = load_accounts()
    
    # Search functionality
    search_term = st.text_input("Search accounts by team, business area, VP, admin, or IT partner", "")
    
    # Filter accounts
    if search_term:
        filtered_accounts = [
            acc for acc in accounts 
            if search_term.lower() in str(acc).lower()
        ]
    else:
        filtered_accounts = accounts
    
    if filtered_accounts:
        st.subheader(f"Accounts ({len(filtered_accounts)} found)")
        
        # Display accounts table
        df = pd.DataFrame(filtered_accounts)
        df_display = df.rename(columns={
            'bsnid': 'BSNID',
            'team': 'Team',
            'business_area': 'Business Area',
            'vp': 'VP',
            'admin': 'Admin',
            'primary_it_partner': 'Primary IT Partner'
        })
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Account selection and details
        st.subheader("Account Details")
        
        account_options = {f"{acc['bsnid']} - {acc['team']}": acc for acc in filtered_accounts}
        
        if account_options:
            selected_display = st.selectbox(
                "Select an account to view details:",
                options=list(account_options.keys()),
                index=0
            )
            
            selected_account = account_options[selected_display]
            
            # Display account details in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**BSNID:**", selected_account['bsnid'])
                st.write("**Team:**", selected_account['team'])
                st.write("**Business Area:**", selected_account['business_area'])
            
            with col2:
                st.write("**VP:**", selected_account['vp'])
                st.write("**Admin:**", selected_account['admin'])
                st.write("**Primary IT Partner:**", selected_account['primary_it_partner'])
            
            # Platform status section
            st.subheader("Platform Status")
            
            platforms = ['Databricks', 'Snowflake', 'Power Platform']
            statuses = ['Not Started', 'In Progress', 'Completed', 'On Hold']
            
            platform_col1, platform_col2, platform_col3 = st.columns(3)
            
            with platform_col1:
                st.write("**Databricks:**")
                databricks_status = st.select_slider(
                    "Databricks Status", 
                    options=statuses, 
                    value="In Progress", 
                    key=f"databricks_{selected_account['bsnid']}"
                )
            
            with platform_col2:
                st.write("**Snowflake:**")
                snowflake_status = st.select_slider(
                    "Snowflake Status", 
                    options=statuses, 
                    value="Not Started", 
                    key=f"snowflake_{selected_account['bsnid']}"
                )
            
            with platform_col3:
                st.write("**Power Platform:**")
                power_platform_status = st.select_slider(
                    "Power Platform Status", 
                    options=statuses, 
                    value="Completed", 
                    key=f"power_platform_{selected_account['bsnid']}"
                )
            
            # Use cases section
            st.subheader("Use Cases")
            
            with st.expander("View Sample Use Cases"):
                st.write("**Use Case 1:**")
                st.write("- **Problem:** Need to optimize ETL pipeline performance")
                st.write("- **Solution:** Implement Apache Spark optimization techniques")
                st.write("- **Leader:** " + selected_account['admin'])
                st.write("- **Status:** In Progress")
                st.write("- **Platform:** Databricks")
                
                st.divider()
                
                st.write("**Use Case 2:**")
                st.write("- **Problem:** Customer segmentation analysis required")
                st.write("- **Solution:** Build ML model for customer clustering")
                st.write("- **Leader:** " + selected_account['admin'])
                st.write("- **Status:** Completed")
                st.write("- **Platform:** Snowflake")
            
            # Add new use case form
            with st.expander("Add New Use Case"):
                new_problem = st.text_area("Problem Description", key=f"new_problem_{selected_account['bsnid']}")
                new_solution = st.text_area("Solution Description", key=f"new_solution_{selected_account['bsnid']}")
                new_leader = st.text_input("Use Case Leader", value=selected_account['admin'], key=f"new_leader_{selected_account['bsnid']}")
                new_status = st.selectbox("Status", statuses, key=f"new_status_{selected_account['bsnid']}")
                new_platform = st.selectbox("Platform", platforms, key=f"new_platform_{selected_account['bsnid']}")
                
                if st.button("Add Use Case", key=f"add_usecase_{selected_account['bsnid']}"):
                    if new_problem and new_solution:
                        st.success("Use case added successfully!")
                    else:
                        st.error("Please fill in both problem and solution descriptions.")
            
            # Recent updates section
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
                    'description': 'Started data warehouse configuration and initial data ingestion'
                },
                {
                    'date': '2024-07-02',
                    'author': selected_account['admin'],
                    'platform': 'Power Platform',
                    'description': 'Created initial dashboards and reports for stakeholder review'
                }
            ]
            
            for update in sample_updates:
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
        if search_term:
            st.info("No accounts found matching your search criteria.")
        else:
            st.warning("No accounts available.")
    
    # Footer
    st.markdown("---")
    st.markdown("**EDIP CRM System** - Professional Customer Relationship Management")

if __name__ == "__main__":
    main()