# EDIP CRM System

A comprehensive Customer Relationship Management (CRM) system built with Streamlit for managing business accounts, use cases, and IT partnerships.

## Features

- **Account Management**: Track teams, business areas, VPs, administrators, and IT partners
- **Use Case Tracking**: Manage use cases with problem descriptions, solutions, leaders, and status
- **Platform Integration**: Monitor onboarding status across Databricks, Snowflake, and Power Platform
- **Updates System**: Track project progress with author, date, platform, and description
- **Search & Filtering**: Advanced search capabilities across all account data
- **Professional UI**: Clean, enterprise-style interface with customizable themes

## Quick Start

1. Install dependencies:
   ```bash
   pip install streamlit pandas
   ```

2. Run the application:
   ```bash
   streamlit run app.py
   ```

3. Access the application at `http://localhost:8501`

## Project Structure

```
├── app.py                   # Main application entry point
├── pages/
│   ├── 1_Account_Details.py # Account detail view
│   ├── 2_Use_Cases.py       # Use case management
│   ├── 3_Admin.py           # Administrative functions
│   └── 4_Updates.py         # Updates management
├── utils/
│   └── data_manager.py      # Data management utilities
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── requirements.txt         # Python dependencies
```

## Configuration

The application uses Streamlit's configuration system. Server settings are configured in `.streamlit/config.toml`:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## Data Management

- **Storage**: In-memory storage using Streamlit's session state
- **Persistence**: Data persists during user sessions but is reset on restart
- **Sample Data**: Includes comprehensive sample accounts and use cases for demonstration

## Navigation

- **All Accounts**: Main dashboard with search and account overview
- **Account Details**: Detailed view with use cases, updates, and platform status
- **Use Cases**: Dedicated use case management with full CRUD operations
- **Updates**: Track project progress and updates across all accounts
- **Admin**: Administrative functions for account and data management

## Development

Built with:
- Python 3.11
- Streamlit 1.46.1+
- Pandas 2.3.0+
- UUID for unique identifiers
- Datetime for timestamp management

## Deployment

Configured for deployment on Replit with autoscale support. The application runs on port 5000 and is accessible via web browser.

## License

This project is developed for internal use and demonstration purposes.