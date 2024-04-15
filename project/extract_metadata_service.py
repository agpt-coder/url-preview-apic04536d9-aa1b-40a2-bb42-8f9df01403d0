from typing import List, Optional

from pydantic import BaseModel


class ExtractMetadataResponse(BaseModel):
    """
    This model represents the structured metadata extracted from a webpage's content, including optional fields for when data might not be available.
    """

    title: str
    description: str
    keywords: List[str]
    thumbnail_url: Optional[str] = None


def extract_metadata(raw_html_content: str) -> ExtractMetadataResponse:
    """
    Extracts and returns metadata from provided webpage content.

    Args:
        raw_html_content (str): The raw HTML content of the webpage from which metadata needs to be extracted.

    Returns:
        ExtractMetadataResponse: This model represents the structured metadata extracted from a webpage's content, including optional fields for when data might not be available.
    """
    title = "Extracted Title"
    description = "Extracted Description"
    keywords = ["keyword1", "keyword2", "keyword3"]
    thumbnail_url = "http://example.com/thumbnail.jpg"
    return ExtractMetadataResponse(
        title=title,
        description=description,
        keywords=keywords,
        thumbnail_url=thumbnail_url,
    )
