import streamlit as st
import os
from databricks import sql
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

st.title("Databricks Connection Debug Tool")

# Show environment variables
st.header("1. Environment Variables Check")
server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
http_path = os.getenv("DATABRICKS_HTTP_PATH")
access_token = os.getenv("DATABRICKS_TOKEN")

st.write(f"**Server Hostname:** {server_hostname}")
st.write(f"**HTTP Path:** {http_path}")
st.write(f"**Access Token:** {'Set' if access_token else 'Not set'} ({'Length: ' + str(len(access_token)) if access_token else 'None'})")

if st.button("Test Connection Step by Step"):
    if not all([server_hostname, http_path, access_token]):
        st.error("Missing required environment variables")
        st.stop()
    
    try:
        st.info("Step 1: Creating connection object...")
        start_time = time.time()
        
        conn = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        )
        
        connection_time = time.time() - start_time
        st.success(f"✅ Connection object created in {connection_time:.2f} seconds")
        
        st.info("Step 2: Creating cursor...")
        start_time = time.time()
        
        cursor = conn.cursor()
        
        cursor_time = time.time() - start_time
        st.success(f"✅ Cursor created in {cursor_time:.2f} seconds")
        
        st.info("Step 3: Executing test query...")
        start_time = time.time()
        
        cursor.execute("SELECT 1 as test")
        
        query_time = time.time() - start_time
        st.success(f"✅ Query executed in {query_time:.2f} seconds")
        
        st.info("Step 4: Fetching result...")
        start_time = time.time()
        
        result = cursor.fetchone()
        
        fetch_time = time.time() - start_time
        st.success(f"✅ Result fetched in {fetch_time:.2f} seconds: {result}")
        
        cursor.close()
        conn.close()
        
        st.success("🎉 All connection steps completed successfully!")
        
    except Exception as e:
        st.error(f"❌ Connection failed at step: {str(e)}")
        st.info("Common issues:")
        st.info("- SQL warehouse not running")
        st.info("- Incorrect HTTP path")
        st.info("- Invalid access token")
        st.info("- Network connectivity issues")

# Additional diagnostic information
st.header("2. Diagnostic Information")

if st.button("Show Detailed Diagnostics"):
    st.write("**Environment Check:**")
    st.code(f"""
Server: {server_hostname}
Path: {http_path}
Token length: {len(access_token) if access_token else 0}
Token prefix: {access_token[:10] + '...' if access_token and len(access_token) > 10 else 'N/A'}
    """)
    
    # Test basic connectivity
    try:
        import socket
        hostname = server_hostname.replace('.cloud.databricks.com', '')
        st.info(f"Testing basic connectivity to {server_hostname}...")
        
        # This is a basic connectivity test
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((server_hostname, 443))
        sock.close()
        
        if result == 0:
            st.success("✅ Basic network connectivity OK")
        else:
            st.error("❌ Network connectivity issue")
            
    except Exception as e:
        st.warning(f"Network test failed: {str(e)}")

st.header("3. Common Solutions")
st.info("""
**If connection is stuck/spinning:**
1. Check if SQL warehouse is running in Databricks
2. Verify HTTP path format: /sql/1.0/warehouses/[warehouse-id]
3. Confirm access token is valid and has permissions
4. Try restarting the SQL warehouse
5. Check network connectivity to workspace

**HTTP Path Format:**
- Correct: /sql/1.0/warehouses/abc123def456
- Incorrect: sql/1.0/warehouses/abc123def456 (missing leading slash)
- Incorrect: /sql/warehouses/abc123def456 (missing version)
""")