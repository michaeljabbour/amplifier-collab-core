"""FastMCP server exposing collaboration tools."""

from fastmcp import FastMCP

from ..providers import get_provider

# Create the MCP server
mcp = FastMCP("amplifier-collaboration")


def create_server(provider_name: str = "m365"):
    """Create and configure the MCP server with tools.
    
    Args:
        provider_name: Which provider to use ('m365', 'google')
        
    Returns:
        Configured FastMCP server
    """
    provider = get_provider(provider_name)
    
    # =========================================================================
    # Channel Tools
    # =========================================================================
    
    @mcp.tool()
    async def list_channels(team_id: str | None = None) -> dict:
        """List available messaging channels.
        
        Args:
            team_id: Optional team/workspace to filter by
        """
        channels = await provider.list_channels(team_id)
        return {
            "channels": [
                {
                    "id": ch.id,
                    "name": ch.name,
                    "team_id": ch.team_id,
                    "team_name": ch.team_name,
                }
                for ch in channels
            ]
        }
    
    @mcp.tool()
    async def read_channel_messages(
        channel_name: str,
        team_id: str | None = None,
        limit: int = 20,
    ) -> dict:
        """Read recent messages from a channel.
        
        Args:
            channel_name: Name of the channel
            team_id: Team ID (required for M365)
            limit: Maximum messages to return
        """
        # Find channel by name
        channels = await provider.list_channels(team_id)
        channel = next((c for c in channels if c.name.lower() == channel_name.lower()), None)
        
        if not channel:
            return {
                "error": f"Channel '{channel_name}' not found",
                "available_channels": [c.name for c in channels],
            }
        
        messages = await provider.get_messages(
            channel_id=channel.id,
            team_id=channel.team_id,
            limit=limit,
        )
        return {
            "channel": channel_name,
            "messages": [
                {
                    "sender": msg.sender,
                    "content": msg.content,
                    "timestamp": msg.timestamp,
                }
                for msg in messages
            ],
        }
    
    @mcp.tool()
    async def post_teams_message(
        channel_name: str,
        message: str,
        title: str | None = None,
    ) -> dict:
        """Post a message to a channel.
        
        Args:
            channel_name: Logical channel name ('general', 'alerts', 'handoffs')
            message: Message content
            title: Optional message title
        """
        try:
            success = await provider.post_message(
                channel_name=channel_name,
                message=message,
                title=title,
            )
            return {"success": success, "channel": channel_name}
        except ValueError as e:
            return {"success": False, "error": str(e)}
    
    # =========================================================================
    # Document Tools
    # =========================================================================
    
    @mcp.tool()
    async def list_sharepoint_sites() -> dict:
        """List available SharePoint sites/document libraries."""
        # This is M365 specific - would need abstraction for Google
        from ..providers.m365 import M365Provider
        if isinstance(provider, M365Provider):
            sites = await provider._client.sites.get()
            return {
                "sites": [
                    {
                        "id": site.id,
                        "name": site.display_name or site.name,
                        "web_url": site.web_url,
                    }
                    for site in (sites.value or [])
                ]
            }
        return {"sites": [], "note": "Only available for M365 provider"}
    
    @mcp.tool()
    async def list_files(
        folder_path: str | None = None,
        site_id: str | None = None,
    ) -> dict:
        """List files in a folder.
        
        Args:
            folder_path: Path to folder (default: root)
            site_id: SharePoint site ID
        """
        documents = await provider.list_documents(
            folder_path=folder_path,
            site_id=site_id,
        )
        return {
            "path": folder_path or "root",
            "files": [
                {
                    "id": doc.id,
                    "name": doc.name,
                    "is_folder": doc.is_folder,
                    "size": doc.size,
                    "web_url": doc.web_url,
                }
                for doc in documents
            ],
        }
    
    @mcp.tool()
    async def upload_file(
        file_name: str,
        content: str,
        folder_path: str | None = None,
        site_id: str | None = None,
    ) -> dict:
        """Upload a file to cloud storage.
        
        Args:
            file_name: Name for the file
            content: File content (text)
            folder_path: Destination folder path
            site_id: SharePoint site ID
        """
        doc = await provider.upload_document(
            name=file_name,
            content=content,
            folder_path=folder_path,
            site_id=site_id,
        )
        return {
            "success": True,
            "file": {
                "id": doc.id,
                "name": doc.name,
                "path": doc.path,
                "web_url": doc.web_url,
            },
        }
    
    @mcp.tool()
    async def download_file(
        document_id: str,
        site_id: str | None = None,
    ) -> dict:
        """Download a file's content.
        
        Args:
            document_id: ID of the document
            site_id: SharePoint site ID
        """
        content = await provider.download_document(
            document_id=document_id,
            site_id=site_id,
        )
        try:
            return {
                "content": content.decode("utf-8"),
                "encoding": "utf-8",
            }
        except UnicodeDecodeError:
            import base64
            return {
                "content": base64.b64encode(content).decode("ascii"),
                "encoding": "base64",
            }
    
    # =========================================================================
    # Directory Tools
    # =========================================================================
    
    @mcp.tool()
    async def list_users(limit: int = 25) -> dict:
        """List users in the organization.
        
        Args:
            limit: Maximum users to return
        """
        users = await provider.list_users(limit=limit)
        return {
            "users": [
                {
                    "id": user.id,
                    "display_name": user.display_name,
                    "email": user.email,
                    "department": user.department,
                }
                for user in users
            ]
        }
    
    @mcp.tool()
    async def get_user(user_id: str) -> dict:
        """Get details about a specific user.
        
        Args:
            user_id: User ID or email address
        """
        user = await provider.get_user(user_id)
        return {
            "id": user.id,
            "display_name": user.display_name,
            "email": user.email,
            "department": user.department,
        }
    
    # =========================================================================
    # Email Tools
    # =========================================================================
    
    @mcp.tool()
    async def send_email(
        to_addresses: list[str],
        subject: str,
        body: str,
        from_user: str | None = None,
    ) -> dict:
        """Send an email.
        
        Args:
            to_addresses: List of recipient email addresses
            subject: Email subject
            body: Email body text
            from_user: Sender email/ID (defaults to admin)
        """
        success = await provider.send_email(
            to=to_addresses,
            subject=subject,
            body=body,
            from_user=from_user,
        )
        return {"success": success, "to": to_addresses, "subject": subject}
    
    return mcp


def main():
    """Run the MCP server."""
    import os
    provider_name = os.environ.get("COLLAB_PROVIDER", "m365")
    server = create_server(provider_name)
    server.run()


if __name__ == "__main__":
    main()
