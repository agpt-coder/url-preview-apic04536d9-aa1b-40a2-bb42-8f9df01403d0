import html
import uuid
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class PreviewResponse(BaseModel):
    """
    A structured snippet containing the essential elements (title, description, thumbnail) optimized for sharing and embedding. This output model serves as a direct translation of input metadata into a consumable format.
    """

    preview_id: str
    title: str
    description: str
    thumbnail_url: str
    url: str
    embed_code: str


async def generate_preview(
    title: str, description: str, thumbnail_url: str, url: str, keywords: List[str]
) -> PreviewResponse:
    """
    Generates a formatted preview snippet from provided metadata for sharing or embedding.

    Args:
        title (str): The title of the webpage to be displayed in the preview.
        description (str): A succinct description or summary of the webpage content.
        thumbnail_url (str): The URL of the thumbnail image to include in the preview.
        url (str): The original URL of the webpage being previewed.
        keywords (List[str]): Relevant keywords extracted from the webpage, aiding in content comprehension.

    Returns:
        PreviewResponse: A structured snippet containing the essential elements (title, description, thumbnail) optimized for sharing and embedding. This output model serves as a direct translation of input metadata into a consumable format.

    This function saves the preview information in the database and returns a PreviewResponse object.
    """
    preview_id = str(uuid.uuid4())
    sanitized_title = html.escape(title)
    sanitized_description = html.escape(description)
    sanitized_thumbnail_url = html.escape(thumbnail_url)
    sanitized_url = html.escape(url)
    embed_code = f'<div><a href="{sanitized_url}" target="_blank"><img src="{sanitized_thumbnail_url}" alt="{sanitized_title}"/><p>{sanitized_title}</p></a><p>{sanitized_description}</p></div>'
    preview = await prisma.models.Preview.prisma().create(
        data={
            "id": preview_id,
            "title": sanitized_title,
            "description": sanitized_description,
            "thumbnail": sanitized_thumbnail_url,
            "keywords": keywords,
            "metadata": {"original_url": sanitized_url, "embed_code": embed_code},
        }
    )
    preview_response = PreviewResponse(
        preview_id=preview_id,
        title=title,
        description=description,
        thumbnail_url=thumbnail_url,
        url=url,
        embed_code=embed_code,
    )
    return preview_response
