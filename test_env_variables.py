import os
import streamlit as st

# Simple test script to check environment variables
st.title("Environment Variables Test")

# Check for Databricks environment variables
env_vars = {
    "DATABRICKS_SERVER_HOSTNAME": os.getenv("DATABRICKS_SERVER_HOSTNAME"),
    "DATABRICKS_HTTP_PATH": os.getenv("DATABRICKS_HTTP_PATH"), 
    "DATABRICKS_TOKEN": os.getenv("DATABRICKS_TOKEN")
}

st.write("## Current Environment Variables:")

for var_name, var_value in env_vars.items():
    if var_value:
        if "TOKEN" in var_name:
            st.success(f"✅ {var_name}: Found (hidden for security)")
        else:
            st.success(f"✅ {var_name}: {var_value}")
    else:
        st.error(f"❌ {var_name}: Not found")

# Show all environment variables (filtered)
st.write("## All Environment Variables (Databricks related):")
all_env = dict(os.environ)
databricks_env = {k: v for k, v in all_env.items() if 'DATABRICKS' in k.upper()}

if databricks_env:
    for key, value in databricks_env.items():
        if "TOKEN" in key.upper() or "PASSWORD" in key.upper():
            st.write(f"**{key}**: [Hidden for security]")
        else:
            st.write(f"**{key}**: {value}")
else:
    st.warning("No Databricks-related environment variables found")

# Instructions
st.write("## Set Environment Variables:")
st.code("""
# If using shell/terminal:
export DATABRICKS_SERVER_HOSTNAME="your-workspace.cloud.databricks.com"
export DATABRICKS_HTTP_PATH="/sql/1.0/warehouses/your-warehouse-id"
export DATABRICKS_TOKEN="your-access-token"

# Then run: streamlit run app_databricks_test.py
""")