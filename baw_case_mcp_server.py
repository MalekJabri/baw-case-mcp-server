"""
BAW Case MCP Server

This MCP server provides tools for managing IBM Business Automation Workflow (BAW) Case Management.
It implements Case, Solution, Activity, and Stage operations from the BAW Case REST API.
"""

import os
import httpx
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

from aicoe_agent_utils.mcp.base_mcp import BaseMCP, tool, Context

# Load environment variables
load_dotenv()


class BAWCaseMCP(BaseMCP):
    """MCP Server for IBM Business Automation Workflow Case Management"""

    def __init__(self):
        """Initialize the BAW Case MCP Server"""
        super().__init__()
        
        # BAW Server Configuration
        self.base_url = os.getenv("BAW_BASE_URL", "https://localhost:9443/bas/CaseManager/CASEREST/v2")
        self.username = os.getenv("BAW_USERNAME", "")
        self.password = os.getenv("BAW_PASSWORD", "")
        
        # HTTP Client configuration
        self.client = httpx.AsyncClient(
            verify=False,  # For development; should be True in production
            timeout=30.0,
            auth=(self.username, self.password)
        )
        
        # CSRF Token storage
        self.csrf_token: Optional[str] = None

    async def _get_csrf_token(self) -> str:
        """
        Obtain a CSRF token from BAW server.
        
        Returns:
            str: The CSRF token
            
        Raises:
            Exception: If token retrieval fails
        """
        if self.csrf_token:
            return self.csrf_token
            
        url = f"{self.base_url}/system/login"
        payload = {"refresh_groups": False}
        
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            self.csrf_token = data.get("csrf_token", "")
            return self.csrf_token
        except Exception as e:
            raise Exception(f"Failed to obtain CSRF token: {str(e)}")

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        require_csrf: bool = True
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to BAW Case API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data
            require_csrf: Whether CSRF token is required
            
        Returns:
            Dict containing the response data
            
        Raises:
            Exception: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        headers = {}
        
        if require_csrf:
            token = await self._get_csrf_token()
            headers["BPMCSRFToken"] = token
        
        try:
            response = await self.client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=headers
            )
            response.raise_for_status()
            return response.json() if response.text else {}
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== SYSTEM OPERATIONS ====================

    @tool
    async def login(self, ctx: Context, refresh_groups: bool = False) -> Dict[str, Any]:
        """
        Obtain IBM Business Automation Workflow CSRF prevention token.
        
        Args:
            ctx: MCP context
            refresh_groups: Whether to refresh the user's group membership information
            
        Returns:
            Dict containing the CSRF token and status
        """
        url = f"{self.base_url}/system/login"
        payload = {"refresh_groups": refresh_groups}
        
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            self.csrf_token = data.get("csrf_token", "")
            return {
                "success": True,
                "csrf_token": self.csrf_token,
                "message": "Successfully obtained CSRF token"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to obtain CSRF token"
            }

    # ==================== SOLUTION OPERATIONS ====================

    @tool
    async def list_solutions(self, ctx: Context) -> Dict[str, Any]:
        """
        List all case solutions.
        
        Args:
            ctx: MCP context
            
        Returns:
            Dict containing list of solutions
        """
        return await self._make_request("GET", "/solutions")

    @tool
    async def create_solution(
        self,
        ctx: Context,
        solution_name: str,
        solution_prefix: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new case solution.
        
        Args:
            ctx: MCP context
            solution_name: Name of the solution
            solution_prefix: Prefix for the solution
            description: Optional description
            
        Returns:
            Dict containing the created solution details
        """
        payload = {
            "solutionName": solution_name,
            "solutionPrefix": solution_prefix
        }
        if description:
            payload["description"] = description
            
        return await self._make_request("POST", "/solutions", json_data=payload)

    @tool
    async def get_solution_deployment_status(
        self,
        ctx: Context,
        solution_acronym: str
    ) -> Dict[str, Any]:
        """
        Get deployment status of a solution.
        
        Args:
            ctx: MCP context
            solution_acronym: The acronym of the solution
            
        Returns:
            Dict containing deployment status
        """
        return await self._make_request(
            "GET",
            f"/solution/{solution_acronym}/deploymentstatus"
        )

    @tool
    async def get_solution_object_stores(
        self,
        ctx: Context,
        solution_acronym: str
    ) -> Dict[str, Any]:
        """
        Get associated object stores for a solution.
        
        Args:
            ctx: MCP context
            solution_acronym: The acronym of the solution
            
        Returns:
            Dict containing associated object stores
        """
        return await self._make_request(
            "GET",
            f"/solution/{solution_acronym}/associatedobjectstores"
        )

    @tool
    async def import_solution_manifest(
        self,
        ctx: Context,
        manifest_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Import a solution manifest.
        
        Args:
            ctx: MCP context
            manifest_data: The manifest data to import
            
        Returns:
            Dict containing import status
        """
        return await self._make_request(
            "POST",
            "/solution/importManifest",
            json_data=manifest_data
        )

    @tool
    async def apply_solution_manifest(
        self,
        ctx: Context,
        solution_acronym: str,
        manifest_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply a manifest to a solution.
        
        Args:
            ctx: MCP context
            solution_acronym: The acronym of the solution
            manifest_data: The manifest data to apply
            
        Returns:
            Dict containing apply status
        """
        return await self._make_request(
            "POST",
            f"/solution/{solution_acronym}/applyManifest",
            json_data=manifest_data
        )

    @tool
    async def upgrade_solution(
        self,
        ctx: Context,
        solution_acronym: str,
        upgrade_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Upgrade a solution.
        
        Args:
            ctx: MCP context
            solution_acronym: The acronym of the solution
            upgrade_data: The upgrade configuration data
            
        Returns:
            Dict containing upgrade status
        """
        return await self._make_request(
            "POST",
            f"/solution/{solution_acronym}/upgradeSolution",
            json_data=upgrade_data
        )

    @tool
    async def import_solution(
        self,
        ctx: Context,
        solution_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Import a solution.
        
        Args:
            ctx: MCP context
            solution_data: The solution data to import
            
        Returns:
            Dict containing import status
        """
        return await self._make_request(
            "POST",
            "/solution/import",
            json_data=solution_data
        )

    @tool
    async def export_solution(
        self,
        ctx: Context,
        solution_acronym: str,
        export_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Export a solution.
        
        Args:
            ctx: MCP context
            solution_acronym: The acronym of the solution
            export_options: Optional export configuration
            
        Returns:
            Dict containing export data
        """
        return await self._make_request(
            "POST",
            f"/solution/{solution_acronym}/export",
            json_data=export_options or {}
        )

    @tool
    async def get_solution_pages(
        self,
        ctx: Context,
        solution_name: str
    ) -> Dict[str, Any]:
        """
        Get solution pages.
        
        Args:
            ctx: MCP context
            solution_name: Name of the solution
            
        Returns:
            Dict containing solution pages
        """
        return await self._make_request(
            "GET",
            f"/solution/{solution_name}/getSolutionPages"
        )

    @tool
    async def get_my_roles(
        self,
        ctx: Context,
        solution_name: str
    ) -> Dict[str, Any]:
        """
        Get current user's roles in a solution.
        
        Args:
            ctx: MCP context
            solution_name: Name of the solution
            
        Returns:
            Dict containing user roles
        """
        return await self._make_request(
            "GET",
            f"/solution/{solution_name}/myroles"
        )

    @tool
    async def configure_custom_widget_extension(
        self,
        ctx: Context,
        widget_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Configure a custom widget extension.
        
        Args:
            ctx: MCP context
            widget_config: Widget configuration data
            
        Returns:
            Dict containing configuration status
        """
        return await self._make_request(
            "POST",
            "/configureCustomWidgetExtension",
            json_data=widget_config
        )

    # ==================== CASE TYPE OPERATIONS ====================

    @tool
    async def get_case_type_properties(
        self,
        ctx: Context,
        case_type_name: str
    ) -> Dict[str, Any]:
        """
        Get properties of a case type.
        
        Args:
            ctx: MCP context
            case_type_name: Name of the case type
            
        Returns:
            Dict containing case type properties
        """
        return await self._make_request(
            "GET",
            f"/casetype/{case_type_name}/properties"
        )

    @tool
    async def get_discretionary_activity_types(
        self,
        ctx: Context,
        case_type_name: str
    ) -> Dict[str, Any]:
        """
        Get discretionary activity types for a case type.
        
        Args:
            ctx: MCP context
            case_type_name: Name of the case type
            
        Returns:
            Dict containing discretionary activity types
        """
        return await self._make_request(
            "GET",
            f"/casetype/{case_type_name}/discretionaryactivitytypes"
        )

    # ==================== CASE OPERATIONS ====================

    @tool
    async def create_case(
        self,
        ctx: Context,
        case_type: str,
        properties: Dict[str, Any],
        target_object_store: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new case instance.
        
        Args:
            ctx: MCP context
            case_type: Type of case to create
            properties: Case properties
            target_object_store: Optional target object store
            
        Returns:
            Dict containing the created case details
        """
        payload = {
            "CaseType": case_type,
            "Properties": properties
        }
        if target_object_store:
            payload["TargetObjectStore"] = target_object_store
            
        return await self._make_request("POST", "/case", json_data=payload)

    @tool
    async def get_case_properties(
        self,
        ctx: Context,
        case_id: str
    ) -> Dict[str, Any]:
        """
        Get properties of a case.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            
        Returns:
            Dict containing case properties
        """
        return await self._make_request("GET", f"/case/{case_id}/properties")

    @tool
    async def update_case_properties(
        self,
        ctx: Context,
        case_id: str,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update properties of a case.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            properties: Properties to update
            
        Returns:
            Dict containing update status
        """
        return await self._make_request(
            "PUT",
            f"/case/{case_id}/updateProperties",
            json_data=properties
        )

    @tool
    async def search_cases(
        self,
        ctx: Context,
        query: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Search for case instances.
        
        Args:
            ctx: MCP context
            query: Search query parameters
            
        Returns:
            Dict containing search results
        """
        return await self._make_request("POST", "/instances", json_data=query)

    # ==================== CASE COMMENT OPERATIONS ====================

    @tool
    async def get_case_comments(
        self,
        ctx: Context,
        case_id: str
    ) -> Dict[str, Any]:
        """
        Get comments for a case.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            
        Returns:
            Dict containing case comments
        """
        return await self._make_request("GET", f"/case/{case_id}/comments")

    @tool
    async def add_case_comment(
        self,
        ctx: Context,
        case_id: str,
        comment_text: str
    ) -> Dict[str, Any]:
        """
        Add a comment to a case.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            comment_text: Text of the comment
            
        Returns:
            Dict containing the added comment details
        """
        payload = {"CommentText": comment_text}
        return await self._make_request(
            "POST",
            f"/case/{case_id}/addComment",
            json_data=payload
        )

    # ==================== CASE ACTIVITY OPERATIONS ====================

    @tool
    async def get_case_activities(
        self,
        ctx: Context,
        case_id: str
    ) -> Dict[str, Any]:
        """
        Get activities for a case.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            
        Returns:
            Dict containing case activities
        """
        return await self._make_request("GET", f"/case/{case_id}/activities")

    @tool
    async def get_discretionary_activities(
        self,
        ctx: Context,
        case_id: str
    ) -> Dict[str, Any]:
        """
        Get discretionary activities for a case.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            
        Returns:
            Dict containing discretionary activities
        """
        return await self._make_request(
            "GET",
            f"/case/{case_id}/activities/discretionary"
        )

    @tool
    async def create_discretionary_activity(
        self,
        ctx: Context,
        case_id: str,
        activity_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a discretionary activity for a case.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            activity_type: Type of activity to create
            properties: Optional activity properties
            
        Returns:
            Dict containing the created activity details
        """
        payload = {"ActivityType": activity_type}
        if properties:
            payload["Properties"] = properties
            
        return await self._make_request(
            "POST",
            f"/case/{case_id}/activities/createDiscretionary",
            json_data=payload
        )

    # ==================== QUICK TASK OPERATIONS ====================

    @tool
    async def create_quick_task(
        self,
        ctx: Context,
        case_id: str,
        task_name: str,
        task_properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a quick task for a case.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            task_name: Name of the task
            task_properties: Task properties
            
        Returns:
            Dict containing the created task details
        """
        payload = {
            "TaskName": task_name,
            "Properties": task_properties
        }
        return await self._make_request(
            "PUT",
            f"/case/{case_id}/quicktask",
            json_data=payload
        )

    @tool
    async def get_quick_task(
        self,
        ctx: Context,
        task_id: str
    ) -> Dict[str, Any]:
        """
        Get details of a quick task.
        
        Args:
            ctx: MCP context
            task_id: ID of the task
            
        Returns:
            Dict containing task details
        """
        return await self._make_request("GET", f"/quicktask/{task_id}")

    # ==================== CASE STAGE OPERATIONS ====================

    @tool
    async def get_all_case_stages(
        self,
        ctx: Context,
        case_id: str
    ) -> Dict[str, Any]:
        """
        Retrieve all stages for a case.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            
        Returns:
            Dict containing all case stages
        """
        return await self._make_request(
            "GET",
            f"/case/{case_id}/stages/retrieveAllStages"
        )

    @tool
    async def get_current_case_stage(
        self,
        ctx: Context,
        case_id: str
    ) -> Dict[str, Any]:
        """
        Retrieve the current stage of a case.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            
        Returns:
            Dict containing current stage details
        """
        return await self._make_request(
            "GET",
            f"/case/{case_id}/stages/retrieveCurrentStage"
        )

    @tool
    async def complete_current_stage(
        self,
        ctx: Context,
        case_id: str
    ) -> Dict[str, Any]:
        """
        Complete the current stage of a case.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            
        Returns:
            Dict containing completion status
        """
        return await self._make_request(
            "POST",
            f"/case/{case_id}/stages/completeCurrentStage"
        )

    @tool
    async def restart_previous_stage(
        self,
        ctx: Context,
        case_id: str
    ) -> Dict[str, Any]:
        """
        Restart the previous stage of a case.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            
        Returns:
            Dict containing restart status
        """
        return await self._make_request(
            "POST",
            f"/case/{case_id}/stages/restartPreviousStage"
        )

    @tool
    async def place_stage_on_hold(
        self,
        ctx: Context,
        case_id: str
    ) -> Dict[str, Any]:
        """
        Place the current stage of a case on hold.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            
        Returns:
            Dict containing hold status
        """
        return await self._make_request(
            "POST",
            f"/case/{case_id}/stages/placeCurrentStageOnHold"
        )

    @tool
    async def release_stage_from_hold(
        self,
        ctx: Context,
        case_id: str
    ) -> Dict[str, Any]:
        """
        Release the current stage of a case from hold.
        
        Args:
            ctx: MCP context
            case_id: ID of the case
            
        Returns:
            Dict containing release status
        """
        return await self._make_request(
            "POST",
            f"/case/{case_id}/stages/releaseCurrentOnHoldStage"
        )

    async def test(self):
        """Test the BAW Case MCP server by calling login and listing solutions"""
        print("Testing BAW Case MCP Server...")
        print(f"Base URL: {self.base_url}")
        print(f"Username: {self.username}")
        
        # Create a mock context
        class MockContext:
            pass
        
        ctx = MockContext()
        
        # Test login
        print("\n1. Testing login...")
        result = await self.login(ctx, refresh_groups=False)
        print(f"Login result: {result}")
        
        if result.get("success"):
            print("\n2. Testing list_solutions...")
            solutions = await self.list_solutions(ctx)
            print(f"Solutions: {solutions}")
        
        await self.client.aclose()
        print("\nTest completed!")


if __name__ == "__main__":
    import sys
    import asyncio
    
    mcp = BAWCaseMCP()
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run test mode
        asyncio.run(mcp.test())
    else:
        # Run MCP server
        mcp.run()

# Made with Bob