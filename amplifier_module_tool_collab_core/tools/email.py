"""Email tool for collaboration."""

from typing import Literal

from .. import get_provider


async def collab_email(
    operation: Literal["send"],
    to: list[str] | None = None,
    subject: str | None = None,
    body: str | None = None,
    from_user: str | None = None,
    provider_name: str = "m365",
) -> dict:
    """Email operations.

    Args:
        operation: Action to perform ('send')
        to: List of recipient email addresses
        subject: Email subject
        body: Email body
        from_user: Sender user ID (optional)
        provider_name: Provider to use ('m365', 'google')

    Returns:
        Operation result dict
    """
    provider = get_provider(provider_name)

    if operation == "send":
        if not to or not subject or not body:
            return {"error": "to, subject, and body required for 'send'"}

        success = await provider.send_email(
            to=to,
            subject=subject,
            body=body,
            from_user=from_user,
        )

        return {
            "success": success,
            "to": to,
            "subject": subject,
        }

    else:
        return {"error": f"Unknown operation: {operation}"}
