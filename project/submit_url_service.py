import prisma
import prisma.models
from pydantic import BaseModel


class SubmitUrlResponse(BaseModel):
    """
    Provides feedback on the successfully submitted URL, including an identifier or message indicating the URL is being processed.
    """

    message: str
    url_id: str


async def submit_url(url: str, user_token: str) -> SubmitUrlResponse:
    """
    Allows external services to submit URLs for processing.

    Args:
    url (str): The webpage URL submitted by the user for generating a preview.
    user_token (str): The authentication token of the user submitting the URL.

    Returns:
    SubmitUrlResponse: Provides feedback on the successfully submitted URL, including an identifier or message indicating the URL is being processed.
    """
    token_owner = await prisma.models.APIToken.prisma().find_unique(
        where={"token": user_token}, include={"User": True}
    )
    if not token_owner:
        raise Exception("Invalid user token.")
    user_url = await prisma.models.UserURL.prisma().create(
        data={"url": url, "userId": token_owner.userId}
    )
    return SubmitUrlResponse(
        message="URL successfully submitted for processing.", url_id=user_url.id
    )
