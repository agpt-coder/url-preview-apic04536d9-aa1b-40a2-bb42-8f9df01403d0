import logging
from contextlib import asynccontextmanager
from typing import List

import project.extract_metadata_service
import project.fetch_webpage_content_service
import project.generate_preview_service
import project.retrieve_preview_service
import project.submit_url_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="URL Preview API",
    lifespan=lifespan,
    description="The endpoint is designed to accept a URL from the user and performs the following functions in sequence: It retrieves the content of the specified webpage, including all textual and multimedia content. It then proceeds to extract relevant metadata from the content, focusing on elements like the page title, description, keywords, and any available meta tags that can enrich the extracted data set. Following the extraction, the system generates a comprehensive preview snippet. This snippet includes the page title, a concise description derived from either the meta description tag or a summary of the page content, and a thumbnail image, which is selected based on relevance and representation of the webpage content. The produced structured preview data encompasses all the aforementioned elements and is formatted for optimal use in link sharing across social media platforms, embedding in webpages, or any other scenario where a concise, informative preview of the webpage content is required. This process relies on a tech stack consisting of Python as the programming language, utilizing FastAPI for creating the efficient and scalable API endpoint. PostgreSQL serves as the database to manage and store extracted content and metadata, while Prisma is employed as the ORM for facilitating interaction between the application and the database. The system is designed with best practices for content extraction and metadata retrieval, ensuring respect for robots.txt, managing request rates to prevent server overload, and using legal and responsible data handling methods. The approach enhances user engagement by providing clear, accessible, and informative webpage previews.",
)


@app.get(
    "/retrieve-preview/{id}",
    response_model=project.retrieve_preview_service.RetrievePreviewResponse,
)
async def api_get_retrieve_preview(
    id: str,
) -> project.retrieve_preview_service.RetrievePreviewResponse | Response:
    """
    Enables retrieval of generated previews by URL or ID.
    """
    try:
        res = await project.retrieve_preview_service.retrieve_preview(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/submit-url", response_model=project.submit_url_service.SubmitUrlResponse)
async def api_post_submit_url(
    url: str, user_token: str
) -> project.submit_url_service.SubmitUrlResponse | Response:
    """
    Allows external services to submit URLs for processing.
    """
    try:
        res = await project.submit_url_service.submit_url(url, user_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/fetch-content",
    response_model=project.fetch_webpage_content_service.FetchContentResponse,
)
async def api_post_fetch_webpage_content(
    url: str,
) -> project.fetch_webpage_content_service.FetchContentResponse | Response:
    """
    Submits URL and retrieves webpage content, adhering to compliance and rate limits.
    """
    try:
        res = await project.fetch_webpage_content_service.fetch_webpage_content(url)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/generate-preview", response_model=project.generate_preview_service.PreviewResponse
)
async def api_post_generate_preview(
    title: str, description: str, thumbnail_url: str, url: str, keywords: List[str]
) -> project.generate_preview_service.PreviewResponse | Response:
    """
    Generates a formatted preview snippet from provided metadata for sharing or embedding.
    """
    try:
        res = await project.generate_preview_service.generate_preview(
            title, description, thumbnail_url, url, keywords
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/extract-metadata",
    response_model=project.extract_metadata_service.ExtractMetadataResponse,
)
async def api_post_extract_metadata(
    raw_html_content: str,
) -> project.extract_metadata_service.ExtractMetadataResponse | Response:
    """
    Extracts and returns metadata from provided webpage content.
    """
    try:
        res = project.extract_metadata_service.extract_metadata(raw_html_content)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
