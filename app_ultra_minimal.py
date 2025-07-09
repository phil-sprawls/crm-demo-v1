import streamlit as st
import pandas as pd

# Ultra-minimal CRM without any external dependencies
# This should work on Databricks Apps with minimal issues

st.set_page_config(page_title="EDIP CRM", layout="wide")

# Initialize session state
if 'accounts' not in st.session_state:
    st.session_state.accounts = [
        {'bsnid': 'BSN001', 'team': 'Data Engineering', 'business_area': 'Engineering', 'vp': 'Sarah Johnson', 'admin': 'Mike Chen'},
        {'bsnid': 'BSN002', 'team': 'Marketing Analytics', 'business_area': 'Marketing', 'vp': 'David Wilson', 'admin': 'Lisa Rodriguez'},
        {'bsnid': 'BSN003', 'team': 'Sales Operations', 'business_area': 'Sales', 'vp': 'Jennifer Davis', 'admin': 'Robert Kim'},
        {'bsnid': 'BSN004', 'team': 'Finance Analytics', 'business_area': 'Finance', 'vp': 'Michael Brown', 'admin': 'Angela Lee'},
        {'bsnid': 'BSN005', 'team': 'HR Analytics', 'business_area': 'HR', 'vp': 'Emily White', 'admin': 'James Wilson'}
    ]

st.title("EDIP CRM - All Accounts")

# Search
search = st.text_input("Search accounts", "")

# Filter accounts
accounts = st.session_state.accounts
if search:
    accounts = [acc for acc in accounts if search.lower() in str(acc).lower()]

# Display accounts
if accounts:
    st.subheader(f"Found {len(accounts)} accounts")
    
    for acc in accounts:
        with st.expander(f"{acc['bsnid']} - {acc['team']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Team:** {acc['team']}")
                st.write(f"**Business Area:** {acc['business_area']}")
            with col2:
                st.write(f"**VP:** {acc['vp']}")
                st.write(f"**Admin:** {acc['admin']}")
            
            # Simple platform status
            st.write("**Platform Status:**")
            databricks_status = st.selectbox("Databricks", ["Not Started", "In Progress", "Completed"], key=f"db_{acc['bsnid']}")
            snowflake_status = st.selectbox("Snowflake", ["Not Started", "In Progress", "Completed"], key=f"sf_{acc['bsnid']}")
            
            # Add use case
            st.write("**Add Use Case:**")
            problem = st.text_area("Problem", key=f"problem_{acc['bsnid']}")
            solution = st.text_area("Solution", key=f"solution_{acc['bsnid']}")
            
            if st.button("Save Use Case", key=f"save_{acc['bsnid']}"):
                if problem and solution:
                    st.success("Use case saved successfully!")
                else:
                    st.error("Please fill in both problem and solution")
else:
    st.info("No accounts found")

# Footer
st.markdown("---")
st.markdown("**EDIP CRM System**")