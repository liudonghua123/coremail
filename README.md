# Coremail SDK for Python

A comprehensive Python SDK for interacting with Coremail XT API v3, providing easy access to all available API endpoints for user, organization, and system management.

## Features

- Full implementation of Coremail XT API v3 endpoints
- Easy configuration via environment variables or explicit parameters
- Automatic token management and caching
- Comprehensive type hints and documentation
- Support for all major API operations (user management, organization management, session management, etc.)

## Installation

```bash
pip install coremail
```

## Configuration

Create a `.env` file in your project root with the following variables:

```env
COREMAIL_BASE_URL=http://your-coremail-server:9900/apiws/v3
COREMAIL_APP_ID=your_app_id@your_domain.com
COREMAIL_SECRET=your_secret_key
```

## Usage

### Basic Usage

```python
from coremail import CoremailClient

# Initialize the client with environment variables
client = CoremailClient()

# Or with explicit parameters
client = CoremailClient(
    base_url="http://your-host-of-coremail:9900/apiws/v3",
    app_id="your_app_id@your-domain.com",
    secret="your_secret_key"
)

# Example: Request a token
token = client.requestToken()
print(f"Token: {token}")

# Example: Get user attributes
user_attrs = client.getAttrs("test_user@your-domain.com")
print(f"User attributes: {user_attrs}")
```

### User Management

```python
# Create a new user
attrs = {
    "display_name": "John Doe",
    "cos_id": 1,
    "quota": 1024
}
client.createUser("john.doe@your-domain.com", "password123", attrs)

# Get user attributes
user_attrs = client.getAttrs("john.doe@your-domain.com")

# Update user attributes
update_attrs = {"display_name": "Jane Doe", "quota": 2048}
client.setAttrs("john.doe@your-domain.com", update_attrs)

# Delete a user
client.delUser("john.doe@your-domain.com")
```

### Organization Management

```python
# Create an organization
org_attrs = {
    "org_name": "Example Organization",
    "domain_name": "example.com",
    "cos_id": [1],
    "num_of_classes": [100],
    "org_status": 0,
    "org_expiry_date": "2025-12-31"
}
client.addOrg("example_org", org_attrs)

# Get organization information
org_info = client.getOrgInfo("example_org")

# Update organization
update_attrs = {"org_name": "Updated Organization Name"}
client.alterOrg("example_org", update_attrs)
```

### Session Management

```python
# User login to get session ID
session_id = client.userLogin("user@domain.com")
print(f"Session ID: {session_id}")

# Check user session
user_info = client.sesTimeOut(session_id)
print(f"User info: {user_info}")

# Logout user
client.userLogout(session_id)
```

## Available Methods

The SDK includes methods for all Coremail XT API v3 endpoints:

### Access Token
- `requestToken()` - Request a new access token

### Login
- `userLogin(user_at_domain)` - User login to get session ID
- `userLoginEx(user_at_domain, attrs)` - User login with additional parameters
- `userExist(user_at_domain)` - Check if user exists
- `userExist2(user_at_domain)` - Check if a user without alias name exists (returns boolean)
- `authenticate(user_at_domain, password)` - Verify user password
- `sesTimeOut(ses_id)` - Check user's session and return user information
- `sesRefresh(ses_id)` - Refresh user's session
- `getSessionVar(ses_id, ses_key)` - Get variable from user's session
- `userLogout(ses_id)` - Logout user session
- `setSessionVar(ses_id, ses_key, ses_var)` - Set variable in user's session

### Organization Management
- `addOrg(org_id, attrs)` - Create organization
- `getOrgInfo(org_id, attrs)` - Get organization info
- `alterOrg(org_id, attrs)` - Modify organization
- `addOrgDomain(org_id, domain_name)` - Add domain to organization
- `delOrgDomain(org_id, domain_name)` - Delete domain from organization
- `addOrgCos(org_id, num_of_classes, cos_name, cos_id)` - Add service level
- `alterOrgCos(org_id, num_of_classes, cos_name, cos_id)` - Update service level
- `delOrgCos(org_id, cos_id)` - Delete service level
- `getOrgCosUser(org_id, cos_id)` - Get users in service level
- `getOrgList()` - Get list of organizations
- `addUnit(org_id, unit_name, attrs)` - Add organizational unit
- `delUnit(org_id, unit_name)` - Delete organizational unit
- `getUnitAttrs(org_id, unit_name, attrs)` - Get organizational unit attributes
- `setUnitAttrs(org_id, unit_name, attrs)` - Set organizational unit attributes

### User Management
- `createUser(user_at_domain, password, attrs)` - Create user
- `deleteUser(user_at_domain)` - Delete user
- `getAttrs(user_at_domain, attrs)` - Get user attributes
- `changeAttrs(user_at_domain, attrs)` - Change user attributes
- `addSmtpAlias(user_at_domain, alias)` - Add SMTP alias for user
- `delSmtpAlias(user_at_domain, alias)` - Delete SMTP alias for user
- `getSmtpAlias(user_at_domain)` - Get SMTP aliases for user
- `setAdminType(user_at_domain, admin_type)` - Set admin type for user
- `getAdminType(user_at_domain)` - Get admin type for user
- `renameUser(old_user_at_domain, new_user_at_domain)` - Rename user
- `moveUser(user_at_domain, target_org_id, target_unit_name)` - Move user to different organization/unit

### Object Management
- `createObj(obj_type, obj_name, org_id, attrs)` - Create object (e.g., mailing list)
- `getObjAttrs(obj_type, obj_name, org_id, attrs)` - Get object attributes
- `setObjAttrs(obj_type, obj_name, org_id, attrs)` - Set object attributes
- `deleteObj(obj_type, obj_name, org_id)` - Delete object

### Domain Management
- `domainExist(domain_name)` - Check if domain exists
- `getDomainList(start, limit)` - Get domain list
- `addDomain25(domain_name, attrs)` - Add domain for port 25 (SMTP)
- `delDomain25(domain_name)` - Delete domain for port 25 (SMTP)
- `addDomainAlias(domain_name, alias_domain_name)` - Add domain alias
- `getDomainAlias(domain_name)` - Get domain aliases
- `delDomainAlias(domain_name, alias_domain_name)` - Delete domain alias
- `getOrgListByDomain(domain_name)` - Get organization list by domain

### Mail Information
- `listMailInfos(user_at_domain, start_time, end_time, attrs)` - List mail information
- `getNewMailInfos(user_at_domain, start_time, end_time, attrs)` - Get new mail information

### Transport
- `smtpTransport(sender, recipient, content)` - SMTP transport for message delivery

### User Lookup
- `getUserFromCasName(cas_name)` - Get user email address from CAS name

## Error Handling

The SDK raises exceptions for API errors:

```python
try:
    user_attrs = client.getAttrs("nonexistent_user@domain.com")
except Exception as e:
    print(f"API Error: {e}")
```

## Development

To run the example:

```bash
python example.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.