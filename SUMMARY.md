# Coremail SDK - Summary

## Project Structure
```
coremail-sdk/
├── coremail_sdk/           # Main package
│   ├── __init__.py         # Package init
│   ├── client.py           # Core API client
│   ├── api/                # High-level API wrapper
│   │   └── __init__.py
│   └── typings/            # Type definitions
│       └── __init__.py
├── tests/                  # Unit tests
│   ├── conftest.py
│   └── test_client.py
├── examples/               # Usage examples
│   └── example_usage.py
├── .env.example           # Environment variables example
├── pyproject.toml         # Project configuration
├── README.md              # Documentation
├── example.py             # Basic usage example
└── docs/                  # Documentation
    └── Coremail XT-v2.pdf
```

## Features Implemented

1. **Core API Client** (`coremail_sdk/client.py`)
   - Token management with automatic refresh
   - Authentication functionality
   - Get user attributes functionality
   - Proper error handling

2. **High-Level API Wrapper** (`coremail_sdk/api/`)
   - Simplified user operations
   - User existence checking
   - Authentication validation

3. **Type Safety** (`coremail_sdk/typings/`)
   - TypedDict definitions for API responses
   - Type hints throughout the codebase
   - MyPy compatibility

4. **Environment Configuration**
   - Uses python-dotenv for environment variables
   - Configurable base URL, app ID, and secret
   - Example .env file included

5. **Testing** (`tests/`)
   - Unit tests for all main functionality
   - Mocked API responses using responses library
   - pytest configuration

6. **Project Configuration**
   - uv package management
   - Proper pyproject.toml setup
   - Dependencies and dev dependencies
   - Type checking with mypy

## API Endpoints Supported

Based on the Coremail XT API examples provided:

1. **POST /requestToken** - Obtain authentication token
2. **POST /getAttrs** - Get user attributes
3. **POST /authenticate** - Authenticate user

## Usage

```python
from coremail_sdk import CoremailClient, CoremailAPI

# Initialize client
client = CoremailClient()

# Or with explicit parameters
client = CoremailClient(
    base_url="http://mail.ynu.edu.cn:9900/apiws/v3",
    app_id="api_user@ynu.edu.cn", 
    secret="your_secret"
)

# Use the API
token = client.request_token()
attrs = client.get_attributes("user@domain.com")
auth_result = client.authenticate("user@domain.com", "password")

# Or use the high-level API wrapper
api = CoremailAPI(client)
user_info = api.get_user_info("user@domain.com")
```

## Development

```bash
# Setup
uv sync

# Run tests
uv run pytest

# Type checking
uv run mypy coremail_sdk

# Format code
uv run black coremail_sdk tests
```

The SDK follows Python best practices, includes comprehensive type annotations, and provides both low-level client access and high-level API wrappers for convenient usage.