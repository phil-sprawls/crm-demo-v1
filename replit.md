# CRM System

## Overview

This is a Streamlit-based Customer Relationship Management (CRM) system designed to manage business accounts, use cases, and platform integrations. The application provides a web interface for tracking teams, business areas, VPs, administrators, and IT partners across different organizational units.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework
- **Language**: Python 3.11
- **UI Components**: Multi-page Streamlit application with navigation tabs and forms
- **Layout**: Wide layout configuration with responsive columns
- **Navigation**: Page-based navigation using Streamlit's native page switching

### Backend Architecture
- **Data Storage**: In-memory storage using Streamlit's session state
- **Data Management**: Centralized data manager utility (`utils/data_manager.py`)
- **State Management**: Session-based state persistence during user sessions
- **UUID Generation**: Automatic unique identifier generation for accounts and use cases

### Application Structure
```
├── app.py                   # Main application entry point (All Accounts view)
├── pages/
│   ├── 1_Account_Details.py  # Account detail view
│   ├── 2_Use_Cases.py       # Use case management
│   └── 3_Admin.py           # Administrative functions
├── utils/
│   └── data_manager.py      # Data management utilities
└── .streamlit/
    └── config.toml          # Streamlit configuration
```

## Key Components

### Main Dashboard (`app.py`)
- Account search and filtering functionality
- Displays all accounts in a tabular format
- Search by team, business area, VP, admin, or IT partner
- Account selection for detailed views

### Account Details Page
- Detailed view of individual account information
- Basic information display (BSNID, team, business area, VP, admin, IT partner)
- External links management section
- Platform status tracking

### Use Cases Management
- Create and edit use cases linked to accounts
- Form-based interface for use case data entry
- Account-specific use case associations

### Admin Panel
- Multi-tab interface for administrative functions
- IT Partner management by business area
- Account creation and management
- Use case and platform administration

### Data Manager
- Centralized data initialization and management
- Session state management for accounts, use cases, and business areas
- CRUD operations for all data entities
- UUID-based unique identification system

## Data Flow

1. **Initialization**: Application starts by initializing default data structures in session state
2. **Search & Filter**: Users can search accounts using text-based filtering
3. **Account Selection**: Users select accounts from the main dashboard to view details
4. **Data Persistence**: All changes are stored in Streamlit's session state during the session
5. **Navigation**: Users navigate between pages using Streamlit's page switching mechanism

### Data Structures
- **Accounts**: Dictionary with BSNID as key, containing team, business area, VP, admin, IT partner info
- **Use Cases**: Dictionary linking use cases to specific accounts
- **Business Areas**: Mapping of business areas to their primary IT partners
- **Platforms**: List of available platforms (Databricks, Snowflake, Power Platform)
- **Statuses**: Predefined status options for onboarding and enablement tiers

## External Dependencies

### Core Dependencies
- **Streamlit (>=1.46.1)**: Web application framework and UI components
- **Pandas (>=2.3.0)**: Data manipulation and tabular data handling
- **UUID**: Built-in Python library for unique identifier generation
- **Datetime**: Built-in Python library for timestamp management

### System Dependencies
- **Python 3.11**: Runtime environment
- **Nix**: Package management and environment setup
- **glibcLocales**: Locale support for internationalization

## Deployment Strategy

### Environment Setup
- **Platform**: Replit with Nix-based environment management
- **Python Version**: 3.11 with stable-24_05 channel
- **Package Management**: UV lock file for dependency resolution

### Deployment Configuration
- **Target**: Autoscale deployment on Replit
- **Port**: 5000 (configured in both .replit and Streamlit config)
- **Server**: Streamlit development server
- **Address**: Bound to 0.0.0.0 for external access

### Workflow Configuration
- **Run Command**: `streamlit run app.py --server.port 5000`
- **Mode**: Parallel execution with port waiting
- **Button**: Project-level run button configuration

### Limitations
- **Data Persistence**: No permanent data storage - data is lost when session ends
- **Multi-user**: No concurrent user support - single session application
- **Authentication**: No user authentication or authorization system
- **Database**: No external database integration

## Changelog

- June 27, 2025. Initial setup
- June 27, 2025. Fixed duplicate account display issue and added comprehensive confirmation messages for all user actions
- June 27, 2025. Implemented enterprise design changes: Updated branding from "CRM System" to "EDIP CRM", removed all emojis for professional appearance, added custom color theme (light background with red primary), and improved navigation consistency
- June 28, 2025. Renamed main application file from "app.py" to "0_All_Accounts.py" for clearer sidebar navigation display
- June 28, 2025. Added platform parameter to Use Cases and implemented Updates functionality with Author, Date, Platform, and Description fields
- June 30, 2025. Enhanced Account Details page to display Platform field in Use Cases and added complete Updates section showing recent updates with full metadata
- June 30, 2025. Created comprehensive sample updates for all demo accounts with realistic project progress tracking across different platforms and timeframes
- June 30, 2025. Added CSS styling for table alignment in All Accounts page
- July 1, 2025. Fixed deployment configuration by creating app.py compatibility file to match deployment settings while preserving 0_All_Accounts.py as main entry point
- July 1, 2025. Fixed all broken navigation links throughout the application: updated Account Details and Admin pages to reference correct main file (0_All_Accounts.py instead of app.py), fixed layout issue with duplicate column usage in Account Details quick actions
- July 1, 2025. Implemented deployment-compatible navigation system with fallback mechanisms: added try-catch navigation logic to handle differences between preview and deployed environments, created full app.py implementation with navigation fallback handling, ensured consistent functionality across both development and production deployments
- July 1, 2025. Replaced complex navigation fallbacks with JavaScript redirect approach: implemented window.location.href redirect to root URL for all "Back to All Accounts" buttons, providing reliable navigation that works consistently in both preview and deployed environments
- July 1, 2025. Reverted to consistent app.py navigation approach: simplified all "Back to All Accounts" buttons to use st.switch_page("app.py") since deployment configuration uses app.py as main entry point, ensuring consistent navigation behavior across preview and deployed environments
- July 1, 2025. Fully reverted to app.py as main application file: renamed 0_All_Accounts.py to backup_all_accounts.py, recreated app.py as the primary main file, updated workflow configuration to run app.py, ensuring complete consistency between preview and deployment environments
- July 9, 2025. Created production-ready Databricks Apps deployment package: identified missing app.yaml as root cause of deployment failures, created app_production.py following databricks-apps-cookbook patterns, updated dependencies to match working examples, configured proper theme and structure for reliable Databricks Apps deployment
- July 9, 2025. Implemented Unity Catalog database integration: created app_databricks.py with full database backend using databricks-sql-connector, designed comprehensive table schema for accounts/use_cases/updates/platforms_status, included automatic table creation and sample data initialization, provided multiple authentication methods and enterprise-grade features like ACID transactions and audit trails
- July 9, 2025. Created database test deployment package: renamed files to app_database.py, requirements_database.txt, app_database.yaml, and .streamlit_database/config.toml for direct use with environment variables, added .env file configuration for user's workspace and schema (corporate_information_technology_raw_dev_000.developer_psprawls), included python-dotenv for environment variable loading
- July 10, 2025. Enhanced database connection troubleshooting: created comprehensive permission checker (check_permissions.py) and connection debugger (debug_connection.py) to systematically identify Unity Catalog access issues, added detailed permissions guide with admin request templates, removed workspace references from code for privacy protection
- July 10, 2025. Implemented environment variable configuration system: removed all hardcoded workspace names and database references from code, added DATABRICKS_CATALOG, DATABRICKS_SCHEMA, and DATABRICKS_TABLE_PREFIX environment variables to .env.template, updated all SQL queries to use configurable parameters while maintaining secure defaults

## User Preferences

Preferred communication style: Simple, everyday language.
User feedback preferences: Show clear confirmation messages when saving any new data across all forms and actions.
Design preferences: Professional enterprise style without emojis, EDIP CRM branding, light color theme with Streamlit default styling.