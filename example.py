"""
Example usage of the Coremail SDK
"""
from coremail import CoremailClient
from dotenv import load_dotenv

load_dotenv()

# Initialize the client with environment variables
client = CoremailClient()

# Or with explicit parameters
# client = CoremailClient(
#     base_url="http://your-host-of-coremail:9900/apiws/v3",
#     app_id="your_app_id@your-domain.com",
#     secret="your_secret_key"
# )

# Example: Request a token
token_response = client.requestToken()
print(f"Token Response: {token_response}")

# Example: Get user attributes

user_at_domain = "john.doe@your-domain.com"
result = client.getAttrs(user_at_domain, ["true_name", "cas_name", "user_status"])
print(f"User attributes result: {result}")

# Example: Get user alias

result = client.getSmtpAlias(user_at_domain)
print(f"User alias result: {result}")