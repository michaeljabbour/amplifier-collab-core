"""Amplifier collaboration core module with M365 provider and shared interfaces."""

from .providers.base import (
    CollaborationProvider,
    User,
    Channel,
    Message,
    Document,
    Task,
)
from .providers.m365 import M365Provider

__all__ = [
    "CollaborationProvider",
    "User",
    "Channel", 
    "Message",
    "Document",
    "Task",
    "M365Provider",
    "mount",
    "get_provider",
]


def get_provider(name: str = "m365") -> CollaborationProvider:
    """Get a collaboration provider by name.
    
    Args:
        name: Provider name ('m365', 'slack', 'google')
        
    Returns:
        Configured provider instance
    """
    providers = {
        "m365": M365Provider,
    }
    
    if name not in providers:
        available = ", ".join(providers.keys())
        raise ValueError(f"Unknown provider '{name}'. Available: {available}")
    
    return providers[name]()


def mount(session):
    """Mount collaboration tools to an Amplifier session.
    
    This is the entry point called by Amplifier's module loader.
    """
    from .tools import channels, documents, directory, email
    
    # Register tools with the session
    session.register_tool("collab_channels", channels.collab_channels)
    session.register_tool("collab_documents", documents.collab_documents)
    session.register_tool("collab_directory", directory.collab_directory)
    session.register_tool("collab_email", email.collab_email)
