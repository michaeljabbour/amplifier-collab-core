"""Amplifier collaboration core library - shared interfaces and utilities.

This library provides the abstract CollaborationProvider interface that all
platform-specific modules (M365, Slack, Google) implement.
"""

from .providers.base import (
    CollaborationProvider,
    User,
    Channel,
    Message,
    Document,
    Task,
)

__all__ = [
    # Data models
    "CollaborationProvider",
    "User",
    "Channel",
    "Message",
    "Document",
    "Task",
    # Registry functions
    "register_provider",
    "get_provider",
    "list_providers",
]


# Provider registry - platform modules register themselves here
_providers: dict[str, type[CollaborationProvider]] = {}


def register_provider(name: str, provider_class: type[CollaborationProvider]) -> None:
    """Register a collaboration provider.

    Called by platform modules (tool-m365, tool-slack, etc.) on import.
    """
    _providers[name] = provider_class


def get_provider(name: str) -> CollaborationProvider:
    """Get an instance of a registered provider.

    Args:
        name: Provider name ('m365', 'slack', 'google')

    Returns:
        Configured provider instance

    Raises:
        ValueError: If provider is not registered
    """
    if name not in _providers:
        available = ", ".join(_providers.keys()) if _providers else "(none registered)"
        raise ValueError(
            f"Provider '{name}' not registered. Available: {available}. "
            f"Make sure the corresponding module is installed (e.g., amplifier-collab-{name})"
        )

    return _providers[name]()


def list_providers() -> list[str]:
    """List all registered provider names."""
    return list(_providers.keys())
