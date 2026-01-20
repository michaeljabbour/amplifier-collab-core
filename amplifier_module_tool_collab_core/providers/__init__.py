"""Collaboration providers."""

from .base import CollaborationProvider, User, Channel, Message, Document, Task
from .m365 import M365Provider

__all__ = [
    "CollaborationProvider",
    "User",
    "Channel",
    "Message",
    "Document",
    "Task",
    "M365Provider",
]
