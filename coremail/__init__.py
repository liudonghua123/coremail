"""
Coremail SDK for interacting with Coremail XT API v3
"""
import os
import requests
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode


class CoremailClient:
    """
    CoremailClient provides methods to interact with Coremail XT API v3.

    The client handles authentication tokens automatically and provides methods
    for all available API endpoints as specified in the Coremail XT documentation.
    """

    def __init__(self, base_url: Optional[str] = None, app_id: Optional[str] = None, secret: Optional[str] = None):
        """
        Initialize the CoremailClient with configuration.
        
        Args:
            base_url: The base URL for the Coremail API (e.g., "http://your-host-of-coremail:9900/apiws/v3")
            app_id: Application ID for authentication (e.g., "your_app_id@your-domain.com")
            secret: Secret key for authentication
        """
        # Use environment variables if not explicitly provided
        self.base_url = base_url or os.getenv("COREMAIL_BASE_URL")
        self.app_id = app_id or os.getenv("COREMAIL_APP_ID")
        self.secret = secret or os.getenv("COREMAIL_SECRET")
        
        if not self.base_url:
            raise ValueError("Base URL must be provided either as parameter or via COREMAIL_BASE_URL environment variable")
        if not self.app_id:
            raise ValueError("App ID must be provided either as parameter or via COREMAIL_APP_ID environment variable")
        if not self.secret:
            raise ValueError("Secret must be provided either as parameter or via COREMAIL_SECRET environment variable")
        
        self.session = requests.Session()
        self._token_cache = None

    def _get_token(self) -> str:
        """
        Get a valid token, using cache if available and not expired.
        """
        if not self._token_cache:
            self._token_cache = self.requestToken()
        return self._token_cache

    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Any:
        """
        Make a request to the specified endpoint with the given data.
        
        Args:
            endpoint: API endpoint (e.g., "/userLogin")
            data: Request data to send
            
        Returns:
            Response data from the API
        """
        url = f"{self.base_url}{endpoint}"
        # Add token to the request data
        request_data = {"_token": self._get_token(), **data}
        
        response = self.session.post(url, json=request_data)
        response.raise_for_status()
        result = response.json()
        
        return result

    def requestToken(self) -> str:
        """
        Request a new access token using app_id and secret.
        
        Args:
            app_id: Application ID for authentication
            secret: Application secret for authentication
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.requestToken()
            >>> print(response)
        """
        url = f"{self.base_url}/requestToken"
        payload = {
            "app_id": self.app_id,
            "secret": self.secret
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        return result["result"]

    def userLogin(self, user_at_domain: str) -> Dict[str, Any]:
        """
        User login to get a session ID.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.userLogin("user@example.com")
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain
        }
        return self._make_request("/userLogin", data)

    def userLoginEx(self, user_at_domain: str, attrs: Optional[str] = None) -> Dict[str, Any]:
        """
        User login with additional parameters and return extra information.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            attrs: Operation attributes as URL-encoded string
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.userLoginEx("user@example.com", "remote_ip=192.168.201.165&cookieKey=Coremail&cookiecheck=123")
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain
        }
        if attrs is not None:
            data["attrs"] = attrs
        return self._make_request("/userLoginEx", data)

    def userExist(self, user_at_domain: str) -> Dict[str, Any]:
        """
        Check if user exists.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.userExist("user@example.com")
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain
        }
        return self._make_request("/userExist", data)

    def authenticate(self, user_at_domain: str, password: str) -> Dict[str, Any]:
        """
        Verify user password.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            password: User password
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.authenticate("user@example.com", "password123")
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain,
            "password": password
        }
        return self._make_request("/authenticate", data)

    def sesTimeOut(self, ses_id: str) -> Dict[str, Any]:
        """
        Check user's session and return user information.
        
        Args:
            ses_id: User session ID (sid)
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.sesTimeOut("BAehsYOOHknssAvQWHORDOnOLEsSNJKD")
            >>> print(response)
        """
        data = {
            "ses_id": ses_id
        }
        return self._make_request("/sesTimeOut", data)

    def sesRefresh(self, ses_id: str) -> Dict[str, Any]:
        """
        Check user's session and refresh access time.
        
        Args:
            ses_id: User session ID (sid)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.sesRefresh("BAehsYOOHknssAvQWHORDOnOLEsSNJKD")
            >>> print(response)
        """
        data = {
            "ses_id": ses_id
        }
        return self._make_request("/sesRefresh", data)

    def getSessionVar(self, ses_id: str, ses_key: str) -> Dict[str, Any]:
        """
        Get variable from user's session.
        
        Args:
            ses_id: User session ID (sid)
            ses_key: Session variable name to get
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.getSessionVar("BAehsYOOHknssAvQWHORDOnOLEsSNJKD", "uidatdomain")
            >>> print(response)
        """
        data = {
            "ses_id": ses_id,
            "ses_key": ses_key
        }
        return self._make_request("/getSessionVar", data)

    def userLogout(self, ses_id: str) -> Dict[str, Any]:
        """
        Logout user session.
        
        Args:
            ses_id: User session ID (sid)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.userLogout("BAehsYOOHknssAvQWHORDOnOLEsSNJKD")
            >>> print(response)
        """
        data = {
            "ses_id": ses_id
        }
        return self._make_request("/userLogout", data)

    def setSessionVar(self, ses_id: str, ses_key: str, ses_var: str) -> Dict[str, Any]:
        """
        Set variable in user's session.
        
        Args:
            ses_id: User session ID (sid)
            ses_key: Session variable name to set
            ses_var: Value to set for the variable
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.setSessionVar("BAyhsYOOeaCsSVQABZahowtpqTvPFYwD", "TEST_VAR", "TEST_VAR_VALUE")
            >>> print(response)
        """
        data = {
            "ses_id": ses_id,
            "ses_key": ses_key,
            "ses_var": ses_var
        }
        return self._make_request("/setSessionVar", data)

    def addOrg(self, org_id: str, attrs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create organization.
        
        Args:
            org_id: Enterprise organization identifier
            attrs: Organization attributes (optional)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> attrs = {
            ...     "org_name": "API Test Organization",
            ...     "domain_name": "api.cn",
            ...     "cos_id": [1],
            ...     "num_of_classes": [1000],
            ...     "org_status": 0,
            ...     "org_expiry_date": "2025-01-01"
            ... }
            >>> response = client.addOrg("apitest", attrs)
            >>> print(response)
        """
        data = {
            "org_id": org_id
        }
        if attrs is not None:
            data["attrs"] = attrs
        return self._make_request("/addOrg", data)

    def getOrgInfo(self, org_id: str, attrs: List[str] = ["org_name", "domain_name", "org_status"]) -> Dict[str, Any]:
        """
        Get organization attributes.

        Args:
            org_id: Enterprise organization identifier
            attrs: List of organization attribute names to retrieve.

        Returns:
            Response from the API (should contain code and result fields)

        Example:
            >>> client = CoremailClient()
            >>> response = client.getOrgInfo("apitest")
            >>> print(response)
            >>> response = client.getOrgInfo("apitest", ["org_name", "domain_name", "org_status"])
            >>> print(response)
        """
        data = {
            "org_id": org_id
        }
        if attrs is not None:
            # Convert list of attribute names to dict with null values
            attrs_dict = {attr: None for attr in attrs}
            data["attrs"] = attrs_dict
        return self._make_request("/getOrgInfo", data)

    def alterOrg(self, org_id: str, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Modify organization attributes.
        
        Args:
            org_id: Enterprise organization identifier
            attrs: Attributes to modify (at least one required)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> attrs = {
            ...     "org_name": "API Test Organization - Modified",
            ...     "org_expiry_date": "2024-09-11"
            ... }
            >>> response = client.alterOrg("apitest", attrs)
            >>> print(response)
        """
        data = {
            "org_id": org_id,
            "attrs": attrs
        }
        return self._make_request("/alterOrg", data)

    def addOrgDomain(self, org_id: str, domain_name: str) -> Dict[str, Any]:
        """
        Add organization domain.
        
        Args:
            org_id: Enterprise organization identifier
            domain_name: Domain name to add (must be pre-created)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.addOrgDomain("apitest", "dev.cn")
            >>> print(response)
        """
        data = {
            "org_id": org_id,
            "domain_name": domain_name
        }
        return self._make_request("/addOrgDomain", data)

    def delOrgDomain(self, org_id: str, domain_name: str) -> Dict[str, Any]:
        """
        Delete organization domain.
        
        Args:
            org_id: Enterprise organization identifier
            domain_name: Domain name to delete
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.delOrgDomain("apitest", "dev.cn")
            >>> print(response)
        """
        data = {
            "org_id": org_id,
            "domain_name": domain_name
        }
        return self._make_request("/delOrgDomain", data)

    def addOrgCos(self, org_id: str, num_of_classes: int, cos_name: Optional[str] = None, cos_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Add organization service level.
        
        Args:
            org_id: Enterprise organization identifier
            num_of_classes: Number of allocatable users
            cos_name: Service level name (alternative to cos_id, cos_name takes priority)
            cos_id: Service level identifier (alternative to cos_name)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.addOrgCos("apitest", 100, cos_id=8)
            >>> print(response)
        """
        data = {
            "org_id": org_id,
            "num_of_classes": num_of_classes
        }
        if cos_name is not None:
            data["cos_name"] = cos_name
        if cos_id is not None:
            data["cos_id"] = cos_id
        return self._make_request("/addOrgCos", data)

    def alterOrgCos(self, org_id: str, num_of_classes: int, cos_name: Optional[str] = None, cos_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Update organization service level.
        
        Args:
            org_id: Enterprise organization identifier
            num_of_classes: Number of allocatable users
            cos_name: Service level name (alternative to cos_id, cos_name takes priority)
            cos_id: Service level identifier (alternative to cos_name)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.alterOrgCos("apitest", 99, cos_id=8)
            >>> print(response)
        """
        data = {
            "org_id": org_id,
            "num_of_classes": num_of_classes
        }
        if cos_name is not None:
            data["cos_name"] = cos_name
        if cos_id is not None:
            data["cos_id"] = cos_id
        return self._make_request("/alterOrgCos", data)

    def delOrgCos(self, org_id: str, cos_id: int) -> Dict[str, Any]:
        """
        Delete organization service level.
        
        Args:
            org_id: Enterprise organization identifier
            cos_id: Service level identifier
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.delOrgCos("apitest", 8)
            >>> print(response)
        """
        data = {
            "org_id": org_id,
            "cos_id": cos_id
        }
        return self._make_request("/delOrgCos", data)

    def getOrgCosUser(self, org_id: str, cos_id: int) -> Dict[str, Any]:
        """
        List all usernames under a specific service level in an organization.
        
        Args:
            org_id: Enterprise organization identifier
            cos_id: Service level identifier
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.getOrgCosUser("apitest", 8)
            >>> print(response)
        """
        data = {
            "org_id": org_id,
            "cos_id": cos_id
        }
        return self._make_request("/getOrgCosUser", data)

    def getOrgList(self) -> Dict[str, Any]:
        """
        Get list of organizations.
        
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.getOrgList()
            >>> print(response)
        """
        data = {}
        return self._make_request("/getOrgList", data)

    def addUnit(self, org_id: str, unit_name: str, attrs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add organizational unit.
        
        Args:
            org_id: Organization identifier
            unit_name: Unit name to add
            attrs: Additional unit attributes (optional)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> attrs = {"description": "Test Unit"}
            >>> response = client.addUnit("org1", "test_unit", attrs)
            >>> print(response)
        """
        data = {
            "org_id": org_id,
            "unit_name": unit_name
        }
        if attrs is not None:
            data["attrs"] = attrs
        return self._make_request("/addUnit", data)

    def delUnit(self, org_id: str, unit_name: str) -> Dict[str, Any]:
        """
        Delete organizational unit.
        
        Args:
            org_id: Organization identifier
            unit_name: Unit name to delete
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.delUnit("org1", "test_unit")
            >>> print(response)
        """
        data = {
            "org_id": org_id,
            "unit_name": unit_name
        }
        return self._make_request("/delUnit", data)

    def getUnitAttrs(self, org_id: str, unit_name: str, attrs: List[str] = ["parent_org_unit_id", "org_unit_name", "org_unit_list_rank", "user_count", "abook_user_count"]) -> Dict[str, Any]:
        """
        Get organizational unit attributes.

        Args:
            org_id: Organization identifier
            unit_name: Unit name
            attrs: List of unit attribute names to retrieve.

        Returns:
            Response from the API (should contain code and result fields)

        Example:
            >>> client = CoremailClient()
            >>> response = client.getUnitAttrs("org1", "test_unit")
            >>> print(response)
            >>> response = client.getUnitAttrs("org1", "test_unit", ["parent_org_unit_id", "org_unit_name", "org_unit_list_rank", "user_count", "abook_user_count"])
            >>> print(response)
        """
        data = {
            "org_id": org_id,
            "unit_name": unit_name
        }
        if attrs is not None:
            # Convert list of attribute names to dict with null values
            attrs_dict = {attr: None for attr in attrs}
            data["attrs"] = attrs_dict
        return self._make_request("/getUnitAttrs", data)

    def setUnitAttrs(self, org_id: str, unit_name: str, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set organizational unit attributes.
        
        Args:
            org_id: Organization identifier
            unit_name: Unit name
            attrs: Attributes to set (at least one required)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> attrs = {"description": "Updated Unit Description"}
            >>> response = client.setUnitAttrs("org1", "test_unit", attrs)
            >>> print(response)
        """
        data = {
            "org_id": org_id,
            "unit_name": unit_name,
            "attrs": attrs
        }
        return self._make_request("/setUnitAttrs", data)

    def createUser(self, user_at_domain: str, password: str, attrs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            password: User password
            attrs: Additional user attributes (optional)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> attrs = {"display_name": "New User", "cos_id": 1}
            >>> response = client.createUser("newuser@example.com", "password123", attrs)
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain,
            "password": password
        }
        if attrs is not None:
            data["attrs"] = attrs
        return self._make_request("/createUser", data)

    def deleteUser(self, user_at_domain: str) -> Dict[str, Any]:
        """
        Delete a user.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.deleteUser("user@example.com")
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain
        }
        return self._make_request("/deleteUser", data)

    def getAttrs(self, user_at_domain: str, attrs: List[str] = ["true_name", "cas_name", "user_status"]) -> Dict[str, Any]:
        """
        Get user attributes.

        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            attrs: List of user attribute names to retrieve (default: ["true_name", "cas_name", "user_status"])

        Returns:
            Response from the API (should contain code and result fields)

        Example:
            >>> client = CoremailClient()
            >>> response = client.getAttrs("test_user@example.com")
            >>> print(response)
            >>> response = client.getAttrs("test_user@example.com", ["true_name", "display_name"])
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain
        }

        # Convert list of attribute names to dict with null values
        attrs_dict = {attr: None for attr in attrs}
        data["attrs"] = attrs_dict
        return self._make_request("/getAttrs", data)

    def changeAttrs(self, user_at_domain: str, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Change user attributes.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            attrs: Attributes to change (at least one required)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> attrs = {"display_name": "Changed Name", "quota": 2048}
            >>> response = client.changeAttrs("user@example.com", attrs)
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain,
            "attrs": attrs
        }
        return self._make_request("/changeAttrs", data)

    def addSmtpAlias(self, user_at_domain: str, alias: str) -> Dict[str, Any]:
        """
        Add SMTP alias for user.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            alias: SMTP alias to add (e.g., "alias@domain.com")
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.addSmtpAlias("user@example.com", "alias@domain.com")
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain,
            "alias": alias
        }
        return self._make_request("/addSmtpAlias", data)

    def delSmtpAlias(self, user_at_domain: str, alias: str) -> Dict[str, Any]:
        """
        Delete SMTP alias for user.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            alias: SMTP alias to delete (e.g., "alias@domain.com")
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.delSmtpAlias("user@example.com", "alias@domain.com")
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain,
            "alias": alias
        }
        return self._make_request("/delSmtpAlias", data)

    def getSmtpAlias(self, user_at_domain: str) -> Dict[str, Any]:
        """
        Get SMTP aliases for user.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.getSmtpAlias("user@example.com")
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain
        }
        return self._make_request("/getSmtpAlias", data)

    def setAdminType(self, user_at_domain: str, admin_type: int) -> Dict[str, Any]:
        """
        Set admin type for user.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            admin_type: Admin type to set (0-regular user, 1-sys admin, etc.)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.setAdminType("admin@example.com", 1)
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain,
            "admin_type": admin_type
        }
        return self._make_request("/setAdminType", data)

    def getAdminType(self, user_at_domain: str) -> Dict[str, Any]:
        """
        Get admin type for user.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.getAdminType("admin@example.com")
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain
        }
        return self._make_request("/getAdminType", data)

    def renameUser(self, old_user_at_domain: str, new_user_at_domain: str) -> Dict[str, Any]:
        """
        Rename user.
        
        Args:
            old_user_at_domain: Current user email address (e.g., "old@example.com")
            new_user_at_domain: New user email address (e.g., "new@example.com")
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.renameUser("old@example.com", "new@example.com")
            >>> print(response)
        """
        data = {
            "old_user_at_domain": old_user_at_domain,
            "new_user_at_domain": new_user_at_domain
        }
        return self._make_request("/renameUser", data)

    def moveUser(self, user_at_domain: str, target_org_id: str, target_unit_name: str) -> Dict[str, Any]:
        """
        Move user to different organization/unit.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            target_org_id: Target organization identifier
            target_unit_name: Target unit name
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.moveUser("user@example.com", "new_org", "new_unit")
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain,
            "target_org_id": target_org_id,
            "target_unit_name": target_unit_name
        }
        return self._make_request("/moveUser", data)

    def createObj(self, obj_type: str, obj_name: str, org_id: str, attrs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create object.
        
        Args:
            obj_type: Object type (e.g., "list" for mailing list)
            obj_name: Object name
            org_id: Organization identifier
            attrs: Additional object attributes (optional)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> attrs = {"description": "Test Mailing List"}
            >>> response = client.createObj("list", "test_list", "org1", attrs)
            >>> print(response)
        """
        data = {
            "obj_type": obj_type,
            "obj_name": obj_name,
            "org_id": org_id
        }
        if attrs is not None:
            data["attrs"] = attrs
        return self._make_request("/createObj", data)

    def getObjAttrs(self, obj_uid: str, attrs: List[str] = ["org_id", "org_unit_id", "obj_class", "obj_email"]) -> Dict[str, Any]:
        """
        Get object attributes.

        Args:
            obj_uid: Organization identifier
            attrs: List of object attribute names to retrieve.

        Returns:
            Response from the API (should contain code and result fields)

        Example:
            >>> client = CoremailClient()
            >>> response = client.getObjAttrs("1_test_19289d00137")
            >>> print(response)
            >>> response = client.getObjAttrs("1_test_19289d00137", ["org_id", "org_unit_id", "obj_class", "obj_email"])
            >>> print(response)
        """
        data = {
            "obj_uid": obj_uid
        }
        if attrs is not None:
            # Convert list of attribute names to dict with null values
            attrs_dict = {attr: None for attr in attrs}
            data["attrs"] = attrs_dict
        return self._make_request("/getObjAttrs", data)

    def setObjAttrs(self, obj_type: str, obj_name: str, org_id: str, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set object attributes.
        
        Args:
            obj_type: Object type (e.g., "list" for mailing list)
            obj_name: Object name
            org_id: Organization identifier
            attrs: Attributes to set (at least one required)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> attrs = {"description": "Updated Mailing List Description"}
            >>> response = client.setObjAttrs("list", "test_list", "org1", attrs)
            >>> print(response)
        """
        data = {
            "obj_type": obj_type,
            "obj_name": obj_name,
            "org_id": org_id,
            "attrs": attrs
        }
        return self._make_request("/setObjAttrs", data)

    def deleteObj(self, obj_type: str, obj_name: str, org_id: str) -> Dict[str, Any]:
        """
        Delete object.
        
        Args:
            obj_type: Object type (e.g., "list" for mailing list)
            obj_name: Object name
            org_id: Organization identifier
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.deleteObj("list", "test_list", "org1")
            >>> print(response)
        """
        data = {
            "obj_type": obj_type,
            "obj_name": obj_name,
            "org_id": org_id
        }
        return self._make_request("/deleteObj", data)

    def domainExist(self, domain_name: str) -> Dict[str, Any]:
        """
        Check if domain exists.
        
        Args:
            domain_name: Domain name to check (e.g., "example.com")
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.domainExist("example.com")
            >>> print(response)
        """
        data = {
            "domain_name": domain_name
        }
        return self._make_request("/domainExist", data)

    def getDomainList(self, start: int = 0, limit: int = 100) -> Dict[str, Any]:
        """
        Get list of domains.
        
        Args:
            start: Starting index for pagination (default: 0)
            limit: Maximum number of domains to return (default: 100)
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.getDomainList(start=0, limit=50)
            >>> print(response)
        """
        data = {
            "start": start,
            "limit": limit
        }
        return self._make_request("/getDomainList", data)

    def addDomain25(self, domain_name: str, attrs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add domain for port 25 (SMTP).
        
        Args:
            domain_name: Domain name to add (e.g., "example.com")
            attrs: Additional domain attributes (optional)
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> attrs = {"mx_record": "mail.example.com"}
            >>> response = client.addDomain25("example.com", attrs)
            >>> print(response)
        """
        data = {
            "domain_name": domain_name
        }
        if attrs is not None:
            data["attrs"] = attrs
        return self._make_request("/addDomain25", data)

    def delDomain25(self, domain_name: str) -> Dict[str, Any]:
        """
        Delete domain for port 25 (SMTP).
        
        Args:
            domain_name: Domain name to delete (e.g., "example.com")
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.delDomain25("example.com")
            >>> print(response)
        """
        data = {
            "domain_name": domain_name
        }
        return self._make_request("/delDomain25", data)

    def addDomainAlias(self, domain_name: str, alias_domain_name: str) -> Dict[str, Any]:
        """
        Add domain alias.
        
        Args:
            domain_name: Original domain name (e.g., "example.com")
            alias_domain_name: Alias domain name to add (e.g., "alias.com")
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.addDomainAlias("example.com", "alias.com")
            >>> print(response)
        """
        data = {
            "domain_name": domain_name,
            "alias_domain_name": alias_domain_name
        }
        return self._make_request("/addDomainAlias", data)

    def getDomainAlias(self, domain_name: str) -> Dict[str, Any]:
        """
        Get domain aliases.
        
        Args:
            domain_name: Domain name to get aliases for (e.g., "example.com")
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.getDomainAlias("example.com")
            >>> print(response)
        """
        data = {
            "domain_name": domain_name
        }
        return self._make_request("/getDomainAlias", data)

    def delDomainAlias(self, domain_name: str, alias_domain_name: str) -> Dict[str, Any]:
        """
        Delete domain alias.
        
        Args:
            domain_name: Original domain name (e.g., "example.com")
            alias_domain_name: Alias domain name to delete (e.g., "alias.com")
            
        Returns:
            Response from the API (should contain code field)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.delDomainAlias("example.com", "alias.com")
            >>> print(response)
        """
        data = {
            "domain_name": domain_name,
            "alias_domain_name": alias_domain_name
        }
        return self._make_request("/delDomainAlias", data)

    def getOrgListByDomain(self, domain_name: str) -> Dict[str, Any]:
        """
        Get organization list by domain.
        
        Args:
            domain_name: Domain name to search by (e.g., "example.com")
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.getOrgListByDomain("example.com")
            >>> print(response)
        """
        data = {
            "domain_name": domain_name
        }
        return self._make_request("/getOrgListByDomain", data)

    def listMailInfos(self, user_at_domain: str, start_time: str, end_time: str, attrs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List mail information.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            start_time: Start time for mail info retrieval (format: yyyy-MM-dd HH:mm:ss)
            end_time: End time for mail info retrieval (format: yyyy-MM-dd HH:mm:ss)
            attrs: Additional attributes for mail info query (optional)
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.listMailInfos("user@example.com", "2023-01-01 00:00:00", "2023-01-02 00:00:00")
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain,
            "start_time": start_time,
            "end_time": end_time
        }
        if attrs is not None:
            data["attrs"] = attrs
        return self._make_request("/listMailInfos", data)

    def getNewMailInfos(self, user_at_domain: str, start_time: str, end_time: str, attrs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get new mail information.
        
        Args:
            user_at_domain: User email address (e.g., "user@example.com")
            start_time: Start time for mail info retrieval (format: yyyy-MM-dd HH:mm:ss)
            end_time: End time for mail info retrieval (format: yyyy-MM-dd HH:mm:ss)
            attrs: Additional attributes for mail info query (optional)
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> response = client.getNewMailInfos("user@example.com", "2023-01-01 00:00:00", "2023-01-02 00:00:00")
            >>> print(response)
        """
        data = {
            "user_at_domain": user_at_domain,
            "start_time": start_time,
            "end_time": end_time
        }
        if attrs is not None:
            data["attrs"] = attrs
        return self._make_request("/getNewMailInfos", data)

    def smtpTransport(self, sender: str, recipient: str, content: str) -> Dict[str, Any]:
        """
        SMTP transport for message delivery.
        
        Args:
            sender: Sender email address (e.g., "sender@example.com")
            recipient: Recipient email address (e.g., "recipient@example.com")
            content: Email content
            
        Returns:
            Response from the API (should contain code and result fields)
            
        Example:
            >>> client = CoremailClient()
            >>> content = "Subject: Test\\n\\nThis is a test email."
            >>> response = client.smtpTransport("sender@example.com", "recipient@example.com", content)
            >>> print(response)
        """
        data = {
            "sender": sender,
            "recipient": recipient,
            "content": content
        }
        return self._make_request("/smtpTransport", data)