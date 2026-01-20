# amplifier-module-tool-collab-core

Core collaboration module for Amplifier with Microsoft 365 provider and shared interfaces.

## Features

- **Unified Interface** - `CollaborationProvider` base class for all platforms
- **M365 Provider** - Full Microsoft Graph integration (Teams, SharePoint, Outlook, Planner)
- **Collaboration Tools** - Ready-to-use tools for channels, documents, directory, email

## Installation

```bash
pip install amplifier-module-tool-collab-core
```

Or from source:
```bash
pip install git+https://github.com/michaeljabbour/amplifier-module-tool-collab-core
```

## Configuration

Set environment variables:

```bash
export M365_TENANT_ID="your-tenant-id"
export M365_CLIENT_ID="your-client-id"
export M365_CLIENT_SECRET="your-client-secret"
export M365_TEAMS_WEBHOOKS="general=https://...,alerts=https://...,handoffs=https://..."
```

## Usage

### As Amplifier Module

The module auto-registers when loaded by Amplifier:

```yaml
# In your bundle
tools:
  - module: tool-collab-core
    source: git+https://github.com/michaeljabbour/amplifier-module-tool-collab-core
```

### Direct Python Usage

```python
import asyncio
from amplifier_module_tool_collab_core import get_provider

async def main():
    provider = get_provider("m365")
    
    # List users
    users = await provider.list_users(limit=5)
    print(f"Found {len(users)} users")
    
    # Post to channel
    await provider.post_message("general", "Hello from Amplifier!")
    
    # List documents
    docs = await provider.list_documents(folder_path="Shared Documents")
    for doc in docs:
        print(f"  {doc.name}")

asyncio.run(main())
```

## Tools

| Tool | Operations | Description |
|------|------------|-------------|
| `collab_channels` | post, read, list | Channel messaging |
| `collab_documents` | upload, download, list | File operations |
| `collab_directory` | list_users, get_user | User lookup |
| `collab_email` | send | Email notifications |

## Provider Interface

To add a new platform, implement `CollaborationProvider`:

```python
from amplifier_module_tool_collab_core import CollaborationProvider

class MyProvider(CollaborationProvider):
    @property
    def name(self) -> str:
        return "myplatform"
    
    async def list_users(self, limit: int = 25) -> list[User]:
        ...
    
    async def post_message(self, channel_name: str, message: str, title: str = None) -> bool:
        ...
    
    # ... implement all abstract methods
```

## License

MIT
