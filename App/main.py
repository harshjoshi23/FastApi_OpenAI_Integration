from fastapi import FastAPI
from pydantic import BaseModel
from utils import generate_description

app = FastAPI()

# Data models
class Order(BaseModel):
    product: str
    units: int

class Product(BaseModel):
    name: str
    notes: str

# Basic GET endpoints
@app.get("/ok")
async def ok_endpoint():
    return {"message": "ok"}

@app.get("/hello")
async def hello_endpoint(name: str = "World"):
    return {"message": f"Hello, {name}!"}

# POST endpoints for orders
@app.post("/orders")
async def place_order(product: str, units: int):
    return {"message": f"Order for {units} units of {product} placed successfully."}

@app.post("/orders_pydantic")
async def place_order_pydantic(order: Order):
    return {"message": f"Order for {order.units} units of {order.product} placed successfully."}

# POST endpoint for product description with OpenAI
@app.post("/product_description")
async def generate_product_description(product: Product):
    description = generate_description(f"Product name: {product.name}, Notes: {product.notes}")
    return {"product_description": description}