# FastApi_OpenAI_Integration

A FastAPI application integrated with OpenAI's ChatGPT to generate product descriptions.


## Overview
This project builds a RESTful API using FastAPI and integrates it with OpenAI's ChatGPT to generate rich product descriptions with emojis. It includes endpoints for basic API testing and product description generation.


## Features
- **Setting Up FastAPI Server**: Created a FastAPI application with endpoints `/ok`, `/hello`, `/orders`, `/orders_pydantic`, and `/product_description`.
- **OpenAI Integration**: Integrated OpenAI's ChatGPT to generate product descriptions, though currently using a mock response due to a quota limit.
- **Testing**: Implemented a `test.py` script to test all endpoints, with error handling for robustness.
- **Results**:
  - Basic endpoints (`/ok`, `/hello`, `/orders`, `/orders_pydantic`) work successfully, returning `200 OK` responses.
  - The `/product_description` endpoint is functional with a mock response, pending resolution of the OpenAI quota limit.

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/harshjoshi23/FastApi_OpenAI_Integration.git
   cd FastApi_OpenAI_Integration
## Provider configuration

The API starts without an OpenAI key. Health checks, API documentation and order
routes remain available. Product generation returns HTTP 503 until
`OPENAI_API_KEY` is set in the deployment environment or local `.env` file.
The provider client is created only for a generation request and closed after
that request. From the repository root, run `uvicorn App.main:app`.

### Provider failure responses

`POST /product_description` returns 504 for provider timeouts, 503 for
connection, rate-limit or provider credential/permission failures, and 502 for
other provider HTTP errors. Provider messages and input notes are not included
in these error responses. A provider authentication failure is a server setup
problem, so it does not return 401 to the API caller.

Each SDK request uses a 20-second timeout with automatic retries disabled.
This reduces long waits and hidden retry traffic; the timeout is an SDK
network-operation limit, not a strict end-to-end deadline. Clients should use
bounded backoff for transient failures. Persistent 503 responses require an
operator to check provider configuration or quota. The endpoint is not
authenticated or rate-limited yet; configure those before public deployment.

Regression tests exercise the real route with simulated SDK exceptions and no
external calls: `python -m pytest tests -q`. Live provider validation still
requires a configured account and is not covered by these tests.
SDK behavior reference: [official OpenAI Python documentation](https://developers.openai.com/api/reference/python).
