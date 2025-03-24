import requests
import json

# Test /ok
response = requests.get("http://127.0.0.1:8000/ok")
print(response.json())  # Expected: {"message": "ok"}

# Test /hello
response = requests.get("http://127.0.0.1:8000/hello?name=Harsh")
print(response.json())  # Expected: {"message": "Hello, Harsh!"}

# Test /orders
response = requests.post("http://127.0.0.1:8000/orders?product=laptop&units=2")
print(response.json())  # Expected: {"message": "Order for 2 units of laptop placed successfully."}

# Test /orders_pydantic
data = {"product": "phone", "units": 1}
response = requests.post("http://127.0.0.1:8000/orders_pydantic", json=data)
print(response.json())  # Expected: {"message": "Order for 1 units of phone placed successfully."}

# Test /product_description
data = {"name": "Laptop", "notes": "4GB RAM, 256 GB Disk"}
response = requests.post("http://127.0.0.1:8000/product_description", json=data)
print(response.json())  # Expected: {"product_description": "<generated text with emojis>"}