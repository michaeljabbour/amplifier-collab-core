# amplifier-module-tool-collab-core

Core collaboration interfaces for Amplifier. Provides the abstract `CollaborationProvider` base class that platform-specific modules implement.

## Overview

This module provides:
- **`CollaborationProvider`** - Abstract interface for all collaboration platforms
- **Data models** - `User`, `Channel`, `Message`, `Document`, `Task`
- **Provider registry** - Register and retrieve platform providers

## Installation

```bash
pip install amplifier-module-tool-collab-core
```

## Platform Modules

Install the platform module(s) you need:

| Platform | Module | Install |
|----------|--------|---------|
| Microsoft 365 | `tool-m365` | `pip install amplifier-module-tool-m365` |
| Slack | `tool-slack` | `pip install amplifier-module-tool-slack` |
| Google Workspace | `tool-google` | Coming soon |

## Usage

```python
from amplifier_module_tool_collab_core import get_provider, list_providers

# Import a platform module to register its provider
import amplifier_module_tool_m365  # Registers 'm365'
import amplifier_module_tool_slack  # Registers 'slack'

# List available providers
print(list_providers())  # ['m365', 'slack']

# Get a provider instance
provider = get_provider("m365")

# Use the unified interface
users = await provider.list_users(limit=5)
await provider.post_message("general", "Hello!")
```

## CollaborationProvider Interface

All platform modules implement this interface:

```python
class CollaborationProvider(ABC):
    @property
    def name(self) -> str: ...
    
    # Users & Directory
    async def list_users(self, limit: int = 25) -> list[User]: ...
    async def get_user(self, user_id: str) -> User: ...
    
    # Channels & Messaging
    async def list_channels(self, team_id: str | None = None) -> list[Channel]: ...
    async def get_messages(self, channel_id: str, limit: int = 20, team_id: str | None = None) -> list[Message]: ...
    async def post_message(self, channel_name: str, message: str, title: str | None = None) -> bool: ...
    
    # Documents & Files
    async def list_documents(self, folder_path: str | None = None, site_id: str | None = None) -> list[Document]: ...
    async def upload_document(self, name: str, content: bytes | str, folder_path: str | None = None, site_id: str | None = None) -> Document: ...
    async def download_document(self, document_id: str, site_id: str | None = None) -> bytes: ...
    
    # Tasks
    async def list_tasks(self, plan_id: str | None = None) -> list[Task]: ...
    
    # Email
    async def send_email(self, to: list[str], subject: str, body: str, from_user: str | None = None) -> bool: ...
```

## Creating a New Provider

```python
from amplifier_module_tool_collab_core import CollaborationProvider, register_provider

class MyPlatformProvider(CollaborationProvider):
    @property
    def name(self) -> str:
        return "myplatform"
    
    # Implement all abstract methods...

# Register on module import
register_provider("myplatform", MyPlatformProvider)
```

## License

MIT
