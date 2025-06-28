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
├── app.py                    # Main application entry point
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

## User Preferences

Preferred communication style: Simple, everyday language.
User feedback preferences: Show clear confirmation messages when saving any new data across all forms and actions.
Design preferences: Professional enterprise style without emojis, EDIP CRM branding, light color theme with Streamlit default styling.