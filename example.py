"""
Basic usage example for Coremail SDK
"""
from coremail import CoremailClient

def main():
    # Create a client instance
    # It will automatically use environment variables if available
    client = CoremailClient()
    
    # Example operations (these will fail without real credentials)
    try:
        # Get a token (this would require real credentials)
        token = client.request_token()
        print(f"Successfully obtained token: {token[:30]}...")
    except Exception as e:
        print(f"Note: Token request failed (expected without real credentials): {e}")
    
    print("\nSDK initialized successfully!")
    print("To use with real credentials, set the following environment variables:")
    print("- COREMAIL_BASE_URL")
    print("- COREMAIL_APP_ID") 
    print("- COREMAIL_SECRET")

if __name__ == "__main__":
    main()