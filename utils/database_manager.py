import streamlit as st
import uuid
from datetime import datetime, date
from databricks import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database configuration from environment
CATALOG_NAME = os.getenv("DATABRICKS_CATALOG", "corporate_information_technology_raw_dev_000")
SCHEMA_NAME = os.getenv("DATABRICKS_SCHEMA", "developer_psprawls")
TABLE_PREFIX = os.getenv("DATABRICKS_TABLE_PREFIX", "edip_crm")

# Database connection
@st.cache_resource
def get_databricks_connection():
    """Get cached Databricks SQL connection"""
    try:
        server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        http_path = os.getenv("DATABRICKS_HTTP_PATH")
        access_token = os.getenv("DATABRICKS_TOKEN")
        
        if not all([server_hostname, http_path, access_token]):
            return None
            
        return sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        )
    except Exception:
        return None

def get_account_by_bsnid(bsnid):
    """Get account details by BSNID"""
    conn = get_databricks_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT bsnid, team, business_area, vp, admin, primary_it_partner,
                       azure_devops_links, artifacts_folder_links
                FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts
                WHERE bsnid = '{bsnid}'
            """)
            result = cursor.fetchone()
            
            if result:
                return {
                    'bsnid': result[0],
                    'team': result[1],
                    'business_area': result[2],
                    'vp': result[3],
                    'admin': result[4],
                    'primary_it_partner': result[5],
                    'azure_devops_links': result[6].split(',') if result[6] else [],
                    'artifacts_folder_links': result[7].split(',') if result[7] else []
                }
            return None
    except Exception:
        return None

def get_account_use_cases(bsnid):
    """Get use cases for an account"""
    conn = get_databricks_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT use_case_id, platform, problem, solution, author, created_at
                FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_use_cases
                WHERE account_bsnid = '{bsnid}'
                ORDER BY created_at DESC
            """)
            results = cursor.fetchall()
            
            use_cases = []
            for row in results:
                use_cases.append({
                    'use_case_id': row[0],
                    'platform': row[1],
                    'problem': row[2],
                    'solution': row[3],
                    'author': row[4],
                    'created_at': row[5]
                })
            return use_cases
    except Exception:
        return []

def get_account_updates(bsnid):
    """Get updates for an account"""
    conn = get_databricks_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT update_id, author, platform, description, update_date, created_at
                FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_updates
                WHERE account_bsnid = '{bsnid}'
                ORDER BY update_date DESC, created_at DESC
            """)
            results = cursor.fetchall()
            
            updates = []
            for row in results:
                updates.append({
                    'update_id': row[0],
                    'author': row[1],
                    'platform': row[2],
                    'description': row[3],
                    'update_date': row[4],
                    'created_at': row[5]
                })
            return updates
    except Exception:
        return []

def get_platform_status(bsnid):
    """Get platform status for an account"""
    conn = get_databricks_connection()
    if not conn:
        return {}
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT platform, status, enablement_tier
                FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_platforms_status
                WHERE account_bsnid = '{bsnid}'
            """)
            results = cursor.fetchall()
            
            platforms = {}
            for row in results:
                platforms[row[0]] = {
                    'status': row[1],
                    'enablement_tier': row[2]
                }
            return platforms
    except Exception:
        return {}

def add_use_case(account_bsnid, platform, problem, solution, author):
    """Add a new use case"""
    conn = get_databricks_connection()
    if not conn:
        return False
    
    try:
        use_case_id = str(uuid.uuid4())
        with conn.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_use_cases
                (use_case_id, account_bsnid, platform, problem, solution, author, created_at, updated_at)
                VALUES ('{use_case_id}', '{account_bsnid}', '{platform}', '{problem}', '{solution}', 
                        '{author}', current_timestamp(), current_timestamp())
            """)
        return True
    except Exception:
        return False

def add_update(account_bsnid, author, platform, description, update_date):
    """Add a new update"""
    conn = get_databricks_connection()
    if not conn:
        return False
    
    try:
        update_id = str(uuid.uuid4())
        with conn.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_updates
                (update_id, account_bsnid, author, platform, description, update_date, created_at)
                VALUES ('{update_id}', '{account_bsnid}', '{author}', '{platform}', '{description}', 
                        '{update_date}', current_timestamp())
            """)
        return True
    except Exception:
        return False

def get_all_accounts():
    """Get all accounts"""
    conn = get_databricks_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT bsnid, team, business_area, vp, admin, primary_it_partner
                FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts
                ORDER BY team
            """)
            results = cursor.fetchall()
            
            accounts = []
            for row in results:
                accounts.append({
                    'bsnid': row[0],
                    'team': row[1],
                    'business_area': row[2],
                    'vp': row[3],
                    'admin': row[4],
                    'primary_it_partner': row[5]
                })
            return accounts
    except Exception:
        return []

def get_all_use_cases():
    """Get all use cases"""
    conn = get_databricks_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT u.use_case_id, u.account_bsnid, a.team, u.platform, u.problem, u.solution, 
                       u.author, u.created_at
                FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_use_cases u
                JOIN {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts a ON u.account_bsnid = a.bsnid
                ORDER BY u.created_at DESC
            """)
            results = cursor.fetchall()
            
            use_cases = []
            for row in results:
                use_cases.append({
                    'use_case_id': row[0],
                    'account_bsnid': row[1],
                    'team': row[2],
                    'platform': row[3],
                    'problem': row[4],
                    'solution': row[5],
                    'author': row[6],
                    'created_at': row[7]
                })
            return use_cases
    except Exception:
        return []

def get_all_updates():
    """Get all updates"""
    conn = get_databricks_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT u.update_id, u.account_bsnid, a.team, u.author, u.platform, u.description, 
                       u.update_date, u.created_at
                FROM {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_updates u
                JOIN {CATALOG_NAME}.{SCHEMA_NAME}.{TABLE_PREFIX}_accounts a ON u.account_bsnid = a.bsnid
                ORDER BY u.update_date DESC, u.created_at DESC
            """)
            results = cursor.fetchall()
            
            updates = []
            for row in results:
                updates.append({
                    'update_id': row[0],
                    'account_bsnid': row[1],
                    'team': row[2],
                    'author': row[3],
                    'platform': row[4],
                    'description': row[5],
                    'update_date': row[6],
                    'created_at': row[7]
                })
            return updates
    except Exception:
        return []