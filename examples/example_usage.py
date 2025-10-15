"""
Example usage of the Coremail SDK
"""
from coremail import CoremailClient, CoremailAPI


def example_usage():
    """
    Example of how to use the Coremail SDK
    """
    # Initialize the client with environment variables or explicit parameters
    client = CoremailClient()
    
    # Alternatively, with explicit parameters:
    # client = CoremailClient(
    #     base_url="http://your-host-of-coremail:9900/apiws/v3",
    #     app_id="api_user@your-host-of-coremail",
    #     secret="your_secret_key"
    # )
    
    print("Coremail SDK Example")
    print("=" * 50)
    
    # Request a token
    try:
        token = client.requestToken()
        print(f"Token obtained: {token[:20]}...")  # Print first 20 chars
    except Exception as e:
        print(f"Error obtaining token: {e}")
        return
    
    # Get user attributes
    try:
        user_attrs = client.getAttrs("test_user@your-host-of-coremail")
        print(f"User attributes: {user_attrs}")
    except Exception as e:
        print(f"Error getting user attributes: {e}")
    
    # Change user attributes
    try:
        change_result = client.changeAttrs("test_user@your-host-of-coremail", {"password": "new_password"})
        print(f"Change attributes result: {change_result}")
    except Exception as e:
        print(f"Error changing attributes: {e}")
    
    # Authenticate a user
    try:
        auth_result = client.authenticate("test_user@your-host-of-coremail", "")
        print(f"Authentication result: {auth_result}")
    except Exception as e:
        print(f"Error authenticating user: {e}")
    
    # Using the API wrapper for higher-level operations
    api = CoremailAPI(client)
    
    # Get user info
    try:
        user_info = api.get_user_info("test_user@your-host-of-coremail")
        print(f"User info via API wrapper: {user_info}")
    except Exception as e:
        print(f"Error getting user info via API wrapper: {e}")
    
    # Change user attributes via API wrapper
    try:
        change_result = api.change_user_attributes("test_user@your-host-of-coremail", {"password": "new_password"})
        print(f"Change attributes via API wrapper: {change_result}")
    except Exception as e:
        print(f"Error changing attributes via API wrapper: {e}")
    
    # Create a new user
    try:
        create_result = api.create_user(
            "newuser@your-host-of-coremail", 
            {"password": "initial_password", "quota_mb": 1024, "user_enabled": True}
        )
        print(f"Create user result: {create_result}")
    except Exception as e:
        print(f"Error creating user: {e}")
    
    # List users
    try:
        users_list = api.list_users(domain="your-host-of-coremail")
        print(f"Users in domain: {users_list}")
    except Exception as e:
        print(f"Error listing users: {e}")
    
    # Domain operations
    try:
        domain_info = api.get_domain_info("your-host-of-coremail")
        print(f"Domain info: {domain_info}")
    except Exception as e:
        print(f"Error getting domain info: {e}")
    
    # List domains
    try:
        domains_list = api.list_domains()
        print(f"List of domains: {domains_list}")
    except Exception as e:
        print(f"Error listing domains: {e}")
    
    # Check if user exists
    try:
        user_exists = api.check_user_exists("test_user@your-host-of-coremail")
        print(f"User exists: {user_exists}")
    except Exception as e:
        print(f"Error checking if user exists: {e}")
    
    # Authenticate user via API wrapper
    try:
        is_authenticated = api.authenticate_user("test_user@your-host-of-coremail", "")
        print(f"User authenticated: {is_authenticated}")
    except Exception as e:
        print(f"Error authenticating user via API wrapper: {e}")
    
    print("=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    example_usage()