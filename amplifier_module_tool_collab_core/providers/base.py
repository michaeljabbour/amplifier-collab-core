"""Abstract collaboration provider interface.

This defines the contract that all collaboration providers must implement.
Providers abstract the differences between M365, Google Workspace, Slack, etc.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class User:
    """Represents a user in the collaboration system."""
    id: str
    display_name: str
    email: str | None = None
    department: str | None = None


@dataclass
class Channel:
    """Represents a messaging channel (Teams channel, Slack channel, etc.)."""
    id: str
    name: str
    description: str | None = None
    team_id: str | None = None
    team_name: str | None = None


@dataclass  
class Message:
    """Represents a channel message."""
    id: str
    content: str
    sender: str
    timestamp: str
    channel_id: str | None = None


@dataclass
class Document:
    """Represents a document in cloud storage."""
    id: str
    name: str
    path: str
    web_url: str | None = None
    size: int | None = None
    is_folder: bool = False


@dataclass
class Task:
    """Represents a task/work item."""
    id: str
    title: str
    status: str
    due_date: str | None = None
    assigned_to: str | None = None


class CollaborationProvider(ABC):
    """Base class for collaboration providers (M365, Slack, Google, etc.).
    
    Each provider implements this interface to normalize the differences
    between platforms while exposing a unified API for collaboration tools.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name (e.g., 'm365', 'slack', 'google')."""
        ...
    
    # =========================================================================
    # Users & Directory
    # =========================================================================
    
    @abstractmethod
    async def list_users(self, limit: int = 25) -> list[User]:
        """List users in the organization."""
        ...
    
    @abstractmethod
    async def get_user(self, user_id: str) -> User:
        """Get a specific user by ID or email."""
        ...
    
    # =========================================================================
    # Channels & Messaging
    # =========================================================================
    
    @abstractmethod
    async def list_channels(self, team_id: str | None = None) -> list[Channel]:
        """List available channels.
        
        Args:
            team_id: Optional team/workspace to filter by
        """
        ...
    
    @abstractmethod
    async def get_messages(
        self, 
        channel_id: str, 
        limit: int = 20,
        team_id: str | None = None,
    ) -> list[Message]:
        """Get recent messages from a channel."""
        ...
    
    @abstractmethod
    async def post_message(
        self,
        channel_name: str,
        message: str,
        title: str | None = None,
    ) -> bool:
        """Post a message to a channel.
        
        Args:
            channel_name: Logical channel name (e.g., 'general', 'alerts')
            message: Message content
            title: Optional message title/subject
            
        Returns:
            True if successful
        """
        ...
    
    # =========================================================================
    # Documents & Files
    # =========================================================================
    
    @abstractmethod
    async def list_documents(
        self, 
        folder_path: str | None = None,
        site_id: str | None = None,
    ) -> list[Document]:
        """List documents in a location."""
        ...
    
    @abstractmethod
    async def upload_document(
        self,
        name: str,
        content: bytes | str,
        folder_path: str | None = None,
        site_id: str | None = None,
    ) -> Document:
        """Upload a document."""
        ...
    
    @abstractmethod
    async def download_document(
        self,
        document_id: str,
        site_id: str | None = None,
    ) -> bytes:
        """Download a document's content."""
        ...
    
    # =========================================================================
    # Tasks & Planning
    # =========================================================================
    
    @abstractmethod
    async def list_tasks(
        self,
        plan_id: str | None = None,
    ) -> list[Task]:
        """List tasks/work items."""
        ...
    
    # =========================================================================
    # Email
    # =========================================================================
    
    @abstractmethod
    async def send_email(
        self,
        to: list[str],
        subject: str,
        body: str,
        from_user: str | None = None,
    ) -> bool:
        """Send an email."""
        ...
