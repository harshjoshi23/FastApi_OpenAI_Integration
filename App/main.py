from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
if __package__:
    from .utils import DescriptionNotConfigured, generate_description
else:
    from utils import DescriptionNotConfigured, generate_description

app = FastAPI()

# Data models
class Order(BaseModel):
    product: str
    units: int = Field(gt=0)

class Product(BaseModel):
    name: str
    notes: str

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to FastApi_OpenAI_Integration! Use /docs to explore the API."}

# Basic GET endpoints
@app.get("/ok")
async def ok_endpoint():
    return {"message": "ok"}

@app.get("/hello")
async def hello_endpoint(name: str = "World"):
    return {"message": f"Hello, {name}!"}

# POST endpoints for orders
@app.post("/orders")
async def place_order(product: str, units: Annotated[int, Query(gt=0)]):
    return {"message": f"Order for {units} units of {product} placed successfully."}

@app.post("/orders_pydantic")
async def place_order_pydantic(order: Order):
    return {"message": f"Order for {order.units} units of {order.product} placed successfully."}

# POST endpoint for product description with OpenAI
@app.post("/product_description")
def generate_product_description(product: Product):
    try:
        description = generate_description(f"Product name: {product.name}, Notes: {product.notes}")
    except DescriptionNotConfigured as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return {"product_description": description}