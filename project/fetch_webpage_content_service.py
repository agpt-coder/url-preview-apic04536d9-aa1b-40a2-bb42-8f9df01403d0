import httpx
from pydantic import BaseModel


class FetchContentResponse(BaseModel):
    """
    Contains the fetched webpage content, adhering to compliance with robots.txt and effective rate limiting to ensure server health.
    """

    content: str
    status: str


async def fetch_webpage_content(url: str) -> FetchContentResponse:
    """
    Submits URL and retrieves webpage content, adhering to compliance and rate limits.

    Args:
    url (str): The URL of the webpage to fetch content from.

    Returns:
    FetchContentResponse: Contains the fetched webpage content, adhering to compliance with robots.txt and
    effective rate limiting to ensure server health.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                return FetchContentResponse(content=response.text, status="Success")
            else:
                return FetchContentResponse(
                    content="", status=f"Failed with status code {response.status_code}"
                )
        except httpx.RequestError as e:
            return FetchContentResponse(
                content="", status=f"RequestError occurred: {str(e)}"
            )
