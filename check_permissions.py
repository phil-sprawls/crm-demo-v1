import streamlit as st
import os
from databricks import sql
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

st.title("Databricks Permissions Checker")
st.markdown("This tool checks your specific permissions for Unity Catalog and SQL warehouses.")

# Environment variables check
st.header("1. Environment Variables")
server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
http_path = os.getenv("DATABRICKS_HTTP_PATH")
access_token = os.getenv("DATABRICKS_TOKEN")

st.write(f"**Server:** {server_hostname}")
st.write(f"**HTTP Path:** {http_path}")
st.write(f"**Token:** {'Set (' + str(len(access_token)) + ' chars)' if access_token else 'Not set'}")

if not all([server_hostname, http_path, access_token]):
    st.error("Missing environment variables. Please configure your .env file first.")
    st.stop()

# Permission checks
if st.button("Check All Permissions"):
    try:
        st.info("Connecting to Databricks...")
        
        # Basic connection test
        conn = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        )
        
        st.success("✅ Basic connection successful")
        
        with conn.cursor() as cursor:
            st.header("2. Basic Identity & Access")
            
            # Check current user
            try:
                cursor.execute("SELECT current_user() as user")
                user = cursor.fetchone()[0]
                st.success(f"✅ Connected as: **{user}**")
            except Exception as e:
                st.error(f"❌ Cannot get current user: {str(e)}")
            
            # Check current database/catalog
            try:
                cursor.execute("SELECT current_catalog() as catalog, current_schema() as schema")
                result = cursor.fetchone()
                st.info(f"Current catalog: **{result[0]}**")
                st.info(f"Current schema: **{result[1]}**")
            except Exception as e:
                st.warning(f"Cannot get current catalog/schema: {str(e)}")
            
            st.header("3. Catalog Access")
            
            # List catalogs
            try:
                cursor.execute("SHOW CATALOGS")
                catalogs = cursor.fetchall()
                st.success(f"✅ Can list catalogs: {len(catalogs)} found")
                
                catalog_names = [row[0] for row in catalogs]
                if 'corporate_information_technology_raw_dev_000' in catalog_names:
                    st.success("✅ **Target catalog found:** corporate_information_technology_raw_dev_000")
                else:
                    st.error("❌ Target catalog 'corporate_information_technology_raw_dev_000' not accessible")
                    st.write("Available catalogs:", catalog_names)
                    
            except Exception as e:
                st.error(f"❌ Cannot list catalogs: {str(e)}")
            
            st.header("4. Schema Access")
            
            # Check target catalog and schema
            try:
                # Get database configuration from environment
                catalog_name = os.getenv("DATABRICKS_CATALOG", "corporate_information_technology_raw_dev_000")
                schema_name = os.getenv("DATABRICKS_SCHEMA", "developer_psprawls")
                
                cursor.execute(f"USE CATALOG {catalog_name}")
                st.success(f"✅ Can USE target catalog: {catalog_name}")
                
                cursor.execute("SHOW SCHEMAS")
                schemas = cursor.fetchall()
                schema_names = [row[0] for row in schemas]
                
                if schema_name in schema_names:
                    st.success(f"✅ **Target schema found:** {schema_name}")
                else:
                    st.error(f"❌ Target schema '{schema_name}' not accessible")
                    st.write("Available schemas:", schema_names)
                    
            except Exception as e:
                st.error(f"❌ Cannot access target catalog: {str(e)}")
            
            st.header("5. Table Creation Permissions")
            
            # Test table creation in target schema
            try:
                cursor.execute(f"USE SCHEMA {catalog_name}.{schema_name}")
                st.success("✅ Can USE target schema")
                
                # Try to create a test table
                test_table_name = "edip_crm_permission_test"
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {test_table_name} (
                        test_id STRING,
                        test_timestamp TIMESTAMP
                    ) USING DELTA
                """)
                st.success("✅ **Can CREATE tables** in target schema")
                
                # Test insert permission
                cursor.execute(f"""
                    INSERT INTO {test_table_name} 
                    VALUES ('test123', current_timestamp())
                """)
                st.success("✅ **Can INSERT data** into tables")
                
                # Test select permission
                cursor.execute(f"SELECT COUNT(*) FROM {test_table_name}")
                count = cursor.fetchone()[0]
                st.success(f"✅ **Can SELECT data** from tables (found {count} records)")
                
                # Clean up test table
                cursor.execute(f"DROP TABLE IF EXISTS {test_table_name}")
                st.success("✅ **Can DROP tables** (cleanup successful)")
                
            except Exception as e:
                st.error(f"❌ Table operations failed: {str(e)}")
                
                # Try to determine specific permission issue
                if "PERMISSION_DENIED" in str(e):
                    st.error("**Permission Issue:** You don't have CREATE TABLE permission in this schema")
                elif "ACCESS_DENIED" in str(e):
                    st.error("**Access Issue:** Schema access denied")
                elif "SCHEMA_NOT_FOUND" in str(e):
                    st.error("**Schema Issue:** Schema doesn't exist or not accessible")
            
            st.header("6. Existing Tables Check")
            
            # Check if CRM tables already exist
            try:
                cursor.execute(f"SHOW TABLES IN {catalog_name}.{schema_name}")
                tables = cursor.fetchall()
                table_names = [row[1] for row in tables]  # Table name is in second column
                
                crm_tables = [name for name in table_names if name.startswith('edip_crm_')]
                
                if crm_tables:
                    st.info(f"**Existing CRM tables found:** {crm_tables}")
                    
                    # Test access to existing tables
                    for table in crm_tables:
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM {catalog_name}.{schema_name}.{table}")
                            count = cursor.fetchone()[0]
                            st.success(f"✅ Can access {table}: {count} records")
                        except Exception as e:
                            st.error(f"❌ Cannot access {table}: {str(e)}")
                else:
                    st.info("No existing CRM tables found - ready for fresh setup")
                    
            except Exception as e:
                st.warning(f"Cannot list tables: {str(e)}")
            
            st.header("7. Required Permissions Summary")
            
            st.markdown("""
            **For EDIP CRM database integration, you need:**
            
            ✅ **CONNECT** - Connect to SQL warehouse  
            ✅ **USE CATALOG** - Access corporate_information_technology_raw_dev_000  
            ✅ **USE SCHEMA** - Access developer_psprawls schema  
            ✅ **CREATE TABLE** - Create new tables in schema  
            ✅ **INSERT** - Add data to tables  
            ✅ **SELECT** - Read data from tables  
            ✅ **UPDATE** - Modify existing data (for CRM updates)  
            ✅ **DELETE** - Remove data if needed  
            
            **Optional but helpful:**  
            ⚠️ **DROP TABLE** - Remove tables for cleanup  
            ⚠️ **ALTER TABLE** - Modify table structure  
            """)
        
        conn.close()
        
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")
        
        # Provide specific guidance based on error type
        if "Invalid access token" in str(e):
            st.error("**Issue:** Access token is invalid or expired")
            st.info("**Solution:** Generate a new personal access token in Databricks")
        elif "HTTP 403" in str(e):
            st.error("**Issue:** Access forbidden - insufficient permissions")
            st.info("**Solution:** Contact your Databricks admin to grant SQL warehouse access")
        elif "HTTP 404" in str(e):
            st.error("**Issue:** SQL warehouse not found")
            st.info("**Solution:** Check your HTTP path - warehouse may be stopped or path incorrect")
        elif "timeout" in str(e).lower():
            st.error("**Issue:** Connection timeout")
            st.info("**Solution:** Check if SQL warehouse is running and network connectivity")

# Permission request template
st.header("8. Request Permissions Template")

if st.button("Generate Permission Request"):
    st.markdown("""
    ### Email Template for Databricks Admin
    
    **Subject:** Databricks Unity Catalog Permissions Request - EDIP CRM Project
    
    **Dear [Admin Name],**
    
    I'm working on the EDIP CRM database integration project and need the following permissions:
    
    **User:** [Your email/username]  
    **Catalog:** corporate_information_technology_raw_dev_000  
    **Schema:** developer_psprawls  
    
    **Required Permissions:**
    - USE CATALOG on corporate_information_technology_raw_dev_000
    - USE SCHEMA on developer_psprawls  
    - CREATE TABLE in developer_psprawls schema
    - SELECT, INSERT, UPDATE permissions on tables with prefix 'edip_crm_'
    - Access to SQL warehouse for database connections
    
    **Purpose:** Creating and managing CRM tables for business account tracking
    
    **Tables to be created:**
    - edip_crm_accounts
    - edip_crm_platforms_status  
    - edip_crm_use_cases
    - edip_crm_updates
    
    Please let me know if you need any additional information.
    
    Thank you,  
    [Your name]
    """)