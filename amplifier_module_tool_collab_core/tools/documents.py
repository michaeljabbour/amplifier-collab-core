"""Document management tool for collaboration."""

from typing import Literal

from .. import get_provider


async def collab_documents(
    operation: Literal["upload", "download", "list"],
    file_name: str | None = None,
    content: str | None = None,
    folder_path: str | None = None,
    document_id: str | None = None,
    site_id: str | None = None,
    provider_name: str = "m365",
) -> dict:
    """Document operations for artifact sharing.
    
    Args:
        operation: Action to perform ('upload', 'download', 'list')
        file_name: Name for uploaded file
        content: File content (for 'upload')
        folder_path: Target folder path
        document_id: Document ID (for 'download')
        site_id: Site/drive ID (platform-specific)
        provider_name: Provider to use ('m365', 'slack', 'google')
        
    Returns:
        Operation result dict
    """
    provider = get_provider(provider_name)
    
    if operation == "upload":
        if not file_name or not content:
            return {"error": "file_name and content required for 'upload'"}
        
        doc = await provider.upload_document(
            name=file_name,
            content=content,
            folder_path=folder_path,
            site_id=site_id,
        )
        
        return {
            "success": True,
            "document": {
                "id": doc.id,
                "name": doc.name,
                "path": doc.path,
                "web_url": doc.web_url,
            },
        }
    
    elif operation == "download":
        if not document_id:
            return {"error": "document_id required for 'download'"}
        
        content_bytes = await provider.download_document(document_id, site_id)
        
        # Try to decode as text, otherwise return size info
        try:
            text_content = content_bytes.decode("utf-8")
            return {
                "success": True,
                "content": text_content,
                "size": len(content_bytes),
            }
        except UnicodeDecodeError:
            return {
                "success": True,
                "content": "(binary content)",
                "size": len(content_bytes),
            }
    
    elif operation == "list":
        docs = await provider.list_documents(folder_path, site_id)
        
        return {
            "folder": folder_path or "root",
            "documents": [
                {
                    "id": d.id,
                    "name": d.name,
                    "is_folder": d.is_folder,
                    "size": d.size,
                    "web_url": d.web_url,
                }
                for d in docs
            ],
        }
    
    else:
        return {"error": f"Unknown operation: {operation}"}
