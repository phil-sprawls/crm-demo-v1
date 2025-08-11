import streamlit as st
import os
from dotenv import load_dotenv
import socket
import requests

# Load environment variables
load_dotenv()

st.title("Databricks Connection Troubleshooter")
st.write("This tool helps diagnose connection issues with your Databricks workspace.")

# Get credentials
server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
http_path = os.getenv("DATABRICKS_HTTP_PATH")
access_token = os.getenv("DATABRICKS_TOKEN")

st.header("1. Environment Variables Check")
st.write("**Server Hostname:**", server_hostname if server_hostname else "❌ Missing")
st.write("**HTTP Path:**", http_path if http_path else "❌ Missing")
st.write("**Access Token:**", "✅ Found" if access_token else "❌ Missing")

if server_hostname:
    st.header("2. Hostname Format Check")
    
    # Check if hostname has protocol
    if server_hostname.startswith(('http://', 'https://')):
        st.error("❌ Remove 'http://' or 'https://' from hostname")
        suggested = server_hostname.replace('https://', '').replace('http://', '')
        st.info(f"Use: {suggested}")
    else:
        st.success("✅ Hostname format looks correct")
    
    st.header("3. DNS Resolution Test")
    try:
        ip = socket.gethostbyname(server_hostname)
        st.success(f"✅ DNS resolves to: {ip}")
        
        # Test HTTPS connection
        st.header("4. HTTPS Connection Test")
        try:
            response = requests.get(f"https://{server_hostname}", timeout=10, allow_redirects=False)
            st.success(f"✅ HTTPS connection successful (Status: {response.status_code})")
        except requests.exceptions.SSLError:
            st.warning("⚠️ SSL certificate issue, but server is reachable")
        except requests.exceptions.ConnectionError as e:
            st.error(f"❌ Connection failed: {e}")
        except requests.exceptions.Timeout:
            st.error("❌ Connection timeout")
            
    except socket.gaierror:
        st.error("❌ DNS resolution failed")
        st.write("**Common causes:**")
        st.write("- Incorrect workspace URL")
        st.write("- Network/firewall restrictions")
        st.write("- Workspace not accessible from this location")
        
        st.header("Workspace URL Examples")
        st.info("""
        **Correct formats:**
        - yourcompany.cloud.databricks.com
        - yourcompany.1.gcp.databricks.com  
        - dbc-12345678-abcd.cloud.databricks.com
        
        **Wrong formats:**
        - https://yourcompany.cloud.databricks.com (remove https://)
        - yourcompany.databricks.com (missing .cloud)
        """)

if http_path:
    st.header("5. HTTP Path Format Check")
    if http_path.startswith('/sql/1.0/warehouses/'):
        st.success("✅ HTTP path format looks correct")
    else:
        st.error("❌ HTTP path should start with '/sql/1.0/warehouses/'")
        st.info("Get correct path from: Databricks → SQL Warehouses → Your Warehouse → Connection Details")

st.header("6. Quick Fix Suggestions")
st.write("**Most common issues:**")
st.write("1. **Wrong hostname format** - Remove https:// prefix")
st.write("2. **Incorrect workspace URL** - Double-check your Databricks workspace URL")
st.write("3. **Network restrictions** - Check if you can access Databricks in your browser")
st.write("4. **Wrong HTTP path** - Get the exact path from SQL Warehouse connection details")

st.header("7. Test Your Credentials")
st.write("Can you access your Databricks workspace in a web browser?")
if server_hostname:
    st.markdown(f"[Test in browser: https://{server_hostname}](https://{server_hostname})")