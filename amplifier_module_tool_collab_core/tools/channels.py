"""Channel messaging tool for collaboration."""

from typing import Literal

from .. import get_provider


async def collab_channels(
    operation: Literal["post", "read", "list"],
    channel_name: str | None = None,
    message: str | None = None,
    title: str | None = None,
    limit: int = 20,
    team_id: str | None = None,
    provider_name: str = "m365",
) -> dict:
    """Channel messaging for multi-instance coordination.

    Args:
        operation: Action to perform ('post', 'read', 'list')
        channel_name: Target channel ('general', 'alerts', 'handoffs')
        message: Message content (for 'post')
        title: Optional message title (for 'post')
        limit: Max messages to return (for 'read')
        team_id: Team/workspace ID (platform-specific)
        provider_name: Provider to use ('m365', 'slack', 'google')

    Returns:
        Operation result dict
    """
    provider = get_provider(provider_name)

    if operation == "post":
        if not channel_name or not message:
            return {"error": "channel_name and message required for 'post'"}

        success = await provider.post_message(channel_name, message, title)
        return {
            "success": success,
            "channel": channel_name,
            "message": message[:100] + "..." if len(message) > 100 else message,
        }

    elif operation == "read":
        if not channel_name:
            return {"error": "channel_name required for 'read'"}

        # Need to find channel ID first
        channels = await provider.list_channels(team_id)
        channel = next(
            (c for c in channels if c.name.lower() == channel_name.lower()), None
        )

        if not channel:
            return {"error": f"Channel '{channel_name}' not found"}

        messages = await provider.get_messages(
            channel.id, limit=limit, team_id=channel.team_id
        )

        return {
            "channel": channel_name,
            "messages": [
                {
                    "sender": m.sender,
                    "content": m.content,
                    "timestamp": m.timestamp,
                }
                for m in messages
            ],
        }

    elif operation == "list":
        channels = await provider.list_channels(team_id)
        return {
            "channels": [
                {
                    "name": c.name,
                    "team": c.team_name,
                    "description": c.description,
                }
                for c in channels
            ],
        }

    else:
        return {"error": f"Unknown operation: {operation}"}
