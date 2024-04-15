from typing import Dict

import prisma
import prisma.models
from pydantic import BaseModel


class RetrievePreviewResponse(BaseModel):
    """
    The structured response containing the preview details.
    """

    title: str
    description: str
    thumbnail: str
    metadata: Dict[str, str]


async def retrieve_preview(id: str) -> RetrievePreviewResponse:
    """
    Enables retrieval of generated previews by URL or ID.

    This function looks up the preview details associated with the given identifier.
    It makes use of the Prisma ORM to retrieve the preview data from the Preview table.
    The returned data includes the title, description, thumbnail URL, and other metadata associated with the preview.

    Args:
        id (str): The unique identifier for the preview to be retrieved.

    Returns:
        RetrievePreviewResponse: The structured response containing the preview details, including the title, description,
                                 thumbnail, and metadata for the webpage.

    Example:
        preview_data = await retrieve_preview('1234abcd')
        print(preview_data)
        > RetrievePreviewResponse(title="Example Page", description="This is an example page description",
        >                         thumbnail="https://example.com/thumbnail.jpg", metadata={"keywords": "example, page"})
    """
    preview = await prisma.models.Preview.prisma().find_unique(where={"id": id})
    if preview is None:
        raise ValueError("Preview with the provided ID does not exist.")
    title = preview.title if preview.title else ""
    description = preview.description if preview.description else ""
    thumbnail = preview.thumbnail if preview.thumbnail else ""
    metadata = preview.metadata if preview.metadata else {}
    return RetrievePreviewResponse(
        title=title, description=description, thumbnail=thumbnail, metadata=metadata
    )
