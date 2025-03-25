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