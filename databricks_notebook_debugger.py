# Databricks Connection Debugger - Notebook Version
# Run this in a Databricks notebook or Jupyter notebook

import os
import socket
import requests
import time
from datetime import datetime

print("=" * 60)
print("DATABRICKS CONNECTION DEBUGGER")
print("=" * 60)
print(f"Timestamp: {datetime.now()}")
print()

# Step 1: Environment Variables
print("STEP 1: CHECKING ENVIRONMENT VARIABLES")
print("-" * 40)

# Check if running in Databricks
try:
    # Try to import databricks libraries
    from databricks import sql
    print("✅ databricks-sql-connector is available")
except ImportError:
    print("❌ databricks-sql-connector not installed")
    print("   Install with: pip install databricks-sql-connector")
    print()

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ python-dotenv loaded")
except ImportError:
    print("⚠️  python-dotenv not available - using system env vars only")

# Get credentials
server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
http_path = os.getenv("DATABRICKS_HTTP_PATH") 
access_token = os.getenv("DATABRICKS_TOKEN")

print(f"Server Hostname: {server_hostname if server_hostname else '❌ NOT SET'}")
print(f"HTTP Path: {http_path if http_path else '❌ NOT SET'}")
print(f"Access Token: {'✅ SET (' + str(len(access_token)) + ' chars)' if access_token else '❌ NOT SET'}")
print()

# Step 2: Hostname Format Validation
if server_hostname:
    print("STEP 2: HOSTNAME FORMAT VALIDATION")
    print("-" * 40)
    
    if server_hostname.startswith(('http://', 'https://')):
        print("❌ HOSTNAME ERROR: Remove 'http://' or 'https://' prefix")
        suggested = server_hostname.replace('https://', '').replace('http://', '')
        print(f"   Correct format: {suggested}")
        server_hostname = suggested  # Fix for testing
    else:
        print("✅ Hostname format looks correct")
    
    # Check common patterns
    if '.cloud.databricks.com' in server_hostname:
        print("✅ Uses standard cloud format")
    elif '.gcp.databricks.com' in server_hostname:
        print("✅ Uses GCP format") 
    elif '.azuredatabricks.net' in server_hostname:
        print("✅ Uses Azure format")
    else:
        print("⚠️  Unusual hostname format - verify it's correct")
    print()

# Step 3: DNS Resolution Test
if server_hostname:
    print("STEP 3: DNS RESOLUTION TEST")
    print("-" * 40)
    
    try:
        start_time = time.time()
        ip_address = socket.gethostbyname(server_hostname)
        dns_time = time.time() - start_time
        print(f"✅ DNS resolution successful: {ip_address}")
        print(f"   Resolution time: {dns_time:.3f} seconds")
    except socket.gaierror as e:
        print(f"❌ DNS resolution failed: {e}")
        print("   Common causes:")
        print("   - Incorrect workspace URL")
        print("   - Network/firewall restrictions")
        print("   - VPN required but not connected")
        print()
        
        # Provide examples
        print("   Valid hostname examples:")
        print("   - company.cloud.databricks.com")
        print("   - company.1.gcp.databricks.com")
        print("   - dbc-12345678-abcd.cloud.databricks.com")
        dns_success = False
    else:
        dns_success = True
    print()

# Step 4: HTTP Path Validation
if http_path:
    print("STEP 4: HTTP PATH VALIDATION")
    print("-" * 40)
    
    if http_path.startswith('/sql/1.0/warehouses/'):
        print("✅ HTTP path format is correct")
        warehouse_id = http_path.split('/')[-1]
        print(f"   Warehouse ID: {warehouse_id}")
    else:
        print("❌ HTTP path format incorrect")
        print("   Should start with: /sql/1.0/warehouses/")
        print("   Get correct path from: SQL Warehouses → Your Warehouse → Connection Details")
    print()

# Step 5: HTTPS Connectivity Test
if server_hostname and 'dns_success' in locals() and dns_success:
    print("STEP 5: HTTPS CONNECTIVITY TEST")
    print("-" * 40)
    
    try:
        start_time = time.time()
        response = requests.get(f"https://{server_hostname}", timeout=10, verify=True)
        https_time = time.time() - start_time
        print(f"✅ HTTPS connection successful")
        print(f"   Status code: {response.status_code}")
        print(f"   Response time: {https_time:.3f} seconds")
    except requests.exceptions.SSLError as e:
        print(f"⚠️  SSL certificate issue: {e}")
        print("   Server may still be reachable")
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
    except requests.exceptions.Timeout:
        print("❌ Connection timeout (>10 seconds)")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    print()

# Step 6: Databricks SQL Connection Test
if all([server_hostname, http_path, access_token]) and 'sql' in locals():
    print("STEP 6: DATABRICKS SQL CONNECTION TEST")
    print("-" * 40)
    
    try:
        print("Creating connection object...")
        start_time = time.time()
        
        conn = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token,
            _retry_delay_min=1,
            _retry_delay_max=10,
            _retry_stop_after_attempts_count=3
        )
        
        conn_time = time.time() - start_time
        print(f"✅ Connection object created ({conn_time:.3f}s)")
        
        print("Creating cursor...")
        start_time = time.time()
        cursor = conn.cursor()
        cursor_time = time.time() - start_time
        print(f"✅ Cursor created ({cursor_time:.3f}s)")
        
        print("Executing test query...")
        start_time = time.time()
        cursor.execute("SELECT 1 as test, current_timestamp() as ts")
        result = cursor.fetchone()
        query_time = time.time() - start_time
        print(f"✅ Query successful ({query_time:.3f}s)")
        print(f"   Result: {result}")
        
        # Test catalog access
        print("Testing catalog access...")
        try:
            cursor.execute("SHOW CATALOGS")
            catalogs = cursor.fetchall()
            print(f"✅ Can list catalogs ({len(catalogs)} found)")
            for cat in catalogs[:3]:  # Show first 3
                print(f"   - {cat[0]}")
            if len(catalogs) > 3:
                print(f"   ... and {len(catalogs) - 3} more")
        except Exception as e:
            print(f"⚠️  Catalog access limited: {e}")
        
        cursor.close()
        conn.close()
        print("✅ Connection test completed successfully")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print()
        print("Common solutions:")
        print("- Verify your personal access token is valid")
        print("- Check if SQL Warehouse is running")
        print("- Confirm you have permissions to the warehouse")
        print("- Try generating a new access token")
    print()

# Step 7: Summary and Recommendations
print("STEP 7: SUMMARY AND NEXT STEPS")
print("-" * 40)

if all([server_hostname, http_path, access_token]):
    print("✅ All credentials are set")
else:
    print("❌ Missing credentials - create .env file with:")
    print("""
DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
DATABRICKS_TOKEN=your-personal-access-token
""")

print()
print("If you're still having issues:")
print("1. Verify you can access Databricks in a web browser")
print("2. Check that your SQL Warehouse is running")
print("3. Generate a new personal access token")
print("4. Contact your Databricks admin about permissions")
print()

print("Test your workspace URL in browser:")
if server_hostname:
    print(f"https://{server_hostname}")
else:
    print("(Set DATABRICKS_SERVER_HOSTNAME first)")

print("=" * 60)
print("DEBUGGING COMPLETE")
print("=" * 60)