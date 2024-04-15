---
date: 2024-04-15T12:11:36.869766
author: AutoGPT <info@agpt.co>
---

# URL Preview API

The endpoint is designed to accept a URL from the user and performs the following functions in sequence: It retrieves the content of the specified webpage, including all textual and multimedia content. It then proceeds to extract relevant metadata from the content, focusing on elements like the page title, description, keywords, and any available meta tags that can enrich the extracted data set. Following the extraction, the system generates a comprehensive preview snippet. This snippet includes the page title, a concise description derived from either the meta description tag or a summary of the page content, and a thumbnail image, which is selected based on relevance and representation of the webpage content. The produced structured preview data encompasses all the aforementioned elements and is formatted for optimal use in link sharing across social media platforms, embedding in webpages, or any other scenario where a concise, informative preview of the webpage content is required. This process relies on a tech stack consisting of Python as the programming language, utilizing FastAPI for creating the efficient and scalable API endpoint. PostgreSQL serves as the database to manage and store extracted content and metadata, while Prisma is employed as the ORM for facilitating interaction between the application and the database. The system is designed with best practices for content extraction and metadata retrieval, ensuring respect for robots.txt, managing request rates to prevent server overload, and using legal and responsible data handling methods. The approach enhances user engagement by providing clear, accessible, and informative webpage previews.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'URL Preview API'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
