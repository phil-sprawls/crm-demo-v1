#!/usr/bin/env python3
"""
Debug script to test Databricks connection
Run this to verify your database credentials work
"""
import os
from dotenv import load_dotenv
from databricks import sql

# Load environment variables
load_dotenv()

def test_connection():
    print("=== Databricks Connection Test ===\n")
    
    # Check environment variables
    server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    http_path = os.getenv("DATABRICKS_HTTP_PATH") 
    access_token = os.getenv("DATABRICKS_TOKEN")
    catalog = os.getenv("DATABRICKS_CATALOG", "corporate_information_technology_raw_dev_000")
    schema = os.getenv("DATABRICKS_SCHEMA", "developer_psprawls")
    table_prefix = os.getenv("DATABRICKS_TABLE_PREFIX", "edip_crm")
    
    print("Environment Variables:")
    print(f"  DATABRICKS_SERVER_HOSTNAME: {server_hostname}")
    print(f"  DATABRICKS_HTTP_PATH: {http_path}")
    print(f"  DATABRICKS_TOKEN: {'Set' if access_token else 'Not set'}")
    print(f"  DATABRICKS_CATALOG: {catalog}")
    print(f"  DATABRICKS_SCHEMA: {schema}")
    print(f"  TABLE_PREFIX: {table_prefix}\n")
    
    # Check for missing credentials
    if not all([server_hostname, http_path, access_token]):
        print("❌ Missing required credentials in .env file")
        print("Please update your .env file with:")
        print("- DATABRICKS_SERVER_HOSTNAME")
        print("- DATABRICKS_HTTP_PATH") 
        print("- DATABRICKS_TOKEN")
        return False
        
    # Check for placeholder values
    if ("your-warehouse-id-here" in http_path or 
        "your-access-token-here" in access_token):
        print("❌ Found placeholder values in .env file")
        print("Please replace placeholder values with your actual credentials")
        return False
    
    # Test database connection
    print("Testing database connection...")
    try:
        conn = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        )
        print("✅ Database connection successful!")
        
        # Test table access
        print("\nTesting table access...")
        with conn.cursor() as cursor:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {catalog}.{schema}.{table_prefix}_accounts")
                result = cursor.fetchone()
                account_count = result[0] if result else 0
                print(f"✅ Found {account_count} accounts in {catalog}.{schema}.{table_prefix}_accounts")
                
                cursor.execute(f"SELECT COUNT(*) FROM {catalog}.{schema}.{table_prefix}_use_cases")
                result = cursor.fetchone()
                use_case_count = result[0] if result else 0
                print(f"✅ Found {use_case_count} use cases in {catalog}.{schema}.{table_prefix}_use_cases")
                
                cursor.execute(f"SELECT COUNT(*) FROM {catalog}.{schema}.{table_prefix}_updates")
                result = cursor.fetchone()
                update_count = result[0] if result else 0
                print(f"✅ Found {update_count} updates in {catalog}.{schema}.{table_prefix}_updates")
                
                print("\n🎉 All tables accessible! Your CRM should work correctly.")
                return True
                
            except Exception as e:
                print(f"❌ Table access failed: {str(e)}")
                print("This usually means:")
                print("- Tables don't exist in the specified catalog/schema")
                print("- Your token doesn't have permissions to access the tables")
                print("- Catalog/schema names are incorrect")
                return False
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        print("This usually means:")
        print("- Server hostname is incorrect")
        print("- HTTP path is incorrect") 
        print("- Access token is invalid or expired")
        print("- Network/firewall issues")
        return False

if __name__ == "__main__":
    test_connection()