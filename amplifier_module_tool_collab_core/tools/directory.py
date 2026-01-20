"""Directory/user lookup tool for collaboration."""

from typing import Literal

from .. import get_provider


async def collab_directory(
    operation: Literal["list_users", "get_user"],
    user_id: str | None = None,
    limit: int = 25,
    provider_name: str = "m365",
) -> dict:
    """User directory operations.
    
    Args:
        operation: Action to perform ('list_users', 'get_user')
        user_id: User ID or email (for 'get_user')
        limit: Max users to return (for 'list_users')
        provider_name: Provider to use ('m365', 'slack', 'google')
        
    Returns:
        Operation result dict
    """
    provider = get_provider(provider_name)
    
    if operation == "list_users":
        users = await provider.list_users(limit=limit)
        
        return {
            "users": [
                {
                    "id": u.id,
                    "name": u.display_name,
                    "email": u.email,
                    "department": u.department,
                }
                for u in users
            ],
        }
    
    elif operation == "get_user":
        if not user_id:
            return {"error": "user_id required for 'get_user'"}
        
        user = await provider.get_user(user_id)
        
        return {
            "user": {
                "id": user.id,
                "name": user.display_name,
                "email": user.email,
                "department": user.department,
            },
        }
    
    else:
        return {"error": f"Unknown operation: {operation}"}
